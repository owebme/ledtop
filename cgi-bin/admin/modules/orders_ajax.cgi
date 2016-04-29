#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}
use Fcntl;                                   # O_EXCL, O_CREAT и O_WRONLY

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);          # вывод ошибок к browser-у 
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;
use Core::Config;
use Core::DB;
use Core::DB::Catalog;
use Core::DB::Work;

my $catalog = new Core::DB::Catalog();

$db = new Core::DB();

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";
require "../engine/lib/Cache/ClearCache.cgi";

$pay=param('pay');
$edit_order=param('edit_order');
$field=param('field');
$val_field=param('val_field');
$change_status=param('change_status');
$id_new=param('id_new');
$id_ready=param('id_ready');
$id_call=param('id_call');
$id_del=param('id_del');
$id_delrel=param('id_delrel');
$order_id=param('order_id');
$change_region=param('change_region');
$change_dispatch=param('change_dispatch');
$change_delivery=param('change_delivery');
$suggestProduct=param('suggestProduct');
$changeOrder=param('changeOrder');
$changeOrderProduct=param('changeOrderProduct');
$changeOrderProductPrice=param('changeOrderProductPrice');
$addOrderProduct=param('addOrderProduct');
$addOrderProductCount=param('addOrderProductCount');
$deleteOrderProduct=param('deleteOrderProduct');
$delivery_list=param('delivery_list');

print header(-type => 'text/html', -charset => 'windows-1251'); 

if ($change_region) {

	$db->update("UPDATE cat_orders SET `ch_region` = ".$change_region." WHERE id='".$order_id."'");
}

if ($change_dispatch) {

	$db->update("UPDATE cat_orders SET `dispatch` = ".$change_dispatch." WHERE id='".$order_id."'");
}

if ($change_delivery) {

	$db->update("UPDATE cat_orders SET `delivery` = ".$change_delivery." WHERE id='".$order_id."'");
}

if ($edit_order) {

	my $id = $edit_order;
	use Encode "from_to";
	from_to($val_field, "utf-8", "cp1251");
	if ($val_field ne "" && $field ne "manager") {
		$db->update("UPDATE cat_orders SET `".$field."`='".$val_field."' WHERE id='".$id."'");
	}
	elsif ($field eq "manager") {
		$db->update("UPDATE cat_orders SET `".$field."`='".$val_field."' WHERE id='".$id."'");
	}
	else {}

}

if ($pay) {

	my $id = $pay;
	my $res = $db->query("SELECT * FROM cat_orders WHERE id = '".$id."' LIMIT 1");
	
	foreach my $line(@$res){
		$pay_status = $line->{pay};
	}

	if ($pay_status eq "0") {
		$db->update("UPDATE cat_orders SET `pay`='1' WHERE id='".$id."'");
		print "1";
	}
	elsif ($pay_status eq "1") {
		$db->update("UPDATE cat_orders SET `pay`='0' WHERE id='".$id."'");
		print "0";
	}
	
}

if ($change_status) {

	if ($id_new) {
		my $id = $id_new;
		$db->update("UPDATE cat_orders SET `status`='0', `order_date`='".$today_sql."' WHERE id='".$id."'");
	}
	elsif ($id_ready) {
		my $id = $id_ready;
		$db->update("UPDATE cat_orders SET `status`='1' WHERE id='".$id."'");
	}
	elsif ($id_call) {
		my $id = $id_call;
		$db->update("UPDATE cat_orders SET `status`='3' WHERE id='".$id."'");
	}	
	elsif ($id_del) {
		my $id = $id_del;
		$db->update("UPDATE cat_orders SET `status`='2' WHERE id='".$id."'");
	}
	elsif ($id_delrel) {
		my $id = $id_delrel;
		$db->delete("DELETE FROM cat_orders WHERE id = '".$id."'");
		$db->delete("DELETE FROM cat_orders_product WHERE order_id = '".$id."'");
	}	
	
}

if ($suggestProduct) {

	my $query = $suggestProduct;
	use Encode "from_to";
	from_to($query, "utf-8", "cp1251");

	my $result = $db->query("SELECT * FROM products_alright WHERE p_art = '".$query."' ORDER BY p_name ASC LIMIT 8");

	if (!$result){
		$query =~s/ /\%/gi;
		$result = $db->query("SELECT * FROM products_alright WHERE p_name LIKE '%".$query."%' ORDER BY p_name ASC LIMIT 8");	
	}
	my $items="";
	if ($result){
		foreach my $item(@$result){
			$items .='<li data-price="'.$item->{"p_price"}.'" data-art="'.$item->{"p_art"}.'" data-packnorm="'.$item->{'p_packnorm'}.'"><em class="autosuggest-art">'.$item->{"p_art"}.'</em><em class="autosuggest-item">'.$item->{"p_name"}.'</em></li>';
		}
		if ($items ne ""){
			print '<ul class="autosuggest product lite">'.$items.'</ul>';
		}
	}
}

