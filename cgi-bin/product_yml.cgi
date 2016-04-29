#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;

my $db = new Core::DB();

print header(-type => 'xml', -charset => 'windows-1251');

require "admin/engine/lib/parametr.cgi";

open(BO, "admin/$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
foreach my $line(@select_sort){chomp($line);
my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
$sort_category=qq~$select_sort_cat_~;
$sort_product=qq~$select_sort_product_~;}
my $sort_ = $sort_product;
$sort_=~ s/\sASC$//g;
$sort_=~ s/\sDESC$//g;
if ($sort_ eq "p_pos"){$sort_product = "pl.".$sort_product; $sort_ = "pl.".$sort_;}
else {$sort_product = "p.".$sort_product; $sort_ = "p.".$sort_;}

open(BO, "admin/$dirs/set_yamarket"); @set_yamarket = <BO>; close(BO);
foreach my $line(@set_yamarket){chomp($line);
my ($name_site_, $name_company_, $delivery_) = split(/\|/, $line);
$name_site=qq~$name_site_~;
$name_company=qq~$name_company_~;
$delivery=qq~$delivery_~;}
if ($delivery eq "Бесплатно"){$delivery = "0";}

my $date = "$year-$mon-$mday $hour:$min";

my $yml ='<?xml version="1.0" encoding="windows-1251"?>
<!DOCTYPE yml_catalog SYSTEM "shops.dtd">
<yml_catalog date="'.$date.'">
	<shop>
		<url>http://'.$ENV{"HTTP_HOST"}.'/</url>
		<name>'.$name_site.'</name>
		<company>LEDTOP-SHOP - светодиодное освещение оптом и в розницу</company>		
		<platform>UpleCMS</platform>
		<email>support@uplecms.ru</email>
		
		<currencies>
			<currency id="RUR" rate="1" plus="0"/>
		</currencies>
		
		';
		
	my $category=""; my $products="";	
	my $result = $db->query("SELECT cat_category.c_name, cat_category.c_id, cat_category.c_pid, cat_category.c_alias FROM cat_category ORDER BY ".$sort_category.";");
	foreach my $line(@$result){
		my $name = $line->{'c_name'};
		$name =~ s/\&/&amp;/g;
		$category .='
			<category id="'.$line->{'c_id'}.'"'.($line->{'c_pid'} ne "0"?' parentId="'.$line->{'c_pid'}.'"':'').'>'.$name.'</category>';	
		
		my $res = $db->query("SELECT p.* FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$line->{'c_id'}."' AND pl.cat_main ='1' ORDER BY ".$sort_product);
		foreach my $item(@$res){
			if ($item->{'p_show'} ne "0" && $item->{'p_price'} > 0){
				my $num_foto = $item->{'p_id'}+1000;
				my $name = str_escape($item->{'p_name'});
				my $art = str_escape($item->{'p_art'});
				my $desc = str_escape($item->{'p_desc_top'});
				my $desc_sm = str_escape($item->{'p_desc_sm'});
				$products .='
			<offer id="'.$item->{'p_id'}.'" available="true">
				<url>http://'.$ENV{"HTTP_HOST"}.'/products/'.$item->{'p_art'}.'/'.$item->{'p_alias'}.'</url>
				<price>'.$item->{'p_price'}.'</price>
				<currencyId>RUR</currencyId>
				<categoryId>'.$line->{'c_id'}.'</categoryId>
				<picture>http://'.$ENV{"HTTP_HOST"}.''.$dirs_catalog_www.'/'.$item->{'p_art'}.'.jpg</picture>
				<store>true</store>
				<pickup>true</pickup>
				<delivery>true</delivery>
				<name>'.$name.'</name>
				'.($item->{'p_art'} ne ""?'<vendorCode>'.$art.'</vendorCode>':'').'
				'.($item->{'p_desc_sm'} ne ""?'<description>'.$desc_sm.'</description>':'').'
			</offer>';
			}
		}
	}
	
	if ($category ne ""){$category = '<categories>'.$category.'
		</categories>';}
	if ($products ne ""){$products = '<offers>'.$products.'
		</offers>';}
	
	$yml .= ''.$category.'
		
		<local_delivery_cost>'.$delivery.'</local_delivery_cost>
		
		'.$products.'

	</shop>
</yml_catalog>';


print $yml;

sub str_escape {
	my $text = shift;
	if ($text ne ""){
		$text =~ s/<script[^>]*?>.*?<\/script>//g;
		$text =~ s/<[\/\!]*?[^<>]*?>//g;
		$text =~ s/([\r\n])[\s]+//g;	
		$text =~ s/\&nbsp;/ /g;
		$text =~ s/\s+/ /g;
		$text =~ s/\&ndash;/-/g;
		$text =~ s/\&mdash;/-/g;
		$text =~ s/\&laquo;//g;
		$text =~ s/\&raquo;//g;
		$text =~ s/\&/&amp;/g;
		$text =~ s/\"//g;
		$text =~ s/\>//g;
		$text =~ s/\<//g;
		$text =~ s/\'//g;
	}
	return $text;  
}		
	