		open(BO, $dirs_home."/orders.txt"); $orders_count = <BO>; close(BO);
		if (!$orders_count){$orders_count = "16326";}
		
		$city = '��� �����:<a href="#"></a>';
		
        my ($sec, $min, $hour) = localtime((stat $dirs_home.'/css/core.css')[9]);
        my $core_css = $sec.$min.$hour;    
        my ($sec, $min, $hour) = localtime((stat $dirs_home.'/js/core.js')[9]);
        my $core_js = $sec.$min.$hour;
        my ($sec, $min, $hour) = localtime((stat $dirs_home.'/admin/site/js/scripts.js')[9]);
        my $scripts_js = $sec.$min.$hour;

		my $banner, $scripts_order, $banner2;
		
		my $sales = '<div class="sale">
						<h3>������</h3>
						<a href="/pages/sales">������<br />���������</a>
					</div>';
					
		my $que = '<div class="answers">
						<h3>������</h3>
						<a href="/pages/faq">�� ������ <br />�������</a>
					</div>';

		if ($adm_act ne "product"){
			$banner = '<div class="sidebar-banner"'.($adm_act eq "basket"?' style="left:28px"':'').'>
						<div class="item banner-slide0 animate4" onclick="location.href=\'/catalog/svetodiodnye-svetilniki/potolochnye-downlight/napravlennyj-svet-220v/page_6\'" data-slide="0">
							<img class="bg" src="/img/banner/slide0.jpg">
							<img class="img animate1" src="/img/banner/slide0a.png">
							<div class="price">�� <strong>569 �</strong></div>
						</div>
						<div class="item banner-slide1 animate4" onclick="location.href=\'/catalog/svetodiodnye-lenty/lenta-klassa-lyuks\'" data-slide="1">
							<img class="bg" src="/img/banner/slide1.jpg">
							<img class="img animate1" src="/img/banner/slide1a.png">
							<div class="price">�� <strong>213 �</strong></div>
						</div>
						<div class="item banner-slide2 animate4" onclick="location.href=\'/catalog/filter/?cid=3&ids=3&gid=2&price_from=5&price_to=5000&proizvoditel_2=on&find_parent=on\'" data-slide="2">
							<img class="bg" src="/img/banner/slide2.jpg">
							<img class="img animate1" src="/img/banner/slide2a.png">
							<div class="price">�� <strong>220 �</strong></div>
						</div>
						<div class="item banner-slide3 animate4" onclick="location.href=\'/catalog/svetodiodnye-svetilniki\'" data-slide="3">
							<img class="bg" src="/img/banner/slide3.jpg">
							<img class="img animate1" src="/img/banner/slide3a.png">
							<div class="price">�� <strong>374 �</strong></div>
						</div>
					</div>';
		}
		
		if ($adm_act eq "product"){
			$que=""; $news="";
			$sales .= '<div class="sale-block">
						<h3>������� ������</h3>
						<div class="sale-block-item">
							<span>5.000 �</span>
							<em>������ <strong>2.5%</strong></em>
						</div>
						<div class="sale-block-item">
							<span>10.000 �</span>
							<em>������ <strong>5%</strong></em>
						</div>
						<div class="sale-block-item">
							<span>25.000 �</span>
							<em>������ <strong>7%</strong></em>
						</div>
						<div class="sale-block-end">
							<a target="_blank" href="/pages/sales">������ <strong>�� 25%</strong></a>
						</div>
					</div>';			
			#$news ='<div class="category-sidebar">
			#			<div class="banner-quality">
			#				<h3>���������� ���� ��������� �� ������ ���� �������� � � ��������</h3>
			#				<img src="/img/banner-quality.png">
			#			</div>
			#		</div>';
		}
		
		my $basket_panel = '<div id="basketPanel">
				<div class="wrap-basketPanel">
					<div class="f-left">
						<a href="#" class="callback"><span>�������� ������</span></a>
					</div>
					<div class="f-right">
						<ul>
							<li class="social">
								<span>����������:</span>
								<div class="fb" title="���������� � Facebook"><i>� Facebook</i></div>
								<div class="vk" title="���������� � ���������"><i>� ���������</i></div>
								<div class="tw" title="���������� � Twitter"><i>� Twitter</i></div>
								<div class="dk" title="���������� � ��������������"><i>� ��������������</i></div>
							</li>
							<li class="cart disabled"><a href="/basket/"><i></i><span>�������</span></a><ins>0</ins><em>���� �����</em></li>
						</ul>
						<a class="button disabled" href="/basket/">�������� �����</a>
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
				<span>���������� �������</span>
				<em>������ ������ �������� �� ���������<br> ����� ������ � �������������<br> �������������� ���������<br> PCI DSS.</em>				
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