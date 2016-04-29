
# Баннеры

sub build_Banner {
	
	my $name = shift;
	my $banner="";
	
	if (-e "$dirs_banners_www2/$name\.txt"){
		open OUT, ("$dirs_banners_www2/$name\.txt"); $banner_file = <OUT>; close(OUT);
		$banner = '<div id="'.$name.'"><img src="'.$dirs_banners_www.'/'.$banner_file.'" alt=""></div>';
	}
	else {
		if (-e "$dirs_banners_www2/$name\.html"){
			open OUT, ("$dirs_banners_www2/$name\.html"); @banner = <OUT>;
			foreach my $text(@banner) {$banner=qq~$banner$text~;}
		}
	}
	
	return $banner;
}

1;