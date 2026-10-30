/* 「场景聚焦」已并入「业务聚焦」页。
   head 里的 meta refresh 是主跳转，这里做兜底（个别环境会忽略 meta refresh）。
   按项目约定，HTML 里不留内联脚本，跳转逻辑放在这个独立文件。 */
location.replace('business.html?s=scene');
