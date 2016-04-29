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

$db->query("ALTER TABLE `cat_product` ADD COLUMN `p_color_rel` varchar(255) NULL AFTER `p_type_id`");
$db->query("ALTER TABLE `products_alright` CHANGE `p_packnorm` `p_packnorm` varchar(255) NULL DEFAULT NULL");
