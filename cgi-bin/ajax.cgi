#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;

my $db = new Core::DB();

require "admin/engine/lib/parametr.cgi";
require "templates/auth.cgi";

print header(-type => 'text/html', -charset => 'windows-1251');


if (param('getCityList') eq "true"){
	
	my $items=""; my $li=""; my $i = 0; my $s = 0;
	my $result = $db->query("SELECT city FROM city ORDER BY population DESC LIMIT 67");
	foreach my $item(@$result){
		if ($i eq "10"){
			$items .= '<ul>'.$li.'</ul>';
			$li="";
		}
		if ($s eq "14"){
			$items .= '<ul>'.$li.'</ul>';
			$li="";	$s = 0;		
		}
		if ($i > 9){
			$s++;
		}
		$li .= '<li><a href="#">'.$item->{'city'}.'</a></li>';
		$i++;
	}	
	
	print $items;
	
}

if ($logined eq "enter"){

	if (param('getPrivateGroups')){

		use Core::DB::Catalog;
		my $catalog = new Core::DB::Catalog();
		
		my $cat_id = param('getPrivateGroups');
		my $products = $catalog->getPrivateGroups($cat_id, "alright");
		
		if ($products){
		
			print $products;
		}
	}
	elsif (param('getPrivateProducts')){

		use Core::DB::Catalog;
		my $catalog = new Core::DB::Catalog();
		
		my $cat_id = param('getPrivateProducts');
		my $products = $catalog->getPrivateProducts($cat_id, "alright", "", $user_group);
		
		if ($products){
		
			print $products;
		}
		else {
			print "empty";
		}
	}
	elsif (param('getPrivateBasket')){

		use Core::DB::Catalog;
		my $catalog = new Core::DB::Catalog();

		my $basket = $catalog->getPrivateBasket($ids);
		print $basket;
	}
	elsif (param('searchPrivateProducts')){
		
		use Core::DB::Catalog;
		my $catalog = new Core::DB::Catalog();

		my $products = $catalog->getPrivateProducts(param('searchPrivateProducts'), "alright", "search", $user_group);
		if ($products){
			print $products;
		}
		else {
			print "empty";
		}
	}
	elsif (param('relatedPrivateProducts')){
		
		use Core::DB::Catalog;
		my $catalog = new Core::DB::Catalog();

		my $products = $catalog->getPrivateProducts(param('relatedPrivateProducts'), "alright", "related", $user_group);
		if ($products){
			print $products;
		}
	}	
}

