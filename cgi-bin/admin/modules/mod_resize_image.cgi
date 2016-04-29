
	sub resize_preview {
	
		my $ext = shift;
		my $num_img = shift;

		my $img_preview = Image::Magick->new;
		$img_preview->Read("$dirs_catalog/$num_img\_$ext\.jpg"); 
		($ox,$oy)=$img_preview->Get('base-columns','base-rows'); 

			if($ox < $oy or $ox == $oy)
			{
				my $delta = $oy/$configconsts{'img_preview'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_preview'}[1];
					
			} else {
				
				my $delta = $ox/$configconsts{'img_preview'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_preview'}[0];
			}
			$img_preview->Resize(geometry=>geometry, width=>$nx, height=>$ny);
			$img_preview->Write("$dirs_catalog/$num_img\_preview.jpg");
	}
	
	sub resize_big {
	
		my $ext = shift;
		my $num_img = shift;
	
		my $image = Image::Magick->new;

		$image->Read("$dirs_catalog/$num_img\_$ext\.jpg"); 
		my ($ox,$oy)=$image->Get('base-columns','base-rows'); 

		my $size_ox = $ox;
		my $size_oy = $oy;
		
		if ($configconsts{'img_normal'}[0] < $size_ox or $configconsts{'img_normal'}[1] < $size_oy) {

			if($ox > $oy or $size_ox > $configconsts{'img_normal'}[0])
			{
				my $delta = $ox/$configconsts{'img_normal'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_normal'}[0];
				
				if ($ny > $configconsts{'img_normal'}[1]){
					my $delta = $oy/$configconsts{'img_normal'}[1];
					$nx = int($ox/$delta);
					$ny = $configconsts{'img_normal'}[1];	
				}						
					
			} else {
				
				my $delta = $oy/$configconsts{'img_normal'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_normal'}[1];						
			}
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			$image->Write("$dirs_catalog/$num_img\_normal.jpg");
			if ($hide_products_watermark ne "1" && $watermark_normal eq "1"){
				watermark("$dirs_catalog/$num_img\_normal.jpg", "normal", $nx, $ny);
			}			
		
		} else {
			
			$image->Write("$dirs_catalog/$num_img\_normal.jpg");
			if ($hide_products_watermark ne "1" && $watermark_normal eq "1"){
				watermark("$dirs_catalog/$num_img\_normal.jpg", "normal", $ox, $oy);
			}			
		}			
	
		my $image = Image::Magick->new;

		$image->Read("$dirs_catalog/$num_img\_$ext\.jpg"); 
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
			$image->Write("$dirs_catalog/$num_img\_big.jpg");
			if ($hide_products_watermark ne "1" && $watermark_big eq "1"){
				watermark("$dirs_catalog/$num_img\_big.jpg", "big", $nx, $ny);
			}
			
		} else {
		
			$image->Write("$dirs_catalog/$num_img\_big.jpg");
			if ($hide_products_watermark ne "1" && $watermark_big eq "1"){
				watermark("$dirs_catalog/$num_img\_big.jpg", "big", $ox, $oy);
			}
		}			
	}
	
	sub resize_small {
	
		my $ext = shift;
		my $num_img = shift;
		my $type_resize = shift;
	
		my $image = Image::Magick->new;
		$image->Read("$dirs_catalog/$num_img\_$ext\.jpg");
		my ($ox, $oy) = $image->Get('base-columns','base-rows');
	
		if ($type_resize eq "half") {

			if($ox < $oy or $ox == $oy)
			{
				my $delta = $oy/$configconsts{'img_small'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_small'}[1];
					
			} else {
				
				my $delta = $ox/$configconsts{'img_small'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_small'}[0];
			}
			
			if ($nx > $configconsts{'img_small'}[0]){
				my $delta = $ox/$configconsts{'img_small'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_small'}[0];	
			}
			if ($ny > $configconsts{'img_small'}[1]){
				my $delta = $oy/$configconsts{'img_small'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_small'}[1];	
			}					

			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			$image->Write("$dirs_catalog/$num_img\_small.jpg");
			if ($hide_products_watermark ne "1" && $watermark_small eq "1"){
				watermark("$dirs_catalog/$num_img\_small.jpg", "small", $nx, $ny);
			}			
			
		} else {
		
			$sizesm = $ox*$oy;
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
				$image->Write("$dirs_catalog/$num_img\_small.jpg");
				if ($hide_products_watermark ne "1" && $watermark_small eq "1"){
					watermark("$dirs_catalog/$num_img\_small.jpg", "small", $nx, $ny);
				}					

			} else {
	
				$image->Write("$dirs_catalog/$num_img\_small.jpg");
				if ($hide_products_watermark ne "1" && $watermark_small eq "1"){
					watermark("$dirs_catalog/$num_img\_small.jpg", "small", $ox, $oy);
				}					
			}
			
		}
	}
	
	sub resize_lite {
		
		my $num = shift;
		my $num_img = shift;
		my $hdr = shift;
		my $hdr_set1 = shift;
		my $hdr_set1_2 = shift;
		my $hdr_set2 = shift;
		my $hdr_set2_2 = shift;
		my $hdr_set3 = shift;
		my $hdr_set3_2 = shift;
		my $hdr_set4 = shift;
		my $hdr_set4_2 = shift;
		my $normalize = shift;
		my $contrast_set = shift;
		my $saturation_set = shift;
		my $sharpness = shift;
		if ($saturation_set eq ""){$saturation_set = 100;}		
	
		my $image = Image::Magick->new;

		$image->Read("$dirs_catalog/$num_img\_$num\_temp.jpg"); 
		my ($ox,$oy)=$image->Get('base-columns','base-rows'); 

		my $size_ox = $ox;
		my $size_oy = $oy;
		
		if ($configconsts{'img_normal'}[0] < $size_ox or $configconsts{'img_normal'}[1] < $size_oy) {

			if($ox > $oy or $size_ox > $configconsts{'img_normal'}[0])
			{
				my $delta = $ox/$configconsts{'img_normal'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_normal'}[0];
				
				if ($ny > $configconsts{'img_normal'}[1]){
					my $delta = $oy/$configconsts{'img_normal'}[1];
					$nx = int($ox/$delta);
					$ny = $configconsts{'img_normal'}[1];	
				}						
					
			} else {
				
				my $delta = $oy/$configconsts{'img_normal'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_normal'}[1];						
			}
			if($hdr > 0){
				$image->Normalize();
				$image->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
				$image->AutoLevel(channel=>All);
			}
			else {
				if($normalize eq "on") {$image->Normalize();}
				if($contrast_set > 0) {$image->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
			}	
			if ($saturation_set > 100 or $saturation_set < 100){$image->Modulate(saturation=>$saturation_set);}
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			if ($sharpness eq "on"){$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);}
			$image->Write("$dirs_catalog/$num_img\_$num\_normal.jpg");
			if ($hide_products_watermark ne "1" && $watermark_normal eq "1"){
				watermark("$dirs_catalog/$num_img\_$num\_normal.jpg", "normal", $nx, $ny);
			}			
		
		} else {
		
			if($hdr > 0){
				$image->Normalize();
				$image->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
				$image->AutoLevel(channel=>All);
			}
			else {
				if($normalize eq "on") {$image->Normalize();}
				if($contrast_set > 0) {$image->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
			}
			if ($saturation_set > 100 or $saturation_set < 100){$image->Modulate(saturation=>$saturation_set);}
			if ($sharpness eq "on"){$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);}					
			$image->Write("$dirs_catalog/$num_img\_$num\_normal.jpg");
			if ($hide_products_watermark ne "1" && $watermark_normal eq "1"){
				watermark("$dirs_catalog/$num_img\_$num\_normal.jpg", "normal", $ox, $oy);
			}			
		}			

		my $image = Image::Magick->new;

		$image->Read("$dirs_catalog/$num_img\_$num\_temp.jpg"); 
		my ($ox,$oy)=$image->Get('base-columns','base-rows'); 

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
			if($hdr > 0){
				$image->Normalize();
				$image->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
				$image->AutoLevel(channel=>All);
			}
			else {
				if($normalize eq "on") {$image->Normalize();}
				if($contrast_set > 0) {$image->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
			}
			if ($saturation_set > 100 or $saturation_set < 100){$image->Modulate(saturation=>$saturation_set);}
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			if ($sharpness eq "on"){$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);}
			$image->Write("$dirs_catalog/$num_img\_$num\_big.jpg");
			if ($hide_products_watermark ne "1" && $watermark_big eq "1"){
				watermark("$dirs_catalog/$num_img\_$num\_big.jpg", "big", $nx, $ny);
			}			
		
		} else {
		
			if($hdr > 0){
				$image->Normalize();
				$image->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
				$image->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
				$image->AutoLevel(channel=>All);
			}
			else {
				if($normalize eq "on") {$image->Normalize();}
				if($contrast_set > 0) {$image->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
			}
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);					
			$image->Write("$dirs_catalog/$num_img\_$num\_big.jpg");
			if ($hide_products_watermark ne "1" && $watermark_big eq "1"){
				watermark("$dirs_catalog/$num_img\_$num\_big.jpg", "big", $ox, $oy);
			}			
		}
		
		my $ox_lite=""; my $oy_lite="";
		if ($resize_more_photo_smart eq "1"){
			if(-e "$dirs_catalog/$num_img\_1_small.jpg"){
				my $image = Image::Magick->new;
				$image->Read("$dirs_catalog/$num_img\_1_small.jpg"); 
				($ox_lite,$oy_lite)=$image->Get('base-columns','base-rows');
			}
			elsif (-e "$dirs_catalog/$num_img\_2_small.jpg"){
				my $image = Image::Magick->new;
				$image->Read("$dirs_catalog/$num_img\_2_small.jpg"); 
				($ox_lite,$oy_lite)=$image->Get('base-columns','base-rows');
			}
			elsif (-e "$dirs_catalog/$num_img\_3_small.jpg"){
				my $image = Image::Magick->new;
				$image->Read("$dirs_catalog/$num_img\_3_small.jpg"); 
				($ox_lite,$oy_lite)=$image->Get('base-columns','base-rows');
			}
		}

		if ($ox_lite ne "" && $oy_lite ne "" or $resize_more_photo_smart eq "0"){
		
			my %configconsts = (
				'img_small' => [$configconsts{'img_lite'}[0],$configconsts{'img_lite'}[1]]
			);
			if ($resize_more_photo_smart eq "1"){
				%configconsts = (
					'img_small' => [$ox_lite,$oy_lite]
				);			
			}
		
			my $img_lite = Image::Magick->new;
			$img_lite->Read("$dirs_catalog/$num_img\_$num\_temp.jpg"); 
			($ox,$oy)=$img_lite->Get('base-columns','base-rows'); 				
		
			$division = $configconsts{'img_small'}[0]/$configconsts{'img_small'}[1];
			
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
			
			if($hdr > 0){
				$img_lite->Normalize();
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
				$img_lite->AutoLevel(channel=>All);
			}
			else {
				if($normalize eq "on") {$img_lite->Normalize();}
				if($contrast_set > 0) {$img_lite->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
			}						
			if ($saturation_set > 100 or $saturation_set < 100){$img_lite->Modulate(saturation=>$saturation_set);}
			$img_lite->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			$img_lite->Crop(x=>$cropx, y=>$cropy);
			$img_lite->Crop($configconsts{'img_small'}[0], $configconsts{'img_small'}[1]);
			if ($sharpness eq "on"){$img_lite->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);}
			$img_lite->Write("$dirs_catalog/$num_img\_$num\_small.jpg");
			if ($hide_products_watermark ne "1" && $watermark_small eq "1"){
				watermark("$dirs_catalog/$num_img\_$num\_small.jpg", "small", $nx, $ny);
			}			
		}
		else {
		
			my $img_lite = Image::Magick->new;
			$img_lite->Read("$dirs_catalog/$num_img\_$num\_temp.jpg"); 
			($ox,$oy)=$img_lite->Get('base-columns','base-rows'); 

			if($ox > $oy or $ox == $oy or $ox > $configconsts{'img_lite'}[0])
			{
				my $delta = $ox/$configconsts{'img_lite'}[0];
				$ny = int($oy/$delta);
				$nx = $configconsts{'img_lite'}[0];					
					
			} else {
			
				my $delta = $oy/$configconsts{'img_lite'}[1];
				$nx = int($ox/$delta);
				$ny = $configconsts{'img_lite'}[1];
				
			}
			if($hdr > 0){
				$img_lite->Normalize();
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
				$img_lite->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
				$img_lite->AutoLevel(channel=>All);
			}
			else {
				if($normalize eq "on") {$img_lite->Normalize();}
				if($contrast_set > 0) {$img_lite->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
			}	
			if ($saturation_set > 100 or $saturation_set < 100){$img_lite->Modulate(saturation=>$saturation_set);}
			$img_lite->Resize(geometry=>geometry, width=>$nx, height=>$ny);
			if ($sharpness eq "on"){$img_lite->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);}
			$img_lite->Write("$dirs_catalog/$num_img\_$num\_small.jpg");
			if ($hide_products_watermark ne "1" && $watermark_small eq "1"){
				watermark("$dirs_catalog/$num_img\_$num\_small.jpg", "small", $nx, $ny);
			}			
		}	
			unlink ("$dirs_catalog/$num_img\_$num\_temp.jpg");
	}
	
	sub effects_image {
	
		my $ext = shift;
		my $num_img = shift;
		my $hdr = shift;
		my $hdr_set1 = shift;
		my $hdr_set1_2 = shift;
		my $hdr_set2 = shift;
		my $hdr_set2_2 = shift;
		my $hdr_set3 = shift;
		my $hdr_set3_2 = shift;
		my $hdr_set4 = shift;
		my $hdr_set4_2 = shift;
		my $normalize = shift;
		my $contrast_set = shift;
		my $saturation_set = shift;
		my $sharpness = shift;
		if ($saturation_set eq ""){$saturation_set = 100;}
	
		my $image = Image::Magick->new;

		$image->Read("$dirs_catalog/$num_img\_$ext\.jpg"); 
		my ($ox,$oy)=$image->Get('base-columns','base-rows');
		
		if($hdr > 0){
			$image->Normalize();
			$image->SigmoidalContrast('contrast'=>$hdr_set1, 'mid-point'=>$hdr_set1_2, sharpen=>True);
			$image->SigmoidalContrast('contrast'=>$hdr_set2, 'mid-point'=>$hdr_set2_2, sharpen=>True);
			$image->SigmoidalContrast('contrast'=>$hdr_set3, 'mid-point'=>$hdr_set3_2, sharpen=>True);
			$image->SigmoidalContrast('contrast'=>$hdr_set4, 'mid-point'=>$hdr_set4_2, sharpen=>True);
			$image->AutoLevel(channel=>All);				
		}
		else {
			if($normalize eq "on") {$image->Normalize();}
			if($contrast_set > 0) {$image->SigmoidalContrast('contrast'=>$contrast_set, 'mid-point'=>100, sharpen=>True);}
		}
		if ($saturation_set > 100 or $saturation_set < 100){$image->Modulate(saturation=>$saturation_set);}
		if ($sharpness eq "on"){$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);}
		$image->Write("$dirs_catalog/$num_img\_$ext\.jpg"); 
	}	
	
	sub watermark {
		my $file = shift;
		my $type = shift;
		my $width = shift;
		my $height = shift;
		if (-e "$dirs_catalog/watermark.png"){
			my $left=0; my $top=0; my $gravity="";
			if ($watermark_pos eq "top-left"){$gravity = "NorthWest";}
			elsif ($watermark_pos eq "top-right"){$gravity = "NorthEast";}
			elsif ($watermark_pos eq "center"){$gravity = "Center"; $top = 20;}
			elsif ($watermark_pos eq "bottom-right"){$gravity = "SouthEast";}
			elsif ($watermark_pos eq "bottom-left"){$gravity = "SouthWest";}
			my $image=Image::Magick->new;
			my $x = $image->Read($file);
			my $layer = Image::Magick->new;
			$layer->Read("$dirs_catalog/watermark.png");
			my ($ox,$oy)=$layer->Get('base-columns','base-rows');
			if ($width < $ox){
				my $delta = $ox/$width;
				$ny = int($oy/$delta);
				$nx = $width;
				$layer->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			}
			$x = $image->Composite(image=>$layer, gravity=>$gravity, x=>$left, y=>$top, opacity=>$watermark_op."%"); 
			$x = $image->Write($file);	
		}
	}
1;			