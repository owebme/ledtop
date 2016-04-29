#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use CGI::FastTemplate; 
use Core::Config;
use Core::DB;

my $db = new Core::DB();

$adm_act = "basket";

require "templates/connection/require.cgi";
require "templates/basket.cgi";

print header(-charset=>'windows-1251'); 

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_basket",
);

require "templates/connection/variables.cgi";

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

