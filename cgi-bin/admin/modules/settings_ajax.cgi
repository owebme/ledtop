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

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";
require "../engine/lib/Cache/ClearCache.cgi";

$select_main_page=param('select_main_page');
$social=param('social');
$social_app=param('social_app');
$add_slide_id=param('add_slide_id');
$add_slide_ox=param('add_slide_ox');
$add_slide_oy=param('add_slide_oy');
$add_slide=param('add_slide');
$del_slide=param('del_slide');

print header(-type => 'text/html', -charset => 'windows-1251'); 

my $db = new Core::DB();

if ($select_main_page) {

	my $sel_option =""; my $sel_option_pages =""; my $sel_option_category ="";
	if (-e "../modules/news.cgi"){$sel_option .="<option value='/cgi-bin/news.cgi'>Раздел «Новости»</option>";}
	if (-e "../modules/articles.cgi"){$sel_option .="<option value='/cgi-bin/articles.cgi'>Раздел «Статьи»</option>";}
	if (-e "../modules/fotolist.cgi"){$sel_option .="<option value='/cgi-bin/gallery.cgi'>Раздел «Фотогелерея»</option>";}
	if (-e "../modules/category.cgi"){
		$sel_option .="<option value='/cgi-bin/catalog.cgi?alias=cat_list'>Раздел «Каталог»</option>";
		$sel_option .="<option value='/cgi-bin/catalog.cgi?alias=all'>Раздел «Все товары»</option>";
	}
	my $result = $db->query("SELECT * FROM strukture WHERE parent = '0' ORDER BY pos ASC");
	foreach my $item(@$result){
		if ($item->{show} eq "1"){
			if ($current_id == $item->{id} or $item->{mirror_link} ne "" or $item->{mirror_id} eq "#!") {$sel_option_pages .='';}
			else {$sel_option_pages .= '<option value="/cgi-bin/index.cgi?num_edit='.$item->{id}.'">'.$item->{name}.'</option>';}
			if (my $sub = recMenuPages($item->{id}, 0) ){
				$sel_option_pages .= $sub;
			}
		}
	}
	sub recMenuPages {
		my $id = shift;
		my $level = shift;
		sub nbsp_page { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
		my $result = $db->query("SELECT * FROM strukture WHERE parent='".$id."' ORDER BY pos ASC"); 
		if ($result){
			foreach my $item(@$result){
				if ($item->{show} eq "1"){
					if ($current_id == $item->{id} or $item->{mirror_link} ne "" or $item->{mirror_id} eq "#!") {$sel_option_pages .='';}
					else {$sel_option_pages .= '<option value="/cgi-bin/index.cgi?num_edit='.$item->{id}.'">'.nbsp_page($level).$item->{name}.'</option>';}			
					if (my $sub = recMenuPages($item->{id}, $level+1)){
						$sel_option_pages .= $sub;
					}
				}
			}
		}
		else {
			return 0;
		}
	}
	
	my $result = $db->query("SELECT * FROM cat_category WHERE c_pid = '0' ORDER BY c_pos ASC");
	foreach my $item(@$result){
		if ($item->{c_show} eq "1"){
			$sel_option_category .= '<option value="/cgi-bin/catalog.cgi?num_edit='.$item->{c_id}.'">'.$item->{c_name}.'</option>';
			if (my $sub = recMenuCategory($item->{c_id}, 0) ){
				$sel_option_category .= $sub;
			}
		}
	}
	sub recMenuCategory {
		my $id = shift;
		my $level = shift;
		sub nbsp_cat { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
		my $result = $db->query("SELECT * FROM cat_category WHERE c_pid = '".$id."' ORDER BY c_pos ASC");
		if ($result){
			foreach my $item(@$result){
				if ($item->{c_show} eq "1"){
					$sel_option_category .= '<option value="/cgi-bin/catalog.cgi?num_edit='.$item->{c_id}.'">'.nbsp_cat($level).$item->{c_name}.'</option>';
					if (my $sub = recMenuCategory($item->{c_id}, $level+1)){
						$sel_option_category .= $sub;
					}	
				}
			}
		}
		else {
			return 0;
		}
	}	
	
	if ($sel_option_pages ne ""){$sel_option .= "<option class='disabled' disabled>Страницы сайта</option>".$sel_option_pages;}
	if ($sel_option_category ne ""){$sel_option .= "<option class='disabled' disabled>Категории каталога</option>".$sel_option_category;}
	
	if ($sel_option ne ""){
		print $sel_option = '<select class="category" name="main_page">'.$sel_option.'</select>';	
	}
}

if ($social eq "create" or $social eq "remove"){

	use LWP::UserAgent;
	open OUT, ("../engine/lib/set_social"); @set_social = <OUT>;
	foreach my $text(@set_social) {$params_social=qq~$params_social$text~;}
	my $ua = LWP::UserAgent->new;
	$ua->timeout(10);
	my $response="";
	if ($social eq "create"){
		my $res = $ua->get(''.$admin_host.'/auth/index.php?domen='.$ENV{"HTTP_HOST"}.'&auth-create='.$social_app.'&ip_address='.$ip.'');
		if ($res->is_success && $res->content eq "ok"){
			$response = $ua->get(''.$admin_host.'/auth/button.php?domen='.$ENV{"HTTP_HOST"}.'&set_social='.$params_social.'&social_app='.$social_app.'&ip_address='.$ip.'');
		}
	}
	elsif ($social eq "remove"){
		$response = $ua->get(''.$admin_host.'/auth/button.php?domen='.$ENV{"HTTP_HOST"}.'&set_social='.$params_social.'&set_button_clear='.$social_app.'&ip_address='.$ip.'');
	}
	if ($response->is_success){
		if ($response->content ne ""){
			open OUT, (">../engine/lib/set_social");	   
				print OUT $response->content; 	   
			close(OUT);
			print "ok";
		}
	}
}

if ($add_slide ne "" && $add_slide_id ne ""){

	my $num = $add_slide_id;
	my $img_ox = $add_slide_ox;
	my $img_oy = $add_slide_oy;
	if ($img_ox eq ""){$img_ox = 750;}
	if ($img_oy eq ""){$img_oy = 388;}
	
	use LWP::Simple;
	my $img = get($add_slide);
	open (FH, ">$dirs_slides/slide$num\.jpg"); binmode FH;
	print FH $img; close FH;
	
	use Image::Magick;
	
	my $image = Image::Magick->new;
	my ($width, $height, $size, $format) = $image->Ping("$dirs_slides/slide$num\.jpg");	
	if ($format ne ""){
	
		%configconsts = (
			'img_resize' => [$img_ox,$img_oy]	
		);
		$image->Read("$dirs_slides/slide$num\.jpg"); 
		($ox,$oy)=$image->Get('base-columns','base-rows'); 				

		my $size_ox = $ox;
		my $size_oy = $oy;
		
		my $division = $configconsts{'img_resize'}[0]/$configconsts{'img_resize'}[1];
		if ($configconsts{'img_resize'}[0] < $size_ox or $configconsts{'img_resize'}[1] < $size_oy) {

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
			$image->Write("$dirs_slides/slide$num\.jpg");
		}
		else {
			$image->Write("$dirs_slides/slide$num\.jpg");
		}
		
		$rand_num=rand(1);

		print '<img src="'.$dirs_slides_www.'/slide'.$num.'.jpg?'.$rand_num.'">';
	}
	ClearCache("../..");
}

if ($del_slide ne "") {

	my $num = $del_slide;
	unlink ("$dirs_slides/slide$num\.jpg");
	
	ClearCache("../..");
}
