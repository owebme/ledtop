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

$db->query("ALTER TABLE `cat_orders` ADD COLUMN `invoiceId` varchar(255) NULL AFTER `payment`");

$db->query("ALTER TABLE `cat_orders` ADD COLUMN `totalPayment` float(9,2) NULL AFTER `total`");

$db->query("ALTER TABLE `cat_orders_product` ADD COLUMN `p_price_value` float(9,2) NULL AFTER `p_price`");