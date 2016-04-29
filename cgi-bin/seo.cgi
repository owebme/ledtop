#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 
use Fcntl;

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;
require "templates/connection/require.cgi";
require "admin/engine/lib/Cache/ReadCache.cgi";
use CGI::FastTemplate; 
use LWP::UserAgent;
use Core::Config;
use Core::DB;
use JSON;

my $db = new Core::DB();

$page_alias=param('alias');
$page=param('page');
$adm_act = "poleznoe";

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_article",
);

require "templates/connection/variables.cgi";

print header( -charset=>'windows-1251');

	my $json = JSON->new();
	
	my $domen = "well-men.ru";
	my $login = "wellmen";
	my $pass = "435435fdgdgdfg";
	my $page_count = 12; # Кол-во статей на странице
	my $symbol = 194; # Кол-во символов в кратком содержании
	my $path = "/poleznoe/"; # Адрес раздела на сайте
	my $name_section = "Полезная информация"; # Название раздела
	
	my $template = 3;
	
	my $styles = '<link href="/css/template3.css" rel="stylesheet">';
	
	# Цветовая гамма
	my $color=""; # green #649d30
				  # orange #fe8000
				  # red #E31255
				  # blue #347eb3

	my $ua = LWP::UserAgent->new;
	$ua->timeout(10);
	my $result="";
	if (!$page_alias){
		my $response = $ua->get('http://upleseo.ru/api/?domen='.$domen.'&login='.$login.'&password='.$pass.'&page_count='.$page_count.'&page_current='.$page.'&symbol='.$symbol.'&format=json');
		if ($response->is_success){
			$result = $response->content;
		}
	}
	elsif ($page_alias){
		my $response = $ua->get('http://upleseo.ru/api/?domen='.$domen.'&login='.$login.'&password='.$pass.'&alias='.$page_alias.'&path='.$path.'&format=json');
		if ($response->is_success){
			$result = $response->content;
		}
	}
	
