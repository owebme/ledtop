#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;

my $db = new Core::DB();

print header(-type => 'xml', -charset => 'windows-1251');

require "admin/engine/lib/parametr.cgi";

my $date = "$year-$mon-$mday";
my $domen = 'http://'.$ENV{"HTTP_HOST"};
my $xml ='<?xml version="1.0" encoding="windows-1251"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
	<url>
		<loc>'.$domen.'/</loc>
		<lastmod>'.$date.'</lastmod>
	</url>';
	
		
	my $pages=""; my $articles=""; my $news=""; my $category=""; my $products=""; my $gallery="";
	my $result = $db->query("SELECT strukture.id, strukture.alias, strukture.show, strukture.show_menu, strukture.mirror_link, strukture.mirror_id FROM strukture ORDER BY id ASC");
	foreach my $line(@$result){
		if ($line->{'show'} ne "0" && $line->{'id'} ne "1" && $line->{'alias'} ne "glavnaya" && $line->{'mirror_link'} eq "" && $line->{'mirror_id'} eq ""){
			$pages .='
	<url>
		<loc>'.$domen.'/pages/'.$line->{'alias'}.'</loc>
	</url>';	
		}
	}
	
	if(-e "admin/modules/articles.cgi"){
		$articles .='
		<url>
			<loc>'.$domen.'/public/</loc>
		</url>';
		my $result = $db->query("SELECT articles.alias, articles.show, articles.show_menu FROM articles ORDER BY id ASC");
		foreach my $line(@$result){
			if ($line->{'show'} ne "0" && $line->{'show_menu'} ne "0"){
				$articles .='
		<url>
			<loc>'.$domen.'/public/'.$line->{'alias'}.'</loc>
		</url>';
			}
		}
	}

	if(-e "admin/modules/news.cgi"){
		$news .='
		<url>
			<loc>'.$domen.'/news/</loc>
		</url>';	
		my $result = $db->query("SELECT news.alias, news.show FROM news ORDER BY id ASC");
		foreach my $line(@$result){
			if ($line->{'show'} ne "0"){
				$news .='
		<url>
			<loc>'.$domen.'/news/'.$line->{'alias'}.'</loc>
		</url>';	
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
	
		my $result = $db->query("SELECT cat_category.c_id, cat_category.c_show, cat_category.c_show_menu, cat_category.c_alias FROM cat_category ORDER BY c_id ASC");
		foreach my $line(@$result){
			if ($line->{'c_show'} ne "0" && $line->{'c_show_menu'} ne "0"){
				$category .='
		<url>
			<loc>'.$domen.'/catalog/'.$line->{'c_alias'}.'</loc>
		</url>';
				
				my $pages_amount="";
				my $res = $db->query("SELECT p.p_art, p.p_alias, p.p_show FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$line->{'c_id'}."' AND pl.cat_main ='1' ORDER BY p.p_id");
				foreach my $item(@$res){
					if ($item->{'p_show'} ne "0"){
						$products .='
		<url>
			<loc>'.$domen.'/products/'.$item->{'p_art'}.'/'.$item->{'p_alias'}.'</loc>
		</url>';
						$pages_amount++;
					}
				}
				my $pages=""; my $num="";
				if ($pages_amount ne ""){
					$pages = $pages_amount/$count_pages;
					$pages = $pages+0.49;
					$pages = sprintf("%.0f",$pages);
					for ($num=1; $num <= $pages; $num++) {
						$category .='
		<url>
			<loc>'.$domen.'/catalog/'.$line->{'c_alias'}.'/page_'.$num.'</loc>
		</url>';
					}			
				}
			}
		}
	}
	
	if(-e "admin/modules/fotogal.cgi"){
		$gallery .='
		<url>
			<loc>'.$domen.'/gallery/</loc>
		</url>';
		my $pos_gallery="";
		open OUT, ("$dirs_foto_www2/pos_album.txt"); $pos_gallery = <OUT>; 
		while ($pos_gallery =~ s/(\d+)//)
		{
			open(BO, "admin/$dirs/fotogal.$1"); @b = <BO>; close (BO);
			my ($name_gallery, $date_gallery, $show_gallery) = split(/\|/, $b[0]);	
			if ($show_gallery eq "on") {
				$gallery .='
	<url>
		<loc>'.$domen.'/gallery/'.$1.'</loc>
	</url>';
			}
		}	
	}
	
	$xml .= ''.$pages.''.$articles.''.$news.''.$category.''.$products.''.$gallery.'
</urlset>';


print $xml;
	
	