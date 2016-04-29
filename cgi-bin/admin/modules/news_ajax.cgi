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
ClearCache("../..");

$news_lamp=param('news_lamp');
$news_del=param('news_del');
$ajax_news_id=param('ajax_news_id');
$ajax_img_url=param('ajax_img_url');
$ajax_img_ox=param('ajax_img_ox');
$ajax_img_oy=param('ajax_img_oy');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();


if ($news_lamp) {

	my $id = $news_lamp;
	my $res = $db->query("SELECT * FROM news WHERE id = '".$id."' LIMIT 1");
	
	foreach my $line(@$res){
		$show = $line->{show};

	}

	if ($show eq "0") {
		$db->update("UPDATE news SET `show`='1' WHERE id='".$id."'");
		print "1";
	}
	elsif ($show eq "1") {
		$db->update("UPDATE news SET `show`='0' WHERE id='".$id."'");
		print "0";
	}
	
}


if ($news_del) {

	my $id = $news_del;
	$db->delete("DELETE FROM news WHERE id = '".$id."'");
	unlink ("$dirs_news/$id\.jpg");
}


if ($ajax_news_id ne "" && $ajax_img_url ne "" && $ajax_img_ox ne "" && $ajax_img_oy ne ""){

	my $num_edit = $ajax_news_id;
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
	
		my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'news';");
		foreach my $item(@$result){	
			$max_num = $item->{Auto_increment};
			$name_file_max = $max_num+1000;			
		}

		if ($num_edit != "empty") {$name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$name_file_max="1001"}}

		use LWP::Simple;
		my $img = get($url);
		open (FH, ">$dirs_news/$name_file_max\.jpg"); binmode FH;
		print FH $img; close FH;
	
		%configconsts = (
			'img_resize' => [$img_ox,$img_oy]	
		);
		$image->Read("$dirs_news/$name_file_max\.jpg"); 
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
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
			$image->Write("$dirs_news/$name_file_max\.jpg");
		}
		else {
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
			$image->Write("$dirs_news/$name_file_max\.jpg");
		}
		
		$rand_num=rand(1);

		print '<img border="0" style="max-height:150px; max-width:220px;" src="'.$dirs_news_www.'/'.$name_file_max.'.jpg?'.$rand_num.'">';
	}		
	else {
		print "error";
	}
}
