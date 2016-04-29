
# Название и титл фотогалереи

if ($page_alias) {
$name=qq~<h1><a class="cat_name" href="/gallery/">$name_fotogal_old</a> - $name_gallery</h1>~;
open OUT, ("admin/$dirs/meta_title"); $title_site = <OUT>; close(OUT);
$title ="$name_gallery // $title_site";
} else {
$name=qq~<h1>$name_fotogal_old</h1>~;
open OUT, ("admin/$dirs/meta_title"); $title_site = <OUT>; close(OUT);
$title ="$name_fotogal_old // $title_site";
}


# Скрипт фотогалереи

my $class="";
if ($script_type eq "highslide"){
	$script_gallery ="
	<script type='text/javascript' src='/js/highslide/highslide-with-gallery.js'></script>
	<link rel='stylesheet' type='text/css' href='/js/highslide/highslide.css' />
	<script type='text/javascript'>
		hs.graphicsDir = '/js/highslide/graphics/';
		hs.align = 'center';
		hs.transitions = ['expand', 'crossfade'];
		hs.outlineType = 'rounded-white';
		hs.fadeInOut = true;
		hs.numberPosition = 'caption';
		hs.dimmingOpacity = 0.75;

		// Add the controlbar
		if (hs.addSlideshow) hs.addSlideshow({
			//slideshowGroup: 'group1',
			interval: 2500,
			repeat: false,
			useControls: true,
			fixedControls: 'fit',
			overlayOptions: {
				opacity: .75,
				position: 'bottom center',
				hideOnMouseOut: true
			}
		});

	</script>";
	
	$class='class="highslide" onclick="return hs.expand(this)"';
}
elsif ($script_type eq "fresco"){
	$script_gallery ='
	<script type="text/javascript" src="/js/fresco/fresco.js"></script>
	<link rel="stylesheet" type="text/css" href="/js/fresco/css/style.css" />';
	
	$class='class="fresco" data-fresco-group="gallery"';	
}
elsif ($script_type eq "kaleidoscope"){
	$script_gallery ='
	<script type="text/javascript" src="/js/jSbox/jSboxKaleidoscope/jquery.jSboxKaleidoscope.js"></script>
	<link rel="stylesheet" type="text/css" href="/js/jSbox/jSboxKaleidoscope/style.css" />';
	
	$class='class="js-kaleidoscope"';	
}
elsif ($script_type eq "photoswipe"){
	$script_gallery ='
	<script type="text/javascript" src="/js/photoswipe/klass.min.js"></script>
	<script type="text/javascript" src="/js/photoswipe/photoswipe.jquery-3.0.5.min.js"></script>
	<link rel="stylesheet" type="text/css" href="/js/photoswipe/photoswipe.css" />
	<script type="text/javascript">
	(function(window, $, PhotoSwipe){
		$(function(){
			var options = {};
			$(".photoswipe").photoSwipe(options);
		});
	}(window, window.jQuery, window.Code.PhotoSwipe));
	</script>';
	
	$class='class="photoswipe"';	
}
if ($script_type eq "jsbox" or $ENV{"REQUEST_URI"} =~ m/jSbox$/){
	$script_gallery ='
	<script type="text/javascript" src="/js/jSbox/jSboxGallery/jquery.jSboxGallery.js"></script>
	<link rel="stylesheet" href="/js/jSbox/jSboxGallery/style.css" />
	<!--[if lt IE 8]>
		<link rel="stylesheet" href="/js/jSbox/jSboxGallery/style.ie.css" />
	<![endif]-->
	<script type="text/javascript">
	$(function(){
		$().jSboxGallery({
			shadowImg: true,
			innerShadow: true,
			socialButton: true
		});	
	});	
	</script>';
	
	$class='class="jSbox-gallery"';	
}

if ($gallery_type ne "0"){
$script_gallery .="
<link rel='stylesheet' type='text/css' href='/admin/site/css/gallery/gallery_type".$gallery_type.".css' />";
}

use Image::Magick;

# Вывод конкретной фотогалереи

if ($page_alias) {

	$gallery = gallery_photo($page_alias, $gallery_type, $script_type);		
}

# Вывод всех фотогалерей		

