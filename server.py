#!/usr/bin/env python3
"""静态站服务器（V351）。

平台默认的 `python3 -m http.server` 不压缩、也不发缓存头，实测线上 CSS/JS/HTML
全部原样传输（main.min.css 48KB、site.js 55KB…），首屏文本约 154KB。这里只做三件事：

1. 对文本类资源做 gzip（HTML/CSS/JS/JSON/SVG），压完约 1/4；
2. 带 `?v=` 的资源发一年 immutable 缓存，HTML 发 no-cache（保证改版即时生效）；
3. 关掉目录列表，屏蔽 .git / .workbuddy 这类不该公开的目录。

图片/字体已经是压缩格式，不再二次 gzip；小于 1KB 的文件压了反而更大，跳过。
压缩结果按 (路径, mtime, 大小) 缓存在内存里，改文件后自动失效。
"""
import gzip
import io
import mimetypes
import os
import posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get('PORT', '8410'))

mimetypes.add_type('image/avif', '.avif')
mimetypes.add_type('image/webp', '.webp')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('text/javascript', '.js')

GZIP_TYPES = {
    'text/html', 'text/css', 'text/plain', 'text/xml', 'text/javascript',
    'application/javascript', 'application/json', 'application/xml',
    'application/manifest+json', 'image/svg+xml',
}
BLOCKED = ('.git', '.workbuddy', '.wbapp_', 'server.py', '__pycache__')
_cache = {}


class Handler(SimpleHTTPRequestHandler):
    server_version = 'gxci/1.0'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    # --- 缓存头 ---------------------------------------------------------
    def end_headers(self):
        path = urlparse(self.path).path
        if path.endswith(('.html', '/')) or path == '':
            self.send_header('Cache-Control', 'no-cache')
        elif 'v=' in self.path or path.startswith('/assets/'):
            self.send_header('Cache-Control', 'public, max-age=31536000, immutable')
        else:
            self.send_header('Cache-Control', 'public, max-age=3600')
        super().end_headers()

    # --- gzip -----------------------------------------------------------
    def send_head(self):
        path = self.translate_path(self.path)
        if any(seg in path for seg in BLOCKED):
            self.send_error(404)
            return None
        if os.path.isfile(path):
            ctype = self.guess_type(path)
            if ctype in GZIP_TYPES and 'gzip' in self.headers.get('Accept-Encoding', ''):
                body = self._gzipped(path)
                if body is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', ctype)
                    self.send_header('Content-Encoding', 'gzip')
                    self.send_header('Content-Length', str(len(body)))
                    self.send_header('Vary', 'Accept-Encoding')
                    self.send_header('Last-Modified', self.date_time_string(os.stat(path).st_mtime))
                    self.end_headers()
                    return io.BytesIO(body)
        return super().send_head()

    def _gzipped(self, path):
        try:
            st = os.stat(path)
            key = (path, st.st_mtime, st.st_size)
            if key in _cache:
                return _cache[key]
            if st.st_size < 1024:
                return None
            with open(path, 'rb') as f:
                raw = f.read()
            body = gzip.compress(raw, 6)
            if len(body) >= len(raw):
                return None
            if len(_cache) > 64:
                _cache.clear()
            _cache[key] = body
            return body
        except OSError:
            return None

    # --- 目录 -----------------------------------------------------------
    def list_directory(self, path):
        self.send_error(404)
        return None

    def translate_path(self, path):
        path = path.split('?', 1)[0].split('#', 1)[0]
        path = posixpath.normpath(unquote(path))
        path = path.lstrip('/')
        words = [w for w in path.split('/') if w not in ('', '.', '..')]
        full = ROOT
        for w in words:
            full = os.path.join(full, w)
        if os.path.isdir(full):
            index = os.path.join(full, 'index.html')
            if os.path.isfile(index):
                return index
        return full

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
