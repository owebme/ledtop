#!/usr/bin/perl
BEGIN {push (@INC, 'lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use CGI::FastTemplate; 
use LWP::UserAgent;
use Core::Config;
use Core::DB;

require "lib/parametr.cgi";
require "lib/set_tinymce";
require "lib/Cache/ClearCache.cgi";

$user_login=param('user_login');
$user_pass=param('user_pass');
$soc_enter_app=param('soc_enter_app');
$soc_enter_id=param('soc_enter_id');
$action=param('action');
$adm_act=param('adm_act');

if ($adm_act eq "") {
	$password_html = access_enter();
}
sub access_enter {
	my $msg = shift;
	my $password_html='
		<form method=post action=/cgi-bin/admin/engine/index.cgi><input type=hidden name=action value=admin>
			<div id="main_enter">
				<a id="logo_enter" href="/admin/"></a>
				<div id="light"></div>
				<div id="enter">
					<input id=input type=input name=user_login autocomplete="off">
					<input id=input type=password name=user_pass autocomplete="off"> 
					<input type="submit" value="" class="button">
					'.$msg.'
				</div>
				<div id="logo_sm"></div>
				'.social_button().'
				<div id="sup_browse">Поддержка:&nbsp; Safari, Chrome, Firefox, Opera, IE 8/9</div>
			</div>
		</form>
		<div style="display:none;">
			<img src="/admin/img/category_bg.png" alt="">
			<img src="/admin/img/category_bg_save.png" alt="">
			<img src="/admin/img/category_bg_delete.png" alt="">
			<img src="/admin/img/category_bg_catalog.png" alt="">
			<img src="/admin/img/add-field.png" alt="">
			<img src="/admin/img/add-field-active.png" alt="">
			<img src="/admin/img/icon_del.png" alt="">
			<img src="/admin/img/icon_del_product.png" alt="">
			<img src="/admin/img/icon_lamp.png" alt="">
			<img src="/admin/img/icon_lamp_off.png" alt="">
			<img src="/admin/img/icon_move.png" alt="">
			<img src="/admin/img/pages_button.png" alt="">
			<img src="/admin/img/pages_button_bg.png" alt="">	
			<img src="/admin/img/pages_button_bg_right.png" alt="">	
			<img src="/admin/img/pages_button_catalog.png" alt="">
			<img src="/admin/img/pages_button_catalog_foto.png" alt="">	
			<img src="/admin/img/pages_button_catalog_list.png" alt="">	
			<img src="/admin/img/pages_input_bg.png" alt="">
			<img src="/admin/img/pages_input_bg_focus.png" alt="">
			<img src="/admin/img/pages_input_bg_focus_name.png" alt="">
			<img src="/admin/img/zoom_foto.png" alt="">	
			<img src="/admin/img/help_robot.png" alt="">
			<img src="/admin/img/help_robot_u.png" alt="">
			<img src="/admin/img/help_robot_g.png" alt="">
			<img src="/admin/img/help_small.png" alt="">
			<img src="/admin/img/help_corner.png" alt="">
		</div>';
					
	return $password_html;
}

sub social_button {
	
	my $button="";
	my $params_social="";
	if (-e "lib/set_social"){open OUT, ("lib/set_social"); @set_social = <OUT>;
	foreach my $text(@set_social) {$params_social=qq~$params_social$text~;}}
	else {open OUT, (">lib/set_social"); print OUT ""; close(OUT);}
	my $ua = LWP::UserAgent->new;
	$ua->timeout(10);
	if ($params_social eq ""){
		$params_social="create";
		my $response = $ua->get(''.$admin_host.'/auth/button.php?domen='.$ENV{"HTTP_HOST"}.'&set_social=0&ip_address='.$ip.'');
		if ($response->is_success){open OUT, (">../engine/lib/set_social"); print OUT $response->content; close(OUT);}		
	}
	my $response = $ua->get(''.$admin_host.'/auth/button.php?domen='.$ENV{"HTTP_HOST"}.'&params_social='.$params_social.'&ip_address='.$ip.'');
	if ($response->is_success){$button = $response->content;}

	return $button;
}	
					
if ($action ne "admin" && $action ne "exit") {

		$cook=cookie("uplecms");
		if ($cook) { 
			($user_login, $user_pass) = split(/\|/, $cook);
			($xxx, $user_pass) = split(/:/, $user_pass);
			($xxx, $user_login) = split(/:/, $user_login);
			$dbg="password-settings/$user_login";
			open (BO, "$dbg");
			@b = <BO>;
			close (BO);
			$zapros_password=$b[0];
			if ($zapros_password){
				if ($zapros_password eq $user_pass) { 
				$logined="ok";
				}
			}
			if ($logined eq "ok") {
				$login="Вы вошли под именем: <b>$user_login</b>";
				$password_html="";
			}
		}
}
elsif ($action eq "exit") { 
		 $date="-12h";
		 $inf="";
		 $cook=cookie("uplecms");
		 ($user_login, $user_pass) = split(/\|/, $cook);
		 ($xxx, $user_login) = split(/:/, $user_login);		 
		 unlink ("password-settings/$user_login");
		 $cookie=cookie(-name => 'uplecms',
	 		 	-value => $inf,
			 	-path => "/",
			 	-expires => $date );  
		 print header(-cookie => $cookie, -charset=>'windows-1251');
}
elsif ($action eq "admin" && $user_login ne "" && $user_pass ne "") {

	my $ua = LWP::UserAgent->new;
	$ua->timeout(10);
	my $response = $ua->get(''.$admin_host.'/cgi-bin/access.cgi?domen='.$ENV{"HTTP_HOST"}.'&login='.$user_login.'&password='.$user_pass.'&soc_enter_app='.$soc_enter_app.'&soc_enter_id='.$soc_enter_id.'&ip_address='.$ip.'');

	if ($response->is_success) {
		$result = $response->content;
	}
	
	if ($result ne "ok") {	
		my $connect = check_connect Core::DB();
		if ($connect){
			my $db = new Core::DB();
			$db->insert("INSERT INTO `stat_enter` (`login`, `pass`, `ip`, `social`, `date`, `status`) VALUES('".$user_login."', '".$user_pass."', '".$ip."', '".$soc_enter_app."', '".$today_sql."', 'Попытка взлома')");
		}
		$password_html = access_enter('<div id="message">Вы ввели неверные данные</div>');
	}
	
}

if ($result ne "ok" && $action ne "exit" && $adm_act eq "" or $logined eq "ok") { 
	print header(-charset=>'windows-1251');
}
elsif ($result ne "ok" && $action ne "exit" && $adm_act ne "") {
	my $URL = "http://".$ENV{"HTTP_HOST"}."/admin/";
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
}

elsif ($result eq "ok") {
		 use Digest::MD5 qw(md5_hex);
		 $user_pass = md5_hex($user_pass);
		 $logined="ok";
		 unlink ("password-settings/admin");
		 open OUT, (">password-settings/$user_login");
			print OUT "$user_pass"; 
		 close(OUT);
	
		 $date="+12h";
		 $inf="login:$user_login|password:$user_pass";
		 $cookie=cookie(-name => 'uplecms',
		 	-value => $inf,
		 	-path => "/",
		 	-expires => $date ); 
			
		my $connect = check_connect Core::DB();
		if ($connect){
			my $db = new Core::DB();
			$db->insert("INSERT INTO `stat_enter` (`login`, `pass`, `ip`, `social`, `date`, `status`) VALUES('".$user_login."', '".$user_pass."', '".$ip."', '".$soc_enter_app."', '".$today_sql."', 'Успешно')");
		}			
	
		print header(-cookie => $cookie, -charset=>'windows-1251');
		
	$password_html="";						
}

if ($logined eq "ok"){

	$user_enter=qq~<form method=post action=/cgi-bin/admin/engine/index.cgi><input type=hidden name=action value=exit><input type="submit" style="color:#999; font-size:19px; border:none; margin-top:6px; background:none; text-decoration:underline; cursor:pointer;" value="Выход"></form>~;
	if (open (TEST, "../modules/$adm_act.cgi")) {
		require "../modules/$adm_act.cgi";
	} else {
		if ($adm_act) {
		$content_html=qq~<table id="sheet">
		<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs">
				<ul>
					<li class="first activetab"><span><a href="#">Сообщение</a></span></li>
				</ul>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">
		<div id="pages"><div class="page_error">Такой страницы не существует.</div>
		</div>
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;
		}
	}

	
open OUT, ("../layouts/meta_title"); $meta_title = <OUT>;	 close(OUT);


open IN, ("../layouts/set_panel"); $set = <IN>;  
 
if ($set eq "0") {$show = qq~style="margin-top:-159px;"~; $active_show = qq~class="active" title="Опустить"~;} else {$show = ""; $active_show = qq~title="Скрыть"~;};

close(IN);

open(BO, "../layouts/set_cat_select"); @cat_current = <BO>; close(BO);
foreach my $line(@cat_current){chomp($line);
my ($cat_current_, $curent_page_) = split(/\|/, $line);
	$cat_current=qq~$cat_current_~;
}	

if ($cat_current ne "all" && $cat_current ne "") {$link_cat = "&cat_show=$cat_current"}
elsif ($cat_current eq "all" or $cat_current eq "") {$link_cat="";}

if(-e "../modules/strukture.cgi"){$pages_set=''; $pages_link='';} else{$pages_set='class="off"'; $pages_link='class="no_link"';}
if(-e "../modules/news.cgi"){$news_set=''; $news_link='';} else{$news_set='class="off"'; $news_link='class="no_link"';}
if(-e "../modules/category.cgi" && -e "../modules/products.cgi"){$products_set=''; $products_link='';} else{$products_set='class="off"'; $products_link='class="no_link"';}
if(-e "../modules/orders.cgi"){$orders_set=''; $orders_link='';} else{$orders_set='class="off"'; $orders_link='class="no_link"';}
if(-e "../modules/fotogal.cgi" && -e "../modules/fotolist.cgi"){$gallery_set=''; $gallery_link='';} else{$gallery_set='class="off"'; $gallery_link='class="no_link"';}
if(-e "../modules/questions.cgi"){$questions_set=''; $questions_link='';} else{$questions_set='class="off"'; $questions_link='class="no_link"';}

$main_menu=qq~<script type="text/javascript" src="/admin/lib/advajax.js"></script>
<script type="text/javascript" src="/admin/js/jquery.cookie.js"></script>
<script type="text/javascript" src="/admin/lib/uploads.js"></script>
<script type="text/javascript" src="/admin/lib/help.js"></script>
<script type="text/javascript" src="/admin/js/thickbox/thickbox.js"></script>
<link rel="stylesheet" href="/admin/js/thickbox/thickbox.css" type="text/css" media="screen" />
<link href="/admin/js/selects/style.css" rel="stylesheet" type="text/css" />
<script type="text/javascript" src="/admin/js/selects/cusel-min-2.5.js"></script>
<script type="text/javascript" src="/admin/js/checkbox/cb_styler.js"></script>
<link rel="stylesheet" href="/admin/js/checkbox/cb_style.css" type='text/css'>
<link rel="stylesheet" type="text/css" media="screen" href="/admin/js/ui-jquery/jquery-ui.css">
<script type="text/javascript" src="/admin/js/ui-jquery/jquery-ui.min.js"></script>
<script type="text/javascript" src="/admin/js/jquery.ui.touch-punch.min.js"></script>
<link rel="stylesheet" type="text/css" media="screen" href="/admin/js/elfinder/css/elfinder.min.css">
<link rel="stylesheet" type="text/css" media="screen" href="/admin/js/elfinder/css/theme.css">
<script type="text/javascript" src="/admin/js/elfinder/js/elfinder.min.js"></script>
<script type="text/javascript" src="/admin/js/elfinder/js/i18n/elfinder.ru.js"></script>
<script type="text/javascript" src="/admin/js/easyTooltip.js"></script>
<script type="text/javascript" src="/admin/js/jquery.easing-1.3.pack.js"></script>
<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
<script src="/js/validate/js/validate_default.js" language="JavaScript" type="text/javascript"></script>
<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" /> 
<script type="text/javascript" src="/admin/lib/main.js"></script>
<link rel="stylesheet" type="text/css" href="/admin/lib/help/style.css" />
<script type="text/javascript" src="/admin/lib/help/intro.js"></script>~;

my $uple_help=""; my $uple_help_bottom=""; my $uple_help_right="";
if (cookie("uple_help") eq "true"){
	$uple_help = "true";
	$uple_help_bottom = cookie("uple_help_bottom");
	$uple_help_right = cookie("uple_help_right");
}
$main_menu .='
	<div id="uple-help"'.($uple_help_bottom > 0?' style="bottom:'.$uple_help_bottom.'px;"':'').' data-show="'.($robot_help eq "1"?'true':'false').'">
		<div class="robot"'.($uple_help eq "true"?' id="open"':'').''.($uple_help_right > 0?' style="right:'.$uple_help_right.'px;"':'').'>
			<img class="r" src="/admin/img/help_robot.png" alt="">
			<img class="u" src="/admin/img/help_robot_u.png" alt="">
			<img class="g" src="/admin/img/help_robot_g.png" alt="">		
		</div>
		<div class="help_open"'.($uple_help ne "true"?' style="bottom:0px; right:0px;"':'').'></div>
	</div>';

$main_menu .=qq~	
	<div id="header" $show>
	
		<div id="headerelements">
	
		<div id="title">
			<h1 id="title_site">$meta_title</h1>
			<a id="siteurl" href="http://www$url_site" target="_blank">www$url_site</a><br />
			<a id="edittitle" href="#">редактировать</a>
		</div>
	
		<div id="menu1">
			<ul>
				<li><a href="/admin" id="uple"><span>Uple</span>CMS</a></li>
				<li><a target="_blank" href="$admin_host/promo/">О системе</a></li>
				<li><a target="_blank" href="$admin_host">Официальный сайт</a></li>
			</ul>
		</div>
		
		<div id="menu2">
		
			<ul>
				<li class="first"><div class="upload" title="Нажмите для загрузки файлов"><input type="file" multiple="true"></div></li>
				<li><a href="/admin/usermanual.html?height=540&width=900&scrollto=usermanual" title="Помощь" class="thickbox">Справка</a></li>
				<li>$user_enter</li>
			</ul>
		</div>
		
		<div id="selectcolor">
			<div><span>Release:</span> $ver_release</div>
			<ul>
				<li><a href="#" title="Серый" id="default"></a></li>
				<li><a href="#" title="Золотой" id="golden"></a></li>
				<li><a href="#" title="Синий" id="blue"></a></li>
				<li><a href="#" title="Красный" id="red"></a></li>
				<li><a href="#" title="Зеленый" id="green"></a></li>
			</ul>
		</div>
		
	</div>
	
	</div>

	<div id="hidetop"><a href="#" $active_show id="showhidetop"></a></div>

	<div id="main_menu">

		<div id="main"><a href="/" target="_blank">Главная</a></div>
		<div id="pages" $pages_set><a $pages_link href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture">Страницы</a></div>
		<div id="news" $news_set><a $news_link href="/cgi-bin/admin/engine/index.cgi?adm_act=news">Новости</a></div>
		<div id="gallery" $gallery_set><a $gallery_link href="/cgi-bin/admin/engine/index.cgi?adm_act=fotogal">Фотогалерея</a></div>
		<div id="products" $products_set><a $products_link href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog">Товары</a></div>
		<div id="orders" $orders_set><a $orders_link href="/cgi-bin/admin/engine/index.cgi?adm_act=orders">Заказы</a></div>
		<div id="questions" $questions_set><a $questions_link href="/cgi-bin/admin/engine/index.cgi?adm_act=questions">Вопросник</a></div>
		<div id="settings"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=settings">Настройки</a></div>

	</div>~;

$welcome =qq~<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs">
				<ul>
					<li class="first activetab"><a href="#"><span>UpleCMS</span></a></li>
				</ul>
			</div>
			
			
			<div id="buttons">
				
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">

		<h3 class="welcome">Вас приветствует система управления UpleCMS</h3>
		
		
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;	
	
} else {$main_menu="";};

$tpl = new CGI::FastTemplate("template/"); 
	$tpl->define( index     => "index.tpl",
);

$tpl->assign(LEFTMENU => "$leftmenu");
$tpl->assign(CONTENT => "$content_html");
$tpl->assign(PASSWORD => "$password_html");
$tpl->assign(MAIN_MENU => "$main_menu");
if ($adm_act eq "") {$tpl->assign(WELCOME => "$welcome");} else {$tpl->assign(WELCOME => "")};
$tpl->parse(MAIN => "index");
$tpl->print();


-1;