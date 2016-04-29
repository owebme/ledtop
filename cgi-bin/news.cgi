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
$adm_act = "news";

if($page_alias){
	$result = $db->query("SELECT * FROM news WHERE news.alias = '".$page_alias."' LIMIT 1");
} else {
	$result = $db->query("SELECT * FROM news WHERE news.id = '".$num_edit."' LIMIT 1");
}
if(!$result){
	header(-status=>'404'); 
}
foreach my $line(@$result){
	$num_edit = $line->{id};
	$name = $line->{name};
	$show = $line->{show};	
	$content = $line->{html};
	if ($line->{title} eq "") {open OUT, ("admin/$dirs/meta_title"); $main_title = <OUT>; close(OUT); $title = $line->{name}." // ".$main_title;}
	else {$title = $line->{title}};
	$description = $line->{meta_desc};
	$keywords = $line->{meta_key};
	$redirect = $line->{n_redirect};
	$maket_news = $line->{maket};
}

if ($redirect ne ""){
	my $URL = "http://".$ENV{"HTTP_HOST"}."".$redirect;
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
}

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_news",
);

require "templates/connection/variables.cgi";


if ($show == 1) {
	print header( -charset=>'windows-1251');
	$name = build_NameNews($name);
	$content = build_New($num_edit, $content, $type_news);
	$news="";
}
elsif ($page_alias eq "") {
	print header( -charset=>'windows-1251');
	open OUT, ("admin/$dirs/meta_title"); $main_title = <OUT>; close(OUT);
	$title = "Все новости // ".$main_title;
	$content = build_New_main($sort_news, $type_news);
	$news="";
}
else {
	print header( -status=> '404 Not found', -charset=>'windows-1251'); 
	$name = '<div class="title"><h1>Такой страницы нет</h1></div>';
	$content = '<div class="content_text"><p>Такой страницы не существует, перейдите на <a href="/">главную</a> страницу</p></div>';
}

$catalog_submenu = build_CatalogSubMenu();

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

require "admin/engine/lib/Cache/SaveCache.cgi";
