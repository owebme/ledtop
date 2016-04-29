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
$error=param('error');
$adm_act = "pages";

if ($page_alias eq "sitemap"){
	my $URL = "http://".$ENV{"HTTP_HOST"}."/pages/kak-kupit";
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
	exit;
}

if($page_alias){
	$result = $db->query("SELECT * FROM strukture WHERE strukture.alias = '".$page_alias."' AND mirror_link ='' LIMIT 1");
} else {
	$result = $db->query("SELECT * FROM strukture WHERE strukture.id = '".$num_edit."' AND mirror_link ='' LIMIT 1");
}
if(!$result){
	header(-status=>'404'); 
}
foreach my $line(@$result){
	$num_edit = $line->{id};
	$parent_sid = $line->{parent};
	$name = $line->{name};
	$name_section = $line->{name};
	$show = $line->{show};
	$show_head = $line->{show_head};
	$content_text = $line->{html};
	$feedback = $line->{feedback};	
	$sitemap = $line->{sitemap};
	if ($line->{title} eq "") {open OUT, ("admin/$dirs/meta_title"); $main_title = <OUT>; close(OUT); $title = $line->{name}." // ".$main_title;}
	else {$title = $line->{title}};
	$description = $line->{meta_desc};
	$keywords = $line->{meta_key};
	$mirror_id = $line->{mirror_id};
	$redirect = $line->{redirect};
	$maket_page = $line->{maket};
}

if ($redirect ne ""){
	my $URL = "http://".$ENV{"HTTP_HOST"}."".$redirect;
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
}

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_page",
);


$name = build_NamePage($name_section);
require "templates/connection/variables.cgi";

if ($num_edit eq "1") {
	$content = "$content_text ".($mirror_id eq "?adm_act=questions"?"".build_Questions()."":"")." ".($feedback==1?"".build_feedbackPage($content_text)."":"")."";
} else { 
	if ($page_alias eq "delivery"){
		$content = build_CalcDelivery().$content_text;
	}
	else {
		$content = "$content_text ".($mirror_id eq "?adm_act=questions"?"".build_Questions()."":"")." ".($feedback==1?"".build_feedbackPage($content_text)."":"")." ".($sitemap==1?"".build_Sitemap()."":"")."";
	}
}

if ($show eq "1") {
	print header( -charset=>'windows-1251');
}
elsif ($error == 404) {
	print header( -status=> '404 Not found', -charset=>'windows-1251'); 
	$name = '<div class="title"><h1>“акой страницы нет</h1></div>';
	$content = '<p>“акой страницы не существует, перейдите на <a href="/">главную</a> страницу</p>';
}
else {
	print header( -status=> '404 Not found', -charset=>'windows-1251'); 
	$name = '<div class="title"><h1>“акой страницы нет</h1></div>';
	$content = '<p>“акой страницы не существует, перейдите на <a href="/">главную</a> страницу</p>';
}

$content = '<div class="content-holder content-text">'.$content.'</div>';

$catalog_submenu = build_CatalogSubMenu();

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

require "admin/engine/lib/Cache/SaveCache.cgi";
