#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}
use Fcntl;                                   # O_EXCL, O_CREAT и O_WRONLY

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);          # вывод ошибок к browser-у 
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;
use File::Copy;	
use Core::DB;
use Core::Config;

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";
require "../engine/lib/Cache/ClearCache.cgi";

$rand_num=rand(1);

$add_img_id=param('add_img_id');
$add_img_p_id=param('add_img_p_id');
$add_image=param('add_image');
$add_images_strip=param('add_images_strip');
$yaimages_alias_big=param('yaimages_alias_big');
$yaimages_alias_reserve=param('yaimages_alias_reserve');
$yaimages_alias_small=param('yaimages_alias_small');
$del_field=param('del_field');
$add_products_data=param('add_products_data');
$add_products_cat_id=param('add_products_cat_id');
$search_word=param('search_word');
$search_page=param('search_page');

print header(-type => 'text/html', -charset => 'windows-1251');

	my $db = new Core::DB();

	open(BO, "$dirs_catalog/settings.txt"); my @categories = <BO>; close(BO);
	foreach my $linee(@categories)
		{
	chomp($linee);
	my ($big_x1, $big_y1, $sm_x1, $sm_y1, $lite_x1, $lite_y1, $check, $hdr_, $type, $load, $normalize_, $contrast_, $saturation_, $sharpness_) = split(/\|/, $linee);
	$big_x=qq~$big_x1~;
	$big_y=qq~$big_y1~;
	$sm_x=qq~$sm_x1~;
	$sm_y=qq~$sm_y1~;
	$lite_x=qq~$lite_x1~;
	$lite_y=qq~$lite_y1~;		
	$auto_small=qq~$check~;
	$hdr=qq~$hdr_~;		
	$type_resize_ok=qq~$type~;
	$ok_auto_load=qq~$load~;
	$normalize=qq~$normalize_~;
	$contrast_ok=qq~$contrast_~;
	$saturation_ok=qq~$saturation_~;
	$sharpness=qq~$sharpness_~;
		}		
	
	$hdr_image = $hdr;
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

	%configconsts = (
		'img_small' => [$sm_x,$sm_y],
		'img_normal' => [$big_x,$big_y],				
		'img_big' => [$zoom_x,$zoom_y],
		'img_preview' => [128,106],
		'img_lite' => [$lite_x,$lite_y],				
	);		
	
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
	
	require "mod_resize_image.cgi";

