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
use Core::DB::Catalog;

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";
require "../engine/lib/Cache/ClearCache.cgi";
ClearCache("../..");

$category_id=param('category_id');
$category_content1=param('category_content1');
$category_content2=param('category_content2');
$category_lamp=param('category_lamp');
$category_del=param('category_del');
$cat_move_up=param('cat_move_up');
$cat_move_down=param('cat_move_down');
$cat_move_pos=param('cat_move_pos');
$cat_move_pid=param('cat_move_pid');
$ajax_cat_id=param('ajax_cat_id');
$ajax_img_url=param('ajax_img_url');
$ajax_img_ox=param('ajax_img_ox');
$ajax_img_oy=param('ajax_img_oy');
$watermark_upload=param('watermark_upload');
$watermark_text=param('watermark_text');
$watermark_size=param('watermark_size');
$watermark_color=param('watermark_color');
$watermark_width=param('watermark_width');
$watermark_height=param('watermark_height');
$watermark_del=param('watermark_del');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();
my $catalog = new Core::DB::Catalog();

if ($category_id ne "" && $category_content1 ne "" or $category_id ne "" && $category_content2 ne "") {

	if ($category_content1 ne "clear" && $category_content1 ne ""){
		$category_content1=Core::DB::Work::trans_html($category_content1);	
		use Encode "from_to";
		from_to($category_content1, "utf-8", "cp1251");
		$db->update("UPDATE cat_category SET `c_desc_bottom`='".$category_content1."' WHERE c_id='".$category_id."'");}
	elsif ($category_content1 eq "clear") {
		$db->update("UPDATE cat_category SET `c_desc_bottom`='' WHERE c_id='".$category_id."'");
	}
	if ($category_content2 ne "clear" && $category_content2 ne ""){
		$category_content2=Core::DB::Work::trans_html($category_content2);	
		use Encode "from_to";
		from_to($category_content2, "utf-8", "cp1251");
		$db->update("UPDATE cat_category SET `c_desc_top`='".$category_content2."' WHERE c_id='".$category_id."'");}
	elsif ($category_content2 eq "clear") {
		$db->update("UPDATE cat_category SET `c_desc_top`='' WHERE c_id='".$category_id."'");
	}
}


if ($cat_move_up && $cat_move_pos or $cat_move_down && $cat_move_pos) {


if ($cat_move_up) {
	my $id = $cat_move_up;
	my $current_pos = $db->query("SELECT `c_pos` FROM cat_category WHERE `c_pid`='".$cat_move_pid."' AND c_id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{c_pos};
	if ($pos ne "1"){
		my $MinPos = $db->query("SELECT `c_pos` FROM cat_category WHERE `c_pid`='".$cat_move_pid."' ORDER BY c_pos ASC LIMIT 1");
		if ($MinPos->[0]->{c_pos} eq $pos){
			$pos = "MinPos";
		}
		if ($pos != "MinPos"){
			$pos = PrevPos($id, $pos);
			ChangePosCat($id, $current_pos->[0]->{c_pos}, $pos, "up");
		}
	}
}
elsif ($cat_move_down) {
	my $id = $cat_move_down;
	my $current_pos = $db->query("SELECT `c_pos` FROM cat_category WHERE `c_pid`='".$cat_move_pid."' AND c_id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{c_pos};
	my $MaxPos = $db->query("SELECT `c_pos` FROM cat_category WHERE `c_pid`='".$cat_move_pid."' ORDER BY c_pos DESC LIMIT 1");
	if ($MaxPos->[0]->{c_pos} eq $pos){
		$pos = "MaxPos";
	}
	if ($pos != "MaxPos"){
		$pos = NextPos($id, $pos);
		ChangePosCat($id, $current_pos->[0]->{c_pos}, $pos, "down");
	}
}

sub PrevPos {
	my $id = shift;
	my $pos = shift;
	$pos = $pos-1;
	my $res = $db->query("SELECT `c_id` FROM cat_category WHERE c_pid='".$cat_move_pid."' AND c_pos = '".$pos."' LIMIT 1");
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
	my $res = $db->query("SELECT `c_id` FROM cat_category WHERE c_pid='".$cat_move_pid."' AND c_pos = '".$pos."' LIMIT 1");
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
		$db->update("UPDATE cat_category SET `c_pos`='-1' WHERE c_id='".$id."' AND c_pid='".$cat_move_pid."'");
		$db->update("UPDATE cat_category SET `c_pos`=`c_pos`+1 WHERE `c_pid`='".$cat_move_pid."' AND `c_pos` >= ".$pos." AND `c_pos` <= '".$current_pos."'");
		$db->update("UPDATE cat_category SET `c_pos`=".$pos." WHERE c_id='".$id."' AND c_pid='".$cat_move_pid."'");
	} elsif ($pos_side eq "down"){
		$db->update("UPDATE cat_category SET `c_pos`='-1' WHERE c_id='".$id."' AND c_pid='".$cat_move_pid."'");
		$db->update("UPDATE cat_category SET `c_pos`=`c_pos`-1 WHERE `c_pid`='".$cat_move_pid."' AND `c_pos` <= ".$pos." AND `c_pos` >= '".$current_pos."'");
		$db->update("UPDATE cat_category SET `c_pos`=".$pos." WHERE c_id='".$id."' AND c_pid='".$cat_move_pid."'");
	}
}

}

if ($category_lamp) {

	my $id = $category_lamp;
	my $res = $db->query("SELECT * FROM cat_category WHERE c_id = '".$id."' LIMIT 1");
	
	foreach my $line(@$res){
		$c_show = $line->{c_show_menu};
	}

	if ($c_show eq "0") {
		$db->update("UPDATE cat_category SET `c_show_menu`='1' WHERE c_id='".$id."'");
		print "1";
	}
	elsif ($c_show eq "1") {
		$db->update("UPDATE cat_category SET `c_show_menu`='0' WHERE c_id='".$id."'");
		print "0";
	}
}

if ($category_del) {

	my $id = $category_del;
	$catalog->delCat($id);
	unlink ($dirs_catalog."/category/".($id+1000).".jpg");
}


if ($ajax_cat_id ne "" && $ajax_img_url ne "" && $ajax_img_ox ne "" && $ajax_img_oy ne ""){

	my $num_edit = $ajax_cat_id;
	my $url = $ajax_img_url;
	my $img_ox = $ajax_img_ox;
	my $img_oy = $ajax_img_oy;
	
	use Encode "from_to";
	from_to($url, "utf-8", "cp1251");
	$url =~ s/\s+//g;
	$url =~ s/(.*)http/http/g;
	
	use Image::Magick;
	
	my $image = Image::Magick->new;
	my ($width, $height, $size, $format) = $image->Ping($url);	
	if ($format ne ""){
	
		my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'cat_category';");
		foreach my $item(@$result){	
			$max_num = $item->{Auto_increment};
			$name_file_max = $max_num+1000;			
		}

		if ($num_edit != "empty") {$name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$name_file_max="1001"}}

		use LWP::Simple;
		my $img = get($url);
		open (FH, ">$dirs_catalog/category/$name_file_max\.jpg"); binmode FH;
		print FH $img; close FH;	
		
		%configconsts = (
			'img_resize' => [$img_ox,$img_oy]	
		);

		$image->Read("$dirs_catalog/category/$name_file_max\.jpg"); 
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
		$image->Write("$dirs_catalog/category/$name_file_max\.jpg");
		
		$rand_num=rand(1);

		print '<img border="0" style="max-height:150px; max-width:220px;" src="'.$dirs_catalog_www.'/category/'.$name_file_max.'.jpg?'.$rand_num.'">';	
	}		
	else {
		print "error";
	}
}

