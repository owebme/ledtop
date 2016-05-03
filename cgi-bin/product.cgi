#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
require "templates/connection/require.cgi";
if (cookie("private_login")){
	require "templates/auth.cgi";
}
else {
	require "admin/engine/lib/Cache/ReadCache.cgi";
}
use CGI::FastTemplate; 
use Core::Config;
use Core::DB;

my $db = new Core::DB();

$article=param('article');
$page_alias=param('alias');
$adm_act = "product";
$error = "";

require "templates/titles.cgi";

if($page_alias && $article =~/\d+/){
	$result = $db->query("SELECT * FROM cat_product WHERE cat_product.p_art = '".$article."' LIMIT 1");
}
if(!$result){
	header(-status=>'404'); 
	$error = "404";
}
else {
	foreach my $line(@$result){
		$num_edit = $line->{p_id};
		$page_alias = $line->{p_art};
		$name = $line->{p_name};
		$show = $line->{p_show};
		$show_head = $line->{p_show_head};		
		$content_text = $line->{p_desc};
		$title = prodTitle($line->{p_art}." ".$line->{p_name}." купить с доставкой по –оссии наложенным платежом, цена в интернет-магазине, технические характеристики");
		$description = ($line->{p_desc_sm}?$line->{p_desc_sm}:prodDesc($line->{p_name}.' купить с доставкой по –оссии в интернет-магазине LEDTop-Shop.ru'));
		$keywords = $line->{p_name}.", купить, цена, оптом, led, светодиоды, освещение, компоненты, технические, характеристики, с доставкой, курьером, почтой, по –оссии, ledtop-shop.ru";
		$redirect = $line->{p_redirect};
		$maket_product = $line->{p_maket};
	}
}

	if (!$result && $page_alias && $article =~/(\d+)\//){
		$article =~s/\//-/g;
		$article =~s/(\d+)-/$1\//g;
		$redirect = '/products/'.$article.'-'.$page_alias;
	}
	elsif (!$result && ($page_alias =~/\d+/ or !$page_alias && $article =~/\d+/)){
		if ($page_alias =~/\d+/){
			$article = $page_alias;
		}
		my $res="";
		if (length($article) eq "4"){
			$res = $db->query("SELECT p_art, p_alias FROM cat_product WHERE p_id = '".$article."'");
			$article = $res->[0]->{p_art};
		}
		else {
			$res = $db->query("SELECT p_alias FROM cat_product WHERE p_art = '".$article."'");
		}
		if ($res->[0]->{p_alias}){
			$redirect = '/products/'.$article.'/'.$res->[0]->{p_alias};
		}
	}
	else {
		my $res = $db->query("SELECT pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE p.p_id = '".$num_edit."' AND pl.cat_main = '1' LIMIT 1");
		$parent_id = findParentCat($res->[0]->{cat_id});
		$name = build_NameProduct($num_edit, $name);
		$content = build_Product($num_edit, $parent_id, $sort_product);
	}

if ($redirect ne ""){
	my $URL = "http://".$ENV{"HTTP_HOST"}."".$redirect;
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
}

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_product",
);

require "templates/connection/variables.cgi";

if ($num_edit) {
	
	print header( -charset=>'windows-1251');
}
else {
	$tpl = new CGI::FastTemplate("admin/$dirs/"); 
		$tpl->define( index     => "maket_html.$maket_product",
	);
	print header( -status=> '404 Not found', -charset=>'windows-1251'); 
	$name = '<div class="title"><h1>“акой страницы нет</h1></div>';
	$content = '<div class="content-holder content-text"><p>“акой страницы не существует, перейдите в <a href="/catalog/">каталог продукции</a></p></div>';
}

$catalog_submenu = build_CatalogSubMenu();

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

if (!$error && !cookie("private_login")){
	require "admin/engine/lib/Cache/SaveCache.cgi";
}