if ($yaimages_alias_big ne "" or $yaimages_alias_reserve ne "" or $yaimages_alias_small ne ""){
	
	my $num = $add_img_id;
	my $p_alias="";
	
	if ($add_img_p_id > 0){	
		$num = $add_img_p_id;		
		if ($resize_photo_single){
			my $res = $db->query("SELECT cat_product.p_art FROM cat_product WHERE p_id = '".$add_img_p_id."'");
			$p_alias = $res->[0]->{p_art};		
		}
		else {
			$p_alias = $add_img_p_id+1000;
		}
	}
	if ($num ne ""){
		use Image::Magick;
		my $alias=""; my $error=""; my $error_big=""; my $image=""; my $width=""; my $height=""; my $size=""; my $format="";
		if ($yaimages_alias_big ne ""){
			#my $ua = LWP::UserAgent->new();
			#$ua->requests_redirectable(undef);
			#my $response = $ua->get($yaimages_alias_big);
			#$response->code =~ /^404$/		
			my $img = Image::Magick->new;
			($width, $height, $size, $format) = $img->Ping($yaimages_alias_big);
			if ($format ne ""){
				use LWP::Simple;
				my $img = get($yaimages_alias_big);
				my $path_small=""; my $path_big="";
				if ($add_img_p_id > 0){
					my $path = $p_alias."_temp";
					$path_small = $p_alias."_small";
					$path_big = $p_alias."_big";
					if ($resize_photo_single){
						$path_small = $path_big = $p_alias;
					}
					open (FH, ">$dirs_catalog/$path\.jpg"); binmode FH;
					print FH $img; close FH;
					if(-e "$dirs_catalog/$path\.jpg"){
						my $ext = "temp";
						saveImage($ext, $p_alias, $type_resize_ok, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
						unlink ("$dirs_catalog/$p_alias\_temp.jpg");
					}			
				}
				else {
					$path_small = "multi/".$num;
					$path_big = "multi/".$num;
					open (FH, ">$dirs_catalog/multi/$num\.jpg"); binmode FH;
					print FH $img; close FH;			
				}				
				$image = '<img src="'.$dirs_catalog_www.'/'.$path_small.'.jpg?'.$rand_num.'" style="height:52px;" alt=""><div class="size"><a class="highslide" onclick="return hs.expand(this)" href="'.$dirs_catalog_www.'/'.$path_big.'.jpg?'.$rand_num.'">'.($width > 0 && $height > 0?''.$width.' x '.$height.'':'не определено').'</a>'.($width < 250 && $width > 0?'<p class="red">(изображение малого размера)</p>':'').'</div>';
			} else {$error = "1"; $error_big = "1";}
		}
		if ($yaimages_alias_reserve ne "" && $error_big eq "1"){
			my $img = Image::Magick->new;
			($width, $height, $size, $format) = $img->Ping($yaimages_alias_reserve);	
			if ($format ne ""){
				use LWP::Simple;
				my $img = get($yaimages_alias_reserve);
				my $path_small=""; my $path_big="";
				if ($add_img_p_id > 0){
					my $path = $p_alias."_temp";
					$path_small = $p_alias."_small";
					$path_big = $p_alias."_big";	
					if ($resize_photo_single){
						$path_small = $path_big = $p_alias;
					}					
					open (FH, ">$dirs_catalog/$path\.jpg"); binmode FH;
					print FH $img; close FH;
					if(-e "$dirs_catalog/$path\.jpg"){
						my $ext = "temp";
						saveImage($ext, $p_alias, $type_resize_ok, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
						unlink ("$dirs_catalog/$p_alias\_temp.jpg");
					}			
				}
				else {
					$path_small = "multi/".$num;
					$path_big = "multi/".$num;
					open (FH, ">$dirs_catalog/multi/$num\.jpg"); binmode FH;
					print FH $img; close FH;			
				}
				$image = '<img src="'.$dirs_catalog_www.'/multi/'.$num.'.jpg?'.$rand_num.'" style="height:52px;" alt=""><div class="size"><a class="highslide" onclick="return hs.expand(this)" href="'.$dirs_catalog_www.'/multi/'.$num.'.jpg?'.$rand_num.'">'.($width > 0 && $height > 0?''.$width.' x '.$height.'':'не определено').'</a>'.($width < 250 && $width > 0?'<p class="red">(изображение малого размера)</p>':'').'</div>';
			} else {$error = "1";}
		}
		if ($yaimages_alias_small ne "" && $error_big eq "1"){
			my $img = Image::Magick->new;
			my ($width_sm, $height_sm, $size, $format) = $img->Ping($yaimages_alias_small);
			if ($width_sm > $width && $height_sm > $height){
				use LWP::Simple;
				my $img = get($yaimages_alias_small);
				my $path_small=""; my $path_big="";
				if ($add_img_p_id > 0){
					my $path = $p_alias."_temp";
					$path_small = $p_alias."_small";
					$path_big = $p_alias."_big";
					if ($resize_photo_single){
						$path_small = $path_big = $p_alias;
					}					
					open (FH, ">$dirs_catalog/$path\.jpg"); binmode FH;
					print FH $img; close FH;
					if(-e "$dirs_catalog/$path\.jpg"){
						my $ext = "temp";
						saveImage($ext, $p_alias, $type_resize_ok, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
						unlink ("$dirs_catalog/$p_alias\_temp.jpg");
					}			
				}
				else {
					$path_small = "multi/".$num;
					$path_big = "multi/".$num;
					open (FH, ">$dirs_catalog/multi/$num\.jpg"); binmode FH;
					print FH $img; close FH;			
				}				
				$image = '<img src="'.$dirs_catalog_www.'/'.$path_small.'.jpg?'.$rand_num.'" style="height:52px;" alt=""><div class="size"><a class="highslide" onclick="return hs.expand(this)" href="'.$dirs_catalog_www.'/'.$path_big.'.jpg?'.$rand_num.'">'.($width_sm > 0 && $height_sm > 0?''.$width_sm.' x '.$height_sm.'':'не определено').'</a>'.($width_sm < 250 && $width_sm > 0?'<p class="red">(изображение малого размера)</p>':'').'</div>';
			}
		}

		if ($image ne ""){
			print $image;
		}
		else {
			print "error";
		}
	}
}

if ($add_image ne "" && ($add_img_id ne "" or $add_img_p_id ne "") or $add_images_strip ne ""){
	
	my $image=""; my $p_alias="";
	
	if ($add_img_p_id > 0){
		if ($resize_photo_single){
			my $res = $db->query("SELECT cat_product.p_art FROM cat_product WHERE p_id = '".$add_img_p_id."'");
			$p_alias = $res->[0]->{p_art};		
		}
		else {
			$p_alias = $add_img_p_id+1000;
		}	
	}
	use LWP::Simple;
	if ($add_image ne ""){
		my $img = get($add_image);
		my $path_small=""; my $path_big="";
		if ($add_img_p_id > 0){
			my $path = $p_alias."_temp";
			$path_small = $p_alias."_small";
			$path_big = $p_alias."_big";
			if ($resize_photo_single){
				$path_small = $path_big = $p_alias;
			}
			open (FH, ">$dirs_catalog/$path\.jpg"); binmode FH;
			print FH $img; close FH;
			if(-e "$dirs_catalog/$path\.jpg"){
				my $ext = "temp";
				saveImage($ext, $p_alias, $type_resize_ok, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);	
				unlink ("$dirs_catalog/$p_alias\_temp.jpg");
			}			
		}
		else {
			$path_small = "multi/".$add_img_id;
			$path_big = "multi/".$add_img_id;
			open (FH, ">$dirs_catalog/multi/$add_img_id\.jpg"); binmode FH;
			print FH $img; close FH;			
		}
		my $img = Image::Magick->new;
		my ($width, $height, $size, $format) = $img->Ping("$dirs_catalog/$path_big\.jpg");	
		$image = '<img src="'.$dirs_catalog_www.'/'.$path_small.'.jpg?'.$rand_num.'" style="height:52px;" alt=""><div class="size"><a class="highslide" onclick="return hs.expand(this)" href="'.$dirs_catalog_www.'/'.$path_big.'.jpg?'.$rand_num.'">'.($width > 0 && $height > 0?''.$width.' x '.$height.'':'не определено').'</a>'.($width < 250 && $width > 0?'<p class="red">(изображение малого размера)</p>':'').'</div>';
	}
	elsif ($add_images_strip ne ""){
		my $num = $rand_num; $num =~s/^0\.//g;
		my $img = get($add_images_strip);
		open (FH, ">$dirs_catalog/multi/upload/$num\.jpg"); binmode FH;
		print FH $img; close FH;	
		$image = 'http://'.$ENV{"HTTP_HOST"}.''.$dirs_catalog_www.'/multi/upload/'.$num.'.jpg?'.$rand_num;
	}
	if ($image ne ""){print $image;}
	else {print "error";}
}

if ($del_field ne ""){
	my $num = $del_field;
	unlink ("$dirs_catalog/multi/$num\.jpg");
}

if ($search_word ne "" && $search_page ne ""){
	my $result="";
	use LWP::UserAgent;
	my $ua = LWP::UserAgent->new;
	$ua->timeout(5);
	my $server_search = $ua->get(''.$admin_host.'/yaimages/search/q='.$search_word.'&p='.$search_page.'&domen='.$ENV{"HTTP_HOST"}.'&ip_address='.$ip.'');
	if ($server_search->is_success){
		$result = $server_search->content;
	}
	print $result;
}

if ($add_products_data ne "" && $add_products_cat_id ne ""){
	my $cat_id = $add_products_cat_id;
	my $data = $add_products_data;
	use Encode "from_to";
	from_to($data, "utf-8", "cp1251");
	
	use Core::DB::Work;
	use Core::DB::Catalog;	

	my $products = new Core::DB::Catalog();
	
	my $p_maket="";
	my $result = $db->query("SELECT p.*, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_id."' AND pl.cat_main ='1' LIMIT 1");
	$p_maket = $result->[0]->{p_maket};

	while ($data =~ m/(.*?)\;\|\;/g) {
		my $value = $1;
		my ($num, $p_id, $art, $name, $desc, $price, $p_count) = split(/\;\;/, $value);
		$name = Core::DB::Work::trans_new($name);
		$desc =~ s/\|\_\|/\n/g;
		$desc = Core::DB::Work::trans_html($desc);
		$price =~ s/\s//g; $price =~ s/\,/\./g; $price =~ s/(\d+)/$1/g;
		my $new_id=""; my $p_alias="";
		if ($name ne ""){
			if ($p_id > 0){
				my $res = $db->query("SELECT cat_product.p_alias FROM cat_product WHERE p_id = '".$p_id."'");
				$p_alias = $res->[0]->{p_alias};	
			}
			else {
				my $res = $db->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1");
				$new_id = $res->[0]->{p_id}+1;
				$p_alias=Core::DB::Work::translit($name);
			}
			if ($new_id > 0){$p_id = $new_id;}
			my %params = (
						'p_id' => $p_id,
						'p_name' => $name,
						'p_desc_sm' => $desc,
						'p_price' => $price,
						'p_art' => $art,					
						'p_show' => "1",
						'p_show_head' => "1",
						'p_alias' => $p_alias,
						'p_maket' => $p_maket				
			);
			if ($p_count ne ""){
				%params = (%params,
					'p_count' => $p_count
				);
			}
			
			if (!$new_id){
				$products->editProduct($p_id, \%params);
			}
			else {
				my %params_rel = (
							'p_pos' => "",
							'cat_p_id' => $p_id,
							'cat_main' => "1",	
							'cat_id' => $cat_id
				);
				$products->addProduct(\%params);
				$products->addProductRel(\%params_rel);	

				if(-e "$dirs_catalog/multi/$num\.jpg"){
					if ($art){$p_alias = $art;}
					copy("$dirs_catalog/multi/$num\.jpg", "$dirs_catalog/$p_alias\_temp.jpg");
					my $ext = "temp";
					saveImage($ext, $p_alias, $type_resize_ok, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
					unlink ("$dirs_catalog/$p_alias\_temp.jpg");
					unlink ("$dirs_catalog/multi/$num\.jpg");
				}
			}
		}
	}
	
	print "ok";
	
	ClearCache("../..");
}

sub saveImage($$) {
	my ($ext, $p_alias, $type_resize_ok, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness) = @_;
	resize_big($ext, $p_alias);
	resize_small($ext, $p_alias, $type_resize_ok);
	resize_preview($ext, $p_alias);
	effects_image("big", $p_alias, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
	effects_image("normal", $p_alias, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
	effects_image("small", $p_alias, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
	effects_image("preview", $p_alias, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
	if ($resize_photo_single){
		rename "$dirs_catalog/$p_alias\_normal.jpg", "$dirs_catalog/$p_alias\.jpg";
		unlink ("$dirs_catalog/$p_alias\_big.jpg");
		unlink ("$dirs_catalog/$p_alias\_small.jpg");
		unlink ("$dirs_catalog/$p_alias\_preview.jpg");		
	}
}

-1;