if ($watermark_upload ne ""){
	
	my $name_file = "watermark.png";
	
	use LWP::Simple;
	my $img = get($watermark_upload);
	open (FH, ">$dirs_catalog/$name_file"); binmode FH;
	print FH $img; close FH;
	use Image::Magick;
	my $image = Image::Magick->new;	
	my ($width, $height, $size, $format) = $image->Ping("$dirs_catalog/$name_file");
	if ($format ne ""){
		
		if ($width > 400){
			$image->Read("$dirs_catalog/$name_file");
			my $delta = $width/400;
			$ny = int($height/$delta);
			$image->Resize(geometry=>geometry, width=>400, height=>$ny);
			$image->Write("$dirs_catalog/$name_file");
			$width = 400; $height = $ny;
		}
		
		my $rand_num=rand(1);
		
		print $width."|".$height."|".$dirs_catalog_www."/".$name_file."?".$rand_num;
	}
}

if ($watermark_text ne "" && $watermark_size ne "" && $watermark_color ne "" && $watermark_width ne "" && $watermark_height ne ""){

	my $name_file = "watermark.png";
	my $font = "$dirs_catalog/../../admin/css/font-face/intro.ttf";
	my $string = $watermark_text;
	my $size = $watermark_size;
	my $color = $watermark_color;	
	my $width = $watermark_width;
	my $height = $watermark_height;
	
	my $left = $size/2;
	my $top = $height*1.07;
	$left = sprintf("%.0f",$left); 
	$top = sprintf("%.0f",$top); 
	
	$width = $width+($size-2);
	$height = $height+($height-($height-2)+10);
	if ($size > 30){
		$top = $top-(($height-30)/12);
		$top = sprintf("%.0f",$top); 
	}
	elsif ($size < 30){
		$top = $top+((30-$height)/12);
		$height = $height/1.07;
		$top = sprintf("%.0f",$top); 
		$height = sprintf("%.0f",$height); 		
	}

	use Image::Magick;
	
	my $image = Image::Magick->new;
	
	$image->Set(size => $width.'x'.$height);
	$image->Read('xc:#010101');
	$image->Set(
				type 		=> 'TrueColor',
				antialias	=>	'True',
				fill		=>	'#'.$color,
				font		=>	$font,
				pointsize	=>	$size,
				);
	$image->Draw(
				primitive	=>	'text',
				points		=>	$left.','.$top,
				text		=>	$string,
				);
	$image->Write("$dirs_catalog/$name_file");

	my $rand_num=rand(1);
	
	print $width."|".$height."|".$dirs_catalog_www."/".$name_file."?".$rand_num;
}

if ($watermark_del ne ""){

	unlink ("$dirs_catalog/watermark.png");
}