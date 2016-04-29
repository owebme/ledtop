#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 
use Fcntl;

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;
require "templates/connection/require.cgi";
require "admin/engine/lib/Cache/ReadCache.cgi";
use CGI::FastTemplate;
use Core::Config;
use Core::DB;

my $db = new Core::DB();

$num_edit=param('num_edit');
$page_alias=param('alias');
$page_articles=param('page');
$adm_act = "articles";

open(BO, "admin/$dirs/sort_articles"); $sort_articles = <BO>; close(BO);

if ($page_alias ne "video"){
	if ($page_alias){
		$result = $db->query("SELECT * FROM articles WHERE articles.alias = '".$page_alias."' LIMIT 1");
	}
	if(!$result){
		header(-status=>'404'); 
	}
	foreach my $line(@$result){
		$num_edit = $line->{id};
		$name = $line->{name};
		$show = $line->{show};	
		$content = $line->{html};
		$title = $line->{title};
		$description = $line->{meta_desc};
		$keywords = $line->{meta_key};
		$redirect = $line->{n_redirect};
		$maket_article = $line->{maket};
	}
}

if ($redirect ne ""){
	my $URL = "http://".$ENV{"HTTP_HOST"}."".$redirect;
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
}

if ($num_edit){
	$tpl = new CGI::FastTemplate("admin/$dirs/"); 
		$tpl->define( index     => "maket_html.2",
	);
}
elsif (!$num_edit or $page_alias eq "video"){
	$tpl = new CGI::FastTemplate("admin/$dirs/"); 
		$tpl->define( index     => "maket_html.$maket_article",
	);	
}

require "templates/connection/variables.cgi";

if ($num_edit){
	($name, $content) = build_Article($num_edit, $name, $content);
}
if ($page_alias eq "video"){
	($name, $content) = build_VideoContent();
	$show = 1;
}

if ($show == 1) {
	print header( -charset=>'windows-1251');
}
elsif ($page_alias eq "") {
	open(BO, "admin/$dirs/set_articles"); @set_articles = <BO>; close(BO);
	foreach my $line(@set_articles){chomp($line);
	my ($limit_articles_, $ajax_save_) = split(/\|/, $line);
	$limit_articles=qq~$limit_articles_~;}

	my $pages_amount="";
	my $result = $db->query("SELECT articles.id FROM articles");
	foreach my $line(@$result){
		$pages_amount++;
	}
	my $pagess="";
	if ($pages_amount ne ""){
		$pagess = $pages_amount/$limit_articles;
		$pagess = $pagess+0.49;
		$pagess = sprintf("%.0f",$pagess);
	}
	
	print header( -charset=>'windows-1251');

	my $page="";
	if ($page_articles ne "all" && $page_articles ne ""){
		$page = " Страница ".$page_articles." //";
	}
	elsif ($page_articles eq ""){
		$page = " Страница 1 //";
	}
	$title = "Все интересное о светодиодном освещении //".$page;
	$content = build_Article_main($page_articles, $limit_articles, $pagess, $sort_articles);
}
else {
	print header( -status=> '404 Not found', -charset=>'windows-1251'); 
	$name = '<div class="title"><h1>Такой страницы нет</h1></div>';
	$content = '<p>Такой страницы не существует, перейдите на <a href="/">главную</a> страницу</p>';
}

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();

require "admin/engine/lib/Cache/SaveCache.cgi";
