#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
require "templates/connection/require.cgi";
use CGI::FastTemplate; 
use URI::Escape;
use Lingua::Stem2::Ru;
use Core::Config;
use Core::DB;

$query=param('q');

my $db = new Core::DB();

if ($query){

	my $q = stemmer(uri_unescape($query));	
	
	my $products=""; my $more_products=""; my $c_alias=""; my $i=""; my $first="";
	my $result = $db->query("SELECT * FROM cat_product WHERE p_art LIKE '%".$q."%'");
	if (!$result){
		$result = $db->query("SELECT * FROM cat_product WHERE p_name LIKE '%".$q."%'");
	}
	if ($result){
	
		my $limit_count="";
		open(BO, "$dirs_catalog_www2/page_settings.txt"); my @pages_count = <BO>; close(BO);
		foreach my $line(@pages_count){chomp($line);
		my ($pages_admin, $pages_site) = split(/\|/, $line);
		$limit_count=qq~$pages_site~;}	
	
		my $p_ids=""; my $counts=""; my $count="";
		foreach my $line(@$result){
			$count++; $i++; my $mark="";
			if ($line->{'p_news'} eq "1"){$mark="new";}
			if ($line->{'p_hit'} eq "1"){$mark="hit";}
			if ($line->{'p_spec'} eq "1"){$mark="spec";}
			my $label = 0;
			if ($count == 3) {$label = "reflect"; $count="";}
			if ($i < ($limit_count+1)){
				$products .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, "", $line->{'p_price'}, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, $label, $mark, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "catalog", $line->{'p_img_url'}, 'Результаты поиска', "", "", "", $line->{'p_color_rel'});
				if ($i == 1){
					$first = "/products/".$line->{'p_art'}."/".$line->{'p_alias'};
				}
			}
			else {
				$counts++;
				$p_ids .= $line->{'p_id'}.",";
			}
		}
		if ($counts > $limit_count){
			$p_ids =~ s/,$//g;
			$more_products = '<div class="more_products" data-limit="'.($limit_count*2).'" data-ids="'.$p_ids.'">Показать еще товары (<span>'.$counts.'</span>)</div>';
		}		
	}
	
	if ($i eq "1"){
		my $URL = "http://".$ENV{"HTTP_HOST"}."".$first;
		print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
	}
	else {
		print header( -charset=>'windows-1251');
		
		$name = '<div class="title"><h1>Результаты поиска «'.$query.'»</h1></div>';
		
		if ($products ne ""){
			$content = build_ProductTags(1,0,"catalog").''.$products.''.build_ProductTags(0,1,"catalog").$more_products;
		}
		else {$content = '<div class="no_result"><p>Ничего не найдено, попробуйте поменять поисковый запрос.</p></div>';}
	}
}
else {
	print header( -charset=>'windows-1251');
	
	$name = '<div class="title"><h1>Пустой запрос</h1></div>';
	$content = '<div class="no_result"><p>Введите слово для поиска.</p></div>';
}

$catalog_submenu = build_CatalogSubMenu();

require "templates/connection/variables.cgi";

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_catalog",
);

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();


sub stemmer {
	my $query = shift;
	if ($query){
		my @words = split / /, $query;
		my $result="";
		foreach my $item(@words){
			$result .= stem_word($item)." ";
		}
		$result =~s/\s$//g;
		$result =~s/\s/\%/gi;
		return $result;
	}
}