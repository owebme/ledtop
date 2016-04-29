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
use Core::DB::Work;
use Core::DB::Pages;

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";
require "../engine/lib/Cache/ClearCache.cgi";

$page_id=param('page_id');
$page_content=param('page_content');
$page_lamp=param('page_lamp');
$page_del=param('page_del');
$hide_del=param('hide_del');
$hide_del_id=param('hide_del_id');
$remove_link=param('remove_link');
$remove_link_id=param('remove_link_id');
$mirror_link=param('mirror_link');
$mirror_link_id=param('mirror_link_id');
$load_razdel=param('load_razdel');
$cat_move_up=param('cat_move_up');
$cat_move_down=param('cat_move_down');
$cat_move_pos=param('cat_move_pos');
$cat_move_pid=param('cat_move_pid');


print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();
my $pages = new Core::DB::Pages();

if ($page_id ne "" && $page_content ne "") {

	if ($page_content ne "clear"){
		$page_content=Core::DB::Work::trans_html($page_content);	
		use Encode "from_to";
		from_to($page_content, "utf-8", "cp1251");
		$db->update("UPDATE strukture SET `html`='".$page_content."' WHERE id='".$page_id."'");}
	elsif ($page_content eq "clear") {
		$db->update("UPDATE strukture SET `html`='' WHERE id='".$page_id."'");
	}
	ClearCache("../..");
}


