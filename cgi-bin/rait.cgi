#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;

my $db = new Core::DB();

print header( -charset=>'windows-1251');

my $result = $db->query("SELECT cat_product.p_id, cat_product.p_name FROM cat_product");
foreach my $line(@$result){
	my $p_id = $line->{'p_id'};
	my $raiting_all = 0; $count = 0;
	my $result = $db->query("SELECT cat_product_raiting.r_raiting FROM cat_product_raiting WHERE p_id ='".$p_id."'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'r_raiting'};
		$count++;
	}	
	my $result = $db->query("SELECT cat_product_reviews.v_raiting FROM cat_product_reviews WHERE p_id ='".$p_id."' AND v_public = '1'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'v_raiting'};
		$count++;
	}
	if ($count > 0){	
		$raiting_all = $raiting_all/$count;
		$raiting_all = sprintf("%.1f",$raiting_all);	
		$db->update("UPDATE cat_product SET `p_raiting`='".$raiting_all."' WHERE p_id='".$p_id."'");
		$db->update("UPDATE cat_product SET `p_raiting_count`='".$count."' WHERE p_id='".$p_id."'");
		print '<h3>'.$line->{'p_name'}.' - '.$raiting_all.' баллов, '.$count.' голосов</h3>';
	}
}
