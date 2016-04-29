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
use Core::DB::Articles;

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";
require "../engine/lib/Cache/ClearCache.cgi";
ClearCache("../..");

$page_id=param('page_id');
$page_content=param('page_content');
$page_lamp=param('page_lamp');
$page_del=param('page_del');
$cat_move_up=param('cat_move_up');
$cat_move_down=param('cat_move_down');
$cat_move_pos=param('cat_move_pos');
$cat_move_pid=param('cat_move_pid');
$ajax_cat_id=param('ajax_cat_id');
$ajax_img_url=param('ajax_img_url');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();

if ($page_id ne "" && $page_content ne "") {

	if ($page_content ne "clear"){
		$page_content=Core::DB::Work::trans_html($page_content);	
		use Encode "from_to";
		from_to($page_content, "utf-8", "cp1251");
		$db->update("UPDATE articles SET `html`='".$page_content."' WHERE id='".$page_id."'");}
	elsif ($page_content eq "clear") {
		$db->update("UPDATE articles SET `html`='' WHERE id='".$page_id."'");
	}
}


if ($cat_move_up && $cat_move_pos or $cat_move_down && $cat_move_pos) {

if ($cat_move_up) {
	my $id = $cat_move_up;
	my $current_pos = $db->query("SELECT `pos` FROM articles WHERE `parent`='".$cat_move_pid."' AND id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{pos};
	if ($pos ne "1"){
		my $MinPos = $db->query("SELECT `pos` FROM articles WHERE `parent`='".$cat_move_pid."' ORDER BY pos ASC LIMIT 1");
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
	my $current_pos = $db->query("SELECT `pos` FROM articles WHERE `parent`='".$cat_move_pid."' AND id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{pos};
	my $MaxPos = $db->query("SELECT `pos` FROM articles WHERE `parent`='".$cat_move_pid."' ORDER BY pos DESC LIMIT 1");
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
	my $res = $db->query("SELECT `id` FROM articles WHERE parent='".$cat_move_pid."' AND pos = '".$pos."' LIMIT 1");
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
	my $res = $db->query("SELECT `id` FROM articles WHERE parent='".$cat_move_pid."' AND pos = '".$pos."' LIMIT 1");
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
		$db->update("UPDATE articles SET `pos`='-1' WHERE id='".$id."' AND parent='".$cat_move_pid."'");
		$db->update("UPDATE articles SET `pos`=`pos`+1 WHERE `parent`='".$cat_move_pid."' AND `pos` >= ".$pos." AND `pos` <= '".$current_pos."'");
		$db->update("UPDATE articles SET `pos`=".$pos." WHERE id='".$id."' AND parent='".$cat_move_pid."'");
	} elsif ($pos_side eq "down"){
		$db->update("UPDATE articles SET `pos`='-1' WHERE id='".$id."' AND parent='".$cat_move_pid."'");
		$db->update("UPDATE articles SET `pos`=`pos`-1 WHERE `parent`='".$cat_move_pid."' AND `pos` <= ".$pos." AND `pos` >= '".$current_pos."'");
		$db->update("UPDATE articles SET `pos`=".$pos." WHERE id='".$id."' AND parent='".$cat_move_pid."'");
	}
}

}



if ($page_lamp) {

	my $id = $page_lamp;
	my $res = $db->query("SELECT * FROM articles WHERE id = '".$id."' LIMIT 1");
	
	foreach my $line(@$res){
		$show = $line->{show_menu};
	}

	if ($show eq "0") {
		$db->update("UPDATE articles SET `show_menu`='1' WHERE id='".$id."'");
		print "1";
	}
	elsif ($show eq "1") {
		$db->update("UPDATE articles SET `show_menu`='0' WHERE id='".$id."'");
		print "0";
	}
}


if ($page_del) {
	
	my $id = $page_del;	
	my $articles = new Core::DB::Articles();
	$articles->del($id);
}

if ($ajax_cat_id ne "" && $ajax_img_url ne ""){

	my $num_edit = $ajax_cat_id;
	my $url = $ajax_img_url;
	
	use Encode "from_to";
	from_to($url, "utf-8", "cp1251");
	$url =~ s/\s+//g;
	$url =~ s/(.*)http/http/g;
	
	use Image::Magick;
	
	my $image = Image::Magick->new;
	my ($width, $height, $size, $format) = $image->Ping($url);	
	if ($format ne ""){
	
		my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'articles';");
		foreach my $item(@$result){	
			$max_num = $item->{Auto_increment};
			$name_file_max = $max_num+1000;			
		}

		if ($num_edit != "empty") {$name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$name_file_max="1001"}}

		use LWP::Simple;
		my $img = get($url);
		open (FH, ">$dirs_img/public/$name_file_max\.jpg"); binmode FH;
		print FH $img; close FH;	
		
		use File::Copy;
		copy("$dirs_img/public/$name_file_max\.jpg", "$dirs_img/public/$name_file_max\_big.jpg");
		
		%configconsts = (
			'img_resize' => [362,272]	
		);

		$image->Read("$dirs_img/public/$name_file_max\.jpg"); 
		($ox,$oy)=$image->Get('base-columns','base-rows'); 				

		$division = $configconsts{'img_resize'}[0]/$configconsts{'img_resize'}[1];
		
		if(($ox/$oy)>$division)
			
		{$nx=int(($ox/$oy)*$configconsts{'img_resize'}[1]);			
		$ny=$configconsts{'img_resize'}[1];
		$cropx = int(($nx-$configconsts{'img_resize'}[0])/2);
		$cropy = 0;
		
		} else {
		
			$ny=int(($oy/$ox)*$configconsts{'img_resize'}[0]);	
			$nx=$configconsts{'img_resize'}[0];
			$cropy = int(($ny-$configconsts{'img_resize'}[1])/2);
			$cropx = 0;		
		}
		
		$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
		$image->Crop(x=>$cropx, y=>$cropy);
		$image->Crop($configconsts{'img_resize'}[0], $configconsts{'img_resize'}[1]);
		$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
		$image->Write("$dirs_img/public/$name_file_max\.jpg");
		
		$rand_num=rand(1);

		print '<img border="0" style="max-height:150px; max-width:220px;" src="/uploads/public/'.$name_file_max.'.jpg?'.$rand_num.'">';	
	}		
	else {
		print "error";
	}
}
