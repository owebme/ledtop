#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;
use Core::DB::Catalog;
use Encode "from_to";
#use Data::Dumper;
use Utils::JSON;

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";

print header(-type => 'text/html', -charset => 'windows-1251');

$db = new Core::DB();

my $catalog = new Core::DB::Catalog();

if (param('changeProvider')) {

	my $item = JSON_take(param('changeProvider'));
	
	if ($item->{"provider"}){
		
		my $tree='<ol class="dd-list">';
		my $provider = $item->{"provider"};
		my $result = $db->query("SELECT c_id, c_name FROM catalog_".$provider." WHERE c_pid = '0'");
		foreach my $item(@$result){
			my $items = "";
			if (my $sub = recMenuSecondary($item->{c_id}) ){
				$items .= $sub;				
			}
			$tree .= '<li class="dd-item dd3-item dd3-item-handle dd-collapsed" data-id="'.$item->{c_id}.'">';
			if ($items){
				$tree .= '<button data-action="collapse" type="button" style="display: none;">Collapse</button>
					<button data-action="expand" type="button" style="display: block;">Expand</button>';
			}
			$tree .= '
				<div class="dd-handle dd3-content dd3-content-handle">
					<span class="dd-content-value">'.$item->{c_name}.'</span>
				</div>';
			if ($items) {$tree .= $items;}
			$tree .= '</li>';
		}
		
		sub recMenuSecondary {
			my $id = shift;
			my $text = '<ol class="dd-list">';
			my $result = $db->query("SELECT c_id, c_name FROM catalog_".$provider." WHERE c_pid='".$id."'");
			if ($result){
				foreach my $item(@$result){
					my $items = "";
					if (my $sub = recMenuSecondary($item->{c_id}) ){
						$items .= $sub;				
					}
					$text .= '<li class="dd-item dd3-item dd3-item-handle dd-collapsed" data-id="'.$item->{c_id}.'">';
					if ($items){
						$text .= '<button data-action="collapse" type="button" style="display: none;">Collapse</button>
							<button data-action="expand" type="button" style="display: block;">Expand</button>';
					}
					$text .= '
						<div class="dd-handle dd3-content dd3-content-handle">
							<span class="dd-content-value">'.$item->{c_name}.'</span>
						</div>';
					if ($items) {$text .= $items;}
					$text .= '</li>';
				}
			} else {
				return 0;
			}
			$text .= '</ol>';
			return $text;
		};
		
		print $tree;
	}	
	
}

if (param('name') eq "change") {

	my $id = param('pk');
	my $value = param('value');
	
	from_to($value, "utf-8", "cp1251");
	
	if ($id > 0 && $value){
		$db->update("UPDATE cat_category SET `c_name`='".$value."' WHERE c_id='".$id."'");
	}
	
	print "true";
}

if (param('addCategory')) {

	my $item = JSON_take(param('addCategory'));
	my $name = $item->{"value"};
	
	from_to($name, "utf-8", "cp1251");
	
	my %params = (
		'c_name' => $name,
		'c_pos' => 0,
		'c_pid' => $item->{"id"},
		'c_supplier' => 0,
		'c_show' => 1,
		'c_show_head' => 1,
		'c_show_menu' => 1,
		'c_hide_child' => 0,
		'c_mirror_id' => "",
		'c_mirror_link' => "",		
		'c_alias' => $catalog->buildCatAlias($name, $item->{"id"}),
		'c_maket' => 2
	);
	
	my $result = $catalog->addCat(\%params);	
	
	if ($result && $result > 0){
		my %params = (
			"id" => $result
		);
		print JSON_result(\%params);
	}
	else {
		print "error";
	}
}

if (param('removeCategory')) {

	my $item = JSON_take(param('removeCategory'));
	my $id = $item->{"id"};
	
	if ($id > 0){
	
		$catalog->delCat($id);
		unlink ($dirs_catalog."/category/".($id+1000).".jpg");
		
		print "true";
	}
}