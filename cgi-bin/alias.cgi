#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;

my $db = new Core::DB();

print header( -charset=>'windows-1251');

my $result = $db->query("SELECT * FROM cat_product");
foreach my $line(@$result){
	my $alias = Core::DB::Work::translit($line->{'p_name'});
	#$db->update("UPDATE cat_product SET `p_alias`='".$alias."' WHERE p_id='".$line->{'p_id'}."'");
	print "Redirect 301 /products/all/".$line->{'p_alias'}." http://well-men.ru/products/all/".$alias."\n";
}
