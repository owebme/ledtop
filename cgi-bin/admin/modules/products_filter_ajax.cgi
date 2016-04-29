#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;
use Core::DB::Catalog;
use Encode "from_to";

require "../engine/lib/parametr.cgi";

$add_filter=param('add_filter');
$add_filter_name=param('add_filter_name');
$add_filter_childs=param('add_filter_childs');
$add_group=param('add_group');
$add_group_cat_ids=param('add_group_cat_ids');
$change_group=param('change_group');
$change_group_name=param('change_group_name');
$change_group_cat_ids=param('change_group_cat_ids');
$add_group_filter=param('add_group_filter');
$add_group_filter_id=param('add_group_filter_id');
$group_filter_sort=param('group_filter_sort');
$group_filter_sort_id=param('group_filter_sort_id');
$del_filter=param('del_filter');
$del_group_filter=param('del_group_filter');
$del_group=param('del_group');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();

my $filter = new Core::DB::Catalog();

if ($add_filter && $add_filter_name) {

	from_to($add_filter, "utf-8", "cp1251");
	from_to($add_filter_name, "utf-8", "cp1251");

	my %params = (
		'field' => $add_filter,
		'name' => $add_filter_name,
		'f_pid' => 0
	);
	$filter->addFilterSet(\%params);
	
	my $parent="";
	my $res = $db->query("SELECT filter_id FROM cat_product_filters_set ORDER BY filter_id DESC LIMIT 1;");
	if ($res->[0]->{filter_id} > 0){
		$parent = $res->[0]->{filter_id};
	}
	
	print $parent;
	
	if ($add_filter_childs){
		from_to($add_filter_childs, "utf-8", "cp1251");
		while ($add_filter_childs =~ m/(.+?)\|/g) {
			my ($name, $field) = split(/\;/, $1);
			if ($name && $field){
				my %params = (
					'field' => $field,
					'name' => $name,
					'f_pid' => $parent
				);
				$filter->addFilterSet(\%params);
			}
		}
	}	
}

if ($add_group && $add_group_cat_ids) {

	from_to($add_group, "utf-8", "cp1251");

	my %params = (
		'c_ids' => $add_group_cat_ids,
		'g_name' => $add_group
	);
	$filter->addFilterGroup(\%params);
	
	my $group="";
	my $res = $db->query("SELECT g_id FROM cat_product_filters_group ORDER BY g_id DESC LIMIT 1;");
	if ($res->[0]->{g_id} > 0){
		$group = $res->[0]->{g_id};
	}
	
	print $group;
}

if ($change_group && $change_group_name && $change_group_cat_ids) {

	my $id = $change_group;
	from_to($change_group_name, "utf-8", "cp1251");

	$db->update("UPDATE cat_product_filters_group SET `g_name` = '".$change_group_name."', `c_ids` = '".$change_group_cat_ids."' WHERE g_id='".$id."'");
}

if ($add_group_filter && $add_group_filter_id){

	my $group_id = $add_group_filter;
	my $filter_id = $add_group_filter_id;
	
	my $field=""; my $name="";
	my $res = $db->query("SELECT * FROM cat_product_filters_set WHERE filter_id = '".$filter_id."' LIMIT 1;");
	if ($res){
		$field = $res->[0]->{field};
		$name = $res->[0]->{name};
	}	
	if ($field && $name){
		my $alias = Core::DB::Work::translit($name);
		my %params = (
			'field' => $field,
			'name' => $name,
			'f_pid' => 0,
			'gid' => $group_id,
			'f_alias' => $alias
		);
		$filter->addFilter(\%params);
		my $res_f_pid = $db->query("SELECT filter_id FROM cat_product_filters ORDER BY filter_id DESC LIMIT 1;");
		my $result = $db->query("SELECT * FROM cat_product_filters_set WHERE f_pid = '".$filter_id."';");
		foreach my $item(@$result){
			my %params = (
				'field' => $item->{'field'},
				'name' => $item->{'name'},
				'f_pid' => $res_f_pid->[0]->{'filter_id'},
				'gid' => $group_id
			);
			$filter->addFilter(\%params);
			$db->delete("DELETE FROM cat_product_filters_set WHERE filter_id = '".$item->{'filter_id'}."'");
		}
		$db->delete("DELETE FROM cat_product_filters_set WHERE filter_id = '".$filter_id."'");
		
		print $res_f_pid->[0]->{'filter_id'};
	}
}

if ($group_filter_sort_id && $group_filter_sort){

	my $group_id = $group_filter_sort_id;
	my $num="";
	while ($group_filter_sort =~ m/(\d+),/g){
		$num++;
		$db->update("UPDATE cat_product_filters SET `f_pos` = '".$num."' WHERE filter_id = '".$1."' AND gid='".$group_id."' AND f_pid = '0'");
	}
}

if ($del_filter) {
	
	my $id = $del_filter;
	$db->delete("DELETE FROM cat_product_filters_set WHERE f_pid = '".$id."'");
	$db->delete("DELETE FROM cat_product_filters_set WHERE filter_id = '".$id."'");
}

if ($del_group_filter) {
	
	my $id = $del_group_filter;
	$db->delete("DELETE FROM cat_product_filters WHERE f_pid = '".$id."'");
	$db->delete("DELETE FROM cat_product_filters WHERE filter_id = '".$id."'");
}

if ($del_group) {
	
	my $id = $del_group;
	$db->delete("DELETE FROM cat_product_filters WHERE gid = '".$id."'");
	$db->delete("DELETE FROM cat_product_filters_group WHERE g_id = '".$id."'");
}
