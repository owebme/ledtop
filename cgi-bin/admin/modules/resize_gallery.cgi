#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB::Catalog;
use Core::DB::Work;
use Core::DB;
use Image::Magick;

require "../engine/lib/parametr.cgi";

print header(-charset=>'windows-1251');

%configconsts = (
	'img_small' => [100,84],
	'img_big' => [821,572]	
);		

my $folder = "lenta";

my $num = 1000; my $result = 1; my $counts="";
opendir (DBDIR, "foto/$folder"); @list_dir = readdir(DBDIR); close DBDIR;
foreach $line_wall(@list_dir) {
	chomp ($line_wall);
	if ($line_wall ne "." && $line_wall ne "..") {
		my ($name, $exec) = split(/\./, $line_wall);
		if ($name && $exec){
			if ($result){$num++;}
			my $file = $name.".".$exec;
			resize_big($num, $folder, $file);
			$result = resize_small($num, $folder, $file);
			if ($result){
				print $file."<br>";
				$counts++;
			}
		}
	}
}

if ($counts){
	print '<h3>Загружено: '.$counts.'</h3>';
}

	sub resize_big {
	
		my $num = shift;
		my $folder = shift;
		my $file = shift;
	
		my $image = Image::Magick->new;

		$image->Read("foto/$folder/$file");
		my ($ox,$oy) = $image->Get('base-columns','base-rows'); 

		my $size_ox = $ox;
		my $size_oy = $oy;
		
		if ($configconsts{'img_big'}[0] < $size_ox or $configconsts{'img_big'}[1] < $size_oy) {
		
			my $delta = $oy/$configconsts{'img_big'}[1];
			$nx = int($ox/$delta);
			$ny = $configconsts{'img_big'}[1];	
			
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);

			if ($nx > $configconsts{'img_big'}[0]){
				$cropy = 0;
				$cropx = int(($nx-$configconsts{'img_big'}[0])/2);
				$image->Crop(x=>$cropx, y=>$cropy);
				$image->Crop($configconsts{'img_big'}[0], $configconsts{'img_big'}[1]);
			}
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.5, amount=>1, threshold=>0);
			$image->Write("$dirs_catalog/$folder/$num\_big.jpg");
			
		} else {
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.5, amount=>1, threshold=>0);
			$image->Write("$dirs_catalog/$folder/$num\_big.jpg");
		}			
	}
	
	sub resize_small {
	
		my $num = shift;
		my $folder = shift;
		my $file = shift;
	
		my $image = Image::Magick->new;
		$image->Read("foto/$folder/$file");
		my ($ox, $oy) = $image->Get('base-columns','base-rows');

		my $sizesm = $ox*$oy;
		$division = $configconsts{'img_small'}[0]/$configconsts{'img_small'}[1];
		
		if (($configconsts{'img_small'}[0]*$configconsts{'img_small'}[1]) < $sizesm) {

			if(($ox/$oy)>$division)
			
				{$nx=int(($ox/$oy)*$configconsts{'img_small'}[1]);			
				$ny=$configconsts{'img_small'}[1];
				$cropx = int(($nx-$configconsts{'img_small'}[0])/2);
				$cropy = 0;
				
			} else {
			
				$ny=int(($oy/$ox)*$configconsts{'img_small'}[0]);	
				$nx=$configconsts{'img_small'}[0];
				$cropy = int(($ny-$configconsts{'img_small'}[1])/2);
				$cropx = 0;		
			}
			
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);						
			$image->Crop(x=>$cropx, y=>$cropy);
			$image->Crop($configconsts{'img_small'}[0], $configconsts{'img_small'}[1]);
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
			$image->Write("$dirs_catalog/$folder/$num\_small.jpg");

		} else {
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
			$image->Write("$dirs_catalog/$folder/$num\_small.jpg");
		}
		if (-e "$dirs_catalog/$folder/$num\_small.jpg"){
			return 1;
		}
	}

1;			