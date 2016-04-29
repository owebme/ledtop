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

$db->query("ALTER TABLE `cat_orders` ADD COLUMN `datePayment` datetime NULL AFTER `payment`");

$db->query("ALTER TABLE `cat_orders` ADD COLUMN `delivery_price` int(11) NULL AFTER `delivery`");