else {

	my $photo="";
	my $photo_list="";
	$gallery_count="";
	open OUT, ("$dirs_foto_www2/pos_album.txt"); $pos_gallery = <OUT>; 
	while ($pos_gallery =~ s/(\d+)//)
	{
		open(BO, "$dirs_foto_www2/fotogal.$1"); @b = <BO>; close (BO);
		($name_gallery, $date_gallery, $show_gallery) = split(/\|/, $b[0]);	
		if ($show_gallery eq "on") {$gallery_list .='<li><a href="/gallery/'.$1.'/">'.$name_gallery.'</a></li>'; $g_show=$1; $gallery_count++;}
		else {$gallery_list .='';}
	}
	
	
	# Если фотогалерея не одна, выводим их
	
	if ($gallery_count > 1) {

		# Если параметр выводить фотографии одним список отключен	
		
		if ($gallery_photo_all ne "all") {$gallery = '<ul class="gallery_name">'.$gallery_list.'</ul>';}
		
		
		# Если параметр выводить фотографии одним список включен
		
		else {
		
			my $photo="";
			my $photo_list="";
			my $num="";
			opendir (DBDIR, "$dirs_foto_www2"); @list_dir = readdir(DBDIR); close DBDIR;
			foreach $line_wall(@list_dir) {
				chomp ($line_wall);
				if ($line_wall ne "." && $line_wall ne "..") {
					($name_file, $num_gallery) = split(/\./, $line_wall);

					if ($name_file eq "fotogal") { 
					opendir (DBDIR, "$dirs_foto_www2/$num_gallery"); @list_dir2 = readdir(DBDIR); close DBDIR;
					@list_dir2=reverse sort (@list_dir2);

					foreach $line_wall2(@list_dir2) {
						chomp ($line_wall2);
						if ($line_wall2 ne "." && $line_wall2 ne "..") {
						($name_file, $exec) = split(/\./, $line_wall2);
						($name_file_s, $nax) = split(/\_/, $name_file);		
						
						if ($nax eq "text") {
						$num++;
						open OUT, ("$dirs_foto_www2/$num_gallery/$name_file_s\_texb.txt"); $imagetext_bg = <OUT>; close OUT;
						open OUT, ("$dirs_foto_www2/$num_gallery/$name_file_s\_text.txt"); $imagetext_sm = <OUT>; close OUT;				
						$random_n=rand(1);	
						
						if ($gallery_type eq "3"){
							my $image = Image::Magick->new;		
							$image->Read("$dirs_foto_www2/$num_gallery/$name_file_s\_small.jpg"); 
							($ox,$oy)=$image->Get('base-columns','base-rows');	
							$photo .="
							<style>
								ul.gallery li div[class*='id".$num."']:before, ul.gallery li div[class*='id".$num."']:after{
									width: ".$ox."px; height: ".$oy."px;
								}
							</style>";
						}
						my $file_size=""; my $mask="";
						if ($script_type eq "kaleidoscope"){
							my $img = Image::Magick->new;
							my ($width, $height, $size, $format) = $img->Ping("$dirs_foto_www2/$num_gallery/$name_file_s\_big.jpg");
							if ($format ne "" && $size > 0){
								if ($format eq "JPEG"){$format = "JPG";}
								$size = $size/1024;
								$size = sprintf("%.0f",$size); 
								$file_size = $format.', '.$size.'&nbsp;КБ';
							}
							$mask = '<div class="img-mask" style="width:'.$width.'px; height:'.$height.'px"></div>';
						}
						
						$photo .='<div class="foto f'.random_int(1, 2).' id'.$num.'"><a '.$class.' '.($script_type eq "fresco" && $imagetext_bg ne ""?'data-fresco-caption="'.$imagetext_bg.'"':'').' href="'.$dirs_foto_www.'/'.$num_gallery.'/'.$name_file_s.'_big.jpg?'.$random_n.'"><img src="'.$dirs_foto_www.'/'.$num_gallery.'/'.$name_file_s.'_small.jpg?'.$random_n.'" '.($script_type eq "photoswipe" && $imagetext_bg ne ""?'alt="'.$imagetext_bg.'"':'alt=""').'>'.($imagetext_sm eq ""?'':'<span class="captionframe"><span class="workcaption"><em>'.$imagetext_sm.'</em></span></span>').''.($script_type eq "kaleidoscope"?'<span class="pic_description">'.$imagetext_bg.'</span><span title="'.$dirs_foto_www.'/'.$num.'/'.$1.'_big.jpg?'.$random_n.'" class="source_img"><span class="img_source_lbl">Скачать фотографию</span><br><span class="file_size"><notypograf>'.$file_size.'</notypograf></span></span>':'').''.$mask.'</a>'.($script_type eq "highslide" && $imagetext_bg ne ""?'<div class="highslide-caption">'.$imagetext_bg.'</div>':'').'</div>';
						$photo_list .='<li>'.$photo.'</li>'; $photo="";
						}
					}
				}
			}
		}
			
		}

		$gallery = '<ul class="gallery type'.$gallery_type.'">'.$photo_list.'</ul>';

		}
	
	}
	
	# Если фотогалерея одна, выводим ее	
	
	else {
		
		$gallery = gallery_photo($g_show, $gallery_type, $script_type);

		open(BO, "$dirs_foto_www2/fotogal.$g_show"); @name_fotogal = <BO>; close(BO);
		foreach my $line(@name_fotogal)
			{
			chomp($line);
			my ($name_fotogal_, $date_fotogal) = split(/\|/, $line);
			$name_fotogal="$name_fotogal_";	
			}
			
		$title ="$name_fotogal // $title_site";
		$name=qq~<h1>$name_fotogal</h1>~;
	}

}

sub gallery_photo {

	my $num = shift;
	my $type = shift;
	my $script = shift;
	
	my $photo="";
	my $photo_list="";	
	my $count="";
	open OUT, ("$dirs_foto_www2/pos_list_$num.txt"); $pos_foto = <OUT>; 
	open OUT, ("$dirs_foto_www2/fotogal_html.$num"); @desc_gallery = <OUT>;
	foreach my $text(@desc_gallery) {$desc_gallery=qq~$desc_gallery$text~;}
	while ($pos_foto =~ s/(\d+)//)
	{
		$count++;
		open OUT, ("$dirs_foto_www2/$num/$1\_texb.txt"); $imagetext_bg = <OUT>; close OUT;
		open OUT, ("$dirs_foto_www2/$num/$1\_text.txt"); $imagetext_sm = <OUT>; close OUT;
		my $random_n=rand(1);
		
		if ($type eq "3"){
			my $image = Image::Magick->new;		
			$image->Read("$dirs_foto_www2/$num/$1\_small.jpg"); 
			my ($ox,$oy)=$image->Get('base-columns','base-rows');
			$photo .="
			<style>
				ul.gallery li div[class*='id".$count."']:before, ul.gallery li div[class*='id".$count."']:after{
					width: ".$ox."px; height: ".$oy."px;
				}
			</style>";
		}
		my $file_size=""; my $mask="";
		if ($script eq "kaleidoscope"){
			my $img = Image::Magick->new;
			my ($width, $height, $size, $format) = $img->Ping("$dirs_foto_www2/$num/$1\_big.jpg");
			if ($format ne "" && $size > 0){
				if ($format eq "JPEG"){$format = "JPG";}
				$size = $size/1024;
				$size = sprintf("%.0f",$size); 
				$file_size = $format.', '.$size.'&nbsp;КБ';
			}
			$mask = '<div class="img-mask" style="width:'.$width.'px; height:'.$height.'px"></div>';
		}

		$photo .='<div class="foto f'.random_int(1, 2).' id'.$count.'"><a '.$class.' '.($script eq "fresco" && $imagetext_bg ne ""?'data-fresco-caption="'.$imagetext_bg.'"':'').' href="'.$dirs_foto_www.'/'.$num.'/'.$1.'_big.jpg?'.$random_n.'"><img src="'.$dirs_foto_www.'/'.$num.'/'.$1.'_small.jpg?'.$random_n.'" '.($script eq "photoswipe" && $imagetext_bg ne ""?'alt="'.$imagetext_bg.'"':'alt=""').'>'.($imagetext_sm eq ""?'':'<span class="captionframe"><span class="workcaption"><em>'.$imagetext_sm.'</em></span></span>').''.($script eq "kaleidoscope"?'<span class="pic_description">'.$imagetext_bg.'</span><span title="'.$dirs_foto_www.'/'.$num.'/'.$1.'_big.jpg?'.$random_n.'" class="source_img"><span class="img_source_lbl">Скачать фотографию</span><br><span class="file_size"><notypograf>'.$file_size.'</notypograf></span></span>':'').''.$mask.'</a>'.($script eq "highslide" && $imagetext_bg ne ""?'<div class="highslide-caption">'.$imagetext_bg.'</div>':'').'</div>';

		$photo_list .='<li>'.$photo.'</li>'; $photo="";
	}
			
	$gallery = '<ul class="gallery type'.$type.'">'.$photo_list.'</ul><div style="clear:both;"></div>'.$desc_gallery.'';

	return $gallery;
}

sub random_int ($$) {
    my($min, $max) = @_;
    return $min if $min == $max;
    ($min, $max) = ($max, $min) if $min > $max;
    return $min + int rand(1 + $max - $min);
}

1;