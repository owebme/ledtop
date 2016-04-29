#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
require "templates/connection/require.cgi";
if (cookie("filter_price")){
	require "admin/engine/lib/Cache/ReadCache.cgi";
}
use CGI::FastTemplate; 
use Core::Config;
use Core::DB;
use Core::DB::Work;

my $db = new Core::DB();

$num_edit=param('num_edit');
$page_alias=param('alias');
$page_cat=param('page');
$adm_act = "catalog";

if ($page_alias eq "t8-1500mm-g13"){
	$redirect = '/catalog/svetodiodnye-lampy/t8-linejnye/t8-1500mm-g13';
}
if ($page_alias eq "t8-600mm-g13"){
	$redirect = '/catalog/svetodiodnye-lampy/t8-linejnye/t8-600mm-g13';
}
elsif ($page_alias eq "t8-lineinye"){
	$redirect = '/catalog/svetodiodnye-lampy/t8-linejnye';
}
elsif ($page_alias eq "alyuminevyj-profil/arlight/ekrany-dlya-arlight"){
	$redirect = '/catalog/alyuminevyj-profil/arlight/ekrany-dlya-arh';
}
elsif ($page_alias eq "t8-lineinye"){
	$redirect = '/catalog/svetodiodnye-lampy/t8-linejnye';
}

if ($page_alias){
	$result_category = $db->query("SELECT * FROM cat_category WHERE cat_category.c_alias = '".$page_alias."' LIMIT 1");
	foreach my $line(@$result_category){
		$num_edit = $line->{c_id};
		$parent_cid = $line->{c_pid};
		$name = $line->{c_name};
		$cat_name = $line->{c_name};
		$cat_pos = $line->{c_pos};
		$show = $line->{c_show};
		$show_head = $line->{c_show_head};	
		$content_top = $line->{c_desc_top};
		if ($content_top ne "") {$content_top = $content_top.'<br>';}
		$content_bottom = $line->{c_desc_bottom};
		$redirect = $line->{c_redirect};
		$maket_catalog = $line->{c_maket};
	}
}

require "templates/titles.cgi";

if ($page_alias =~/\/$/){
	$page_alias =~ s/\/$//g;
	$redirect = '/catalog/'.$page_alias;
}

if ($num_edit){

	%titles = catTitle($num_edit);

	$title = $titles{'title'};
	$description = $titles{'desc'};
	$keywords = $titles{'keys'};

	if (!$title){
		$title = buildTitle($num_edit, "category");
	}
	if ($page_cat){
		my $string = length($title);
		if ($string > 60){
			$title=substr($title,0,60); $title = $title.'...';
		}
		$title .= ' // Страница '.$page_cat;
	}
}

if ($redirect ne ""){
	my $URL = "http://".$ENV{"HTTP_HOST"}."".$redirect;
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
}

