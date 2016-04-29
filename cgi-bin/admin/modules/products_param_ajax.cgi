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

$add_main_param=param('add_main_param');
$param_type=param('param_type');
$param_cat_id=param('param_cat_id');
$del_param=param('del_param');
$getRowsParamsUnic=param('getRowsParamsUnic');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();

my $param = new Core::DB::Catalog();

if ($add_main_param && $param_type) {

	from_to($add_main_param, "utf-8", "cp1251");
	
	if (!$param_cat_id){$param_cat_id = 0;}
	
	$add_main_param =~ s/^\s+//g;
	$add_main_param =~ s/\s+$//g;
	
	my $result = $db->query("SELECT id FROM cat_product_fields_set WHERE cat_id ='".$param_cat_id."' AND f_name = '".$add_main_param."' AND type = '".$param_type."'");
	if (!$result){
		my %params = (
			'cat_id' => $param_cat_id,
			'f_name' => $add_main_param,
			'type' => $param_type
		);
		$param->addParamSet(\%params);
		
		my $res = $db->query("SELECT id FROM cat_product_fields_set WHERE cat_id ='".$param_cat_id."' ORDER BY f_pos DESC LIMIT 1;");
		if ($res->[0]->{id} > 0){
			print $res->[0]->{id};
		}
	}
}

if ($del_param) {
	
	my $id = $del_param;
	my $res = $db->query("SELECT f_name FROM cat_product_fields_set WHERE id = '".$id."' LIMIT 1;");
	my $name = $res->[0]->{f_name};
	
	$db->delete("DELETE FROM cat_product_fields WHERE f_name = '".$name."'");
	$db->delete("DELETE FROM cat_product_fields_set WHERE id = '".$id."'");
}

if ($getRowsParamsUnic){

	my $id = $getRowsParamsUnic;
	
	my $result="";
	my $res = $db->query("SELECT f_name FROM cat_product_fields_set WHERE cat_id = '".$id."' ORDER BY f_pos ASC");
	if ($res){
		foreach my $item(@$res){
			$result .='<tr><td class="name">'.$item->{'f_name'}.'</td><td><input name="fields_unic_'.$item->{'f_name'}.'" type="text" value="" autocomplete="off"></td></tr>';
		}
		print $result;
	}
	else {
		print "not";
	}
}
