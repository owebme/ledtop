
# Фотографии проектов (скроллер)

my $foto_limit = 20; # кол-во отображаемых

sub build_galleryLite {
	my $gallery="";
	my $num="";
	my $pos_gallery="";
	my $pos_foto="";
	my $photo_list="";	

	use Image::Magick;
	open OUT, ("$dirs_foto_www2/pos_album.txt"); $pos_gallery = <OUT>; 
	while ($pos_gallery =~ s/(\d+);//)
	{
		my $num_gallery = $1;
		$num++;
		if ($num > $foto_limit){last;}
		open OUT, ("$dirs_foto_www2/pos_list_$num_gallery\.txt"); $pos_foto = <OUT>; 
		while ($pos_foto =~ s/(\d+);//)
		{
			my $img = Image::Magick->new;
			my $num_foto = $1;
			my ($width, $height, $size, $format) = $img->Ping("$dirs_foto_www2/$num_gallery/$num_foto\_small.jpg");
			if ($width ne "" && $size ne "" && $format ne ""){
				open OUT, ("$dirs_foto_www2/$num_gallery/$num_foto\_text.txt"); $imagetext_sm = <OUT>; close OUT;
				my $random_n=rand(1);
				
				my $photo .='<li><a href="'.$dirs_foto_www.'/'.$num_gallery.'/'.$num_foto.'_big.jpg?'.$random_n.'" class="lightbox" rel="group"><img src="'.$dirs_foto_www.'/'.$num_gallery.'/'.$num_foto.'_small.jpg?'.$random_n.'" alt="'.$imagetext_sm.'"><i></i></a></li>';
				
				$photo_list .= $photo;
				last;
			}
		}
	}				
	if ($photo_list ne ""){
		$gallery='<div class="container load"><ul>'.$photo_list.'</ul></div><span class="arrow_right"></span>';		
	}
				
	return $gallery;
}

1;