if ($parent_cid eq "0" && $show == 1){

	print header( -charset=>'windows-1251');

	require "templates/connection/variables.cgi";
	
	$parent_id = $parent_cid;
	
	$name = build_NameCategory($name, $parent_cid);
	
	$parent_id = findParentCat($num_edit);

	$content = '<div class="category-list">
					<div class="column-holder">
						'.build_CatalogTree($sort_category, $num_edit).'
					</div>
				</div>';
	
	if ($content_top){
		$content = '<div class="content-holder content-text content-category">'.$content_top.'</div>'.$content;
	}
	if ($content_bottom){
		$content = $content.'<div class="content-holder content-text content-category">'.$content_bottom.'</div>';
	}
	
	$content .= categoryFooter($parent_id);
	
	if ($content_bottom){
		$news = '<div class="category-sidebar">'.categorySidebar($num_edit).'</div>';
	}
	
	$products_filter = filterProducts($num_edit);
	
	$tpl = new CGI::FastTemplate("admin/$dirs/"); 
		$tpl->define( index     => "maket_html.$maket_catalog",
	);
}
else {
	open(BO, "$dirs_catalog_www2/page_settings.txt"); my @pages_count = <BO>; close(BO);
	foreach my $line(@pages_count)
		{
	chomp($line);
	my ($pages_admin, $pages_site) = split(/\|/, $line);
	$count_pages=qq~$pages_site~;
		}

	my $filter_price="";	
	if (cookie("filter_price_cat") ne "" && cookie("filter_price") ne "" && cookie("filter_price_pointer") ne ""){
		if ($page_alias == cookie("filter_price_cat")){
			if (cookie("filter_price_pointer") eq "to"){$filter_price="AND p.p_price <= '".cookie("filter_price")."' AND p.p_price != '0'";}
			elsif (cookie("filter_price_pointer") eq "from"){$filter_price="AND p.p_price > '".cookie("filter_price")."' AND p.p_price != '0'";}
		}
		else {}
	}
	if ($page_alias){
		if ($page_alias eq "all"){$products = $db->query("SELECT * FROM cat_product");}
		else {
			$products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$num_edit."' ".$filter_price." AND p.p_show != '0'");
		}
	}
		
	if ($page_alias eq "all"){$num_edit="all"; $show="1";}
		
	if ($page_alias ne "cat_list"){
		my $pages_amount="";
		foreach my $product(@{$products}){
			$pages_amount++;
		}

		my $pagess="";
		if ($pages_amount ne ""){
			$pagess = $pages_amount/$count_pages;
			$pagess = $pagess+0.49;
			$pagess = sprintf("%.0f",$pagess);
		}

		if ($page_alias eq "all"){
			open OUT, ("admin/$dirs/meta_title"); $title = <OUT>; close(OUT);
			$name = '<div class="title"><h1>Каталог продукции</h1></div>';
		}
		else {$name = build_NameCategory($name, $parent_cid, $pages_amount);}
		
		$parent_id = findParentCat($parent_cid);
		
		require "templates/connection/variables.cgi";		
		
		$product_cat = build_ProductCat($num_edit, $page_cat, $count_pages, $cat_name, $page_alias, $pagess, $sort_product, $parent_id);
		if ($page_cat ne "") {$content_top=""; $content_bottom="";}
		
		my $next_cat = $db->query("SELECT c_name, c_alias FROM cat_category WHERE c_pid = '".$parent_cid."' AND c_pos > '".$cat_pos."' LIMIT 2");
		if (!$next_cat){
			$next_cat = $db->query("SELECT c_name, c_alias FROM cat_category WHERE c_pid = '".$parent_cid."' AND c_pos < '".$cat_pos."' LIMIT 2");
		}
		my $related_category="";
		if ($next_cat->[0]->{'c_name'}){
		
			$related_category .='
					<div class="related-category">
						<ul>
							<li>Смотрите также:</li>
							<li>
								<a href="/catalog/'.$next_cat->[0]->{'c_alias'}.'" title="'.$next_cat->[0]->{'c_name'}.'">'.$next_cat->[0]->{'c_name'}.'</a>
							</li>';

			if ($next_cat->[1]->{'c_name'}){
				$related_category .='
							<li>
								<a href="/catalog/'.$next_cat->[1]->{'c_alias'}.'" title="'.$next_cat->[1]->{'c_name'}.'">'.$next_cat->[1]->{'c_name'}.'</a>
							</li>';
			}
			$related_category .='
						</ul>
					</div>';
		}
		
		$content = ''.($content_top?'<div class="category_content_top">'.$content_top.'</div>':'').''.$product_cat.''.$related_category.''.($content_bottom?'<br><div class="content-holder content-text content-category">'.$content_bottom.'</div>':'<br>').'';
		
	}

	if ($page_alias eq "cat_list"){
		$title = "Каталог светодиодной продукции в нашем интернет-магазине LEDTOP-SHOP.ru";
		$name = '<div class="title"><h1>Каталог продукции</h1></div>';
		require "templates/connection/variables.cgi";
		$content = build_Category($sort_category, "big");
		$show="1";
	}

	$tpl = new CGI::FastTemplate("admin/$dirs/"); 
		$tpl->define( index     => "maket_html.$maket_catalog",
	);

	if ($show == 1) {
		print header( -charset=>'windows-1251');
		$products_filter = filterProducts($num_edit);
		if ($products_filter){$news="";}
	}
	else {
		print header( -status=> '404 Not found', -charset=>'windows-1251'); 
		$name = '<div class="title"><h1>Такой страницы нет</h1></div>';
		$content = '<div class="content-holder content-text"><p>Такой страницы не существует, перейдите в <a href="/catalog/">каталог продукции</a></p></div>';
	}
	
	$catalog_submenu = build_CatalogSubMenu($num_edit, $parent_cid, $sort_category);
}

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

if (!cookie("filter_price")){
	require "admin/engine/lib/Cache/SaveCache.cgi";
}
