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

if (param('saveCatalog')) {

	my $item = JSON_take(param('saveCatalog'));
	my $result = $item->{"data"};
	if ($result){
	
		my %data_providers=();
		my $data = $db->query("SELECT id, alias FROM catalog_providers");
		foreach my $item(@$data){
			%data_providers = (%data_providers,
				$item->{"id"} => $item->{"alias"}
			);		
		}
	
		sub jsonData {
			my %data = ();
			my $array = shift;
			my $parent = shift;
			my $pos = 0;
			foreach my $item(@$array){
				$pos++;
				my %row = (
					$item->{"id"} => {
						"parent" => $parent,
						"pos" => $pos
					}
				);
				%data = (%data, %row);
				if ($item->{"children"}){
					my $children = jsonData($item->{"children"}, $item->{"id"});
					%data = (%data, %{$children});
				}				
			}
			return \%data;
		}
		
		my $data = jsonData($result, 0);
	
		while (my ($id, $params) = each(%{$data})){
			$db->update("UPDATE cat_category SET `c_pos`='".$params->{"pos"}."', `c_pid`='".$params->{"parent"}."' WHERE c_id='".$id."'");
		}
		
		my @binds; my %links=();
		my $res_links = $db->query("SELECT * FROM cat_category_links");
		foreach my $link(@$res_links){
			if ($link->{"bind"} eq "0"){
				push(@binds, $link->{"p_cid"});
			}
			if ($links{$link->{"p_id"}}){
				push($links{$link->{"p_id"}}, $link->{"p_cid"});
			}
			else {
				my @array = ($link->{"p_cid"});
				$links{$link->{"p_id"}} = \@array;
			}
		}
		
		#$db->query("TRUNCATE TABLE `cat_product_rel`");

		sub jsonLinks {
			my $array = shift;
			foreach my $item(@$array){
				
				my $id = $item->{"id"};
				
				#$db->delete("DELETE FROM cat_category_links WHERE id = '".$id."'");
				
				if ($item->{"links"}){
					
					my $providers = $item->{"links"};
					
					foreach my $provider(@$providers){
						
						my $p_id = $provider->{"id"};
						my $items = $provider->{"items"};
						
						foreach my $link(@$items){
							
							if ($link->{"id"} ~~ $links{$p_id}) {
								#print "next => ".$link->{"id"}."\n";
								next;
							}
							else {
								#print "NOT next => ".$link->{"id"}."\n";
							}
							
							my $title = $link->{"title"};
							from_to($title, "utf-8", "cp1251");
							
							$db->insert("INSERT INTO `cat_category_links` (`id`, `p_id`, `p_cid`, `name`, `bind`) VALUES('".$id."', '".$p_id."', '".$link->{"id"}."', '".$title."', '".($link->{"id"} ~~ @binds ? "0" : "1")."')");							
							
							my $ids = getCatIds($data_providers{$p_id}, $link->{"id"});
							my $products = $db->query("SELECT p_id FROM cat_product WHERE cat_id IN (".$link->{"id"}.$ids.") AND p_supplier ='".$p_id."'");
							foreach my $product(@$products){
								my %params = (
									'cat_p_id' => $product->{"p_id"},
									'cat_id' => $id
								);	
								$catalog->addProductRel(\%params);	
							}
						}
					}
				}
				if ($item->{"children"}){
					jsonLinks($item->{"children"});
				}				
			}
		}
		
		jsonLinks($result);
		
		print "true";
	}
}

sub getCatIds {
	my $result="";
	my $alias = shift;
	my $id = shift;
	my $data = $db->query("SELECT c_id FROM catalog_".$alias." WHERE c_pid ='".$id."'");
	foreach my $item(@$data){
		$result .= ",".$item->{"c_id"};
		if (my $sub = getCatIds($alias, $item->{"c_id"})){
			$result	.= $sub;
		}				
	}
	return $result;
}	

if (param('removeLink')) {

	my $item = JSON_take(param('removeLink'));
	my $id = $item->{"id"};
	my $p_id = $item->{"p_id"};
	my $alias = $item->{"alias"};
	
	if ($id > 0 && $p_id > 0 && $alias){
	
		$db->delete("DELETE FROM cat_category_links WHERE p_cid = '".$id."' AND p_id = '".$p_id."'");
	
		my $ids = getCatIds($alias, $id);
		my $result = $db->query("SELECT p_id FROM cat_product WHERE cat_id IN (".$id.$ids.") AND p_supplier ='".$p_id."'");
		foreach my $item(@$result){
			$db->delete("DELETE FROM cat_product_rel WHERE cat_p_id = '".$item->{"p_id"}."'");
		}
		print "true";
	}
}

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