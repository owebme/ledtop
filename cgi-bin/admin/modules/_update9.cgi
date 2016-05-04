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

# $db->query("ALTER TABLE `cat_product` ADD COLUMN `cat_id` int(11) NULL AFTER `p_id`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_stock` varchar(255) NULL AFTER `p_color_rel`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_waiting` varchar(255) NULL AFTER `p_stock`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_possible` varchar(255) NULL AFTER `p_waiting`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_color` varchar(255) NULL AFTER `p_possible`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_pack` varchar(255) NULL AFTER `p_color`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_packnorm` varchar(255) NULL AFTER `p_pack`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_unit` varchar(255) NULL AFTER `p_packnorm`");
# $db->query("ALTER TABLE `cat_product` ADD COLUMN `p_related` varchar(255) NULL AFTER `p_unit`");
# $db->query("ALTER TABLE `cat_product` DROP COLUMN `p_count`");

my $result = $db->query("SELECT c_id, c_name FROM cat_category WHERE c_desc_bottom != ''");
foreach my $item(@$result){
	print $item->{'c_name'}."<br>";
}