if ($result =~/^<p>(.+?)<\/p>/){
	$title = $name_section;
	$name = '<h1>'.$name_section.'</h1>';
	$content = $result;
}
else {

	# Вывод статей списком
	if (!$page_alias && $result){
		my $articles = $json->decode($result);
		my %hash = %{$articles};
		my $article=""; my $count="";
		foreach my $key (sort {$hash{$a}->{pos} <=> $hash{$b}->{pos}} keys %hash) {
			my $url = $path.$hash{$key}->{alias};
			if ($hash{$key}->{name}){
				$article .='
				<div class="art-article" onclick="document.location=\''.$url.'\'">
					<div class="art-photo">
						<a href="'.$url.'"><img src="'.$hash{$key}->{img}.'" alt="'.$hash{$key}->{keys}.'"></a>
						<div class="art-clear"></div>
					</div>
					<div class="art-text">
						<div class="art-head">
							<div class="art-date">'.date($hash{$key}->{date}).'</div>
							<a href="'.$url.'" class="art-name"><h2>'.$hash{$key}->{name}.'</h2></a>
							<div class="art-clear"></div>
						</div>
						<p>'.$hash{$key}->{content}.'</p>
						<div class="art-more">
							<a class="art-more-link" href="'.$url.'">Подробнее »</a>
						</div>
					</div>
					<div class="art-clear"></div>
				</div>';
			}
			else {
				$count = $hash{$key}->{count};
			}
		}
		if ($article){	
			my $pages="";
			if ($count > 0){
				$pages = $count/$page_count;
				$pages = $pages+0.49;
				$pages = sprintf("%.0f",$pages);
			}		
			my $i=1; my $p=""; my $pagess="";
			while ($i <= $pages) {
				if ($i > ($page-4) && $i < ($page-2)){
					$pagess .= '<li><a href="'.$path.($i > 1?'page_'.$i.'':'').'">&larr;</a></li>';
				}			
				elsif ($i > ($page-3) && $i < ($page+3) && $page > 2 or $page < 3 && $i < 6){
					if ($i == $page) {$p = '<li class="art-active"><a href="#">'.$page.'</a></li>';}
					elsif ($page == "") {$p = ''.($i == 1?'<li class="art-active"><a href="#">'.$i.'</a></li>':'<li><a href="'.$path.'page_'.$i.'">'.$i.'</a></li>').'';}
					else {$p = ''.($i == 1?'<li><a href="'.$path.'">'.$i.'</a></li>':'<li><a href="'.$path.'page_'.$i.'">'.$i.'</a></li>').'';}
					$pagess .= $p;
				}
				elsif ($i > ($page+2) && $i < ($page+4) && $page > 2 or $page < 3 && $i == 6){
					$pagess .= '<li><a href="'.$path.'page_'.$i.'">&rarr;</a></li>';
				}
				$i++;
			}
			if ($i == "2") {$pagess ="";} else {$pagess = '<ul class="art-pagination"><li class="art-first">Страница</li>'.$pagess.'</ul>';}
			
			$article ='
			<div id="art-mainArticle">
				<div class="art-body">	
					<h1>'.$name_section.'</h1>
					<div class="art-nav">
						'.$pagess.'
						<div class="art-path"><a href="/">Главная</a></div>
					</div>
					<div class="art-clear"></div>
					'.($template eq "3"?'<div id="art-blog" class="art-blog effect-2">':'').'
						'.$article.'		
					'.($template eq "3"?'</div>':'').'
					<div class="art-nav-bottom">
						'.$pagess.'
					</div>
					<div class="art-clear"></div>
				</div>
			</div>';
			
			$article = $styles.$article.'
			<script type="text/javascript">
				if (window.jQuery == undefined) {
					document.write(\'<scr\'+\'ipt type="text/javascript" src="http://upleseo.ru/\'+\'js/jquery-1.8.2.min.js">\'+\'<\/scr\'+\'ipt>\');
				}
			</script>';
			
			if ($template eq "2"){
				$article = $article.'		
				<script type="text/javascript">
					$(function(){
						var color="";
						color = " style=\"color:"+$(".art-more-link").css("background-color")+"\""
						$(".art-name h2").each(function(){
							var me = $(this),t=me.html().split(" ");
							me.html("<span"+color+">"+t.shift()+"</span> "+t.join(" "));
						});	
					});
				</script>'; 
			}
			elsif ($template eq "3"){	
				$article = $article.'
				<script src="http://upleseo.ru/js/template3/modernizr.custom.js"></script>
				<script src="http://upleseo.ru/js/template3/masonry.pkgd.min.js"></script>
				<script src="http://upleseo.ru/js/template3/imagesloaded.js"></script>
				<script src="http://upleseo.ru/js/template3/classie.js"></script>
				<script src="http://upleseo.ru/js/template3/AnimOnScroll.js"></script>
				<script>
					new AnimOnScroll( document.getElementById("art-blog"), {
						minDuration : 0.4,
						maxDuration : 0.7,
						viewportFactor : 0.2
					} );
				</script>';
			}

			if ($color){
				$article .='<style>.art-date, .art-date *, .art-name:hover h2, .art-pagination .art-active, .art-path a, .art-document a {color:'.$color.' !important;} .art-more-link, .art-active {background:'.$color.' !important;}</style>';
			}			
			
			$title = $name_section.($page > 1?' // Страница '.$page.'':'').'';
			
			$content = $article;
		}
	}
	
	# Вывод содержания статьи
	elsif ($page_alias && $result){
		my $hash = $json->decode($result);
		my $article="";
		my $header=""; my $text=""; my $date="";
		while (my($key,$value) = each(%{$hash})){
			if ($key eq "title"){$title = $value;}
			if ($key eq "header"){$header = $value;}
			if ($key eq "content"){$text = $value;}
			if ($key eq "date"){$date = $value;}
		}	
		$article ='
			<div id="art-mainArticle">
				<div class="art-body">
					<h1>'.$header.'</h1>
					<div class="art-nav">
						<div class="art-path right">&larr; <a href="'.$path.'">'.$name_section.'</a></div>
					</div>
					<div class="art-document">
						'.$text.'
					</div>
					'.($date?'<div class="art-document-date">Дата публикации: '.$date.'</div>':'').'
				</div>
			</div>';

		$article = $styles.$article.'
			<script type="text/javascript">
				if (window.jQuery == undefined) {
					document.write(\'<scr\'+\'ipt type="text/javascript" src="http://upleseo.ru/\'+\'js/jquery-1.8.2.min.js">\'+\'<\/scr\'+\'ipt>\');
				}
			</script>					
			<script src="http://upleseo.ru/js/jSboxGallery/jquery.jSboxGallery.js"></script>
			<link rel="stylesheet" href="http://upleseo.ru/js/jSboxGallery/style.css" />
			<!--[if lt IE 8]>
				<link rel="stylesheet" href="http://upleseo.ru/js/jSboxGallery/style.ie.css" />
			<![endif]-->
			<script type="text/javascript">
				$(function(){
					$(".art-document").find("img").each(function(){
						var src = $(this).attr("src");
						$(this).wrap(\'<a href="\'+src+\'" class="jSbox-gallery"></a>\');
					});
					$().jSboxGallery();
				});
			</script>';

		if ($color){
			$article .='<style>.art-date, .art-date *, .art-name:hover h2, .art-pagination .art-active, .art-path a, .art-document a {color:'.$color.' !important;} .art-more-link, .art-active {background:'.$color.' !important;}</style>';
		}
			
		$content = $article;
		
		$content .= '<div class="link-to-catalog center"><span>&rarr;</span><a href="/">Перейти в каталог продукции</a><span>&larr;</span></div>';
	}
}
	
sub date {
	my $date = shift;
	my ($year, $mouth, $day) = split(/\-/, $date);
	if ($mouth eq "01") {$mouth = "января";}
	if ($mouth eq "02") {$mouth = "февраля";}
	if ($mouth eq "03") {$mouth = "марта";}
	if ($mouth eq "04") {$mouth = "апреля";}
	if ($mouth eq "05") {$mouth = "мая";}
	if ($mouth eq "06") {$mouth = "июня";}
	if ($mouth eq "07") {$mouth = "июля";}
	if ($mouth eq "08") {$mouth = "августа";}
	if ($mouth eq "09") {$mouth = "сентября";}
	if ($mouth eq "10") {$mouth = "октября";}
	if ($mouth eq "11") {$mouth = "ноября";}
	if ($mouth eq "12") {$mouth = "декабря";}
	
	return '<strong>'.$day.'</strong><span class="art-date-month">'.$mouth.'<br><span class="art-date-year">'.$year.'</span>';
}	

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

require "admin/engine/lib/Cache/SaveCache.cgi";
