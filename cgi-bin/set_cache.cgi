#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use LWP::UserAgent;
use Digest::MD5 qw(md5_hex);
use Core::Config;
use Core::DB;

$limit=param('limit');

my $db = new Core::DB();

print header(-charset=>'windows-1251');

require "admin/engine/lib/parametr.cgi";

my $domen = 'http://'.$ENV{"HTTP_HOST"};

	goto_url($domen.'/');

	my $count="";
	my $result = $db->query("SELECT strukture.id, strukture.alias, strukture.show, strukture.show_menu, strukture.mirror_link, strukture.mirror_id FROM strukture ORDER BY id ASC");
	foreach my $line(@$result){
		if ($line->{'show'} ne "0" && $line->{'id'} ne "1" && $line->{'alias'} ne "glavnaya" && $line->{'mirror_link'} eq "" && $line->{'mirror_id'} eq ""){
			if (!-e 'cache/'.md5_hex('/pages/'.$line->{'alias'})){
				goto_url($domen.'/pages/'.$line->{'alias'});
			}
		}
	}

	if(-e "admin/modules/news.cgi"){
		goto_url($domen.'/news/');
		my $result = $db->query("SELECT news.alias, news.show FROM news ORDER BY id ASC");
		foreach my $line(@$result){
			if ($line->{'show'} ne "0"){
				if (!-e 'cache/'.md5_hex('/news/'.$line->{'alias'})){
					goto_url($domen.'/news/'.$line->{'alias'});
				}
			}
		}	
	}
	
	if(-e "admin/modules/category.cgi"){
		my $count_pages="";
		open(BO, "$dirs_catalog_www2/page_settings.txt"); my @pages_count = <BO>; close(BO);
		foreach my $line(@pages_count)
			{
		chomp($line);
		my ($pages_admin, $pages_site) = split(/\|/, $line);
		$count_pages=qq~$pages_site~;
			}
		
		my $result = $db->query("SELECT cat_category.c_id, cat_category.c_pid, cat_category.c_show, cat_category.c_show_menu, cat_category.c_alias FROM cat_category ORDER BY c_id ASC");
		foreach my $line(@$result){
			if ($line->{'c_show'} ne "0" && $line->{'c_show_menu'} ne "0" && $line->{'c_pid'} < 11){
				if (!-e 'cache/'.md5_hex('/catalog/'.$line->{'c_alias'})){
					goto_url($domen.'/catalog/'.$line->{'c_alias'});
				}
			}
		}
	}
	
	sub goto_url {
		my $url = shift;
		if ($limit ne ""){$count++; if ($count > $limit){exit;}}		
		my $ua = LWP::UserAgent->new;
		$ua->get($url);
		print $url."<br>";
	}
	
	