if ($cat_move_up && $cat_move_pos or $cat_move_down && $cat_move_pos) {

if ($cat_move_up) {
	my $id = $cat_move_up;
	my $current_pos = $db->query("SELECT `pos` FROM strukture WHERE `parent`='".$cat_move_pid."' AND id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{pos};
	if ($pos ne "1"){
		my $MinPos = $db->query("SELECT `pos` FROM strukture WHERE `parent`='".$cat_move_pid."' ORDER BY pos ASC LIMIT 1");
		if ($MinPos->[0]->{pos} eq $pos){
			$pos = "MinPos";
		}
		if ($pos != "MinPos"){
			$pos = PrevPos($id, $pos);
			ChangePosCat($id, $current_pos->[0]->{pos}, $pos, "up");
		}
	}
}
elsif ($cat_move_down) {
	my $id = $cat_move_down;
	my $current_pos = $db->query("SELECT `pos` FROM strukture WHERE `parent`='".$cat_move_pid."' AND id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{pos};
	my $MaxPos = $db->query("SELECT `pos` FROM strukture WHERE `parent`='".$cat_move_pid."' ORDER BY pos DESC LIMIT 1");
	if ($MaxPos->[0]->{pos} eq $pos){
		$pos = "MaxPos";
	}
	if ($pos != "MaxPos"){
		$pos = NextPos($id, $pos);
		ChangePosCat($id, $current_pos->[0]->{pos}, $pos, "down");
	}
}

sub PrevPos {
	my $id = shift;
	my $pos = shift;
	$pos = $pos-1;
	my $res = $db->query("SELECT `id` FROM strukture WHERE parent='".$cat_move_pid."' AND pos = '".$pos."' LIMIT 1");
	if (ref($res) ne 'ARRAY'){
		PrevPos($id, $pos);
	}
	else {
		return $pos;
	}
}

sub NextPos {
	my $id = shift;
	my $pos = shift;
	$pos = $pos+1;
	my $res = $db->query("SELECT `id` FROM strukture WHERE parent='".$cat_move_pid."' AND pos = '".$pos."' LIMIT 1");
	if (ref($res) ne 'ARRAY'){
		NextPos($id, $pos);
	}
	else {
		return $pos;
	}
}
	
sub ChangePosCat {
	my $id = shift;
	my $current_pos = shift;
	my $pos = shift;
	my $pos_side = shift;
	if ($pos_side eq "up"){
		$db->update("UPDATE strukture SET `pos`='-1' WHERE id='".$id."' AND parent='".$cat_move_pid."'");
		$db->update("UPDATE strukture SET `pos`=`pos`+1 WHERE `parent`='".$cat_move_pid."' AND `pos` >= ".$pos." AND `pos` <= '".$current_pos."'");
		$db->update("UPDATE strukture SET `pos`=".$pos." WHERE id='".$id."' AND parent='".$cat_move_pid."'");
	} elsif ($pos_side eq "down"){
		$db->update("UPDATE strukture SET `pos`='-1' WHERE id='".$id."' AND parent='".$cat_move_pid."'");
		$db->update("UPDATE strukture SET `pos`=`pos`-1 WHERE `parent`='".$cat_move_pid."' AND `pos` <= ".$pos." AND `pos` >= '".$current_pos."'");
		$db->update("UPDATE strukture SET `pos`=".$pos." WHERE id='".$id."' AND parent='".$cat_move_pid."'");
	}
}
	ClearCache("../..");
}



if ($page_lamp) {

	my $id = $page_lamp;
	my $res = $db->query("SELECT * FROM strukture WHERE id = '".$id."' LIMIT 1");
	
	foreach my $line(@$res){
		$show = $line->{show_menu};
	}

	if ($show eq "0") {
		$db->update("UPDATE strukture SET `show_menu`='1' WHERE id='".$id."'");
		print "1";
	}
	elsif ($show eq "1") {
		$db->update("UPDATE strukture SET `show_menu`='0' WHERE id='".$id."'");
		print "0";
	}
	ClearCache("../..");
}

if ($hide_del ne "" && $hide_del_id ne "") {

	my $id = $hide_del_id;

	if ($hide_del eq "yes") {
		$db->update("UPDATE strukture SET `hide_del`='1' WHERE id='".$id."'");
		print "1";
	}
	elsif ($hide_del eq "no") {
		$db->update("UPDATE strukture SET `hide_del`='0' WHERE id='".$id."'");
		print "0";
	}	
}

if ($remove_link ne "" && $remove_link_id ne "") {

	my $id = $remove_link_id;

	if ($remove_link eq "yes") {
		$db->update("UPDATE strukture SET `mirror_id`='#!' WHERE id='".$id."'");
		print "1";
	}
	elsif ($remove_link eq "no") {
		$db->update("UPDATE strukture SET `mirror_id`='' WHERE id='".$id."'");
		print "0";
	}	
	ClearCache("../..");
}

if ($mirror_link ne "" && $mirror_link_id ne "") {

	my $id = $mirror_link_id;

	if ($mirror_link ne "reset") {
		my $mirror_id ="";
		if ($mirror_link eq "/news/"){$mirror_id = "?adm_act=news";}
		elsif ($mirror_link eq "/public/"){$mirror_id = "?adm_act=articles";}
		elsif ($mirror_link eq "/gallery/"){$mirror_id = "?adm_act=fotogal";}
		elsif ($mirror_link eq "/catalog/"){$mirror_id = "?adm_act=category";}
		elsif ($mirror_link eq "/catalog/all"){$mirror_id = "?adm_act=products";}
		elsif ($mirror_link eq "/poleznoe/"){$mirror_id = "#";}
		else {
			$mirror_id = "?adm_act=strukture&num_edit=".$mirror_link;
			my $result = $db->query("SELECT strukture.id, strukture.alias FROM strukture WHERE id = '".$mirror_link."'");
			foreach my $item(@$result){
				if ($item->{id} eq "1"){$mirror_link = "/";}
				else {$mirror_link = "/pages/".$item->{alias};}
			}
		}		
		if ($mirror_link_id eq "questions"){
			my $alias = $mirror_link;
			$alias =~ s/\/pages\///g;
			$db->update("UPDATE strukture SET `mirror_id`='?adm_act=questions' WHERE alias='".$alias."'");
		}
		else {
			$db->update("UPDATE strukture SET `mirror_link`='".$mirror_link."' WHERE id='".$id."'");
			$db->update("UPDATE strukture SET `mirror_id`='".$mirror_id."' WHERE id='".$id."'");
		}
		print $mirror_id;
	}
	elsif ($mirror_link eq "reset") {
		$db->update("UPDATE strukture SET `mirror_link`='' WHERE id='".$id."'");
		$db->update("UPDATE strukture SET `mirror_id`='' WHERE id='".$id."'");
		print "reset";
	}
	ClearCache("../..");
}

if ($load_razdel) {

	my $current_id = $load_razdel;
	my $sel_option ="";
	if (-e "../modules/news.cgi"){$sel_option .="<option value='/news/'>Раздел «Новости»</option>";}
	if (-e "../modules/articles.cgi"){$sel_option .="<option value='/public/'>Раздел «Статьи»</option>";}
	if (-e "../modules/fotolist.cgi"){$sel_option .="<option value='/gallery/'>Раздел «Фотогалерея»</option>";}
	if (-e "../modules/questions.cgi"){$sel_option .="<option value='questions'>Раздел «Вопросник»</option>";}
	if (-e "../modules/category.cgi"){$sel_option .="<option value='/catalog/'>Раздел «Каталог»</option>";}
	if (-e "../modules/products.cgi"){$sel_option .="<option value='/catalog/all'>Раздел «Все товары»</option>";}
	if (-e "../../seo.cgi"){$sel_option .="<option value='/poleznoe/'>Раздел «Полезное»</option>";}	
	my $result = $db->query("SELECT * FROM strukture WHERE parent = '0' ORDER BY pos ASC");
	foreach my $item(@$result){
		if ($current_id == $item->{id} or $item->{mirror_link} ne "" or $item->{mirror_id} eq "#!") {$sel_option .='';}
		else {$sel_option .= '<option value="'.$item->{id}.'">'.$item->{name}.'</option>';}
		if( my $sub = recMenu($item->{id}, 0) ){
			$sel_option .= $sub;
		}		
	}
	sub recMenu{
		my $id = shift;
		my $level = shift;
		sub nbsp { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
		my $result = $db->query("SELECT * FROM strukture WHERE parent='".$id."' ORDER BY pos ASC"); 
		if ($result){
			foreach my $item(@$result){
				if ($current_id == $item->{id} or $item->{mirror_link} ne "" or $item->{mirror_id} eq "#!") {$sel_option .='';}
				else {$sel_option .= '<option value="'.$item->{id}.'">'.nbsp($level).$item->{name}.'</option>';}			
				if (my $sub = recMenu($item->{id}, $level+1)){
					$sel_option .= $sub;
				}		
			}
		}
		else {
			return 0;
		}
	}
	
	print $sel_option;	
}


if ($page_del) {

	my $id = $page_del;
	$pages->del($id);
	
	ClearCache("../..");
}
