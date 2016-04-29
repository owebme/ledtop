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

$db->query("ALTER TABLE `users` CHANGE `status` `group` int(11) NULL DEFAULT NULL");