Title: wordpress config 
Date: 2013-08-25 12:14
Tags: wordpress, config

# 我的wordpress设置

记录对wordpress和某些插件的设置或改进。
## wordpress设置

### ping服务列表
参考[怎样为wordpress独立博客添加百度PING服务](http://jingyan.baidu.com/article/3f16e00394d2242591c103ec.html)和[wordpress rss ping 快速使搜索引擎收录](http://17610376.blog.51cto.com/366886/130436)这两篇文章，进行如下设置。

安装插件[wordpress ping optimizer](http://wordpress.org/extend/plugins/wordpress-ping-optimizer/)。

设置=>撰写=>更新服务
    http://blogsearch.google.com/ping/RPC2
    http://ping.baidu.com/ping/RPC2
    http://api.my.yahoo.com/RPC2
    http://api.my.yahoo.com/rss/ping
    http://ping.feedburner.com
    http://www.zhuaxia.com/rpc/server.php
    http://www.xianguo.com/xmlrpc/ping.php
    http://www.feedsky.com/api/RPC2
    http://blog.iask.com/RPC2
    http://ping.blog.qikoo.com/rpc2.php
    http://rpc.pingomatic.com/
    http://rpc.technorati.com/rpc/ping
    http://www.blogsdominicanos.com/ping/
## 针对wordpress的修改

### 修改摘要长度

对于wordpress2.8.0之后的版本，在theme的functions.php里添加如下代码，把140改为需要的摘要长度即可.

	function custom_excerpt_length( $length ) {
		return 140;
	}
	add_filter( 'excerpt_length', 'custom_excerpt_length', 999 );

### Minify js和css

将部分插件的javascript和css代码统一放在:
    wp-content/custom.js
    wp-content/custom.css
使用w3 total cache的Minify（手动模式）整合并压缩所有内部的javascript和css代码。
需要注意的是，javascript代码最好置于`</body>`标签前，被其他js文件依赖的javascript（比如jquery）应当放在前面。
## 针对插件的修改

### Advanced Custom Fields
配合主题添加许可协议的post-meta。

首先添加一个select类型的field，名为license_type，许可协议的名称和值使用''|''分隔，如下:

	
	CC BY-NC-ND 3.0 CN|http://creativecommons.org/licenses/by-nc-nd/3.0/cn/ : CC BY-NC-ND 3.0 CN
	CC0|http://creativecommons.org/publicdomain/zero/1.0/deed.zh : CC0

然后在主题的post-meta区，添加如下代码:

	<?php
	    $license_type = get_field('license_type');
	    if ($license_type) {
	        list($license_name, $license_url) = split('[|]', $license_type);
	        printf('许可协议 `<a title="本文的许可协议" href="%s">`%s`</a>`, $license_url, $license_name);
	    } else {
	        printf('许可协议 `<a title="本文的许可协议" href="http://blog.atime.me/agreement/">`使用协议`</a>`);
	    }
	?>

### W3 Total Cache

`<wrap center round alert 100%>`
w3tc无法正常缓存非ascii路径的文件。
`</wrap>`
#### 禁用w3tc的page cache clean，使用ocp+cron自动cache

研究w3tc page cache preload问题的时候，在[这里](http://wordpress.org/support/topic/w3-total-cache-page-cache-not-preloading)发现了[ocp](http://patrickmylund.com/projects/ocp/)，即Optimus Cache Prime，可以配合w3tc自动重建缓存。因此不需要w3tc Page Cache的Cache Preload和Garbage Collection功能了。

Cache Preload直接在Page Cache选项里禁用即可。若要禁用Garbage Collection功能，在w3tc的PgCache.php中将run()函数的下面一段代码注释掉:

	
	/* remove page cache clean job and do this with ocp
	if ($this->_config->get_string('pgcache.engine') == 'file' || 
	        $this->_config->get_string('pgcache.engine') == 'file_generic') {
	    add_action('w3_pgcache_cleanup', array(
	        &$this,
	        'cleanup'
	    ));
	   }

	*/

然后下载ocp并配置cron来自动重建缓存。
#### w3tc异步加载js

W3 Total Cache的Minify手动模式已经支持Non Blocking加载js代码，不过不支持async加载。修改其Minify.php文件的get_script()函数，在合适的位置添加如下一句即可:

	c.async = true;

### Social Medias Connect

为了让''选择要同步的账户''框默认选择默认账户，而不是''不进行同步''，修改插件的SMConnect.php文件，在函数''show_meta_box()''中，交换select下拉列表元件的显示顺序，最后改为如下效果:

	echo `<p>``<strong>`选择要同步的账户：`</strong>``<br/>`;
	echo `<select data-url="'.admin_url().'" id="smc-user-change" name="smc-user">`;
	if($sync_user_id){
	   $myuser=new WP_User($sync_user_id);
	   echo `<option value="'.$sync_user_id.'">`.$myuser->display_name.'（默认账号）`</option>`;
	}
	if($sync_user_id!=$curr_user_id){
	   $myuser=new WP_User($curr_user_id);
	   echo `<option value="'.$curr_user_id.'">`.$myuser->display_name.'（你自己）`</option>`;
	}
	echo `<option value="">`不进行同步`</option>`;
	echo `</select>` `<img id="smc-loading-img" src="'.$this->`base_dir.'/images/loading-publish.gif"           style="display:none;" alt="" />`</p>`;

### Live Blogging

显示样式默认为:

	`<p>`
	    `<strong>`$DATE`</strong>`
	`</p>`
	$CONTENT
	`<div style="width:100%; height:1px; background-color:#6f6f6f; margin-bottom:3px;">`
	`</div>`

修改为

	`<div style = "background-color: white;margin: 0.7em 0px 3em 0px;padding: 1.5em 1.5em 0.5em 1.5em;-webkit-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2), 0 0 50px rgba(0, 0, 0, 0.1);-moz-box-shadow: 0 0 4px rgba(0, 0, 0, 0.2), 0 0 50px rgba(0, 0, 0, 0.1);box-shadow: 0 0 5px rgba(0, 0, 0, 0.2), 0 0 50px rgba(0, 0, 0, 0.1);margin-bottom: 15px;">`
	`<p>`
	    `<strong>`$DATE`</strong>`
	`</p>`
	$CONTENT
	`</div>`


### Google Sitemaps V3 for qtranslate

配合ocp和cron实现自动更新w3tc的页面缓存，具体修改思路在[将wordpress打造成一个伪静态博客](http://blog.atime.me/2012/12/make-wordpress-a-pseudo-static-blog/)里描述，代码相关的介绍记录在[:codes:snippets:wordpress_tweak_ocp_sitemap](/codes/snippets/wordpress_tweak_ocp_sitemap)。

### Table of contents plus(TOC+)

添加如下功能:点击h1以下级别的标题时，平滑滚动到目录列表的对应列表项。

设置方面，将TOC+的高级设置里的"顶部偏移"设为0px。php代码方面，修改toc.php。修改后的代码放在[这里](https///github.com/wilbur-ma/wordpress-tweak/tree/master/table-of-contents-plus)，1211版本的patch放在[这里](https///github.com/wilbur-ma/wordpress-tweak/blob/master/patch/table-of-contents-plus-1211.patch)。


## 针对主题的修改

### Responsive
针对主题Responsive 1.8.4.1的修改，源码放在[这里](https///github.com/wilbur-ma/wordpress-tweak/tree/master/responsive)。
#### blog.php

将分类链接挪到post-meta里

	`<div class="post-meta">`
	    `<?php responsive_post_meta_data(); ?>`
	    `<?php printf(__('分类 %s', 'responsive'), get_the_category_list(', ')); ?>` 
	    `<?php if ( comments_open() ) : ?>`
	    `<span class="comments-link">`
	    ...
	`</div>`

#### footer.php

1. 在`</body>`标签前添加自定义的js脚本

	`<script type="text/javascript" src="http://static.atime.me/js/wordpress3_custom.js">``</script>`

2. 修改版权年限，效果为''2012-''，添加cc许可协议80*15图片。

	`<div class="grid col-300 copyright">`
	    `<?php esc_attr_e('&copy;', 'responsive'); ?>` 
	    2012-`<?php _e(date('Y')); ?>`
	    `<a href="<?php echo home_url('/') ?>`" title="`<?php echo esc_attr(get_bloginfo('name', 'display')); ?>`">
	        `<?php bloginfo('name'); ?>`
	    `</a>` / 
	    `<a href="http://blog.atime.me/about/#License_Disclaimer">`许可协议和免责声明`</a>` / 
	    `<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/cn/">`
	        `<img alt="知识共享许可协议" src="http://i.creativecommons.org/l/by-nc-nd/3.0/cn/80x15.png" width="80px" height="15px" />`
	    `</a>`
	`</div>``<!-- end of .copyright -->`

#### header.php

1. 添加favicon。

	`<link rel="shortcut icon" href="http://static.atime.me/images/favicon.ico" />`

2. 添加自定义的css文件。

	`<link rel="stylesheet" href="http://static.atime.me/css/wordpress3_custom.css" type="text/css" />` 

#### single.php

将分类链接挪到post-meta里

	`<div class="post-meta">`
	    `<?php responsive_post_meta_data(); ?>`
	    `<?php printf(__('分类 %s', 'responsive'), get_the_category_list(', ')); ?>` 
	    `<?php if ( comments_open() ) : ?>`
	    `<span class="comments-link">`
	    ...
	`</div>`

#### style.css

将段落间距由1.6em改为1.2em。

	/* =Margins & Paddings
	-------------------------------------------------------------- */
	p, hr, dl, pre, form, table, address, blockquote {
	    /*margin: 1.6em 0;*/
	    margin: 1.2em 0;
	}

#### languages/zh_CN.po

将

	
	msgid "Posted in %s"
	msgstr "文章分类 %s"

改为

	
	msgid "Posted in %s"
	msgstr "分类：%s"

改完后，可参考[这里](/tools/debian/tricks#编译po文件)的方法编译po文件。
## 参考资料

*  [[http://developer.yahoo.com/performance/rules.html|
Best Practices for Speeding Up Your Web Site]]

*  [Plugin API/Filter Reference/excerpt length](http://codex.wordpress.org/Plugin_API/Filter_Reference/excerpt_length)
*  [Optimus Cache Prime Project](http://patrickmylund.com/projects/ocp/)
*  [怎样为wordpress独立博客添加百度PING服务](http://jingyan.baidu.com/article/3f16e00394d2242591c103ec.html)
*  [wordpress rss ping 快速使搜索引擎收录](http://17610376.blog.51cto.com/366886/130436)

