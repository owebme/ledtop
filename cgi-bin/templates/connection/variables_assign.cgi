		open(BO, $dirs_home."/orders.txt"); $orders_count = <BO>; close(BO);
		if (!$orders_count){$orders_count = "16326";}
		
		$city = 'Ваш город:<a href="#"></a>';
		
        my ($sec, $min, $hour) = localtime((stat $dirs_home.'/css/core.css')[9]);
        my $core_css = $sec.$min.$hour;    
        my ($sec, $min, $hour) = localtime((stat $dirs_home.'/js/core.js')[9]);
        my $core_js = $sec.$min.$hour;
        my ($sec, $min, $hour) = localtime((stat $dirs_home.'/admin/site/js/scripts.js')[9]);
        my $scripts_js = $sec.$min.$hour;

		my $banner, $scripts_order, $banner2;
		
		my $sales = '<div class="sale">
						<h3>Скидки</h3>
						<a href="/pages/sales">Узнать<br />подробнее</a>
					</div>';
					
		my $que = '<div class="answers">
						<h3>Ответы</h3>
						<a href="/pages/faq">на частые <br />вопросы</a>
					</div>';

		if ($adm_act ne "product"){
			$banner = '<div class="sidebar-banner"'.($adm_act eq "basket"?' style="left:28px"':'').'>
						<div class="item banner-slide0 animate4" onclick="location.href=\'/catalog/svetodiodnye-svetilniki/potolochnye-downlight/napravlennyj-svet-220v/page_6\'" data-slide="0">
							<img class="bg" src="/img/banner/slide0.jpg">
							<img class="img animate1" src="/img/banner/slide0a.png">
							<div class="price">от <strong>569 р</strong></div>
						</div>
						<div class="item banner-slide1 animate4" onclick="location.href=\'/catalog/svetodiodnye-lenty/lenta-klassa-lyuks\'" data-slide="1">
							<img class="bg" src="/img/banner/slide1.jpg">
							<img class="img animate1" src="/img/banner/slide1a.png">
							<div class="price">от <strong>213 р</strong></div>
						</div>
						<div class="item banner-slide2 animate4" onclick="location.href=\'/catalog/filter/?cid=3&ids=3&gid=2&price_from=5&price_to=5000&proizvoditel_2=on&find_parent=on\'" data-slide="2">
							<img class="bg" src="/img/banner/slide2.jpg">
							<img class="img animate1" src="/img/banner/slide2a.png">
							<div class="price">от <strong>220 р</strong></div>
						</div>
						<div class="item banner-slide3 animate4" onclick="location.href=\'/catalog/svetodiodnye-svetilniki\'" data-slide="3">
							<img class="bg" src="/img/banner/slide3.jpg">
							<img class="img animate1" src="/img/banner/slide3a.png">
							<div class="price">от <strong>374 р</strong></div>
						</div>
					</div>';
		}
		
		if ($adm_act eq "product"){
			$que=""; $news="";
			$sales .= '<div class="sale-block">
						<h3>Разовые скидки</h3>
						<div class="sale-block-item">
							<span>5.000 Р</span>
							<em>Скидка <strong>2.5%</strong></em>
						</div>
						<div class="sale-block-item">
							<span>10.000 Р</span>
							<em>Скидка <strong>5%</strong></em>
						</div>
						<div class="sale-block-item">
							<span>25.000 Р</span>
							<em>Скидка <strong>7%</strong></em>
						</div>
						<div class="sale-block-end">
							<a target="_blank" href="/pages/sales">Скидки <strong>до 25%</strong></a>
						</div>
					</div>';			
			#$news ='<div class="category-sidebar">
			#			<div class="banner-quality">
			#				<h3>Приобретая нашу продукцию вы можете быть уверенны в её качестве</h3>
			#				<img src="/img/banner-quality.png">
			#			</div>
			#		</div>';
		}
		
		my $basket_panel = '<div id="basketPanel">
				<div class="wrap-basketPanel">
					<div class="f-left">
						<a href="#" class="callback"><span>Заказать звонок</span></a>
					</div>
					<div class="f-right">
						<ul>
							<li class="social">
								<span>Поделиться:</span>
								<div class="fb" title="поделиться в Facebook"><i>в Facebook</i></div>
								<div class="vk" title="поделиться в ВКонтакте"><i>в ВКонтакте</i></div>
								<div class="tw" title="поделиться в Twitter"><i>в Twitter</i></div>
								<div class="dk" title="поделиться в Одноклассниках"><i>в Одноклассниках</i></div>
							</li>
							<li class="cart disabled"><a href="/basket/"><i></i><span>Корзина</span></a><ins>0</ins><em>Пока пусто</em></li>
						</ul>
						<a class="button disabled" href="/basket/">Оформить заказ</a>
					</div>
				</div>
			</div>';
		
		if ($adm_act eq "private"){
			$banner=""; $sales=""; $que=""; $basket_panel="";
			$catalog_submenu = $user_status;
			$body_id = ' id="body-private"';
		}
		elsif ($adm_act eq "basket" or $adm_act eq "pages" && $page_alias eq "delivery"){
			$basket_panel="";
			
			$products_viewed ='<div class="sidebar-security hidden-block">
				<i></i>
				<span>Безопасные платежи</span>
				<em>Сервис оплаты работает по Стандарту<br> Банка России и соответствует<br> международному стандарту<br> PCI DSS.</em>				
			</div>'; 
			
			$scripts_order ='<script type="text/javascript" src="/js/delivery/jquery-ui.min.js"></script>
			<script type="text/javascript" src="/js/delivery/form2js.js"></script>
			<script type="text/javascript" src="/js/delivery/json2.js"></script>
			<script type="text/javascript" src="/js/delivery/calc.js"></script>
			<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
			<script src="/js/validate/js/validate.js" language="JavaScript" type="text/javascript"></script>
			<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
			<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" />';
		}
		if ($adm_act eq "pages" && $page_alias eq "delivery"){
			$scripts_order ='<script type="text/javascript" src="/js/delivery/jquery-ui.min.js"></script>
			<script type="text/javascript" src="/js/delivery/form2js.js"></script>
			<script type="text/javascript" src="/js/delivery/json2.js"></script>
			<script type="text/javascript" src="/js/delivery/calc.js"></script>';
		}
		if ($adm_act eq "basket" or $adm_act eq "product" or $adm_act eq "catalog"){
			$banner2 ='<div class="sidebar-banner2"></div>';
		}
		if ($adm_act eq "pages" && $page_alias eq "sales"){
			$basket_panel="";
		}
		elsif ($adm_act eq "pages" && $page_alias eq "test"){
			$counter="";
			$basket_panel="";
		}
	
		$tpl->assign(NAME => "$name");
		$tpl->assign(CONTENT => "$content");
		$tpl->assign(TITLE => "$title");
		$tpl->assign(DESCRIPTION => "$description");
		$tpl->assign(KEYWORDS => "$keywords");
		$tpl->assign(BODY_ID => "$body_id");
		$tpl->assign(PAGES_MENU => "$pages_menu");
		$tpl->assign(PAGES_MENU_LIMIT => "$pages_menu_limit");
		$tpl->assign(PAGES_SUBMENU => "$pages_submenu");
		$tpl->assign(PAGES_TREE => "$pages_tree");
		$tpl->assign(CATALOG_MENU => "$catalog_menu");
		$tpl->assign(CATALOG_MENU_LIMIT => "$catalog_menu_limit");
		$tpl->assign(CATALOG_TREE => "$catalog_tree");
		$tpl->assign(CATALOG_CATEGORY => "$catalog_category");
		$tpl->assign(CATALOG_SUBMENU => "$catalog_submenu");
		$tpl->assign(BRANDS => "$brands");		
		$tpl->assign(SELECT_BRANDS => "$select_brands");
		$tpl->assign(PRODUCTS_HIT => "$products_hit");
		$tpl->assign(PRODUCTS_NEW => "$products_new");
		$tpl->assign(PRODUCTS_SPEC => "$products_spec");
		$tpl->assign(PRODUCTS_RANDOM => "$products_random");
		$tpl->assign(PRODUCTS_VIEWED => "$products_viewed");
		$tpl->assign(PRODUCTS_FILTER => "$products_filter");
		$tpl->assign(ORDERS_COUNT => "$orders_count");		
		$tpl->assign(GALLERY_LITE => "$gallery_lite");
		$tpl->assign(BASKET_PANEL => "$basket_panel");
		$tpl->assign(BANNER => "$banner");
		$tpl->assign(BANNER2 => "$banner2");
		$tpl->assign(BANNER_VER1 => "$banner_ver1");
		$tpl->assign(BANNER_VER2 => "$banner_ver2");
		$tpl->assign(BANNER_VER3 => "$banner_ver3");
		$tpl->assign(BANNER_GOR1 => "$banner_gor1");
		$tpl->assign(BANNER_GOR2 => "$banner_gor2");
		$tpl->assign(BANNER_GOR3 => "$banner_gor3");
		$tpl->assign(SALES => "$sales");
		$tpl->assign(QUE => "$que");
		$tpl->assign(NEWS => "$news");
		$tpl->assign(ARTICLES => "$articles");
		$tpl->assign(FADE_PAGE => "$fade_page");
		$tpl->assign(CALLBACK => "$callback");
		$tpl->assign(COUNTER => "$counter");
		$tpl->assign(VALUTA => "$valuta");
		$tpl->assign(POGODA => "$pogoda");
		$tpl->assign(METAL => "$metal");
		$tpl->assign(PHONE => "$phone");
		$tpl->assign(CITY => "$city");
		$tpl->assign(ADDRESS => "$address");
		$tpl->assign(TIMEMODE => "$timemode");
		$tpl->assign(COPYRIGHT => "$copyright");		
		$tpl->assign(PRIVATE_PANEL => "$private_panel");
		$tpl->assign(SLIDESHOW => "$slideshow");
		$tpl->assign(RAND_N => "$random_n");
		$tpl->assign(CORE_CSS => "$core_css");
		$tpl->assign(CORE_JS => "$core_js");
		$tpl->assign(SCRIPTS_ORDER => "$scripts_order");
		$tpl->assign(SCRIPTS_JS => "$scripts_js");

		1;