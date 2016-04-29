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

my $result = $db->query("SELECT p.p_id, p.p_name, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id = '107' OR pl.cat_id = '108' OR pl.cat_id = '109'");
foreach my $item(@$result){
	if ($item->{'p_name'} =~/Å27/){
		print $item->{'p_name'}." - ".$item->{'cat_main'}."<br>";
		$db->delete("DELETE FROM cat_product_rel WHERE cat_p_id = '".$item->{'p_id'}."' AND cat_id = '".$item->{'cat_id'}."' AND cat_main = '".$item->{'cat_main'}."'");
	}
}


