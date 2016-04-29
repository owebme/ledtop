
# ׁכאיהרמף

sub build_slideShow {

	my $slideshow=""; $rand_num=rand(1);
	opendir (DBDIR, $dirs_slides_www2); @list_dir = readdir(DBDIR); close DBDIR;
	@list_dir = sort(@list_dir);
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $exec) = split(/\./, $line_wall);
			if ($exec eq "jpg"){
				$slideshow .='<div class="unit" style="background:url('.$dirs_slides_www.'/'.$name_file.'.'.$exec.'?'.$rand_num.') center center no-repeat;"></div>';
			}
		}
	}
	if ($slideshow ne ""){
		$slideshow='<div id="slideshow">'.$slideshow.'</div>';
	}
				
	return $slideshow;
}

1;