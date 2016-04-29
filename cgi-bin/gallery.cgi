#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
require "templates/connection/require.cgi";
require "admin/engine/lib/Cache/ReadCache.cgi";
use CGI::FastTemplate; 
use Core::Config;
use Core::DB;

my $db = new Core::DB();

$num_edit=param('num_edit');
$page_alias=param('alias');
$img_num=param('img_num');
$soc_enter=param('social');
$adm_act = "gallery";

open(BO, "admin/$dirs/set_fotogal"); @set_fotogal = <BO>; close(BO);

foreach my $line(@set_fotogal)
	{
	chomp($line);
	my ($name_fotogal, $show_all, $hide_resize, $gallery_type_, $script_type_) = split(/\|/, $line);
	$name_fotogal_old="$name_fotogal";	
	$gallery_photo_all="$show_all";
	$gallery_type="$gallery_type_";
	$script_type="$script_type_";
	}

open(BO, "$dirs_foto_www2/fotogal.$page_alias"); @list = <BO>; close (BO);
($name_gallery, $date, $show) = split(/\|/, $list[0]);

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_gallery",
);


require "templates/connection/variables.cgi";

if ($show eq "off"){
	print header( -status=> '404 Not found', -charset=>'windows-1251'); 
	$name = "<h1>Ошибка 404</h1>";
	$content = "Страница не найдена.";
}
else {
	if ($img_num=~ m/([0-9]+)/){
		my $URL = "http://".$ENV{"HTTP_HOST"}."/gallery".($page_alias ne ""?"/".$page_alias."":"")."/?jSbox#img".$img_num;
		print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
	}
	else {
		print header( -charset=>'windows-1251');
		require "templates/gallery.cgi";
		$content = "$script_gallery $gallery";
	}
}

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

require "admin/engine/lib/Cache/SaveCache.cgi";
