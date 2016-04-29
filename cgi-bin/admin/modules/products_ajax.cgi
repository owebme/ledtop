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

open(OUT, "$dirs_catalog/show_settings.txt"); $show_set = <OUT>; 	
	if ($show_set eq "foto") {$show_foto = "active"} else {$show_foto="";}
	if ($show_set eq "list") {$show_list = "active"} else {$show_list="";}
close(OUT);

open(BO, "$dirs_catalog/page_settings.txt"); my @pages_count = <BO>; close(BO);
	foreach my $line(@pages_count)
		{
	chomp($line);
	my ($pages_admin, $pages_site) = split(/\|/, $line);
	$count_pages=qq~$pages_admin~;
		}
		
open(BO, "../$dirs/set_catalog"); @set_catalog = <BO>; close(BO);
foreach my $line(@set_catalog){chomp($line);
my ($ajax_save_old_, $count_more_, $cat_desc_top_, $cat_desc_bottom_, $pr_desc_ext_, $content_wide_, $set_foto_hide_, $img_ext_url_) = split(/\|/, $line);
$img_ext_url =qq~$img_ext_url_~;}		

open(BO, "../$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
foreach my $line(@select_sort){chomp($line);
my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
$sort_products=qq~$select_sort_product_~;}
$sort_products_=$sort_products;
$sort_pr=$sort_products;
$sort_products_=~ s/\sASC$//g;
$sort_products_=~ s/\sDESC$//g;	
if ($sort_products_ eq "p_pos"){$sort_products = "pl.".$sort_products; $sort_products_ = "pl.".$sort_products_;}
else {$sort_products = "p.".$sort_products; $sort_products_ = "p.".$sort_products_;}

$rand_num=rand(1);

$product_id=param('product_id');
$product_content1=param('product_content1');
$product_content2=param('product_content2');
$product_content_lite=param('product_content_lite');
$cat_show_ajax=param('cat_show_ajax');
$cat_show_all=param('cat_show_all');
$cat_show_all_list=param('cat_show_all_list');
$cat_show_all_foto=param('cat_show_all_foto');
$cat_show_select=param('cat_show_select');
$cat_show_select_append=param('cat_show_select_append');
$add_product_rec_id=param('add_product_rec_id');
$add_product_recomend=param('add_product_recomend');
$resort_product_rec_id=param('resort_product_rec_id');
$resort_product_recomend=param('resort_product_recomend');
$del_product_rec_id=param('del_product_rec_id');
$del_product_recomend=param('del_product_recomend');
$add_product_hits=param('add_product_hits');
$add_product_hits_id=param('add_product_hits_id');
$resort_product_hits=param('resort_product_hits');
$resort_product_hits_ids=param('resort_product_hits_ids');
$del_product_hits_id=param('del_product_hits_id');
$del_product_hits=param('del_product_hits');
$cat_current=param('cat_current');
$cat_resort=param('cat_resort');
$product_up=param('product_up');
$product_down=param('product_down');
$product_move=param('product_move');
$product_pos=param('product_pos');
$product_pos_step_left=param('product_pos_step_left');
$product_pos_step_right=param('product_pos_step_right');
$product_cat_id=param('product_cat_id');
$product_moved_cat=param('product_moved_cat');
$product_show=param('product_show');
$product_lamp=param('product_lamp');
$product_del=param('product_del');
$cat_move_up=param('cat_move_up');
$cat_move_down=param('cat_move_down');
$cat_move_pos=param('cat_move_pos');
$cat_move_pid=param('cat_move_pid');
$del_foto=param('del_foto');
$del_foto_num=param('del_foto_num');
$size_foto=param('size_foto');
$show_foto=param('show_foto');
$show_foto_page=param('show_foto_page');
$show_list=param('show_list');
$show_list_page=param('show_list_page');
$save_product=param('save_product');
$product_name=param('product_name');
$product_name_id=param('product_name_id');
$product_price=param('product_price');
$curent_page=param('curent_page');
$type_foto=param('type_foto');
$foto_id=param('foto_id');
$num_id=param('num_id');
$img_url=param('img_url');
$param_big_x=param('param_big_x');
$param_big_y=param('param_big_y');
$param_sm_x=param('param_sm_x');
$param_sm_y=param('param_sm_y');
$param_lite_x=param('param_lite_x');
$param_lite_y=param('param_lite_y');
$param_hdr=param('param_hdr');
$param_normalize=param('param_normalize');
$param_contrast=param('param_contrast');
$param_saturation=param('param_saturation');
$param_sharpness=param('param_sharpness');
$param_resize=param('param_resize');
$param_type_resize=param('param_type_resize');
$imgCrop=param('imgCrop');
$cropImgX1=param('cropImgX1');
$cropImgY1=param('cropImgY1');
$imgCropW=param('imgCropW');
$imgCropH=param('imgCropH');
$CropImgWidth=param('CropImgWidth');
$CropImgHeight=param('CropImgHeight');
$test_image=param('test_image');
$test_image_drop=param('test_image_drop');
$image_effects=param('image_effects');
$autocomplete=param('autocomplete');
$search_word=param('search_word');
$product_clone=param('product_clone');
$reviews_raiting=param('reviews_raiting');
$reviews_raiting_id=param('reviews_raiting_id');
$reviews_raiting_name=param('reviews_raiting_name');
$reviews_raiting_text=param('reviews_raiting_text');
$reviews_public_id=param('reviews_public_id');
$reviews_delete_id=param('reviews_delete_id');
$reviews_edit_id=param('reviews_edit_id');
$reviews_edit_text=param('reviews_edit_text');
$product_hits=param('product_hits');
$search_product_select=param('search_product_select');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();

if ($product_id ne "" && $product_content1 ne "" or $product_id ne "" && $product_content2 ne "") {

	if ($product_content1 ne "clear" && $product_content1 ne ""){
		$product_content1=Core::DB::Work::trans_html($product_content1);	
		use Encode "from_to";
		from_to($product_content1, "utf-8", "cp1251");
		$db->update("UPDATE cat_product SET `p_desc_bottom`='".$product_content1."' WHERE p_id='".$product_id."'");}
	elsif ($product_content1 eq "clear") {
		$db->update("UPDATE cat_product SET `p_desc_bottom`='' WHERE p_id='".$product_id."'");
	}
	if ($product_content2 ne "clear" && $product_content2 ne ""){
		$product_content2=Core::DB::Work::trans_html($product_content2);	
		use Encode "from_to";
		from_to($product_content2, "utf-8", "cp1251");
		$db->update("UPDATE cat_product SET `p_desc_top`='".$product_content2."' WHERE p_id='".$product_id."'");}
	elsif ($product_content2 eq "clear") {
		$db->update("UPDATE cat_product SET `p_desc_top`='' WHERE p_id='".$product_id."'");
	}
	if ($product_content_lite ne "clear" && $product_content_lite ne ""){
		$product_content_lite=Core::DB::Work::trans_html($product_content_lite);	
		use Encode "from_to";
		from_to($product_content_lite, "utf-8", "cp1251");
		$db->update("UPDATE cat_product SET `p_desc_sm`='".$product_content_lite."' WHERE p_id='".$product_id."'");}
	elsif ($product_content_lite eq "clear") {
		$db->update("UPDATE cat_product SET `p_desc_sm`='' WHERE p_id='".$product_id."'");
	}	
}

if ($cat_current or $curent_page) {
	my $page = 1;
	if ($curent_page){$page = $curent_page;}
	if (!$cat_current){
		open(BO, "../$dirs/set_cat_select"); $cat_current = <BO>; close(BO);
		$cat_current =~ s/(\d+)\|(\d+)/$1/g;
	}
	open OUT, (">../$dirs/set_cat_select");
		print OUT "$cat_current|$page"; 
	close(OUT);
}

if ($cat_show_all) {

	my $show_set="";
	if ($cat_show_all_foto eq "load"){
		$show_set = "foto";
		open OUT, (">$dirs_catalog/show_settings.txt");
			print OUT "foto"; 
		close(OUT);		
	}
	elsif ($cat_show_all_list eq "load"){
		$show_set = "list";
		open OUT, (">$dirs_catalog/show_settings.txt");
			print OUT "list"; 
		close(OUT);		
	}	

	my $pagess="";
	if ($curent_page eq ""){
		my $product_page = $db->query("SELECT * FROM cat_product");
		my $pages_amount="";
		foreach my $product(@$product_page){
			$pages_amount++;
		}

		$pagess = $pages_amount/$count_pages;
		$pagess = $pagess+0.49;
		$pagess = sprintf("%.0f",$pagess); 
		my $i=1;
		while ($i <= $pagess) {
			my $style="";
			if ($i > 9 && $i < 100){$style=' style="padding:7px 8px 8px 7px;"';}
			elsif ($i > 99){$style=' style="padding:7px 4px 8px 4px;"';}
			$pages .= '<a href="#" '.($curent_page == $i?'id="current"':'').' '.($curent_page == "" && $i == 1?'id="current"':'').''.$style.' class="page" id_page="'.$i.'">'.$i.'</a>&nbsp;&nbsp;&nbsp;';
			$i++;
		}
		if ($i == "2") {$pages ="";}
	}	

	my $product = $db->query("SELECT p.*, DATE_FORMAT(p_date_add, \"%Y-%m-%d\") as p_date_add, DATE_FORMAT(p_date_up, \"%Y-%m-%d\") as p_date_up FROM cat_product AS p ORDER BY p_name ASC ".($curent_page!=""?"LIMIT ".($curent_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");
	
	
	if ($show_set eq "foto") {
	
		$content_html .= '<ul id="product_foto">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}		
		$p_id = $line->{p_id};
		$img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}
		
		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

		$content_html .= '<li p_id="'.$line->{p_id}.'"><a href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').'<a class="product_del" href="#" del_id="'.$line->{p_id}.'" title="Удалить товар"></a></li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div id=\"allProducts\"><div class=\"message\">В данной категории товаров нет.</div></div>"}
	

	} else {	
	
		$content_html .= '<ul id="product_list">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}			
		$p_id = $line->{p_id};
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}		
		
		$content_html .= '<li p_id="'.$line->{p_id}.'" '.($line->{p_show}==1?'':'class="off"').'><span class="move" id="off"></span><a href="#" '.($line->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$line->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$line->{p_name}.'" href="#" class="product_del" del_id="'.$line->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$line->{p_name}.'</a>'.($line->{p_price}!=""?'<span class="price"><span class="cost_list">'.$line->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div id=\"allProducts\"><div class=\"message\">Товаров нет в каталоге.</div></div>"}

	}	
	
	if ($curent_page eq "" && $p_id ne ""){		
		$content_html ='<div id="allProducts">'.$content_html.'</div>';
	}
	if ($curent_page ne "" && $p_id ne "" or $curent_page eq "" && $p_id ne "") {
		if ($curent_page eq ""){
			if ($pagess > 15){
				$content_html .= '<div class="pages wide"><a href="#" class="page_left">«</a><div class="container"><div class="width">'.$pages.'</div></div><a href="#" class="page_right">»</a></div>';
			}
			else {$content_html .= '<div class="pages"><div class="container">'.$pages.'</div></div>';}	
		}		
		print "$content_html";
	}	
}



if ($cat_show_ajax) {

	my $pagess="";
	if ($curent_page eq "" or $save_product eq "1"){
		
		my $product_page = $db->query("SELECT p.*, ".$sort_products_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_show_ajax."' ORDER BY ".$sort_products."");
		my $pages_amount="";
		foreach my $product(@$product_page){
			$pages_amount++;
		}

		$pagess = $pages_amount/$count_pages;
		$pagess = $pagess+0.49;
		$pagess = sprintf("%.0f",$pagess); 
		my $i=1;
		while ($i <= $pagess) {
			my $style="";
			if ($i > 9 && $i < 100){$style=' style="padding:7px 8px 8px 7px;"';}
			elsif ($i > 99){$style=' style="padding:7px 4px 8px 4px;"';}
			$pages .= '<a href="#" '.($curent_page == $i?'id="current"':'').' '.($curent_page == "" && $i == 1?'id="current"':'').''.$style.' class="page_cat" id_category="'.$cat_show_ajax.'" id_page="'.$i.'">'.$i.'</a>&nbsp;&nbsp;&nbsp;';
			$i++;
		}
		if ($i == "2") {$pages ="";}
	}

	if ($save_product eq "1" && $curent_page eq ""){$curent_page = $pagess;}
	my $product = $db->query("SELECT p.*, ".$sort_products_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_show_ajax."' ORDER BY ".$sort_products." ".($curent_page!=""?"LIMIT ".($curent_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");

	
	if ($show_set eq "foto") {
	
		$content_html .= '<ul id="product_foto" id_cat="'.$cat_show_ajax.'">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
		$p_id = $line->{p_id};
		$img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}		

		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

		$content_html .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'"><a href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').''.($sort_pr eq "p_pos ASC"?'<a class="move_left" href="#" id_move="'.$line->{p_id}.'"></a><a class="move_right" href="#" id_move="'.$line->{p_id}.'"></a>':'').'<a class="product_del" href="#" del_id="'.$line->{p_id}.'" title="Удалить товар"></a></li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div id=\"allProducts\"><div class=\"message\">В данной категории товаров нет.</div></div>"}	
	

	} else {
	
		$content_html .= '<ul id="product_list" id_cat="'.$cat_show_ajax.'">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}		
		$p_id = $line->{p_id};
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			
		
		$content_html .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'" '.($line->{p_show}==1?'':'class="off"').'><span class="move" '.($sort_pr eq "p_pos ASC"?'p_id="'.$line->{p_id}.'" cat_id="'.$line->{cat_id}.'" p_pos="'.$line->{p_pos}.'"><a class="up upper" href="#"></a><a class="down downer" href="#"></a>':'id="off">').'</span><a href="#" '.($line->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$line->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$line->{p_name}.'" href="#" class="product_del" del_id="'.$line->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$line->{p_name}.'</a>'.($line->{p_price}!=""?'<span class="price"><span class="cost_list">'.$line->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div id=\"allProducts\"><div class=\"message\">В данной категории товаров нет.</div></div>"}	
	
	}
	
	if ($curent_page eq "" && $p_id ne "" or $save_product eq "1" && $p_id ne ""){		
		$content_html ='<div id="allProducts">'.$content_html.'</div>';
	}
	if ($curent_page ne "" && $p_id ne "" or $curent_page eq "" && $p_id ne "" or $save_product eq "1" && $p_id ne "") {
		if ($curent_page eq "" or $save_product eq "1"){
			if ($pagess > 15){
				$content_html .= '<div class="pages wide"><a href="#" class="page_left">«</a><div class="container"><div class="width">'.$pages.'</div></div><a href="#" class="page_right">»</a></div>';
			}
			else {$content_html .= '<div class="pages"><div class="container">'.$pages.'</div></div>';}	
		}		
		print "$content_html";
	}	
}



if ($show_foto) {

	open OUT, (">$dirs_catalog/show_settings.txt");
		print OUT "foto"; 
	close(OUT);

	if ($show_foto ne "undefined") {
	
		my $product = $db->query("SELECT p.*, ".$sort_products_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$show_foto."' ORDER BY ".$sort_products." ".($show_foto_page!=""?"LIMIT ".($show_foto_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");

		$content_html .= '<ul id="product_foto" id_cat="'.$show_foto.'">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
		$p_id = $line->{p_id};
		$img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			

		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

		$content_html .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'"><a href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').''.($sort_pr eq "p_pos ASC"?'<a class="move_left" href="#" id_move="'.$line->{p_id}.'"></a><a class="move_right" href="#" id_move="'.$line->{p_id}.'"></a>':'').'<a class="product_del" href="#" del_id="'.$line->{p_id}.'" title="Удалить товар"></a></li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div class=\"message\">В данной категории товаров нет.</div>"} else {print "$content_html";}
	
	}
	
	else {
	
		my $product = $db->query("SELECT * FROM cat_product ORDER BY p_name ASC ".($show_foto_page!=""?"LIMIT ".($show_foto_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");

		$content_html .= '<ul id="product_foto">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
		$p_id = $line->{p_id};
		$img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			

		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

		$content_html .= '<li p_id="'.$line->{p_id}.'"><a href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').'<a class="product_del" href="#" del_id="'.$line->{p_id}.'" title="Удалить товар"></a></li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div class=\"message\">Товаров нет в каталоге.</div>"} else {print "$content_html";}	
	
	}

}



if ($show_list) {

	open OUT, (">$dirs_catalog/show_settings.txt");
		print OUT "list"; 
	close(OUT);

	if ($show_list ne "undefined") {
	
		my $product = $db->query("SELECT p.*, ".$sort_products_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$show_list."' ORDER BY ".$sort_products." ".($show_list_page!=""?"LIMIT ".($show_list_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");

		$content_html .= '<ul id="product_list" id_cat="'.$show_list.'">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}		
		$p_id = $line->{p_id};
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			
		
		$content_html .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'" '.($line->{p_show}==1?'':'class="off"').'><span class="move" '.($sort_pr eq "p_pos ASC"?'p_id="'.$line->{p_id}.'" cat_id="'.$line->{cat_id}.'" p_pos="'.$line->{p_pos}.'"><a class="up upper" href="#"></a><a class="down downer" href="#"></a>':'id="off">').'</span><a href="#" '.($line->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$line->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$line->{p_name}.'" href="#" class="product_del" del_id="'.$line->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$line->{p_name}.'</a>'.($line->{p_price}!=""?'<span class="price"><span class="cost_list">'.$line->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div class=\"message\">В данной категории товаров нет.</div>"} else {print "$content_html";}
	
	}
	
	else {
	
		my $product = $db->query("SELECT * FROM cat_product ORDER BY p_name ASC ".($show_list_page!=""?"LIMIT ".($show_list_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");
		
		$content_html .= '<ul id="product_list">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}		
		$p_id = $line->{p_id};
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			
		
		$content_html .= '<li p_id="'.$line->{p_id}.'" '.($line->{p_show}==1?'':'class="off"').'><span class="move" id="off"></span><a href="#" '.($line->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$line->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$line->{p_name}.'" href="#" class="product_del" del_id="'.$line->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$line->{p_name}.'</a>'.($line->{p_price}!=""?'<span class="price"><span class="cost_list">'.$line->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';
		}

		$content_html .= '</ul>';
		
		if ($p_id eq "") {print "<div class=\"message\">Товаров нет в каталоге.</div>"} else {print "$content_html";}	
	
	}

}



if ($product_up && $product_cat_id && $product_pos or $product_down && $product_cat_id && $product_pos or $product_move && $product_cat_id) {

if ($product_move){
	my $id = $product_move;
	my $current_pos = $db->query("SELECT `p_pos` FROM cat_product_rel WHERE `cat_id`='".$product_cat_id."' AND cat_p_id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{p_pos};
	my $product_pos="";
	if ($current_pos ne "1"){
		if ($product_pos_step_left eq "1"){
			$product_pos = PrevPos($id, $pos);
			ChangePos($id, $current_pos->[0]->{p_pos}, $product_pos, "up");	
			print $product_pos;
		}
		elsif ($product_pos_step_right eq "1"){
			$product_pos = NextPos($id, $pos);
			ChangePos($id, $current_pos->[0]->{p_pos}, $product_pos, "down");
			print $product_pos;
		}
		else {
			my $product_pos_move="";
			if ($product_pos_step_left){
				$product_pos_move = PosMulti($id, $pos, $product_pos_step_left, "left");
				ChangePos($id, $current_pos->[0]->{p_pos}, $product_pos_move, "up");
			}
			elsif ($product_pos_step_right){
				$product_pos_move = PosMulti($id, $pos, $product_pos_step_right, "right");
				ChangePos($id, $current_pos->[0]->{p_pos}, $product_pos_move, "down");
			}
			print $product_pos_move;
		}
	}
}


if ($product_up) {
	my $id = $product_up;
	my $current_pos = $db->query("SELECT `p_pos` FROM cat_product_rel WHERE `cat_id`='".$product_cat_id."' AND cat_p_id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{p_pos};
	my $product_pos="";
	if ($pos ne "1"){
		my $MinPos = $db->query("SELECT `p_pos` FROM cat_product_rel WHERE `cat_id`='".$product_cat_id."' ORDER BY p_pos ASC LIMIT 1");
		if ($MinPos->[0]->{p_pos} eq $pos){
			$pos = "MinPos";
		}
		if ($pos != "MinPos"){
			$product_pos = PrevPos($id, $pos);
			ChangePos($id, $current_pos->[0]->{p_pos}, $product_pos, "up");
		}
	}
}
elsif ($product_down) {
	my $id = $product_down;
	my $current_pos = $db->query("SELECT `p_pos` FROM cat_product_rel WHERE `cat_id`='".$product_cat_id."' AND cat_p_id = '".$id."' LIMIT 1");
	my $pos = $current_pos->[0]->{p_pos};
	my $product_pos="";	
	my $MaxPos = $db->query("SELECT `p_pos` FROM cat_product_rel WHERE `cat_id`='".$product_cat_id."' ORDER BY p_pos DESC LIMIT 1");
	if ($MaxPos->[0]->{p_pos} eq $pos){
		$pos = "MaxPos";
	}
	if ($pos != "MaxPos"){
		$product_pos = NextPos($id, $pos);
		ChangePos($id, $current_pos->[0]->{p_pos}, $product_pos, "down");
	}
}

sub PrevPos {
	my $id = shift;
	my $pos = shift;
	$pos = $pos-1;
	my $res = $db->query("SELECT `cat_p_id` FROM cat_product_rel WHERE cat_id='".$product_cat_id."' AND p_pos = '".$pos."' LIMIT 1");
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
	my $res = $db->query("SELECT `cat_p_id` FROM cat_product_rel WHERE cat_id='".$product_cat_id."' AND p_pos = '".$pos."' LIMIT 1");
	if (ref($res) ne 'ARRAY'){
		NextPos($id, $pos);
	}
	else {
		return $pos;
	}
}

sub PosMulti {
	my $id = shift;
	my $pos = shift;
	my $step = shift;
	my $move = shift;
	if ($move eq "right"){
		$pos = $pos+1;
		my $res = $db->query("SELECT `cat_p_id` FROM cat_product_rel WHERE cat_id='".$product_cat_id."' AND p_pos = '".$pos."' LIMIT 1");
		if (ref($res) ne 'ARRAY' or ref($res) eq 'ARRAY' && $step ne "1"){
			if (ref($res) eq 'ARRAY'){$step--;}
			PosMulti($id, $pos, $step, "right");
		}
		else {
			return $pos;
		}	
	}
	elsif ($move eq "left"){
		$pos = $pos-1;
		my $res = $db->query("SELECT `cat_p_id` FROM cat_product_rel WHERE cat_id='".$product_cat_id."' AND p_pos = '".$pos."' LIMIT 1");
		if (ref($res) ne 'ARRAY' or ref($res) eq 'ARRAY' && $step ne "1"){
			if (ref($res) eq 'ARRAY'){$step--;}
			PosMulti($id, $pos, $step, "left");
		}
		else {
			return $pos;
		}	
	}	
}
	
sub ChangePos {
	my $id = shift;
	my $current_pos = shift;
	my $pos = shift;
	my $pos_side = shift;
	if ($pos_side eq "up"){
		$db->update("UPDATE cat_product_rel SET `p_pos`='-1' WHERE cat_p_id='".$id."' AND cat_id='".$product_cat_id."'");
		$db->update("UPDATE cat_product_rel SET `p_pos`=`p_pos`+1 WHERE `cat_id`='".$product_cat_id."' AND `p_pos` >= ".$pos." AND `p_pos` <= '".$current_pos."'");
		$db->update("UPDATE cat_product_rel SET `p_pos`=".$pos." WHERE cat_p_id='".$id."' AND cat_id='".$product_cat_id."'");
	} elsif ($pos_side eq "down"){
		$db->update("UPDATE cat_product_rel SET `p_pos`='-1' WHERE cat_p_id='".$id."' AND cat_id='".$product_cat_id."'");
		$db->update("UPDATE cat_product_rel SET `p_pos`=`p_pos`-1 WHERE `cat_id`='".$product_cat_id."' AND `p_pos` <= ".$pos." AND `p_pos` >= '".$current_pos."'");
		$db->update("UPDATE cat_product_rel SET `p_pos`=".$pos." WHERE cat_p_id='".$id."' AND cat_id='".$product_cat_id."'");
	}
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
			$pos = PrevPosCat($id, $pos);
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
		$pos = NextPosCat($id, $pos);
		ChangePosCat($id, $current_pos->[0]->{c_pos}, $pos, "down");
	}
}

sub PrevPosCat {
	my $id = shift;
	my $pos = shift;
	$pos = $pos-1;
	my $res = $db->query("SELECT `c_id` FROM cat_category WHERE c_pid='".$cat_move_pid."' AND c_pos = '".$pos."' LIMIT 1");
	if (ref($res) ne 'ARRAY'){
		PrevPosCat($id, $pos);
	}
	else {
		return $pos;
	}
}

sub NextPosCat {
	my $id = shift;
	my $pos = shift;
	$pos = $pos+1;
	my $res = $db->query("SELECT `c_id` FROM cat_category WHERE c_pid='".$cat_move_pid."' AND c_pos = '".$pos."' LIMIT 1");
	if (ref($res) ne 'ARRAY'){
		NextPosCat($id, $pos);
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


if ($cat_resort){

		my $num="";
		my $products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_resort."' ORDER BY pl.p_pos ASC");
		foreach my $item(@$products){
			$num++;
			$db->update("UPDATE cat_product_rel SET `p_pos`='".$num."' WHERE cat_p_id='".$item->{p_id}."' AND p_pos = '".$item->{p_pos}."' AND cat_id='".$cat_resort."'");
		}

		my $product_page = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_resort."' ORDER BY pl.p_pos ASC");
		my $pages_amount="";
		foreach my $product(@$product_page){
			$pages_amount++;
		}

		my $pagess = $pages_amount/$count_pages;
		$pagess = $pagess+0.49;
		$pagess = sprintf("%.0f",$pagess); 
		my $i=1;
		while ($i <= $pagess) {
			my $style="";
			if ($i > 9 && $i < 100){$style=' style="padding:7px 8px 8px 7px;"';}
			elsif ($i > 99){$style=' style="padding:7px 4px 8px 4px;"';}		
			$pages .= '<a href="#" '.($curent_page == $i?'id="current"':'').' '.($curent_page == "" && $i == 1?'id="current"':'').''.$style.' class="page_cat" id_category="'.$cat_resort.'" id_page="'.$i.'">'.$i.'</a>&nbsp;&nbsp;&nbsp;';
			$i++;
		}
		if ($i == "2") {$pages ="";}

		my $product = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_resort."' ORDER BY pl.p_pos ASC ".($curent_page!=""?"LIMIT ".($curent_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");

		$content_html .= '<ul id="product_foto" id_cat="'.$cat_resort.'">';	
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
		$p_id = $line->{p_id};
		$img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}		

		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

		$content_html .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'"><a href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').''.($sort_pr eq "p_pos ASC"?'<a class="move_left" href="#" id_move="'.$line->{p_id}.'"></a><a class="move_right" href="#" id_move="'.$line->{p_id}.'"></a>':'').'<a class="product_del" href="#" del_id="'.$line->{p_id}.'" title="Удалить товар"></a></li>';
		}

		if ($pagess > 15){
			$content_html .= '</ul><div class="pages wide"><a href="#" class="page_left">«</a><div class="container"><div class="width">'.$pages.'</div></div><a href="#" class="page_right">»</a></div>';
		}
		else {$content_html .= '</ul><div class="pages"><div class="container">'.$pages.'</div></div>';}
		
		if ($p_id eq "") {print "<div class=\"message\">В данной категории товаров нет.</div>"} else {print "$content_html";}
}

if ($search_product_select ne ""){

	use Lingua::Stem2::Ru;
	
	my $word = $search_product_select;
	use Encode "from_to";
	from_to($word, "utf-8", "cp1251");
	$word = stemmer($word);

	my $products="";
	my $result = $db->query("SELECT * FROM cat_product WHERE p_art LIKE '%".$word."%'");
	if (!$result){
		$result = $db->query("SELECT * FROM cat_product WHERE p_name LIKE '%".$word."%'");
	}
	if ($result){
		foreach my $line(@$result){
			my $string = length($line->{p_name});
			if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
			$p_id = $line->{p_id};
			$img_id = $p_id+1000;
			
			my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
			if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			

			$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

			$products .= '<li class="new" data-id="'.$line->{p_id}.'">'.$img_sm.'<span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').'</li>';
		}
	}
	if (!$result) {print '<div class="no_result">Ничего не найдено, попробуйте поменять поисковый запрос.</div>';}
	else {print '<ul>'.$products.'<div class="clear" style="clear:both"></div></ul>';}	
}

if ($cat_show_select ne ""){

	my $cat_id = $cat_show_select;
	my $current = $cat_show_select_append;
	my $products="";
	my $result = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_id."' ORDER BY pl.p_pos ASC ".($cat_show_select_append!=""?"LIMIT ".$current.",48":"LIMIT 0,48")."");
	foreach my $line(@$result){
		my $string = length($line->{p_name});
		if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
		$p_id = $line->{p_id};
		$img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}			

		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

		$products .= '<li class="new" data-id="'.$line->{p_id}.'">'.$img_sm.'<span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').'</li>';
	}
	if ($cat_show_select_append eq ""){
		if ($p_id eq "") {print '<div class="no_result">В данной категории товаров нет.</div>';}
		else {print '<ul>'.$products.'<div class="clear" style="clear:both"></div></ul>';}	
	}
	else {
		if ($products eq ""){
			print "end";
		}
		else {
			print $products;
		}
	}
}

if ($add_product_rec_id ne "" && $add_product_recomend ne ""){
	
	my $p_id = $add_product_rec_id;
	my $ids = $add_product_recomend;
	my $last_pos="";
	my $result = $db->query("SELECT * FROM cat_product_recomend WHERE rec_id ='".$p_id."' ORDER BY r_pos DESC LIMIT 1");
	foreach my $item(@$result){
		$last_pos = $item->{r_pos};
	}	
	my $current_pos = $last_pos+1;	
	my $products = new Core::DB::Catalog();
	my %params = (
		'rec_id' => $p_id,
		'p_ids' => $ids,
		'r_pos' => $current_pos
	);			
	$db->delete("DELETE FROM cat_product_recomend WHERE rec_id = '".$p_id."' AND p_ids = '".$ids."'");
	$products->addProductRec(\%params);	

	$db->update("UPDATE cat_product_recomend SET `r_pos`='-1' WHERE p_ids='".$ids."' AND rec_id='".$p_id."'");
	$db->update("UPDATE cat_product_recomend SET `r_pos`=`r_pos`+1 WHERE `rec_id`='".$p_id."' AND `r_pos` >= '1' AND `r_pos` <= '".$current_pos."'");
	$db->update("UPDATE cat_product_recomend SET `r_pos`='1' WHERE p_ids='".$ids."' AND rec_id='".$p_id."'");	
	
	my $num="";
	my $products = $db->query("SELECT * FROM cat_product_recomend WHERE rec_id ='".$p_id."' ORDER BY r_pos ASC");
	foreach my $item(@$products){
		$num++; $db->update("UPDATE cat_product_recomend SET `r_pos`='".$num."' WHERE p_ids='".$ids."' AND r_pos = '".$item->{r_pos}."' AND rec_id='".$p_id."'");
	}
}

if ($resort_product_rec_id ne "" && $resort_product_recomend ne ""){
	
	my $p_id = $resort_product_rec_id;
	my $ids = $resort_product_recomend;
	
	my $num="";
	while ($ids =~ m/(\d+)\|/g) {
		$num++;
		$db->update("UPDATE cat_product_recomend SET `r_pos`='".$num."' WHERE p_ids='".$1."' AND rec_id='".$p_id."'");
	}
}

if ($del_product_rec_id ne "" && $del_product_recomend ne ""){

	my $p_id = $del_product_rec_id;
	my $ids = $del_product_recomend;
	
	$db->delete("DELETE FROM cat_product_recomend WHERE rec_id = '".$p_id."' AND p_ids = '".$ids."'");
}

if ($add_product_hits ne "" && $add_product_hits_id ne ""){
	
	my $hit_id = $add_product_hits;
	my $ids = $add_product_hits_id;
	my $last_pos="";
	my $result = $db->query("SELECT * FROM cat_product_hits WHERE hit_id ='".$hit_id."' ORDER BY p_pos DESC LIMIT 1");
	foreach my $item(@$result){
		$last_pos = $item->{p_pos};
	}	
	my $current_pos = $last_pos+1;	
	my $products = new Core::DB::Catalog();
	my %params = (
		'hit_id' => $hit_id,
		'p_ids' => $ids,
		'p_pos' => $current_pos
	);			
	$db->delete("DELETE FROM cat_product_hits WHERE hit_id = '".$hit_id."' AND p_ids = '".$ids."'");
	$products->addProductHit(\%params);	

	$db->update("UPDATE cat_product_hits SET `p_pos`='-1' WHERE p_ids='".$ids."' AND hit_id='".$hit_id."'");
	$db->update("UPDATE cat_product_hits SET `p_pos`=`p_pos`+1 WHERE `hit_id`='".$hit_id."' AND `p_pos` >= '1' AND `p_pos` <= '".$current_pos."'");
	$db->update("UPDATE cat_product_hits SET `p_pos`='1' WHERE p_ids='".$ids."' AND hit_id='".$hit_id."'");	
	
	my $num="";
	my $products = $db->query("SELECT * FROM cat_product_hits WHERE hit_id ='".$hit_id."' ORDER BY p_pos ASC");
	foreach my $item(@$products){
		$num++; $db->update("UPDATE cat_product_hits SET `p_pos`='".$num."' WHERE p_ids='".$ids."' AND p_pos = '".$item->{p_pos}."' AND hit_id='".$hit_id."'");
	}
}

if ($resort_product_hits ne "" && $resort_product_hits_ids ne ""){
	
	my $hit_id = $resort_product_hits;
	my $ids = $resort_product_hits_ids;
	
	my $num="";
	while ($ids =~ m/(\d+)\|/g) {
		$num++;
		$db->update("UPDATE cat_product_hits SET `p_pos`='".$num."' WHERE p_ids='".$1."' AND hit_id='".$hit_id."'");
	}
}

if ($del_product_hits ne "" && $del_product_hits_id ne ""){

	my $hit_id = $del_product_hits;
	my $ids = $del_product_hits_id;
	
	$db->delete("DELETE FROM cat_product_hits WHERE hit_id = '".$hit_id."' AND p_ids = '".$ids."'");
}

if ($product_moved_cat && $product_cat_id){

	my $products = new Core::DB::Catalog();

	my $id = $product_moved_cat;
	my $cat_id = $product_cat_id;
	$db->delete("DELETE FROM cat_product_rel WHERE cat_p_id = '".$id."'");
	
	my $last_pos="";
	my $result = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_id."' ORDER BY pl.p_pos DESC LIMIT 1");
	foreach my $item(@$result){
		$last_pos = $item->{p_pos};
	}	
	my $current_pos = $last_pos+1;	
	my %params_rel = (
		'p_pos' => $current_pos,
		'cat_p_id' => "$id",
		'cat_main' => "1",
		'cat_id' => $cat_id
	);			
	$products->addProductRel(\%params_rel);	

	$db->update("UPDATE cat_product_rel SET `p_pos`='-1' WHERE cat_p_id='".$id."' AND cat_id='".$cat_id."'");
	$db->update("UPDATE cat_product_rel SET `p_pos`=`p_pos`+1 WHERE `cat_id`='".$cat_id."' AND `p_pos` >= '1' AND `p_pos` <= '".$current_pos."'");
	$db->update("UPDATE cat_product_rel SET `p_pos`='1' WHERE cat_p_id='".$id."' AND cat_id='".$cat_id."'");	
	
	my $num="";
	my $products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_id."' ORDER BY pl.p_pos ASC");
	foreach my $item(@$products){
		$num++;
		$db->update("UPDATE cat_product_rel SET `p_pos`='".$num."' WHERE cat_p_id='".$item->{p_id}."' AND p_pos = '".$item->{p_pos}."' AND cat_id='".$cat_id."'");
	}		
	
	print "moved";
}


if ($product_name) {

	my $id = $product_name_id;
	use Encode "from_to";
	from_to($product_name, "utf-8", "cp1251");
	if ($product_name ne "") {
		$db->update("UPDATE cat_product SET `p_name`='".$product_name."' WHERE p_id='".$id."'");
	}
	else {}
	
}

if ($product_price) {

	my $id = $product_name_id;
	use Encode "from_to";
	from_to($product_price, "utf-8", "cp1251");
	if ($product_price ne "") {
		$product_price =~ s/\ //g;
		$db->update("UPDATE cat_product SET `p_price`='".$product_price."' WHERE p_id='".$id."'");
	}
	else {}
	
}


if ($product_lamp) {

	my $id = $product_lamp;
	my $res = $db->query("SELECT * FROM cat_product WHERE p_id = '".$id."' LIMIT 1");
	
	foreach my $line(@$res){
		$p_show = $line->{p_show};
	}

	if ($p_show eq "0") {
		$db->update("UPDATE cat_product SET `p_show`='1' WHERE p_id='".$id."'");
		print "1";
	}
	elsif ($p_show eq "1") {
		$db->update("UPDATE cat_product SET `p_show`='0' WHERE p_id='".$id."'");
		print "0";
	}
	
}


if ($product_del) {

	my $id = $product_del;
	$db->delete("DELETE FROM cat_product WHERE p_id = '".$id."'");
	$db->delete("DELETE FROM cat_product_rel WHERE cat_p_id = '".$id."'");
	$db->delete("DELETE FROM cat_product_fields WHERE p_id = '".$id."'");

	$num = $product_del+1000;
	
	unlink ("$dirs_catalog/$num\_small.jpg");
	unlink ("$dirs_catalog/$num\_normal.jpg");	
	unlink ("$dirs_catalog/$num\_big.jpg");	
	unlink ("$dirs_catalog/$num\_preview.jpg");

	for ($i=1; $i<13; $i++) {
		if(-e "$dirs_catalog/$num\_$i\_small.jpg"){
			unlink ("$dirs_catalog/$num\_$i\_small.jpg");
		}
		if(-e "$dirs_catalog/$num\_$i\_normal.jpg"){
			unlink ("$dirs_catalog/$num\_$i\_normal.jpg");
		}
		if(-e "$dirs_catalog/$num\_$i\_big.jpg"){
			unlink ("$dirs_catalog/$num\_$i\_big.jpg");
		}
	}
}

if ($del_foto) {

	if ($size_foto eq "small") { unlink ("$dirs_catalog/$del_foto\_small.jpg"); unlink ("$dirs_catalog/$del_foto\_preview.jpg");}
	if ($size_foto eq "big") { unlink ("$dirs_catalog/$del_foto\_big.jpg"); unlink ("$dirs_catalog/$del_foto\_normal.jpg");}
	if ($size_foto eq "lite" && $del_foto_num ne "") {
		unlink ("$dirs_catalog/$del_foto\_$del_foto_num\_small.jpg");
		unlink ("$dirs_catalog/$del_foto\_$del_foto_num\_normal.jpg");
		unlink ("$dirs_catalog/$del_foto\_$del_foto_num\_big.jpg");
	}	
}

if ($autocomplete eq "load"){
	
	my $result='{';

	my $res = $db->query("SELECT cat_product.p_id, cat_product.p_name, cat_product.p_price FROM cat_product WHERE p_show != '0'");
	foreach my $line(@$res){
		my $name = $line->{'p_name'};
		$name =~ s/'//g;
		$name =~ s/"//g;
		$result .= '"'.($line->{'p_id'}+1000).'['.($line->{'p_price'} > 0?''.$line->{'p_price'}.'':'0').']": "'.$name.'",';
	}
	$result =~ s/,$//g;
	$result .='}';
	
	print $result;
}

if ($search_word ne ""){

	use Lingua::Stem2::Ru;
	
	my $word = $search_word;
	use Encode "from_to";
	from_to($word, "utf-8", "cp1251");
	$word = stemmer($word);	
	
	my $products="";
	my $result = $db->query("SELECT * FROM cat_product WHERE p_art LIKE '%".$word."%'");
	if (!$result){
		$result = $db->query("SELECT * FROM cat_product WHERE p_name LIKE '%".$word."%'");
	}
	if ($result){
		foreach my $line(@$result){
			if ($show_set eq "foto"){
				my $size_name="";
				my $string = length($line->{p_name});
				if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
				my $p_id = $line->{p_id};
				my $img_id = $p_id+1000;	

				my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
				if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}	
				
				$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';

				$products .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'"><a href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($line->{p_show}==1?'':'style="color:#aaa"').' >'.$line->{p_name}.'</span>'.($line->{p_price}!=""?'<span class="price"><span class="cost">'.$line->{p_price}.'</span>,-</span>':'').'<a class="product_del" href="#" del_id="'.$line->{p_id}.'" title="Удалить товар"></a></li>';
			}
			elsif ($show_set eq "list") {
				my $size_name="";
				my $string = length($line->{p_name});
				if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}		
				my $p_id = $line->{p_id};
				
				my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
				if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}					
				
				$products .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'" '.($line->{p_show}==1?'':'class="off"').'><span id="off" class="move"></span><a href="#" '.($line->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$line->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$line->{p_name}.'" href="#" class="product_del" del_id="'.$line->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$line->{p_name}.'</a>'.($line->{p_price}!=""?'<span class="price"><span class="cost_list">'.$line->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';
			}
		}
	}
	
	if ($products ne ""){
		if ($show_set eq "foto"){
			$products = '<ul id="product_foto">'.$products.'</ul>';
		}
		elsif ($show_set eq "list"){
			$products = '<ul id="product_list">'.$products.'</ul>';
		}
		$products = '<div id="allProducts">'.$products.'</div>';
	}
	else {
		$products = '<div id="allProducts"><div class="message">Ничего не найдено, попробуйте поменять поисковый запрос.</div></div>';
	}
	
	print $products;
}

if ($product_clone ne ""){

	my $id = $product_clone;
	my $products = new Core::DB::Catalog();

	my $res = $db->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1");
	my $cat_id=""; my $p_pos=""; my $p_id = $res->[0]->{p_id}+1;
	my $result = $db->query("SELECT p.*, pl.p_pos, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_id ='".$id."' AND pl.cat_main ='1' LIMIT 1");
	foreach my $item(@$result){
		$cat_id = $item->{cat_id};
		$p_pos = $item->{p_pos};
		%params = (
					'p_id' => $p_id,
					'p_name' => $item->{p_name},
					'p_desc_bottom' => $item->{p_desc_bottom},
					'p_desc_top' => $item->{p_desc_top},
					'p_desc_sm' => $item->{p_desc_sm},
					'p_price' => $item->{p_price},
					'p_price_old' => $item->{p_price_old},
					'p_art' => $item->{p_art}."d",					
					'p_title' => $item->{p_title},
					'p_meta_desc' => $item->{p_meta_desc},
					'p_meta_key' => $item->{p_meta_key},
					'p_date_up' => $item->{p_date_up},
					'p_date_add' => $item->{p_date_add},
					'p_show' => $item->{p_show},
					'p_show_head' => $item->{p_show_head},
					'p_alias' => $item->{p_alias},
					'p_redirect' => $item->{p_redirect},
					'p_type_id' => $item->{p_type_id},
					'p_maket' => $item->{p_maket}				
		);
		%params_rel = (
					'p_pos' => $item->{p_pos},
					'cat_p_id' => $p_id,
					'cat_main' => "1",	
					'cat_id' => $cat_id
		);
	}		
		$products->addProduct(\%params);
		$products->addProductRel(\%params_rel);	
		
		use File::Copy;
		my $img = $p_id+1000; my $img_copy = $id+1000;
		if(-e "$dirs_catalog/$img_copy\_preview.jpg"){copy("$dirs_catalog/$img_copy\_preview.jpg", "$dirs_catalog/$img\_preview.jpg");}
		if(-e "$dirs_catalog/$img_copy\_small.jpg"){copy("$dirs_catalog/$img_copy\_small.jpg", "$dirs_catalog/$img\_small.jpg");}
		if(-e "$dirs_catalog/$img_copy\_normal.jpg"){copy("$dirs_catalog/$img_copy\_normal.jpg", "$dirs_catalog/$img\_normal.jpg");}
		if(-e "$dirs_catalog/$img_copy\_big.jpg"){copy("$dirs_catalog/$img_copy\_big.jpg", "$dirs_catalog/$img\_big.jpg");}
		for ($num=1; $num<13; $num++) {
			if(-e "$dirs_catalog/$img_copy\_$num\_small.jpg"){copy("$dirs_catalog/$img_copy\_$num\_small.jpg", "$dirs_catalog/$img\_$num\_small.jpg");}
			if(-e "$dirs_catalog/$img_copy\_$num\_normal.jpg"){copy("$dirs_catalog/$img_copy\_$num\_normal.jpg", "$dirs_catalog/$img\_$num\_normal.jpg");}
			if(-e "$dirs_catalog/$img_copy\_$num\_big.jpg"){copy("$dirs_catalog/$img_copy\_$num\_big.jpg", "$dirs_catalog/$img\_$num\_big.jpg");}
		}
		
		$db->update("UPDATE cat_product_rel SET `p_pos`='".$p_pos."' WHERE cat_p_id='".$p_id."' AND cat_id='".$cat_id."' AND cat_main ='1'");
		
		my $num="";
		my $result = $db->query("SELECT p.*, pl.p_pos, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_id."' ORDER BY pl.p_pos ASC");
		foreach my $item(@$result){
			$num++;
			$db->update("UPDATE cat_product_rel SET `p_pos`='".$num."' WHERE cat_p_id='".$item->{p_id}."' AND p_pos = '".$item->{p_pos}."' AND cat_id='".$cat_id."'");
		}
		
	print $p_id;
}

if ($reviews_raiting ne "" && $reviews_raiting_id ne ""){

	my $p_id = $reviews_raiting_id;
	my $name = $reviews_raiting_name;
	my $text = $reviews_raiting_text;
	my $raiting_all = $reviews_raiting; my $count=1;
	my $result = $db->query("SELECT cat_product_raiting.r_raiting FROM cat_product_raiting WHERE p_id ='".$p_id."'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'r_raiting'};
		$count++;
	}	
	my $result = $db->query("SELECT cat_product_reviews.v_raiting FROM cat_product_reviews WHERE p_id ='".$p_id."' AND v_public = '1'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'v_raiting'};
		$count++;
	}
	$raiting_all = $raiting_all/$count;
	$raiting_all = sprintf("%.1f",$raiting_all);
	
	$db->update("UPDATE cat_product SET `p_raiting`='".$raiting_all."' WHERE p_id='".$p_id."'");
	$db->update("UPDATE cat_product SET `p_raiting_count`='".$count."' WHERE p_id='".$p_id."'");
	
	use Encode "from_to";
	from_to($name, "utf-8", "cp1251");
	from_to($text, "utf-8", "cp1251");
	$text =~ s/</&lt;/g;
	$text =~ s/>/&gt;/g;
	$text =~ s/\n/\<br>/g;
	$text =~ s/\'/\\'/g;
	
	my $new_id="";
	my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'cat_product_reviews';");
	foreach my $item(@$result){	
		$new_id = $item->{Auto_increment};	
	}	

	$db->insert("INSERT INTO `cat_product_reviews` (`p_id`, `v_raiting`, `v_name`, `v_text`, `v_user_id`, `v_user_ip`, `v_public`, `v_date`) VALUES('".$p_id."', '".$reviews_raiting."', '".$name."', '".$text."', NULL, '".$ENV{'REMOTE_ADDR'}."', '1', '".$today_sql."')");
	
	print $new_id;
}

if ($reviews_public_id ne ""){

	my $p_id=""; my $raiting="";
	my $res_raiting = $db->query("SELECT cat_product_reviews.p_id, cat_product_reviews.v_raiting FROM cat_product_reviews WHERE v_id ='".$reviews_public_id."'");
	foreach my $line(@$res_raiting){
		$p_id = $line->{'p_id'};
		$raiting = $line->{'v_raiting'};
	}	
	my $raiting_all = $raiting; my $count=1;
	my $result = $db->query("SELECT cat_product_raiting.r_raiting FROM cat_product_raiting WHERE p_id ='".$p_id."'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'r_raiting'};
		$count++;
	}	
	my $result = $db->query("SELECT cat_product_reviews.v_raiting FROM cat_product_reviews WHERE p_id ='".$p_id."' AND v_public = '1'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'v_raiting'};
		$count++;
	}
	$raiting_all = $raiting_all/$count;
	$raiting_all = sprintf("%.1f",$raiting_all);
	
	$db->update("UPDATE cat_product_reviews SET `v_public`='1' WHERE v_id='".$reviews_public_id."'");
	$db->update("UPDATE cat_product SET `p_raiting`='".$raiting_all."' WHERE p_id='".$p_id."'");
	$db->update("UPDATE cat_product SET `p_raiting_count`='".$count."' WHERE p_id='".$p_id."'");	
}

if ($reviews_edit_id ne "" && $reviews_edit_text ne ""){

	my $id = $reviews_edit_id;
	my $text = $reviews_edit_text;
	use Encode "from_to";
	from_to($text, "utf-8", "cp1251");
	$text =~ s/\n/\<br>/g;
	$text =~ s/\'/\\'/g;

	$db->update("UPDATE cat_product_reviews SET `v_text`='".$text."' WHERE v_id='".$id."'");
}

if ($reviews_delete_id ne ""){

	my $p_id="";
	my $res_raiting = $db->query("SELECT cat_product_reviews.p_id FROM cat_product_reviews WHERE v_id ='".$reviews_delete_id."'");
	foreach my $line(@$res_raiting){
		$p_id = $line->{'p_id'};
		$db->delete("DELETE FROM cat_product_reviews WHERE v_id = '".$reviews_delete_id."' AND p_id = '".$p_id."' LIMIT 1");
	}
	my $raiting_all=""; my $count="";
	my $result = $db->query("SELECT cat_product_raiting.r_raiting FROM cat_product_raiting WHERE p_id ='".$p_id."'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'r_raiting'};
		$count++;
	}	
	my $result = $db->query("SELECT cat_product_reviews.v_raiting FROM cat_product_reviews WHERE p_id ='".$p_id."' AND v_public = '1'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'v_raiting'};
		$count++;
	}
	$raiting_all = $raiting_all/$count;
	$raiting_all = sprintf("%.1f",$raiting_all);
	
	$db->update("UPDATE cat_product SET `p_raiting`='".$raiting_all."' WHERE p_id='".$p_id."'");
	$db->update("UPDATE cat_product SET `p_raiting_count`='".$count."' WHERE p_id='".$p_id."'");	
}

if ($image_effects ne "" && $type_foto ne ""){

	my $num_edit = $foto_id;
	my $type = $type_foto;
	my $hdr = $param_hdr;
	$hdr_image = $hdr;
	if ($hdr_image eq "OFF"){$hdr_image = 0;}
	else {$hdr_image =~ s/\%//g;}
	my $saturation_ok = $param_saturation;
	from_to($saturation_ok, "utf-8", "cp1251");
	if ($saturation_ok eq "OFF"){$saturation_ok = 0;}
	elsif ($saturation_ok eq "Ч/Б"){$saturation_ok = -100;}
	else {$saturation_ok =~ s/\+//g;}	
	my $contrast_ok = $param_contrast;
	if ($contrast_ok eq "OFF"){$contrast_ok = 0;}
	else {$contrast_ok =~ s/\+//g;}
	my $normalize = $param_normalize;
	if ($normalize eq "1") {$normalize="on";} else {$normalize="";}
	my $sharpness = $param_sharpness;
	if ($sharpness eq "1") {$sharpness="on";} else {$sharpness="";}
	
	my $hdr = $hdr_image/100;
	if ($hdr > 1){$hdr = $hdr*1.25;}
	my $hdr_set1 = 0.75*$hdr;
	my $hdr_set1_2 = 0;
	my $hdr_set2 = 0.85*$hdr;
	my $hdr_set2_2 = 50;
	my $hdr_set3 = 1.25*$hdr;
	my $hdr_set3_2 = 75;
	my $hdr_set4 = 1.35*$hdr;
	my $hdr_set4_2 = 100;

	my $saturation_set = $saturation_ok+100;
	my $contrast_set = ($contrast_ok/10)*1.5;	
	
	my $result = $db->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1;");
	foreach my $item(@$result){	
		$my = $item->{p_id};
		if ($max_num < $my) {$max_num=$my;}
		$name_file_max=$my+1000;			
	}

	if ($num_edit != "empty") {$max_num=$num_edit; $name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$max_num="1"; $name_file_max="1001"} else {$max_num++; $name_file_max++;}}	
	
	if ($type eq "big" && $image_effects ne "no_upload"){
		use LWP::Simple;
		my $img = get($image_effects);
		open (FH, ">$dirs_catalog/$name_file_max\_big.jpg"); binmode FH;
		print FH $img; close FH;
		open (FH2, ">$dirs_catalog/$name_file_max\_normal.jpg"); binmode FH2;
		print FH2 $img; close FH2;		
	}
	elsif ($type eq "small" && $image_effects ne "no_upload"){
		use LWP::Simple;
		my $img = get($image_effects);
		open (FH, ">$dirs_catalog/$name_file_max\_small.jpg"); binmode FH;
		print FH $img; close FH;		
	}
	
	require "mod_resize_image.cgi";

	if ($type eq "big"){
		my $ext = "big";
		effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
		my $ext = "normal";
		effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
	}
	elsif ($type eq "small"){
		my $ext = "small";
		effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
		%configconsts = (
			'img_preview' => [128,106],
		);		
		resize_preview($ext, $name_file_max);
		my $ext = "preview";
		effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
	}	
	
	if ($type eq "big"){print '<img class="paste" data-url="'.$dirs_catalog_www.'/'.$name_file_max.'_big.jpg" style="max-height:240px; max-width:220px;" src="'.$dirs_catalog_www.'/'.$name_file_max.'_normal.jpg?'.$rand_num.'"><a size_foto="big" id_del="'.$name_file_max.'" class="del_foto" href="#" style="opacity: 0.67;"></a>';}
	elsif ($type eq "small"){print '<img class="paste" data-url="'.$dirs_catalog_www.'/'.$name_file_max.'_small.jpg?'.$rand_num.'" style="max-height:200px; max-width:220px;" src="'.$dirs_catalog_www.'/'.$name_file_max.'_small.jpg?'.$rand_num.'"><a size_foto="small" id_del="'.$name_file_max.'" class="del_foto" href="#" style="opacity: 0.67;"></a>';}

}

if ($imgCrop ne "" && $type_foto ne "" && $cropImgX1 ne "" && $cropImgY1 ne "" && $imgCropW ne "" && $imgCropH ne "" && $CropImgWidth ne "" && $CropImgHeight ne ""){

	my $num_edit = $foto_id;
	my $type = $type_foto;

	my $result = $db->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1;");
	foreach my $item(@$result){	
		$my = $item->{p_id};
		if ($max_num < $my) {$max_num=$my;}
		$name_file_max=$my+1000;			
	}

	if ($num_edit != "empty") {$max_num=$num_edit; $name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$max_num="1"; $name_file_max="1001"} else {$max_num++; $name_file_max++;}}
	
	if ($type eq "big"){
		use LWP::Simple;
		my $img = get($imgCrop);
		open (FH, ">$dirs_catalog/$name_file_max\_temp.jpg"); binmode FH;
		print FH $img; close FH;
	}
	elsif ($type eq "small"){
		use LWP::Simple;
		my $img = get($imgCrop);
		open (FH, ">$dirs_catalog/$name_file_max\_temp.jpg"); binmode FH;
		print FH $img; close FH;		
	}
	elsif ($type eq "lite"){
		use LWP::Simple;
		my $img = get($imgCrop);
		open (FH, ">$dirs_catalog/$name_file_max\_$num_id\_temp.jpg"); binmode FH;
		print FH $img; close FH;
	}
	
	my $size=""; my $ext=""; my $size_x=""; my $size_y="";
	if ($type eq "big"){$size = 'style="max-width:220px; max-height:240px;"'; $ext = "normal"; $size_x = $param_big_x; $size_y = $param_big_y;}
	elsif ($type eq "small"){$size = 'style="max-width:220px; max-height:200px;"'; $ext = "small"; $size_x = $param_sm_x; $size_y = $param_sm_y;}
	elsif ($type eq "lite"){$size = 'style="max-width:114px; max-height:90px;"'; $ext = "$num_id\_lite"; $size_x = $param_lite_x; $size_y = $param_lite_y;}

	use Image::Magick;
	
	if ($type eq "big"){
	
		if ($hide_products_zoom eq "1"){$zoom_x = 600; $zoom_y = 600;}
		else {$zoom_x = 960; $zoom_y = 1200;}
		
		my %configconsts = (
			'img_big' => [$zoom_x,$zoom_y]
		);
		
		my $image = Image::Magick->new;

		$image->Read("$dirs_catalog/$name_file_max\_temp.jpg");
		my ($ox,$oy) = $image->Get('base-columns','base-rows'); 

		my $size_ox = $ox;
		my $size_oy = $oy;
		
		if ($configconsts{'img_big'}[0] < $size_ox or $configconsts{'img_big'}[1] < $size_oy) {

			if($ox > $oy or $size_ox > $configconsts{'img_big'}[0])
			{
				my $delta = $ox/$configconsts{'img_big'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_big'}[0];
				
				if ($ny > $configconsts{'img_big'}[1]){
					my $delta = $oy/$configconsts{'img_big'}[1];
					$nx = int($ox/$delta);
					$ny = $configconsts{'img_big'}[1];	
				}					
					
			} else {				
				my $delta = $oy/$configconsts{'img_big'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_big'}[1];						
			}
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			$image->Write("$dirs_catalog/$name_file_max\_big.jpg");
		
		} else {					
			$image->Write("$dirs_catalog/$name_file_max\_big.jpg");
		}	
	}

	my $image = Image::Magick->new;
	$image->Read("$dirs_catalog/$name_file_max\_temp.jpg");
	my ($ox,$oy) = $image->Get('base-columns','base-rows');
	my $ratio = $ox/$CropImgWidth;

	$image->Crop(geometry=>''.($imgCropW*$ratio).'x'.($imgCropH*$ratio).'+'.($cropImgX1*$ratio).'+'.($cropImgY1*$ratio).'');
	$image->Resize(geometry=>geometry, width=>$size_x, height=>$size_y);
	$image->Write("$dirs_catalog/$name_file_max\_$ext.jpg");
	
	if ($type eq "small"){
		%configconsts = (
			'img_preview' => [128,106],
		);	
		require "../modules/mod_resize_image.cgi";
		resize_preview($ext, $name_file_max);
	}	
	unlink ("$dirs_catalog/$name_file_max\_temp.jpg");
	
	$rand_num=rand(1);
	print '<img '.$size.' class="cropping" '.($type eq "big"?'data-url="'.$dirs_catalog_www.'/'.$name_file_max.'_big.jpg"':'').' src="'.$dirs_catalog_www.'/'.$name_file_max.'_'.$ext.'.jpg?'.$rand_num.'" alt=""><a class="del_foto" href="#" style="opacity: 0.67;"></a>';
	
}

if ($img_url ne "" && $type_foto ne "" && $foto_id ne "" or $type_foto eq "test_image"){

	use Encode "from_to";
	my $num_edit = $foto_id;
	my $type = $type_foto;
	my $url = $img_url;	
	my $big_x = $param_big_x;
	my $big_y = $param_big_y;
	my $sm_x = $param_sm_x;
	my $sm_y = $param_sm_y;
	my $lite_x = $param_lite_x;
	my $lite_y = $param_lite_y;	
	my $hdr = $param_hdr;
	$hdr_image = $hdr;
	if ($hdr_image eq "OFF"){$hdr_image = 0;}
	else {$hdr_image =~ s/\%//g;}
	my $saturation_ok = $param_saturation;
	from_to($saturation_ok, "utf-8", "cp1251");
	if ($saturation_ok eq "OFF"){$saturation_ok = 0;}
	elsif ($saturation_ok eq "Ч/Б"){$saturation_ok = -100;}
	else {$saturation_ok =~ s/\+//g;}	
	my $contrast_ok = $param_contrast;
	if ($contrast_ok eq "OFF"){$contrast_ok = 0;}
	else {$contrast_ok =~ s/\+//g;}
	my $normalize = $param_normalize;
	if ($normalize eq "1") {$normalize="on";} else {$normalize="";}
	my $sharpness = $param_sharpness;
	if ($sharpness eq "1") {$sharpness="on";} else {$sharpness="";}
	my $auto_resize = $param_resize;
	my $type_resize = $param_type_resize;	
	
	my $hdr = $hdr_image/100;
	if ($hdr > 1){$hdr = $hdr*1.25;}
	my $hdr_set1 = 0.75*$hdr;
	my $hdr_set1_2 = 0;
	my $hdr_set2 = 0.85*$hdr;
	my $hdr_set2_2 = 50;
	my $hdr_set3 = 1.25*$hdr;
	my $hdr_set3_2 = 75;
	my $hdr_set4 = 1.35*$hdr;
	my $hdr_set4_2 = 100;

	my $saturation_set = $saturation_ok+100;
	my $contrast_set = ($contrast_ok/10)*1.5;	
	
	if ($hide_products_zoom eq "1"){$zoom_x = 600; $zoom_y = 600;}
	else {$zoom_x = 960; $zoom_y = 1200;}	
	
	use Image::Magick;
	
	if ($url ne "" && $type ne "test_image"){
		$url =~ s/\s+//g;
		$url =~ s/(.*)http/http/g;
		my $image = Image::Magick->new;
		my ($width, $height, $size, $format) = $image->Ping($url);	
		
		if ($format ne ""){
		
			my $result = $db->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1;");
			foreach my $item(@$result){	
				$my = $item->{p_id};
				if ($max_num < $my) {$max_num=$my;}
				$name_file_max=$my+1000;			
			}

			if ($num_edit != "empty") {$max_num=$num_edit; $name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$max_num="1"; $name_file_max="1001"} else {$max_num++; $name_file_max++;}}	
			
			if ($type eq "big"){
				use LWP::Simple;
				my $img = get($url);
				open (FH, ">$dirs_catalog/$name_file_max\_temp.jpg"); binmode FH;
				print FH $img; close FH;	
			}
			elsif ($type eq "small"){
				use LWP::Simple;
				my $img = get($url);
				open (FH, ">$dirs_catalog/$name_file_max\_temp.jpg"); binmode FH;
				print FH $img; close FH;	
			}
			elsif ($type eq "lite"){
				use LWP::Simple;
				my $img = get($url);
				open (FH, ">$dirs_catalog/$name_file_max\_$num_id\_temp.jpg"); binmode FH;
				print FH $img; close FH;	
			}	
		
			%configconsts = (
				'img_small' => [$sm_x,$sm_y],
				'img_normal' => [$big_x,$big_y],				
				'img_big' => [$zoom_x,$zoom_y],
				'img_preview' => [128,106],
				'img_lite' => [$lite_x,$lite_y],				
			);
			
			require "mod_resize_image.cgi";
			
			my $ext = "temp";
			
			if ($type eq "big"){
				
				if ($auto_resize){
					resize_big($ext, $name_file_max);
					unlink ("$dirs_catalog/$name_file_max\_$ext.jpg");
				}
				else {
					rename "$dirs_catalog/$name_file_max\_$ext.jpg", "$dirs_catalog/$name_file_max\_big.jpg";
					use File::Copy;
					copy("$dirs_catalog/$name_file_max\_big.jpg", "$dirs_catalog/$name_file_max\_normal.jpg");					
				}
			}
			elsif ($type eq "small"){

				if ($auto_resize){
					resize_small($ext, $name_file_max, $type_resize);
					resize_preview($ext, $name_file_max);
					unlink ("$dirs_catalog/$name_file_max\_$ext.jpg");
				}
				else {
					rename "$dirs_catalog/$name_file_max\_$ext.jpg", "$dirs_catalog/$name_file_max\_small.jpg";
					use File::Copy;
					copy("$dirs_catalog/$name_file_max\_small.jpg", "$dirs_catalog/$name_file_max\_preview.jpg");
				}
			}
			elsif ($type eq "lite"){
			
				if ($hide_products_watermark ne "1"){
					open(BO, "$dirs_catalog/watermark.txt"); my @categories = <BO>; close(BO);
					foreach my $linee(@categories)
						{
					chomp($linee);
					my ($watermark_pos_, $watermark_op_, $watermark_big_, $watermark_normal_, $watermark_small_, $watermark_text_, $watermark_size_, $watermark_color_) = split(/\|/, $linee);
					$watermark_pos=qq~$watermark_pos_~;
					$watermark_op=qq~$watermark_op_~;
					$watermark_big=qq~$watermark_big_~;
					$watermark_normal=qq~$watermark_normal_~;
					$watermark_small=qq~$watermark_small_~;
					$watermark_text=qq~$watermark_text_~;
					$watermark_size=qq~$watermark_size_~;
					$watermark_color=qq~$watermark_color_~;
						}
				}			

				resize_lite($num_id, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
			}
		
			$rand_num=rand(1);
					
			if ($type eq "big"){print '<img class="paste" data-url="'.$dirs_catalog_www.'/'.$name_file_max.'_big.jpg" style="max-height:240px; max-width:220px;" src="'.$dirs_catalog_www.'/'.$name_file_max.'_normal.jpg?'.$rand_num.'"><a size_foto="big" id_del="'.$name_file_max.'" class="del_foto" href="#" style="opacity: 0.67;"></a>';}
			elsif ($type eq "small"){print '<img class="paste" data-url="'.$dirs_catalog_www.'/'.$name_file_max.'_small.jpg?'.$rand_num.'" style="max-height:200px; max-width:220px;" src="'.$dirs_catalog_www.'/'.$name_file_max.'_small.jpg?'.$rand_num.'"><a size_foto="small" id_del="'.$name_file_max.'" class="del_foto" href="#" style="opacity: 0.67;"></a>';}
			elsif ($type eq "lite"){print '<a class="highslide" href="'.$dirs_catalog_www.'/'.$name_file_max.'_'.$num_id.'_big.jpg?'.$rand_num.'" title="Увеличить" onclick="return hs.expand(this)"><img style="max-height:90px; max-width:114px;" src="'.$dirs_catalog_www.'/'.$name_file_max.'_'.$num_id.'_small.jpg?'.$rand_num.'"></a><a href="#" size_foto="lite" id_foto="'.$num_id.'" id_del="'.$name_file_max.'" class="del_photo"></a>';}
			
		}
		else {
			print "error";
		}		
	}
	elsif ($type eq "test_image"){
	
		%configconsts = (
			'img_small' => [176,176],
			'img_normal' => [220,240],
			'img_big' => [960,600],
			'img_preview' => [128,106],
			'img_lite' => [100,84],
		);
		
		require "mod_resize_image.cgi";	
	
		if ($test_image ne ""){
			use LWP::Simple;
			my $img = get($test_image);
			open (FH, ">$dirs_catalog/test_temp.jpg"); binmode FH;
			print FH $img; close FH;
			open (FH, ">$dirs_catalog/test_org_temp.jpg"); binmode FH;
			print FH $img; close FH;
		}
		else {
			use File::Copy;
			copy("$dirs_catalog/../../admin/scripts/hdr/img/test.jpg", "$dirs_catalog/test_temp.jpg");
		}
		
		my $ext = "temp";
		
		resize_big($ext, "test");
		resize_small($ext, "test", "full");
		effects_image("normal", "test", $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
		effects_image("big", "test", $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);		
		effects_image("small", "test", $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);		
		
		$rand_num=rand(1);
		if ($test_image ne ""){
			resize_small($ext, "test_org", "full");
			print '<a class="highslide img1" onclick="return hs.expand(this)" href="'.$dirs_catalog_www.'/test_org_temp.jpg?'.$rand_num.'"><img src="'.$dirs_catalog_www.'/test_org_small.jpg?'.$rand_num.'"></a>';
		}
		else {
			print '<a class="highslide img1" onclick="return hs.expand(this)" href="/admin/scripts/hdr/img/test.jpg?'.$rand_num.'"><img style="width:152px; height:152px;" class="test" src="/admin/scripts/hdr/img/test.jpg?'.$rand_num.'"></a>';	
		}
		
		print '<a class="highslide img2" onclick="return hs.expand(this)" href="'.$dirs_catalog_www.'/test_big.jpg?'.$rand_num.'"><img '.($test_image_drop eq ""?'class="test" style="width:152px; height:152px;"':'').' src="'.$dirs_catalog_www.'/test_small.jpg?'.$rand_num.'"></a>';
		
		if ($test_image_drop ne ""){
			print '<a href="#" title="Применить настройки изображения" class="apply" data-type="'.$test_image_drop.'">Применить</a>';
		}
		
	}
	
}	

if ($product_hits eq "true"){

	my $result, $product_hit, $product_spec, $product_new;
	
	my $rand_num=rand(1);
	my $res = $db->query("SELECT p.p_show, p.p_img_url, p.p_art, pl.* FROM cat_product AS p JOIN cat_product_hits AS pl ON(pl.p_ids=p.p_id) ORDER BY pl.hit_id ASC, pl.p_pos ASC");
	foreach my $line(@$res){
		my $p_id = $line->{p_ids};
		my $img_id = $p_id+1000;
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}
		
		$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$res->[0]->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.3"').' alt=""></div>';
		
		if ($line->{hit_id} eq "1"){
			$product_spec .='<li data-id="'.$p_id.'">'.$img_sm.'<a href="#" class="del_p"></a></li>';
		}
		elsif ($line->{hit_id} eq "2"){
			$product_new .='<li data-id="'.$p_id.'">'.$img_sm.'<a href="#" class="del_p"></a></li>';
		}
		elsif ($line->{hit_id} eq "3"){
			$product_hit .='<li data-id="'.$p_id.'">'.$img_sm.'<a href="#" class="del_p"></a></li>';
		}		
	}

	$result .='
			<div class="products_hits products_select">';
	if ($hide_products_spec ne "1"){
		$result .='
				<h3>Спецпредложение</h3>
				<div class="products_select_wrapper">
					<div class="container">
						<ul data-param="1">
							'.$product_spec.'
							<li class="add"><div class="foto"><span><em>Добавить товары</em></span></div></li>
						</ul>
						
					</div>
					<div class="add_product"><p>Перетащите товары<br> в эту область</p></div>
				</div>
				<div class="clear"></div>';
	}
	if ($hide_products_new ne "1"){
		$result .='
				<h3>Новые поступления</h3>
				<div class="products_select_wrapper">
					<div class="container">
						<ul data-param="2">
							'.$product_new.'
							<li class="add"><div class="foto"><span><em>Добавить товары</em></span></div></li>
						</ul>
					</div>
					<div class="add_product"><p>Перетащите товары<br> в эту область</p></div>
				</div>
				<div class="clear"></div>';
	}
	if ($hide_products_hit ne "1"){
		$result .='
				<h3>Хиты продаж</h3>
				<div class="products_select_wrapper">
					<div class="container">
						<ul data-param="3">
							'.$product_hit.'
							<li class="add"><div class="foto"><span><em>Добавить товары</em></span></div></li>
						</ul>
					</div>
					<div class="add_product"><p>Перетащите товары<br> в эту область</p></div>
				</div>
				<div class="clear"></div>';
	}	
	$result .='
			</div>';
			
	print '<div id="allProducts">'.$result.'<ul id="product_foto"></ul></div>';
}

sub stemmer {
	my $query = shift;
	if ($query){
		my @words = split / /, $query;
		my $result="";
		foreach my $item(@words){
			$result .= stem_word($item)." ";
		}
		$result =~s/\s$//g;
		$result =~s/\s/\%/gi;
		return $result;
	}
}