if ($delivery_list) {

	my %hash=();
	my $result = $db->query("SELECT r.*, s.date_send FROM cat_orders AS r JOIN cat_orders_sender AS s ON(r.id=s.order_id) WHERE s.date_send > NOW() - INTERVAL 10 DAY AND r.status ='0' AND r.dispatch ='2' ORDER BY s.date_send ASC");
	my $table=""; 
	if ($result){
		foreach my $item(@$result){
			if (!$hash{$item->{"id"}}){
				$table .='<tr><td>№'.$item->{"id"}.'</td><td>'.$item->{"phone"}.'</td><td>'.$item->{"name"}.'</td><td>'.$item->{"date_send"}.'</td></tr>';
				%hash = (%hash, $item->{"id"} => $item->{"phone"});
			}
		}
		if ($table){
			$table = '<table style="width:100%; font:14px Arial">'.$table.'</table>';
			print $table;
		}
	}
}

if ($changeOrder) {

	my $id = $changeOrder;
	
	my $user_group=""; my %group = (); my $price="";
	my $result = $db->query("SELECT user_id FROM cat_orders WHERE id = '".$id."'");
	if ($result->[0]->{user_id} > 0){
		my $res = $db->query("SELECT users.group FROM users WHERE id = '".$result->[0]->{user_id}."'");
		if ($res->[0]->{group}){
			$user_group = $res->[0]->{group};
			my $result = $db->query("SELECT * FROM users_group_category WHERE group_id = '".$user_group."'");
			if ($result){
				foreach my $item(@$result){
					%group = (%group,
						$item->{'cat_id'} => $item->{'type'}
					);
				}
			}			
		}
	}
	
	if ($deleteOrderProduct){
		$db->delete("DELETE FROM cat_orders_product WHERE p_art ='".$deleteOrderProduct."' AND order_id = '".$id."' LIMIT 1");
	}
	else {
		my $p_art = $addOrderProduct;
		my $count = $addOrderProductCount;
		
		if ($addOrderProduct eq $changeOrderProduct){
			$db->update("UPDATE cat_orders_product SET `p_count`='".$count."'".($changeOrderProductPrice > 0?", `p_price`='".$changeOrderProductPrice."'":"")." WHERE order_id = '".$id."' AND p_art = '".$changeOrderProduct."'");
			if ($changeOrderProductPrice > 0){
				$price = $changeOrderProductPrice;
			}
		}
		else {
			my $result = $db->query("SELECT * FROM products_alright WHERE p_art = '".$p_art."' LIMIT 1");
			my $p_name = $result->[0]->{"p_name"};
			$price = $result->[0]->{"p_price"};
			if ($user_group > 0){
				my $group_price = $catalog->getPrivateGroupPrice($result->[0]->{"cat_id"}, \%group);
				if ($group_price){
					if ($group_price eq "opt_small"){$price = $result->[0]->{'p_price_opt'};}
					elsif ($group_price eq "opt_large"){$price = $result->[0]->{'p_price_opt_large'};}
				}
			}			
			if ($addOrderProduct && $changeOrderProduct){
				$db->update("UPDATE cat_orders_product SET `p_art`='".$p_art."', `p_name`='".$p_name."', `p_price`='".$price."', `p_count`='".$count."' WHERE order_id = '".$id."' AND p_art = '".$changeOrderProduct."'");
			}
			elsif ($addOrderProduct){
				$db->insert("INSERT INTO `cat_orders_product` (`order_id`, `p_art`, `p_name`, `p_price`, `p_count`) VALUES('".$id."', '".$p_art."', '".$p_name."', '".$price."', '".$count."')");
			}
		}
	}
	
	my $total = 0;
	my $result = $db->query("SELECT cat_orders_product.p_price, cat_orders_product.p_count FROM cat_orders_product WHERE order_id = '".$id."'");
	foreach my $item(@$result){
		$total = $total+($item->{"p_price"}*$item->{"p_count"});
	}
	if ($total > 0){
		$db->update("UPDATE cat_orders SET `total`='".$total."' WHERE id = '".$id."'");
	}
	
	print $total."|".$price;
}
