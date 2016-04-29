	$menu_act=param('menu_act');

$content_html=qq~$content_html
<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs" class="wide">
				<ul>
					<li class="first activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=settings"><span>Настройки</span></a></li>~;
if ($access ne "error") {$content_html=qq~$content_html				
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=backup"><span>Восстановление</span></a></li>~;
	if ($hide_banners ne "1") {
		$content_html=qq~$content_html<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=banners"><span>Баннеры</span></a></li>~;
	}
	$content_html=qq~$content_html
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1"><span>Макет сайта</span></a></li>
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&css_edit=ok"><span>Cтили сайта</span></a></li>~;
	if ($hide_templates ne "1") {
		$content_html=qq~$content_html<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=template"><span>Модули</span></a></li>~;
	}
}

$content_html=qq~$content_html					
				</ul>
			</div>
			
			
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">
		<div id="pages">~;	
		
	
	($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
	if ($mday < 10 ) { $mdays="0"; $mday="$mdays$mday";}
	$mon++; if ($mon < 10 ) { $mon="0$mon";}
	$year=1900+$year; 
	$today="$year-$mon-$mday";

	if ($menu_act eq "") {
		old_saves ();
		menu_listing ();
		
	} elsif ($menu_act eq "ok")  {

		$title_site=param('title_site');
		$name_site=param('name_site');
		$cache_mode=param('cache_mode');
		$dir_main=param('dir_main');
		$dir_cgi=param('dir_cgi');		
		$main_page=param('main_page');
		$dir_css=param('dir_css');
		$dir_fonts=param('dir_fonts');
		$robot_help=param('robot_help');
		$maket_page=param('maket_page');
		$maket_article=param('maket_article');
		$maket_news=param('maket_news');
		$maket_gallery=param('maket_gallery');
		$maket_catalog=param('maket_catalog');
		$maket_product=param('maket_product');
		$maket_product_compare=param('maket_product_compare');
		$maket_basket=param('maket_basket');
		$maket_private=param('maket_private');
		$email_feedback=param('email_feedback');
		$email_orders=param('email_orders');
		$fade_page=param('fade_page');
		$counter=param('counter');
		$host_db=param('host_db');
		$user_db=param('user_db');
		$password_db=param('password_db');
		$name_db=param('name_db');
		$yamarket_name=param('yamarket_name');
		$yamarket_fullname=param('yamarket_fullname');
		$yamarket_delivery=param('yamarket_delivery');		
		$payment_login=param('payment_login');
		$payment_pass1=param('payment_pass1');
		$payment_pass2=param('payment_pass2');
		$phone_code1=param('phone_code1');
		$phone_code2=param('phone_code2');
		$phone_num1=param('phone_num1');
		$phone_num2=param('phone_num2');
		$address=param('address');
		$timemode=param('timemode');
		$copyright=param('copyright');
		$slide_ox=param('slide_ox');
		$slide_oy=param('slide_oy');
		
		$address =~ s/\n/\<br\>/g;
		$timemode =~ s/\n/\<br\>/g;
		$copyright =~ s/\n/\<br\>/g;

		$title_site =~ s/\'/\"/g;
		
		if ($main_page eq ""){$main_page ='<!--#include virtual="/cgi-bin/index.cgi?num_edit=1"-->';}
		else {$main_page = '<!--#include virtual="'.$main_page.'"-->'};
		if ($maket_page eq ""){$maket_page ="1";}
		if ($maket_article eq ""){$maket_article ="1";}	
		if ($maket_news eq ""){$maket_news ="1";}
		if ($maket_gallery eq ""){$maket_gallery ="1";}
		if ($maket_catalog eq ""){$maket_catalog ="1";}
		if ($maket_product eq ""){$maket_product ="1";}
		if ($maket_product_compare eq ""){$maket_product_compare ="1";}		
		if ($maket_basket eq ""){$maket_basket ="1";}	
		if ($maket_private eq ""){$maket_private ="1";}	
		
		my $dir_index = $dir_main;
		if ($dir_cgi eq "on") {$dir_index="";}
		open OUT, (">../../../$dir_index/index.html");
			print OUT "$main_page"; 
		close(OUT);			

		open OUT, (">../layouts/set_maket");
			print OUT "$maket_page|$maket_article|$maket_news|$maket_gallery|$maket_catalog|$maket_product|$maket_product_compare|$maket_basket|$maket_private"; 
		close(OUT);		

		open OUT, (">../$dirs/meta_title");
			print OUT "$title_site"; 
		close(OUT);
	
		open OUT, (">../layouts/set_phone");
			print OUT "$phone_code1|$phone_num1|$phone_code2|$phone_num2"; 
		close(OUT);		
		open OUT, (">../layouts/set_address");
			print OUT "$address"; 
		close(OUT);
		open OUT, (">../layouts/set_timemode");
			print OUT "$timemode"; 
		close(OUT);
		open OUT, (">../layouts/set_copyright");
			print OUT "$copyright"; 
		close(OUT);		
		
		$access_mysql=qq~package Core::Config;

%Core::Config::DB = (
						'host' => '$host_db',
						'user' => '$user_db',
						'password' => '$password_db',
						'db' => '$name_db',
					);
1;~;
		
		open OUT, (">../engine/lib/Core/Config.pm");
			print OUT "$access_mysql"; 
		close(OUT);
		
		$new_email_feedback = $email_feedback;
			$new_email_feedback =~ s/\@/\\@/;
		$new_email_orders = $email_orders;
			$new_email_orders =~ s/\@/\\@/;

		if ($dir_cgi eq "on") {$new_dir_cgi="1";} else {$new_dir_cgi="0";} 	

		if ($new_dir_cgi eq "1") {
		open OUT, (">../../../admin/backup/access");
			print OUT "$host_db|$user_db|$password_db|$name_db"; 
		close(OUT);
		$dirs_slides="../../../files/slides";
		$dirs_banners="../../../files/banners";
		}
		else {
		open OUT, (">../../../$dirs_site/admin/backup/access");
			print OUT "$host_db|$user_db|$password_db|$name_db"; 
		close(OUT);
		$dirs_slides="../../../$dirs_site/files/slides";
		$dirs_banners="../../../$dirs_site/files/banners";
		}
			
		if ($fade_page eq "on") {$new_fade_page="1";} else {$new_fade_page="0";}
		if ($cache_mode eq "on") {$cache_mode="1";} else {$cache_mode="0";} 	
			
		open OUT, (">../layouts/settings");
			print OUT "$name_site|$cache_mode|$dir_main|$new_dir_cgi|$dir_css|$dir_fonts|$new_email_feedback|$new_email_orders|$new_fade_page|$payment_login|$payment_pass1|$payment_pass2|$robot_help"; 
		close(OUT);
		
		if ($hide_products_yamarket ne "1"){
			my $string = length($yamarket_name);
			if ($string > 20){
				$yamarket_name=substr($yamarket_name,0,20); $yamarket_name=qq~$yamarket_name~;
			}
			if ($yamarket_delivery > 0 or $yamarket_delivery eq "0" or $yamarket_delivery eq ""){
				if ($yamarket_delivery eq "" or $yamarket_delivery eq "0"){$yamarket_delivery = "Бесплатно";}
			}
			else {$yamarket_delivery = "Бесплатно";}
			open OUT, (">../layouts/set_yamarket");
				print OUT "$yamarket_name|$yamarket_fullname|$yamarket_delivery"; 
			close(OUT);		
		}
		
		if ($hide_slideshow_edit ne "1"){
			open OUT, (">$dirs_slides/settings.txt");
				print OUT "$slide_ox|$slide_oy"; 
			close(OUT);	
		}

		if ($new_dir_cgi eq "1") {$dirs=qq~
		\$dirs_home="..";
		\$dirs_css="../../../$dir_css";
		\$dirs_fonts="$dir_fonts";		
		\$dirs_img="../../../uploads";
		\$dirs_catalog="../../../files/catalog";
		\$dirs_catalog_www="/files/catalog";
		\$dirs_catalog_www2="../files/catalog";		
		\$dirs_foto="../../../files/gallery";
		\$dirs_foto_www="/files/gallery";
		\$dirs_foto_www2="../files/gallery";
		\$dirs_gallery_css="../../../admin/site/css/gallery";		
		\$dirs_news="../../../files/news";
		\$dirs_news_www="/files/news";
		\$dirs_news_www2="../files/news";
		\$dirs_slides="../../../files/slides";
		\$dirs_slides_www="/files/slides";
		\$dirs_slides_www2="../files/slides";
		\$dirs_banners="../../../files/banners";
		\$dirs_banners_www="/files/banners";
		\$dirs_banners_www2="../files/banners";
		\$dirs_public="../../../files/public";
		\$dirs_public_www="/files/public";
		\$dirs_public_www2="../files/public";
		\$dirs_video="../../../files/video";
		\$dirs_video_www="/files/video";
		\$dirs_video_www2="../files/video";~;}
		else {$dirs=qq~
		\$dirs_home="../\$dirs_site";
		\$dirs_css="../../../\$dirs_site/$dir_css";
		\$dirs_fonts="$dir_fonts";		
		\$dirs_img="../../../\$dirs_site/uploads";
		\$dirs_catalog="../../../\$dirs_site/files/catalog";
		\$dirs_catalog_www="/files/catalog";
		\$dirs_catalog_www2="../\$dirs_site/files/catalog";		
		\$dirs_foto="../../../\$dirs_site/files/gallery";
		\$dirs_foto_www="/files/gallery";
		\$dirs_foto_www2="../\$dirs_site/files/gallery";
		\$dirs_gallery_css="../../../\$dirs_site/admin/site/css/gallery";
		\$dirs_news="../../../\$dirs_site/files/news";
		\$dirs_news_www="/files/news";
		\$dirs_news_www2="../\$dirs_site/files/news";
		\$dirs_slides="../../../\$dirs_site/files/slides";
		\$dirs_slides_www="/files/slides";
		\$dirs_slides_www2="../\$dirs_site/files/slides";
		\$dirs_banners="../../../\$dirs_site/files/banners";
		\$dirs_banners_www="/files/banners";
		\$dirs_banners_www2="../\$dirs_site/files/banners";
		\$dirs_public="../../../\$dirs_site/files/public";
		\$dirs_public_www="/files/public";
		\$dirs_public_www2="../\$dirs_site/files/public";
		\$dirs_video="../../../\$dirs_site/files/video";
		\$dirs_video_www="/files/video";
		\$dirs_video_www2="../\$dirs_site/files/video";~;}		
		
		$parametrs=qq~
		\$url_site=".$name_site";
		\$dirs_site="$dir_main";
		\$cache_mode="$cache_mode";
		\$email_feedback="$new_email_feedback";
		\$email_orders="$new_email_orders";
		\$robot_help="$robot_help";
		\$maket_page="$maket_page";
		\$maket_article="$maket_article";		
		\$maket_news="$maket_news";
		\$maket_gallery="$maket_gallery";
		\$maket_catalog="$maket_catalog";
		\$maket_product="$maket_product";
		\$maket_product_compare="$maket_product_compare";
		\$maket_basket="$maket_basket";
		\$maket_private="$maket_private";
		
		$dirs
		~;		
		
		open OUT, (">../engine/lib/set_parametrs");
			print OUT "$parametrs"; 
		close(OUT);	

		use DBI;		
		
		my $dsn = "DBI:mysql:database=$name_db;host=$host_db;port=3306";
		$dbh = DBI->connect( $dsn, $user_db, $password_db ) or $mysql_error ="Проверьте доступы подключения к базе.";		

		if ($mysql_error) {
		open OUT, (">>../engine/lib/set_parametrs");
			print OUT "\$access = \"error\";"; 
		close(OUT);
		$content_html=qq~$content_html<div class="delete_page">Проверьте доступы подключения к базе.</div>~;}
		else {
			if ($new_dir_cgi eq "0") {
				if(-e "../../../$dir_main/$dir_css") {$css_warning="";} else {$css_warning="Проверьте правильность указания пути к стилям (CSS)."}
				if(-e "../../../$dir_main/index.html") {$content_html=qq~$content_html<div class="save_page">Настройки сохранены. $css_warning</div>~;}
				else {
				open OUT, (">>../engine/lib/set_parametrs");
					print OUT "\$access = \"error\";"; 
				close(OUT);				
				$content_html=qq~$content_html<div class="delete_page">Проверьте правильность указания корня директории.</div>~;}
			
			} else {
				if(-e "../../../$dir_css") {$css_warning="";} else {$css_warning="Проверьте правильность указания пути к стилям (CSS)."}
				if(-e "../../../index.html") {$content_html=qq~$content_html<div class="save_page">Настройки сохранены. $css_warning</div>~;}
				else {
				open OUT, (">>../engine/lib/set_parametrs");
					print OUT "\$access = \"error\";"; 
				close(OUT);				
				$content_html=qq~$content_html<div class="delete_page">Уберите галку "cgi-bin находится в корне".</div>~;}
			}
		}

		open OUT, (">../engine/lib/counter");
			print OUT "$counter"; 
		close(OUT);	
		
		my $mod_news=""; my $mod_articles=""; my $mod_catalog=""; my $mod_products=""; my $mod_products_hit=""; my $mod_questions=""; my $mod_contacts="";
		if(-e "../modules/news.cgi"){$mod_news="1";}
		if(-e "../modules/articles.cgi"){$mod_articles="1";}
		if(-e "../modules/category.cgi"){$mod_catalog="1";}
		if(-e "../modules/products.cgi"){$mod_products="1";
			if ($hide_products_hit ne "1" or $hide_products_spec ne "1" or $hide_products_new ne "1"){
				$mod_products_hit="1";
			}
		}
		if(-e "../modules/questions.cgi"){$mod_questions="1";}		
		
		if ($hide_phone1_set ne "1" or $hide_phone2_set ne "1" or $hide_address_set ne "1" or $hide_timemode_set ne "1" or $hide_copyright_set ne "1"){$mod_contacts="1";}
		
		my $require ='
		require "admin/engine/lib/parametr.cgi";
		'.($mod_news eq "1"?'require "templates/news.cgi";':'').'
		'.($mod_articles eq "1"?'require "templates/articles.cgi";':'').'
		require "templates/name.cgi";
		'.($hide_private ne "1"?'require "templates/auth.cgi";
		require "templates/private.cgi";':'').'
		require "templates/pages.cgi";
		'.($mod_catalog eq "1"?'require "templates/catalog.cgi";':'').'
		'.($mod_products eq "1"?'require "templates/products.cgi";':'').'		
		'.($mod_products_hit eq "1"?'require "templates/products_hit.cgi";':'').'
		'.($hide_products_random ne "1"?'require "templates/products_random.cgi";':'').'
		require "templates/feedback.cgi";
		require "templates/sitemap.cgi";
		require "templates/fadepage.cgi";
		'.($mod_questions eq "1"?'require "templates/questions.cgi";':'').'
		'.($mod_contacts eq "1"?'require "templates/contacts.cgi";
		my ($phone, $address, $timemode, $copyright) = build_Contacts();':'').'
		'.($hide_valuta ne "1"?'require "templates/valuta.cgi";':'').'
		'.($hide_pogoda ne "1"?'require "templates/pogoda.cgi";':'').'
		'.($hide_metal ne "1"?'require "templates/metal.cgi";':'').'
		'.($hide_callback ne "1"?'require "templates/callback.cgi";':'').'
		'.($hide_gallery_lite ne "1"?'require "templates/gallery_lite.cgi";':'').'
		'.($hide_slideshow_edit ne "1"?'require "templates/slideshow.cgi";':'').'
		'.($hide_banners ne "1"?'require "templates/banners.cgi";':'').'
		open(BO, "admin/$dirs/sort_strukture"); $sort_pages = <BO>; close(BO);
		'.($mod_catalog eq "1"?'open(BO, "admin/$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
		foreach my $line(@select_sort){chomp($line);
		my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
		$sort_category=qq~$select_sort_cat_~;
		$sort_product=qq~$select_sort_product_~;}':'').'
		'.($mod_news eq "1"?'open(BO, "admin/$dirs/sort_news"); $sort_news = <BO>; close(BO);
		open(BO, "admin/$dirs/set_news"); @set_news = <BO>; close(BO);
		foreach my $line(@set_news){chomp($line);
		my ($limit_news_, $type_news_) = split(/\|/, $line);
		$limit_news=qq~$limit_news_~; $type_news=qq~$type_news_~;}':'').'
		'.($mod_articles eq "1"?'open(BO, "admin/$dirs/sort_articles"); $sort_articles = <BO>; close(BO);
		open(BO, "admin/$dirs/set_articles"); @set_articles = <BO>; close(BO);
		foreach my $line(@set_articles){chomp($line);
		my ($limit_articles_, $ajax_save_) = split(/\|/, $line);
		$limit_articles=qq~$limit_articles_~;}':'').'
		open OUT, ("admin/engine/lib/counter"); @counter = <OUT>;
		foreach my $text(@counter) {$counter=qq~$counter$text~;}
		$random_n = rand(1);
		1;';		
		open OUT, (">../../templates/connection/require.cgi");
			print OUT "$require"; 
		close(OUT);	
		
		my $pages_menu=""; my $pages_menu_limit=""; my $pages_submenu=""; my $pages_tree="";
		my $catalog_menu=""; my $catalog_menu_limit=""; my $catalog_tree=""; my $catalog_category=""; my $news_lite="";
		my $articles_lite=""; my $gallery_lite=""; my $slideshow="";
		opendir (DBDIR, "../layouts"); @list_dir = readdir(DBDIR); close DBDIR;
		foreach $line_wall(@list_dir) {
			chomp ($line_wall);
			if ($line_wall ne "." && $line_wall ne "..") {
				($name_file, $num) = split(/\./, $line_wall);
				if ($name_file eq "maket_html") {
					my $maket_file="";				
					open OUT, ("../layouts/maket_html.$num"); @maket = <OUT>;
					foreach my $text(@maket) {$maket_file=qq~$maket_file$text~;}			
					if ($maket_file =~ /\$PAGES_MENU/){$pages_menu="1";}
					if ($maket_file =~ /\$PAGES_MENU_LIMIT/){$pages_menu_limit="1";}
					if ($maket_file =~ /\$PAGES_SUBMENU/){$pages_submenu="1";}
					if ($maket_file =~ /\$PAGES_TREE/){$pages_tree="1";}
					if ($maket_file =~ /\$CATALOG_MENU/){$catalog_menu="1";}
					if ($maket_file =~ /\$CATALOG_MENU_LIMIT/){$catalog_menu_limit="1";}
					if ($maket_file =~ /\$CATALOG_TREE/){$catalog_tree="1";}
					if ($maket_file =~ /\$CATALOG_CATEGORY/){$catalog_category="1";}
					if ($maket_file =~ /\$NEWS/){$news_lite="1";}
					if ($maket_file =~ /\$ARTICLES/){$articles_lite="1";}
					if ($maket_file =~ /\$PRODUCTS_RANDOM/){$products_random="1";}
					if ($maket_file =~ /\$GALLERY_LITE/){$gallery_lite="1";}
					if ($maket_file =~ /\$SLIDESHOW/){$slideshow="1";}
				}
			}
		}	
		
		my $variables ='
		'.($pages_menu eq "1"?'$pages_menu = build_PagesMenu($sort_pages);':'').'
		'.($pages_menu_limit eq "1"?'$pages_menu_limit = build_PagesMenuLimit($sort_pages);':'').'
		'.($pages_submenu eq "1"?'$pages_submenu = build_PagesSubMenu($num_edit, $name_section, $parent_sid, $page_alias, $sort_pages);':'').'
		'.($pages_tree eq "1"?'$pages_tree = build_PagesTree($sort_pages);':'').'
		'.($catalog_menu eq "1"?'$catalog_menu = build_CatalogMenu($sort_category);':'').'
		'.($catalog_menu_limit eq "1"?'$catalog_menu_limit = build_CatalogMenuLimit($sort_category);':'').'
		'.($catalog_tree eq "1"?'if ($adm_act ne "private"){$catalog_tree = build_CatalogTree($sort_category);}':'').'
		'.($catalog_category eq "1"?'if ($adm_act ne "private"){$catalog_category = build_Category($sort_category);}':'').'
		'.($news_lite eq "1"?'$news = build_News($limit_news, $sort_news, $type_news);':'').'
		'.($articles_lite eq "1"?'$articles = build_Articles($limit_articles, $sort_articles);':'').'
		'.($gallery_lite eq "1" && $hide_gallery_lite ne "1"?'$gallery_lite = build_galleryLite();':'').'
		'.($slideshow eq "1" && $hide_slideshow_edit ne "1"?'$slideshow = build_slideShow();':'').'
		'.($hide_banners ne "1"?'$banner_ver1 = build_Banner("banner_ver1"); $banner_ver2 = build_Banner("banner_ver2"); $banner_ver3 = build_Banner("banner_ver3"); $banner_gor1 = build_Banner("banner_gor1"); $banner_gor2 = build_Banner("banner_gor2"); $banner_gor3 = build_Banner("banner_gor3");':'').'
		'.($hide_products_hit ne "1"?'if ($adm_act eq "pages" && $num_edit eq "1"){$products_hit = build_ProductHit("hit");}':'').'
		'.($hide_products_new ne "1"?'if ($adm_act eq "pages" && $num_edit eq "1"){$products_new = build_ProductHit("new");}':'').'
		'.($hide_products_spec ne "1"?'if ($adm_act eq "pages" && $num_edit eq "1"){$products_spec = build_ProductHit("spec");}':'').'
		'.($products_random eq "1" && $hide_products_random ne "1"?'$products_random = build_ProductRandom();':'').'
		if ($adm_act eq "pages" && $num_edit eq "1"){
			if ($products_hit ne ""){$products_hit .= $script_product_hit;}
			elsif ($products_new ne ""){$products_new .= $script_product_hit;}
			elsif ($products_spec ne ""){$products_spec .= $script_product_hit;}
		}
		1;';
		open OUT, (">../../templates/connection/variables.cgi");
			print OUT "$variables"; 
		close(OUT);	
		
		my $variables_assign="";
		open OUT, ("../../templates/connection/variables_assign.cgi"); @var_assign = <OUT>;
		foreach my $text(@var_assign) {$variables_assign=qq~$variables_assign$text~;}

		if ($variables_assign eq ""){
		$variables_assign ='
		$tpl->assign(NAME => "$name");
		$tpl->assign(CONTENT => "$content");
		$tpl->assign(TITLE => "$title");
		$tpl->assign(DESCRIPTION => "$description");
		$tpl->assign(KEYWORDS => "$keywords");
		$tpl->assign(PAGES_MENU => "$pages_menu");
		$tpl->assign(PAGES_MENU_LIMIT => "$pages_menu_limit");
		$tpl->assign(PAGES_SUBMENU => "$pages_submenu");
		$tpl->assign(PAGES_TREE => "$pages_tree");
		$tpl->assign(CATALOG_MENU => "$catalog_menu");
		$tpl->assign(CATALOG_MENU_LIMIT => "$catalog_menu_limit");
		$tpl->assign(CATALOG_TREE => "$catalog_tree");
		$tpl->assign(CATALOG_CATEGORY => "$catalog_category");
		$tpl->assign(PRODUCTS_HIT => "$products_hit");
		$tpl->assign(PRODUCTS_NEW => "$products_new");
		$tpl->assign(PRODUCTS_SPEC => "$products_spec");
		$tpl->assign(PRODUCTS_RANDOM => "$products_random");
		$tpl->assign(GALLERY_LITE => "$gallery_lite");
		$tpl->assign(BANNER_VER1 => "$banner_ver1");
		$tpl->assign(BANNER_VER2 => "$banner_ver2");
		$tpl->assign(BANNER_VER3 => "$banner_ver3");
		$tpl->assign(BANNER_GOR1 => "$banner_gor1");
		$tpl->assign(BANNER_GOR2 => "$banner_gor2");
		$tpl->assign(BANNER_GOR3 => "$banner_gor3");
		$tpl->assign(NEWS => "$news");
		$tpl->assign(ARTICLES => "$articles");
		$tpl->assign(FADE_PAGE => "$fade_page");
		$tpl->assign(CALLBACK => "$callback");
		$tpl->assign(COUNTER => "$counter");
		$tpl->assign(VALUTA => "$valuta");
		$tpl->assign(POGODA => "$pogoda");
		$tpl->assign(METAL => "$metal");
		$tpl->assign(PHONE => "$phone");
		$tpl->assign(ADDRESS => "$address");
		$tpl->assign(TIMEMODE => "$timemode");
		$tpl->assign(COPYRIGHT => "$copyright");
		$tpl->assign(PRIVATE_PANEL => "$private_panel");
		$tpl->assign(SLIDESHOW => "$slideshow");
		$tpl->assign(RAND_N => "$random_n");

		1;';		
		open OUT, (">../../templates/connection/variables_assign.cgi");
			print OUT "$variables_assign"; 
		close(OUT);
		}
		
		my $css_edit="";
		open OUT, ("$dirs_css"); @css_edit = <OUT>;
		foreach my $text(@css_edit) {$css_edit=qq~$css_edit$text~;}		
		
		my $css_tinymce="";
		if ($dir_fonts ne ""){
			$dir_fonts =~ s/^\///g;
			$css_tinymce .="\@import url('/".$dir_fonts."');\n";
		}
		while ($css_edit =~ m/#content (.+?){(.+?)}/g) {
			if ($1 eq "a "){
				my $link = $2;
				$link =~ s/;$/ \!important;/g;
				$css_tinymce .= "a {".$link."}\n";
			}
			else {$css_tinymce .= $1."{".$2."}\n";}
		}
		while ($css_edit =~ m/#content (.+?){\s+(.*)/g) {
			$css_tinymce .= $1."{".$2."}\n";
		}		
		$dirs_css =~ s/\/(\w+).css$/\/style_tinymce.css/g;

		open OUT, (">$dirs_css");	   
				print OUT "$css_tinymce"; 	   
		close(OUT); 

		ClearCache("../..", "1");
		if ($cache_mode eq "1"){mkdir ("../../cache", 0755);}
		elsif ($cache_mode eq "0"){rmdir ("../../cache");}
		
		old_saves ();
		menu_listing ();
	} 
	

sub old_saves {

		open(BO, "../layouts/meta_title"); $ok_title_site_old = <BO>; close(BO);
		
		$ok_title_site_old =~ s/\"/\'/g;

		use Core::Config;
	
		open(BO, "../layouts/settings"); my @settings = <BO>; close(BO);
		foreach my $line(@settings)
			{
		chomp($line);
		my ($name_site, $cache_mode, $dir_main, $dir_cgi, $dir_css, $dir_fonts, $email_feedback, $email_orders, $fade_page, $payment_login, $payment_pass1, $payment_pass2, $robot_help) = split(/\|/, $line);
		$ok_name_site_old=qq~$name_site~;
		$ok_cache_mode_old=qq~$cache_mode~;
		$ok_dir_main_old=qq~$dir_main~;
		$ok_dir_cgi_old=qq~$dir_cgi~;
		$ok_dir_css_old=qq~$dir_css~;
		$ok_dir_fonts_old=qq~$dir_fonts~;
		$email_feedback_old=qq~$email_feedback~;
		$email_orders_old=qq~$email_orders~;
		$fade_page_old=qq~$fade_page~;
		$ok_payment_login_old=qq~$payment_login~;
		$ok_payment_pass1_old=qq~$payment_pass1~;
		$ok_payment_pass2_old=qq~$payment_pass2~;
		$ok_robot_help_old=qq~$robot_help~;
			}
			
		if ($hide_products_yamarket ne "1"){
			open(BO, "../layouts/set_yamarket"); my @set_yamarket = <BO>; close(BO);
			foreach my $line(@set_yamarket)
				{
			chomp($line);
			my ($yamarket_name, $yamarket_fullname, $yamarket_delivery) = split(/\|/, $line);
			$ok_yamarket_name_old=qq~$yamarket_name~;
			$ok_yamarket_fullname_old=qq~$yamarket_fullname~;
			$ok_yamarket_delivery_old=qq~$yamarket_delivery~;
				}	
		}

		$ok_email_feedback_old = $email_feedback_old;
			$ok_email_feedback_old =~ s/\\@/\@/;
		$ok_email_orders_old = $email_orders_old;
			$ok_email_orders_old =~ s/\\@/\@/;		
			
		
		if ($ok_dir_cgi_old eq "1") {open(BO, "../../../admin/backup/access"); @access_db = <BO>; close(BO);}
		else {open(BO, "../../../$ok_dir_main_old/admin/backup/access"); @access_db = <BO>; close(BO);}
		
		open(BO, "../layouts/set_maket"); @set_maket = <BO>; close(BO);
		foreach my $line(@set_maket){chomp($line);
		my ($select_page_, $select_article_, $select_news_, $select_gallery_, $select_catalog_, $select_product_, $select_product_compare_, $select_basket_, $select_private_) = split(/\|/, $line);
		$select_page=qq~$select_page_~; $select_article=qq~$select_article_~; $select_news=qq~$select_news_~; $select_gallery=qq~$select_gallery_~; $select_catalog=qq~$select_catalog_~; $select_product=qq~$select_product_~; $select_product_compare=qq~$select_product_compare_~; $select_basket=qq~$select_basket_~; $select_private=qq~$select_private_~;}
		
		$maket_list=""; $maket_page=""; $maket_article=""; $maket_news=""; $maket_gallery="";
		$maket_catalog=""; $maket_product=""; $maket_product_compare=""; $maket_basket=""; $maket_private="";
		opendir (DBDIR, "../layouts"); @list_dir = readdir(DBDIR); close DBDIR;
		foreach $line_wall(@list_dir) {
			chomp ($line_wall);
			if ($line_wall ne "." && $line_wall ne "..") {
				($name_file, $num) = split(/\./, $line_wall);
				if ($name_file eq "maket" && $num ne "404") { 
					open (BO, "../layouts/$line_wall"); @b = <BO>; close (BO);
					($name_old, $date_old) = split(/\|/, $b[0]);
					$maket_page .= '<option value="'.$num.'" '.($num==$select_page?'selected':'').'>'.$name_old.'</option>';
					$maket_article .= '<option value="'.$num.'" '.($num==$select_article?'selected':'').'>'.$name_old.'</option>';
					$maket_news .= '<option value="'.$num.'" '.($num==$select_news?'selected':'').'>'.$name_old.'</option>';
					$maket_gallery .= '<option value="'.$num.'" '.($num==$select_gallery?'selected':'').'>'.$name_old.'</option>';
					$maket_catalog .= '<option value="'.$num.'" '.($num==$select_catalog?'selected':'').'>'.$name_old.'</option>';
					$maket_product .= '<option value="'.$num.'" '.($num==$select_product?'selected':'').'>'.$name_old.'</option>';
					$maket_product_compare .= '<option value="'.$num.'" '.($num==$select_product_compare?'selected':'').'>'.$name_old.'</option>';
					$maket_basket .= '<option value="'.$num.'" '.($num==$select_basket?'selected':'').'>'.$name_old.'</option>';
					$maket_private .= '<option value="'.$num.'" '.($num==$select_private?'selected':'').'>'.$name_old.'</option>';
				}
			}
		}
		if ($hide_makets ne "1"){
			$maket_list = '
				<tr>
					<td class="name small"></td>
					<td class="small">
						<a title="Изменить" class="ext" href="#">Макет по умолчанию</a>
					</td>
				</tr>
				<tr>
					<td colspan="2" class="small">
						<table class="help_maket ext_param lite" id="page_new">
							<tr>
								<td class="name">Cтраницы</td>
								<td>
								<select class="category" name="maket_page" style="width:197px;">
									'.$maket_page.'
								</select>
								</td>
							</tr>';
							if(-e "../modules/articles.cgi"){
							$maket_list .='
							<tr>
								<td class="name">Статьи</td>
								<td>
								<select class="category" name="maket_article" style="width:197px;">
									'.$maket_article.'
								</select>
								</td>
							</tr>';}							
							if(-e "../modules/news.cgi"){
							$maket_list .='
							<tr>
								<td class="name">Новости</td>
								<td>
								<select class="category" name="maket_news" style="width:197px;">
									'.$maket_news.'
								</select>
								</td>
							</tr>';}
							if(-e "../modules/fotogal.cgi"){
							$maket_list .='
							<tr>
								<td class="name">Фотогалерея</td>
								<td>
								<select class="category" name="maket_gallery" style="width:197px;">
									'.$maket_gallery.'
								</select>
								</td>
							</tr>';}
							if(-e "../modules/category.cgi"){
							$maket_list .='
							<tr>
								<td class="name">Список товаров</td>
								<td>
								<select class="category" name="maket_catalog" style="width:197px;">
									'.$maket_catalog.'
								</select>
								</td>
							</tr>';}							
							if(-e "../modules/products.cgi"){
							$maket_list .='
							<tr>
								<td class="name">Карточка товара</td>
								<td>
								<select class="category" name="maket_product" style="width:197px;">
									'.$maket_product.'
								</select>
								</td>
							</tr>';}
							if($hide_products_compare ne "1"){
							$maket_list .='
							<tr>
								<td class="name">Сравнение товаров</td>
								<td>
								<select class="category" name="maket_product_compare" style="width:197px;">
									'.$maket_product_compare.'
								</select>
								</td>
							</tr>';}							
							if(-e "../modules/orders.cgi"){
							$maket_list .='
							<tr>
								<td class="name">Корзина товаров</td>
								<td>
								<select class="category" name="maket_basket" style="width:197px;">
									'.$maket_basket.'
								</select>
								</td>
							</tr>';}
							if($hide_private ne "1"){
							$maket_list .='
							<tr>
								<td class="name">Личный кабинет</td>
								<td>
								<select class="category" name="maket_private" style="width:197px;">
									'.$maket_private.'
								</select>
								</td>
							</tr>';}							
				$maket_list .='							
						</table>
					</td>
				</tr>';
		}
		
		$slideshow_edit=""; $slide_ox=""; $slide_oy="";
		if ($hide_slideshow_edit ne "1"){
			mkdir "$dirs_slides", 0755;
			if (!-e "$dirs_slides/settings.txt"){
				open OUT, (">$dirs_slides/settings.txt");
					print OUT "750|388";
				close(OUT);
			}
			open(BO, "$dirs_slides/settings.txt"); my @settings = <BO>; close(BO);
			foreach my $line(@settings){
				chomp($line);
				my ($slide_ox_, $slide_oy_) = split(/\|/, $line);
				$slide_ox=qq~$slide_ox_~;
				$slide_oy=qq~$slide_oy_~;
			}
			if ($slide_ox eq ""){$slide_ox = 750;}
			if ($slide_oy eq ""){$slide_oy = 388;}
			my $slideshow=""; my $num=""; $rand_num=rand(1);
			opendir (DBDIR, $dirs_slides); @list_dir = readdir(DBDIR); close DBDIR;
			@list_dir = sort(@list_dir);
			foreach $line_wall(@list_dir) {
				chomp ($line_wall);
				if ($line_wall ne "." && $line_wall ne "..") {
					($name_file, $exec) = split(/\./, $line_wall);
					if ($exec eq "jpg"){
						$num = $name_file; $num =~ s/slide//g;
						$slideshow .='<div class="slide" data-index="'.$num.'"><div class="foto"><img src="'.$dirs_slides_www.'/'.$name_file.'.'.$exec.'?'.$rand_num.'" alt=""></div><input title="Сменить картинку" type="file" class="file"><a title="Удалить слайд" href="#" class="del"></a></div>';
					}
				}
			}
			if ($num eq ""){$num=1001;} else {$num = $num+1;}
			$slideshow='<tr><td></td><td class="name_main"><br>Слайдер изображений</td></tr>
			<tr><td colspan="2">
				<div class="slideshow">
					<div class="container">'.$slideshow.'<div class="slide add" data-index="'.$num.'"><div class="foto"><span><em>Добавить слайд</em></span></div><input title="Добавить слайд" type="file" class="file"><a title="Удалить слайд" href="#" class="del"></a></div></div><div class="clear"></div>	
					<div class="help_slides options"><h3>Авторазмер</h3><input class="size" type="text" name="slide_ox" value="'.$slide_ox.'"><input class="size" type="text" name="slide_oy" value="'.$slide_oy.'"></div>
				</div>
			</td></tr>';

			$slideshow_edit = $slideshow;
		}
		
		my $dir_index = $ok_dir_main_old;
		if ($ok_dir_cgi_old eq "1") {$dir_index="";}
		if(-e "../../../$dir_index/index.html") {
			my $main_page_old="";
			open OUT, ("../../../$dir_index/index.html"); $main_page_old = <OUT>;
			while ($main_page_old =~ m/<!--#include virtual="(.*)"-->/g) {
				$ok_main_page_old = $1;
			}
		}
		
		foreach my $line(@access_db)
			{
		chomp($line);
		my ($host_db, $user_db, $password_db, $name_db) = split(/\|/, $line);
		$ok_host_db_old=qq~$host_db~;
		$ok_user_db_old=qq~$user_db~;
		$ok_password_db_old=qq~$password_db~;
		$ok_name_db_old=qq~$name_db~;		
			}	
			
		open(BO, "../layouts/set_phone"); my @phone = <BO>; close(BO);
		foreach my $line(@phone)
			{
		chomp($line);
		my ($phone_code1, $phone_num1, $phone_code2, $phone_num2) = split(/\|/, $line);
		$ok_phone_code1_old=qq~$phone_code1~;
		$ok_phone_num1_old=qq~$phone_num1~;
		$ok_phone_code2_old=qq~$phone_code2~;
		$ok_phone_num2_old=qq~$phone_num2~;
			}			
			
		open OUT, ("../layouts/set_address"); @address_old = <OUT>;
		foreach my $text(@address_old) {$address_old=qq~$address_old$text~;}
		$address_old =~ s/\<br\>/\n/g;
		open OUT, ("../layouts/set_timemode"); @timemode_old = <OUT>;
		foreach my $text(@timemode_old) {$timemode_old=qq~$timemode_old$text~;}
		$timemode_old =~ s/\<br\>/\n/g;
		open OUT, ("../layouts/set_copyright"); @copyright_old = <OUT>;
		foreach my $text(@copyright_old) {$copyright_old=qq~$copyright_old$text~;}
		$copyright_old =~ s/\<br\>/\n/g;		

		open OUT, ("../engine/lib/counter"); @counter_old = <OUT>;

}
	

sub menu_listing {

$current_domen = $ENV{"HTTP_HOST"};
$current_domen =~ s/^www\.//g;
	
$content_html=qq~$content_html
<script type="text/javascript" src="/admin/lib/help/settings/settings.js"></script>	
<script type="text/javascript" src="/admin/lib/settings.js"></script>
<form method="post" action="/cgi-bin/admin/engine/index.cgi">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">
			<div class="body_contacts">
				<div class="container help_contacts">~;
				if ($hide_phone1_set ne "1"){
				$content_html.=qq~
					<h4>Телефон</h4>
					<div class="item"><input class="code" name="phone_code1" type="text" value="$ok_phone_code1_old"><input class="phone" name="phone_num1" type="text" value="$ok_phone_num1_old"></div>~;
				}
				if ($hide_phone2_set ne "1"){
				$content_html.=qq~
					<div class="item"><input class="code" name="phone_code2" type="text" value="$ok_phone_code2_old"><input class="phone" name="phone_num2" type="text" value="$ok_phone_num2_old"></div>~;
				}
				if ($hide_address_set ne "1"){
				$content_html.=qq~
					<h4>Адрес</h4>
					<div class="item"><textarea class="address" name="address">$address_old</textarea></div>~;
				}
				if ($hide_timemode_set ne "1"){
				$content_html.=qq~
					<h4>Режим работы</h4>
					<div class="item"><textarea class="timemode" name="timemode">$timemode_old</textarea></div>~;
				}
				if ($hide_copyright_set ne "1"){
				$content_html.=qq~
					<h4>Copyright</h4>
					<div class="item"><textarea class="copyright" name="copyright">$copyright_old</textarea></div>~;
				}				
				$content_html.='
					<div class="help_social">
						<h4>Организовать вход через</h4>
						<div class="item">
							'.social_button().'
						</div>
					</div>';	
				$content_html.=qq~				
				</div>
			</div>			
			<table id="page_new" class="settings" style="margin-bottom:0px;">
			<tr>
				<td class="name"></td><td class="name_main">Глобальные настройки</td>
			</tr>
			<tr class="help_title">
				<td class="name">Основной титл сайта</td><td><input type="text" name="title_site" value="$ok_title_site_old"></td>
			</tr>
			<tr>
				<td class="name">Имя домена</td><td><input type="text" name="name_site" value="$current_domen"></td>
			</tr>
			<tr class="help_cache">
				<td class="name cache"><i class="icon turbocache"><i></td><td><input class="js-cbox" name="cache_mode" type="checkbox"~;
			if($ok_cache_mode_old eq "1"){
				$content_html.= qq~ checked~;
			}
			$content_html.=qq~><div class="cache_info"><span>Заметно ускорит работу сайта, рекомендуется для интернет-магазинов</span></div></td>
			</tr>			
			<tr>
				<td class="name">Директория корень на хостинге</td><td><input style="float:left;" type="text" name="dir_main" value="$ok_dir_main_old" class="small"><span class="val"><input name="dir_cgi" type="checkbox" class="cb"~;
			if($ok_dir_cgi_old eq "1"){
				$content_html.= qq~ checked~;
			}
			$content_html.='> cgi-bin находится в корне</span></td>
			</tr>
			<tr class="help_main_page">
				<td class="name"><div class="scroll"><span>Главная страница</span><a href="#" class="change_main_page">Изменить</a></div></td><td><input type="text" name="main_page" value="'.$ok_main_page_old.'" class="normal"></td>
			</tr>			
			<tr>
				<td class="name">Путь к стилям (CSS)</td><td><input type="text" name="dir_css" value="'.$ok_dir_css_old.'" class="normal"></td>
			</tr>
			<tr>
				<td class="name">Путь к шрифтам (font-face)</td><td><input type="text" name="dir_fonts" value="'.$ok_dir_fonts_old.'" class="normal"></td>
			</tr>	
			<tr>
				<td class="name">Робот помощник</td><td>
					<select class="category" name="robot_help">
						<option value="0"'.($ok_robot_help_old eq "0"?' selected':'').'>По умолчанию скрыт</option>
						<option value="1"'.($ok_robot_help_old eq "1"?' selected':'').'>По умолчанию активен</option>
					</select>
				</td>
			</tr>
				'.$maket_list;
			if ($hide_fadepage ne "1"){	
				$content_html.= qq~<tr>
					<td class="name">Плавная смена страниц</td><td><input name="fade_page" type="checkbox" class="cb"~;
				if($fade_page_old eq "1"){
					$content_html.= qq~ checked~;
				}
				$content_html.=qq~></td>
				</tr>~;
			}
$content_html.= qq~
			<tr>
				<td colspan="2" class="small">
					<table class="help_mysql" id="page_new">
						<tr>
							<td class="name"></td>
							<td class="name_main"><br>Доступы к MySQL</td>
						</tr>
						<tr>
							<td class="name">Host</td><td><input type="text" name="host_db" value="$ok_host_db_old" class="normal"></td>
						</tr>
						<tr>
							<td class="name">User</td><td><input type="text" name="user_db" value="$ok_user_db_old" class="normal"></td>
						</tr>
						<tr>
							<td class="name">Password</td><td><input type="text" name="password_db" value="$ok_password_db_old" class="normal"></td>
						</tr>
						<tr>
							<td class="name">Название базы</td><td><input type="text" name="name_db" value="$ok_name_db_old" class="normal"></td>
						</tr>
					</table>
				</td>
			</tr>		
			<tr>
				<td class="name"></td><td class="name_main"><br>Настройка почты</td>
			</tr>
			<tr class="help_feedback">
				<td class="name">Почта для обратной связи</td><td><input type="text" name="email_feedback" value="$ok_email_feedback_old" class="normal"></td>
			</tr>
			<tr class="help_orders">
				<td class="name">Почта для уведомления заказов</td><td><input type="text" name="email_orders" value="$ok_email_orders_old" class="normal"></td>
			</tr>~;
			if ($hide_products_yamarket ne "1"){
			$content_html.=qq~
			<tr>
				<td colspan="2" class="small">
					<table class="help_yamarket" id="page_new">
						<tr>
							<td class="name">
								<div class="yamarket_img">
									<div class="icon"></div>
								</div>
							</td>
							<td class="name_main"><br>Yandex.Маркет</td>
						</tr>		
						<tr>
							<td class="name" title="Не более 20 символов">Краткое название магазина</td><td><input type="text" name="yamarket_name" value="$ok_yamarket_name_old" class="normal"></td>
						</tr>
						<tr>
							<td class="name">Полное наименование компании</td><td><input type="text" name="yamarket_fullname" value="$ok_yamarket_fullname_old" class="normal"></td>
						</tr>	
						<tr>
							<td class="name">Стоимость доставки в рублях</td><td><input type="text" name="yamarket_delivery" value="$ok_yamarket_delivery_old" class="normal"></td>
						</tr>
					</table>
				</td>
			</tr>~;}			
			if ($hide_payment_set ne "1"){
			$content_html.=qq~
			<tr>
				<td colspan="2" class="small">
					<table class="help_payment" id="page_new">
						<tr>			
							<td class="name">
								<div class="payment_img">
									<div class="robokassa"></div>
									<div class="robot"></div>
								</div>
							</td>
							<td class="name_main" title="Реквизиты платежной системы"><br>Платежная система</td>
						</tr>		
						<tr>
							<td class="name">Логин</td><td><input type="text" name="payment_login" value="$ok_payment_login_old" class="normal"></td>
						</tr>
						<tr>
							<td class="name">Пароль инициализации оплаты</td><td><input type="text" name="payment_pass1" value="$ok_payment_pass1_old" class="normal"></td>
						</tr>	
						<tr>
							<td class="name">Пароль оповещения платежа</td><td><input type="text" name="payment_pass2" value="$ok_payment_pass2_old" class="normal"></td>
						</tr>
					</table>
				</td>
			</tr>~;}
			$content_html.=qq~
				$slideshow_edit
			<tr>
				<td class="name"></td><td class="name_main"><br>Счетчик</td>
			</tr>
			<tr>
				<td class="name"></td><td class="help_counter"><textarea name="counter" class="counter">@counter_old</textarea></td>
			</tr>
			</table>

			<div style="text-align:left; margin-left:310px;"><input type="submit" name="save" value="Сохранить" class="button" /></div>
</form>			
	
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>
~;
}
-1;