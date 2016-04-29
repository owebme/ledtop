#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB::Work;
use Core::DB;
use Digest::MD5 qw(md5_hex);

print header(-charset=>'windows-1251');

my $db = new Core::DB();

my $result = $db->query("SELECT p_id, p_name FROM cat_product");
foreach my $item(@$result){
	$db->update("UPDATE cat_product SET `p_alias` = '".Core::DB::Work::translit($item->{'p_name'})."' WHERE p_id = '".$item->{'p_id'}."'");
	print Core::DB::Work::translit($item->{'p_name'})."<br>";
}


