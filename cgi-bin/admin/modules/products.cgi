use Core::DB::Catalog;
use Core::DB::Work;

my $products = new Core::DB::Catalog();
my $db = new Core::DB();

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
	$ok_ajax_save=qq~$ajax_save_old_~;
	$count_more =qq~$count_more_~;
	$product_desc_ext =qq~$pr_desc_ext_~;
	$content_wide =qq~$content_wide_~;
	$set_foto_hide =qq~$set_foto_hide_~;
	$img_ext_url =qq~$img_ext_url_~;}
	
	if ($ok_ajax_save == "0" or $ok_ajax_save == "") {$button_save = '<input type="submit" name="save" value="Сохранить" class="button save" />'; $check_ajax='';}
	else {$button_save = '<a class="ajaxSave" href="#">Сохранить</a>'; $check_ajax='checked';}	

	open(BO, "../$dirs/set_cat_select"); @cat_current = <BO>; close(BO);
	foreach my $line(@cat_current){chomp($line);
	my ($cat_current_, $curent_page_) = split(/\|/, $line);
		$cat_current=qq~$cat_current_~;
		$curent_page=qq~$curent_page_~;	
	}	
	if ($cat_current ne "") {
		if ($cat_current ne "all") {$cat_current = $cat_current; $view_all="";}
		else {$cat_current=""; $view_all="all";}
	}

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

#################################################

	open(BO, "$dirs_catalog/settings.txt"); my @categories = <BO>; close(BO);
		foreach my $linee(@categories)
			{
		chomp($linee);
		my ($big_x1, $big_y1, $sm_x1, $sm_y1, $lite_x1, $lite_y1, $check, $hdr, $type, $resize, $normalize, $contrast, $saturation, $sharpness) = split(/\|/, $linee);
		$big_x=qq~$big_x1~;
		$big_y=qq~$big_y1~;
		$sm_x=qq~$sm_x1~;
		$sm_y=qq~$sm_y1~;
		$lite_x=qq~$lite_x1~;
		$lite_y=qq~$lite_y1~;		
		$auto_small=qq~$check~;
		$ok_hdr_image=qq~$hdr~;		
		$ok_type_resize=qq~$type~;
		$ok_auto_resize=qq~$resize~;
		$ok_auto_normalize=qq~$normalize~;
		$ok_contrast=qq~$contrast~;
		$ok_saturation=qq~$saturation~;
			}

$imagemagik="1";

	open(OUT, "$dirs_catalog/show_settings.txt"); $show_set = <OUT>; 	
		if ($show_set eq "foto") {$show_foto = "active"} else {$show_foto="";}
		if ($show_set eq "list") {$show_list = "active"} else {$show_list="";}
	close(OUT);
	
	open(OUT, "$dirs_catalog/valut_settings.txt"); $ok_valut = <OUT>; close(OUT);	

#################################################

	$menu_act=param('menu_act');
	$num_edit=param('num_edit');
	$cat_show=param('cat_show');
	$adm_save=param('adm_save');	
	$name=param('name');
	$name=Core::DB::Work::trans_new($name);	
	$date_add=param('date_add');
	$date_up=param('date_up');
	$title=param('title');
	$meta_desc=param('meta_desc');	
	$meta_key=param('meta_key');		
	$elm1=param('elm1');
	$elm1=Core::DB::Work::trans_html($elm1);		
	$elm1_sm=param('elm1_sm');	
	$elm1_sm=Core::DB::Work::trans_html($elm1_sm);
	$elm1_lite=param('elm1_lite');	
	$elm1_lite=Core::DB::Work::trans_html($elm1_lite);
	$supplier=param('supplier');
	$parent=param('parent');
	$price=param('price');
	$price =~ s/\s//g;
	$price =~ s/\,/\./g;
	$price =~ s/(\d+)/$1/g;
	$price_opt=param('price_opt');
	$price_opt =~ s/\s//g;
	$price_opt =~ s/\,/\./g;
	$price_opt =~ s/(\d+)/$1/g;
	$price_opt_large=param('price_opt_large');
	$price_opt_large =~ s/\s//g;
	$price_opt_large =~ s/\,/\./g;
	$price_opt_large =~ s/(\d+)/$1/g;
	$price_cost=param('price_cost');
	$price_cost =~ s/\s//g;
	$price_cost =~ s/\,/\./g;
	$price_cost =~ s/(\d+)/$1/g;	
	$price_old=param('price_old');
	$price_old =~ s/\s//g;
	$price_old =~ s/\,/\./g;
	$price_old =~ s/(\d+)/$1/g;
	$article=param('article');	
	$avail=param('avail');
	$alias=param('alias');
	if ($num_edit eq "" && $article){
		$alias = $article;
	}
	$product_type=param('product_type');	
	if ( $alias eq "" ) {
		my $self = new Core::DB();
		my $my = '';
		my $max_num = '';
		my $result = $self->query("SELECT * FROM cat_product WHERE p_id;");
		foreach my $item(@$result){	
			$my = $item->{p_id};
			if ($max_num < $my) {$max_num=$my;}	
		}

		if ($num_edit ne "") {$max_num=$num_edit} else {if ($max_num eq "") {$max_num="1";} else {$max_num++;}}

		$alias=1000+$max_num;
		
	} else {$alias=Core::DB::Work::translit( $alias )};
	$redirect=param('redirect');
	if ( $redirect ne "" ) {$redirect =~ s/^\///g; $redirect = "/".$redirect;}	
	$show=param('show');
	$show_head=param('show_head');
	$hit=param('hit');
	$spec=param('spec');
	$news=param('news');
	$maket=param('maket');
	$posup=param('posup');
	$posdown=param('posdown');	
	$par=param('par');
	$lamp=param('lamp');
	
	my $products_type="";
	if ($hide_products_type ne "1"){
		$products_type ='<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_type&par=new"><span>'.$pr_type_name.'</span></a></li>';
	}
	my $products_param="";
	if ($hide_products_param ne "1"){
		$products_param ='<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>';
	}	

if ($num_edit eq "") {
$new_pages =qq~<li class="first activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
$products_param
$products_type~;
} else {
$new_pages =qq~<li class="first activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
$products_param
$products_type~;
}
if ($par) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li class="activetab"><a id="click_pages_new" href="#"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
$products_param
$products_type~;
}
	
$content_html=qq~$content_html<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs">
				<ul>
					$new_pages
				</ul>
			</div>
			
			
			<div id="buttons">
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=category&settings=set" id="cstmz">Настроить модуль</a>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content" style="position:relative;">~;
$content_html .='		
		<div id="catalog"'.($content_wide eq "1"?' class="wide"':'').'>
<script type="text/javascript" src="/admin/js/jquery.opacityrollover.js"></script>		
<script type="text/javascript" src="/admin/lib/products.js?'.rand(1).'"></script>';	
		

	if( param('posup') ne "" ){
		$products->PosUpProduct($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";		
	}
	
	if( param('posdown') ne "" ){
		$products->PosDownProduct($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";			
	}
	
	if( $lamp eq "on" ){
		$products->lamp_on_product($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";	
	}

	if( $lamp eq "off" ){
		$products->lamp_off_product($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";		
	}	
	
	($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
	if ($mday < 10 ) { $mdays="0"; $mday="$mdays$mday";}
	$mon++; if ($mon < 10 ) { $mon="0$mon";}
	$year=1900+$year; 
	$today="$year-$mon-$mday $hour:$min:$sec";
	$ok_date_add_old="$year-$mon-$mday $hour:$min:$sec";
	
	if ($hit eq "on") {$hit_ok = "1"} else {$hit_ok = "0"};
	if ($spec eq "on") {$spec_ok = "1"} else {$spec_ok = "0"};
	if ($news eq "on") {$news_ok = "1"} else {$news_ok = "0"};

	if ($menu_act eq "") {
		if($num_edit ne ""){
			my $products = $products->getProduct($num_edit);
			$parent = $products->{cat_id};
			$product_type = $products->{p_type_id};	
			$ok_supplier = $products->{p_supplier};
			$ok_name_old = $products->{p_name};
			$ok_name_old=Core::DB::Work::trans_edit($ok_name_old);				
			$ok_title_old = $products->{p_title};
			$ok_meta_desc_old = $products->{p_meta_desc};
			$ok_meta_key_old = $products->{p_meta_key};				
			$ok_alias_old = $products->{p_alias};
			$ok_redirect_old = $products->{p_redirect};
			$ok_price = $products->{p_price};
			$ok_price_opt = $products->{p_price_opt};
			$ok_price_opt_large = $products->{p_price_opt_large};
			$ok_price_cost = $products->{p_price_cost};
			$ok_price_old = $products->{p_price_old};
			$ok_article_old = $products->{p_art};
			$ok_avail_old = $products->{p_count};
			$ok_sort_old = $products->{p_pos};
			$ok_elm_old[0] = $products->{p_desc_bottom};
			$ok_elm_sm_old[0] = $products->{p_desc_top};
			$ok_elm_lite_old[0] = $products->{p_desc_sm};			
			$ok_show_old = $products->{p_show};
			$ok_show_head_old = $products->{p_show_head};
			$ok_hit_old = $products->{p_hit};
			$ok_spec_old = $products->{p_spec};
			$ok_news_old = $products->{p_news};
			$ok_raiting_old = $products->{p_raiting};
			$ok_raiting_count_old = $products->{p_raiting_count};
			$ok_maket_old = $products->{p_maket};
			$today=$products->{p_date_up};
			$ok_date_add_old=$products->{p_date_add};			
		}
		
	} elsif ($menu_act eq "ok") {
	
		my $self = new Core::DB();

		my $result = $self->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1;");
		foreach my $item(@$result){	
			$my = $item->{p_id};
			if ($max_num < $my) {$max_num=$my;}
			$name_file_max=$my+1000;			
		}

		if ($num_edit ne "") {$max_num=$num_edit; $name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$max_num="1"; $name_file_max="1001"} else {$max_num++; $name_file_max++;}}


		$sm_x=param('sm_x');
		$sm_y=param('sm_y');
		$big_x=param('big_x');
		$big_y=param('big_y');	
		$lite_x=param('lite_x');
		$lite_y=param('lite_y');
		$auto_first=param('auto_first');
		$auto_small=param('auto_small');
		$hdr=param('hdr');
		$type_resize=param('type_resize');
		$normalize=param('normalize');		
		$contrast=param('contrast');
		$saturation=param('saturation');
		$sharpness=param('sharpness');
		$resize=param('resize');
		$imagesm=param('imagesm');
		$imagesm_resize=param('imagesm_resize');
		$imagesm_effect=param('imagesm_effect');
		$imagebg=param('imagebg');
		$imagebg_resize=param('imagebg_resize');
		$imagebg_effect=param('imagebg_effect');
		$image_lite1=param('image_lite1');
		$image_lite2=param('image_lite2');
		$image_lite3=param('image_lite3');
		$image_lite4=param('image_lite4');
		$image_lite5=param('image_lite5');
		$image_lite6=param('image_lite6');
		$image_lite7=param('image_lite7');
		$image_lite8=param('image_lite8');
		$image_lite9=param('image_lite9');
		$image_lite10=param('image_lite10');
		$image_lite11=param('image_lite11');
		$image_lite12=param('image_lite12');

		$hdr_image = $hdr;
		if ($hdr_image eq "OFF"){$hdr_image = 0;}
		else {$hdr_image =~ s/\%//g;}
		$saturation_ok = $saturation;
		if ($saturation_ok eq "OFF"){$saturation_ok = 0;}
		elsif ($saturation_ok eq "Ч/Б"){$saturation_ok = -100;}
		else {$saturation_ok =~ s/\+//g;}
		$contrast_ok = $contrast;
		if ($contrast_ok eq "OFF"){$contrast_ok = 0;}
		else {$contrast_ok =~ s/\+//g;}		
		if($type_resize eq "on") {$type_resize_ok=qq~full~;} else {$type_resize_ok=qq~half~;}
		if($normalize eq "on") {$normalize_ok="1";} else {$normalize_ok="0";}
		if($sharpness eq "on") {$sharpness_ok="1";} else {$sharpness_ok="0";}
		if($resize eq "on") {$resize_ok="1";} else {$resize_ok="0";}
		if($lite_x eq ""){$lite_x="100";} if($lite_y eq ""){$lite_y="84";}
		
		open OUT, (">$dirs_catalog/settings.txt");
			print OUT "$big_x|$big_y|$sm_x|$sm_y|$lite_x|$lite_y|1|$hdr_image|$type_resize_ok|$resize_ok|$normalize_ok|$contrast_ok|$saturation_ok|$sharpness_ok"; 
		close(OUT);

		if ($imagesm && $imagesm_resize eq "") {
		   open OUT, (">$dirs_catalog/$name_file_max\_small.jpg");
		    binmode (OUT);
		    while (<$imagesm>) { print OUT "$_"; } 
		   close(OUT);
		}

		if ($imagebg && $imagebg_resize eq "") {
		   open OUT, (">$dirs_catalog/$name_file_max\_big.jpg");
		    binmode (OUT);
		    while (<$imagebg>) { print OUT "$_"; } 
		   close(OUT);
		}
		
		if ($imagebg ne "" or $imagesm ne ""){
			use File::Copy;
			if ($auto_small eq "1" && $imagebg ne "" && $imagesm eq "" && $imagebg_resize eq "" or $auto_small eq "1" && $imagebg ne "" && $imagesm eq "" && $imagebg_resize eq "no" && $imagesm_resize eq ""){copy("$dirs_catalog/$name_file_max\_big.jpg", "$dirs_catalog/$name_file_max\_temp.jpg");}
			else {
				if ($imagebg ne "" && $imagebg_resize eq ""){copy("$dirs_catalog/$name_file_max\_big.jpg", "$dirs_catalog/$name_file_max\_temp_big.jpg");}
				if ($imagesm ne "" && $imagesm_resize eq ""){copy("$dirs_catalog/$name_file_max\_small.jpg", "$dirs_catalog/$name_file_max\_temp_small.jpg");}
			}
		}		
		
		if ($image_lite1) {open OUT, (">$dirs_catalog/$name_file_max\_1_temp.jpg"); binmode (OUT);
			while (<$image_lite1>) { print OUT "$_"; } close(OUT);}
		if ($image_lite2) {open OUT, (">$dirs_catalog/$name_file_max\_2_temp.jpg"); binmode (OUT);
			while (<$image_lite2>) { print OUT "$_"; } close(OUT);}
		if ($image_lite3) {open OUT, (">$dirs_catalog/$name_file_max\_3_temp.jpg"); binmode (OUT);
			while (<$image_lite3>) { print OUT "$_"; } close(OUT);}
		if ($image_lite4) {open OUT, (">$dirs_catalog/$name_file_max\_4_temp.jpg"); binmode (OUT);
			while (<$image_lite4>) { print OUT "$_"; } close(OUT);}
		if ($image_lite5) {open OUT, (">$dirs_catalog/$name_file_max\_5_temp.jpg"); binmode (OUT);
			while (<$image_lite5>) { print OUT "$_"; } close(OUT);}
		if ($image_lite6) {open OUT, (">$dirs_catalog/$name_file_max\_6_temp.jpg"); binmode (OUT);
			while (<$image_lite6>) { print OUT "$_"; } close(OUT);}
		if ($image_lite7) {open OUT, (">$dirs_catalog/$name_file_max\_7_temp.jpg"); binmode (OUT);
			while (<$image_lite7>) { print OUT "$_"; } close(OUT);}
		if ($image_lite8) {open OUT, (">$dirs_catalog/$name_file_max\_8_temp.jpg"); binmode (OUT);
			while (<$image_lite8>) { print OUT "$_"; } close(OUT);}
		if ($image_lite9) {open OUT, (">$dirs_catalog/$name_file_max\_9_temp.jpg"); binmode (OUT);
			while (<$image_lite9>) { print OUT "$_"; } close(OUT);}
		if ($image_lite10) {open OUT, (">$dirs_catalog/$name_file_max\_10_temp.jpg"); binmode (OUT);
			while (<$image_lite10>) { print OUT "$_"; } close(OUT);}
		if ($image_lite11) {open OUT, (">$dirs_catalog/$name_file_max\_11_temp.jpg"); binmode (OUT);
			while (<$image_lite11>) { print OUT "$_"; } close(OUT);}
		if ($image_lite12) {open OUT, (">$dirs_catalog/$name_file_max\_12_temp.jpg"); binmode (OUT);
			while (<$image_lite12>) { print OUT "$_"; } close(OUT);}
			
		if ($imagemagik eq "1") {
		
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

			use Image::Magick;
			
			require "../modules/mod_resize_image.cgi";
			
			if ($image_lite1 ne ""){resize_lite("1", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite2 ne ""){resize_lite("2", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite3 ne ""){resize_lite("3", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite4 ne ""){resize_lite("4", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite5 ne ""){resize_lite("5", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite6 ne ""){resize_lite("6", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite7 ne ""){resize_lite("7", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite8 ne ""){resize_lite("8", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite9 ne ""){resize_lite("9", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite10 ne ""){resize_lite("10", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite11 ne ""){resize_lite("11", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}
			if ($image_lite12 ne ""){resize_lite("12", $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);}

			if ($resize eq "on"){
				if ($auto_small eq "1" && $imagebg ne "" && $imagesm eq "") {
					if ($imagebg_resize eq "" && $imagesm_resize eq ""){
						my $ext = "temp";
						resize_preview($ext, $name_file_max);
						resize_big($ext, $name_file_max);
						resize_small($ext, $name_file_max, $type_resize_ok);
						
						unlink ("$dirs_catalog/$name_file_max\_$ext\.jpg");
					}
					elsif ($imagebg_resize eq "no" && $imagesm_resize eq ""){
						my $ext = "temp";
						resize_preview($ext, $name_file_max);
						resize_small($ext, $name_file_max, $type_resize_ok);
						
						unlink ("$dirs_catalog/$name_file_max\_$ext\.jpg");
					}
					elsif ($imagesm_resize eq "no" && $imagebg_resize eq ""){
						my $ext = "temp";
						resize_big($ext, $name_file_max);
						
						unlink ("$dirs_catalog/$name_file_max\_$ext\.jpg");
					}				
				}
				else {
					if ($imagebg ne "" && $imagebg_resize eq "") {
						my $ext = "temp_big";
						resize_big($ext, $name_file_max);
						
						unlink ("$dirs_catalog/$name_file_max\_$ext\.jpg");
					}
					if ($imagesm ne "" && $imagesm_resize eq "") {
						my $ext = "temp_small";
						resize_small($ext, $name_file_max, $type_resize_ok);
						resize_preview($ext, $name_file_max);

						unlink ("$dirs_catalog/$name_file_max\_$ext\.jpg");
					}
				}
			}
			if ($hide_products_watermark ne "1"){
				if ($imagebg_resize eq "no" && $watermark_big eq "1"){
					my $image = Image::Magick->new;
					$image->Read("$dirs_catalog/$name_file_max\_big.jpg"); 
					my ($ox,$oy) = $image->Get('base-columns','base-rows'); 						
					watermark("$dirs_catalog/$name_file_max\_big.jpg", "big", $ox, $oy);
				}
				if ($imagebg_resize eq "no" && $watermark_normal eq "1"){
					my $image = Image::Magick->new;
					$image->Read("$dirs_catalog/$name_file_max\_normal.jpg"); 
					my ($ox,$oy) = $image->Get('base-columns','base-rows'); 						
					watermark("$dirs_catalog/$name_file_max\_normal.jpg", "normal", $ox, $oy);						
				}
				if ($imagesm_resize eq "no" && $watermark_small eq "1"){
					my $image = Image::Magick->new;
					$image->Read("$dirs_catalog/$name_file_max\_small.jpg"); 
					my ($ox,$oy) = $image->Get('base-columns','base-rows'); 						
					watermark("$dirs_catalog/$name_file_max\_small.jpg", "small", $ox, $oy);						
				}				
			}			
			
			if ($imagebg_effect eq ""){
				my $ext = "big";
				effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
				my $ext = "normal";
				effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
			}
			if ($imagesm_effect eq ""){
				my $ext = "small";
				effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
				my $ext = "preview";
				effects_image($ext, $name_file_max, $hdr, $hdr_set1, $hdr_set1_2, $hdr_set2, $hdr_set2_2, $hdr_set3, $hdr_set3_2, $hdr_set4, $hdr_set4_2, $normalize, $contrast_set, $saturation_set, $sharpness);
			}
			if ($resize_photo_single){
				if (-e "$dirs_catalog/$name_file_max\_normal.jpg"){
					rename "$dirs_catalog/$name_file_max\_normal.jpg", "$dirs_catalog/$alias\.jpg";
					unlink ("$dirs_catalog/$name_file_max\_big.jpg");
					unlink ("$dirs_catalog/$name_file_max\_small.jpg");
					unlink ("$dirs_catalog/$name_file_max\_preview.jpg");
				}
			}
		}		

			my %params = (
					'p_id' => "$max_num",
					'p_name' => "$name",
					'p_desc_bottom' => "$elm1",
					'p_desc_top' => "$elm1_sm",
					'p_desc_sm' => "$elm1_lite",
					'p_supplier' => "$supplier",
					'p_price' => "$price",
					'p_price_opt' => "$price_opt",
					'p_price_opt_large' => "$price_opt_large",
					'p_price_cost' => "$price_cost",
					'p_price_old' => "$price_old",	
					'p_count' => "$avail",
					'p_hit' => "$hit_ok",
					'p_spec' => "$spec_ok",
					'p_news' => "$news_ok",
					'p_art' => "$article",	
					'p_title' => "$title",
					'p_meta_desc' => "$meta_desc",
					'p_meta_key' => "$meta_key",
					'p_date_up' => "$today",
					'p_date_add' => "$date_add",
					'p_show' => $show,
					'p_show_head' => $show_head,
					'p_alias' => Core::DB::Work::translit($name),
					'p_redirect' => $redirect,
					'p_type_id' => $product_type,
					'p_maket' => "$maket"					
			);
			my %params_rel = (
					'cat_p_id' => "$max_num",
					'cat_main' => "1",	
					'cat_id' => $parent
			);	
			
		if ($num_edit ne ""){
			$products->editProduct($num_edit, \%params);
			$products->editProductRel($num_edit, \%params_rel);	
			ClearCache("../..");
		} else {
			if ($name){
				$products->addProduct(\%params);
				$products->addProductRel(\%params_rel);	
				ClearCache("../..");
			}
		}
		
		if ($hide_products_param ne "1"){
		
			my %vars = ();
			my @params = param();
			foreach my $item(@params){
				%vars = (%vars, $item => param($item))
			}
			
			if ($num_edit){
				$db->delete("DELETE FROM cat_product_fields WHERE p_id = '".$num_edit."'");
			}
			
			my $parent_cid = findParentCat($parent);
			my $result = $db->query("SELECT f_name FROM cat_product_fields_set WHERE cat_id = '0' OR cat_id = '".$parent_cid."'");
			if ($result){
				foreach my $item(@$result){
					my $field=""; my $unic = 0;
					if ($vars{'fields_main_'.$item->{'f_name'}}){
						$field = $vars{'fields_main_'.$item->{'f_name'}};
					}					
					elsif ($vars{'fields_unic_'.$item->{'f_name'}}){
						$field = $vars{'fields_unic_'.$item->{'f_name'}};
						$unic = 1;
					}
					if ($field){
						$field =~ s/^\s+//g;
						$field =~ s/\s+$//g;
						my %params = (
							'p_id' => $max_num,
							'field' => $item->{'f_name'},
							'value' => $field,	
							'unic' => $unic
						);
						$products->addParam(\%params);
					}
				}
			}
		}
		
		if ($auto_first && !$num_edit && $parent){
			my $res = $db->query("SELECT p_id FROM cat_product ORDER BY p_id DESC LIMIT 1;");
			if ($res->[0]->{p_id} > 0){
				my $p_id = $res->[0]->{p_id};
				my $result = $db->query("SELECT pl.* FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE pl.cat_id ='".$parent."' AND pl.cat_main = '1' AND p.p_id != '".$p_id."' ORDER BY pl.p_pos ASC");
				if (scalar @$result > 1){
					$db->update("UPDATE cat_product_rel SET `p_pos`='1' WHERE cat_p_id='".$p_id."' AND cat_id='".$parent."' AND cat_main = '1'");
					my $pos = 1;
					foreach my $item(@$result){
						$pos++;
						$db->update("UPDATE cat_product_rel SET `p_pos`='".$pos."' WHERE cat_p_id='".$item->{cat_p_id}."' AND cat_id='".$parent."' AND cat_main = '1'");
					}
				}
			}
		}		
		
		sub findParentCat {
			my $c_pid = shift;
			my $res = $db->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$c_pid."'");
			foreach my $line(@$res){
				my $result = $line->{c_id}; 
				if ($line->{c_pid} eq "0"){
					return $result; last;
				}
				else {
					if (my $ids = findSubParentCat($line->{c_pid})){
						$result = $ids;
					}
					if ($result){
						return $result; last;
					}
				}
			}
			sub findSubParentCat {
				my $parent = shift;
				my $result="";
				my $res_parent = $db->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$parent."'");
				if ($res_parent){
					foreach my $line(@$res_parent){
						my $result = $line->{c_id};
						if ($line->{c_pid} eq "0"){
							return $result; last;
						}
						else {
							if (my $ids = findSubParentCat($line->{c_pid})){
								$result = $ids;
							}
							if ($result){
								return $result; last;
							}
						}
					}
				}
			}
		}		
		
		$content_html=qq~$content_html
		<script>
		\$(document).ready(function(){
			\$("a.cat_show_all").parent().parent().removeClass("active");
			\$("div#category_products ul li a.show_cat").each(function(){
				if (\$(this).attr("cat_show") == $parent) {\$(this).addClass("active");};
			});
			\$("div#main_menu div#products a").attr("href", "/cgi-bin/admin/engine/index.cgi?adm_act=products&cat_show="+$parent);				
			var params = new Object();
			params.cat_show_ajax = $parent;
			params.cat_current = $parent;
			params.save_product = "1"
			params.curent_page = $curent_page
			\$.post('../modules/products_ajax.cgi', params, function(data){
				\$("div#allProducts").replaceWith(data);
				if (isNaN(\$("#product_foto").html())){
					sortProduct("#product_foto");
				}
				else if (isNaN(\$("#product_list").html())){
					sortProduct("#product_list");
				}
				move_product();
				move_product_foto();
				lamp_product();
				del_product();
				rename_product();
				edit_price();
				edit_price_list();
				\$().PagesScroll();
				\$().ContextMenu();
			});	
		});
		</script>
		
		<div class="save_page">Товар сохранен "$name" сохранен.</div>~;
		$num_edit="";
		$parents="";
		$menu_act="";
		$list_older="";
			
		
	} elsif ($menu_act eq "del"){
		$products->delProduct($num_edit);
		$content_html=qq~$content_html<div class="delete_page">Товар удален.</div>~;
		$num_edit="";
		$parents="";
		$menu_act="";
		$list_older="";	
	}
	
	$maket_list=""; $maket_item="";
	opendir (DBDIR, "../$dirs"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $num) = split(/\./, $line_wall);
			if ($name_file eq "maket" && $num ne "404") { 
				open (BO, "../$dirs/$line_wall"); @b = <BO>; close (BO);
				($name_old, $date_old) = split(/\|/, $b[0]);
				my $select="";
				if ($ok_maket_old ne ""){$select = $ok_maket_old;} else {$select = $maket_product;}
				$maket_item .= '<option value="'.$num.'" '.($num==$select?'selected':'').'>'.$name_old.'</option>';
			}
		}
	}

	if ($maket_item ne "" && $hide_makets ne "1"){
		$maket_list = '
			<tr class="help_maket">
				<td class="name">Привязать товар к макету</td>
				<td>
					<select class="category" name="maket" style="width:197px;">
						'.$maket_item.'
					</select>
				</td>
			</tr>';
	}	


sub treeCat
{
	
	my $sort="";
	open(BO, "../$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
	foreach my $line(@select_sort){chomp($line);
	my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
	$sort=qq~$select_sort_cat_~;}

	use Core::DB;
	my $self = new Core::DB();

	my $globalid = shift || undef;
	my $parent = shift || undef;
	
	my $tree = "";
	$tree .= '<ul class="level0">';	
	my $active = "";
	my $parents = "";
	my $sel_category = "";
	my $result = $self->query("SELECT * FROM cat_category WHERE c_pid=0 ORDER BY ".$sort.";");
	my $main_parent = $self->query("SELECT * FROM cat_product_rel WHERE cat_p_id='".$num_edit."' AND cat_main='1' LIMIT 1;");
	foreach my $item(@$main_parent){
		$active = $item->{cat_id};
	}

	my $active_type="";
	my $parents_auto="";	
	if ($hide_products_type ne "1"){
		my $main_type = $self->query("SELECT p_type_id FROM cat_product WHERE p_id='".$num_edit."' LIMIT 1;");
		foreach my $item(@$main_type){
			$active_type = $item->{p_type_id};
		}
		
		my $type_result = $self->query("SELECT t_id, t_name FROM cat_product_type");
		foreach my $item(@$type_result){
			$parents_auto .= '<option style="padding-left:5px; padding-top:3px;" value="'.$item->{t_id}.'" '.($active_type==$item->{t_id}?'selected':'').'>'.$item->{t_name}.'</option>';	
		}
	}
	
	foreach my $item(@$result){

		$cat_name = $item->{c_name};
		$string = length($item->{c_name});
		if ($string > 26){$cat_name=substr($cat_name,0,26); $cat_name=qq~$cat_name...~; $title_name="$item->{c_name}";} else {$cat_name=$item->{c_name}; $title_name="";}	
		
		$tree .= '<li><span class="move" '.($sort eq "c_pos ASC"?'c_id="'.$item->{c_id}.'" c_pos="'.$item->{c_pos}.'" c_pid="'.$item->{c_pid}.'"><a class="up upper_cat" href="#"></a><a class="down downer_cat" href="#"></a>':'id="off">').'</span>';
		$tree .= '<a class="show_cat" title="'.$title_name.'" cat_show='.$item->{c_id}.' '.($item->{c_show}==1?'':'style="color:#aaa"').' href="#">'.$cat_name.'</a>';
		
		if ($par eq "new" && $cat_current ne ""){	
			$parents .= '<option style="font-weight:bold" value="'.$item->{c_id}.'" '.($cat_current==$item->{c_id}?'selected':'').'>'.$item->{c_name}.'</option>';
		}
		else {
			$parents .= '<option style="font-weight:bold" value="'.$item->{c_id}.'" '.($active==$item->{c_id}?'selected':'').'>'.$item->{c_name}.'</option>';		
		}
		$sel_category .= '<option style="font-weight:bold" value="'.$item->{c_id}.'" '.($cat_current==$item->{c_id}?'selected':'').'>'.$item->{c_name}.'</option>';

		if( my $sub = recMenu($item->{c_id}, 0) ){
			$tree .= $sub;
		}
		$tree .= '</li>';

	}
	
	sub recMenu{
		my $id = shift;
		my $level = shift;
		sub nbsp { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
		my $text = '<ul class="level'.($level+1).'">';
		my $cat_level=$level+1;
		
			$result_parent = $db->query("SELECT * FROM cat_category WHERE c_id='".$id."'");
			my $hide_child="";
			my $show_child_count="";
			if($result_parent){ 
				foreach my $items(@$result_parent){
					$hide_child = $items->{c_hide_child};
					$show_child_count = $items->{c_show_child_count};
				}
			}
			if ($hide_child == 1) {$hide_child=" hide"} else {$hide_child=""};		
		
		my $result = $self->query("SELECT * FROM cat_category WHERE c_pid='".$id."' ORDER BY ".$sort.";");
		if($result){
			my $i_cat_old="";
			foreach my $item2(@$result){
				$i_cat_old++;
			}
			my $i_cat="";
			foreach my $item(@$result){
				$i_cat++;
				$cat_name = $item->{c_name};
				$string = length($item->{c_name});
				if ($cat_level == 1) {$st=25;} else {$st=20;}
				if ($string > $st){$cat_name=substr($cat_name,0,$st); $cat_name=qq~$cat_name...~; $title_name="$item->{c_name}";} else {$cat_name=$item->{c_name}; $title_name="";}	
				
				$text .= '<li><span class="move" '.($sort eq "c_pos ASC"?'c_id="'.$item->{c_id}.'" c_pos="'.$item->{c_pos}.'" c_pid="'.$item->{c_pid}.'"><a class="up upper_cat" href="#"></a><a class="down downer_cat" href="#"></a>':'id="off">').'</span><div class="point'.($i_cat==$i_cat_old?' last':'').'"></div>';
				$text .= '<a class="show_cat'.$hide_child.''.($show_child_count < $i_cat && $show_child_count !=0?' hide':'').'" title="'.$title_name.'" cat_show='.$item->{c_id}.' '.($item->{c_show}==1?'':'style="color:#aaa"').' href="#">'.$cat_name.'</a>';
				if ($par eq "new" && $cat_current ne ""){	
					$parents .= '<option'.($cat_level == 1?' style="color:#0e517e"':'').' value="'.$item->{c_id}.'" '.($cat_current==$item->{c_id}?'selected':'').' '.($globalid==$item->{c_id}?'disabled':'').'>'.nbsp($level).$item->{c_name}.'</option>';
				}
				else {
					$parents .= '<option'.($cat_level == 1?' style="color:#0e517e"':'').' value="'.$item->{c_id}.'" '.($active==$item->{c_id}?'selected':'').' '.($globalid==$item->{c_id}?'disabled':'').'>'.nbsp($level).$item->{c_name}.'</option>';				
				}
				$sel_category .= '<option'.($cat_level == 1?' style="color:#0e517e"':'').' value="'.$item->{c_id}.'" '.($cat_current==$item->{c_id}?'selected':'').' '.($globalid==$item->{c_id}?'disabled':'').'>'.nbsp($level).$item->{c_name}.'</option>';
				
				if( my $sub = recMenu($item->{c_id}, $level+1) ){
					$text .= $sub;
				}
				$text .= '</li>';
			}

		} else {
			return 0;
		}
		$text .= '</ul>';
		return $text;
	};
	$text .= '</ul>';
    return ($tree, $parents, $sel_category, $parents_auto);
}	

	my ($tree, $parents, $sel_category, $parents_auto) = treeCat( $num_edit, $parent, $sel_cat, $parents_auto );
	$list_older .= $tree;
	menu_listing($parents, $sel_category, $parents_auto);
	


sub menu_listing {
 my $parents = shift;
 my $sel_category = shift;
 my $parents_auto = shift;

$select_category=qq~<select class="category">$sel_category</select>~; 
$sel_category=qq~<td class="name">Товар в категории<em>*</em></td><td><select style="width:362px" name="parent" class="category">$parents</select></td>~;
if ($parents_auto ne "") {
$product_type_sel=qq~<td class="name">Выберите $pr_type_name_sm<em>*</em></td><td><select name="product_type" class="category"><option style="padding-left:5px; padding-top:3px;" value="">не выбран</option>$parents_auto</select></td>~;
} else {$product_type_sel="";}

if ($par eq "new") {

$rand_num=rand(1);

if(-e "$dirs_catalog/$num_edit\_normal.jpg")
{$foto_big =qq~<div class="prev_img get_image" data-image="big" style="max-width:220px;"><img style="max-width:220px;" src="$dirs_catalog_www/$num_edit\_nomrmal.jpg?$rand_num" width="$sm_x" border="0"></div>~;}
else { $foto_big = qq~<div class="prev_img get_image" data-image="big" style="width:220px; height:140px;"><img src="/admin/img/gallery_no_photo_sm.png" border="0"></div>~; }

if(-e "$dirs_catalog/$num_edit\_small.jpg")
{$foto_sm =qq~<div class="prev_img get_image" data-image="small" style="max-width:220px;"><img style="max-width:220px;" src="$dirs_catalog_www/$num_edit\_small.jpg?$rand_num" width="$sm_x" border="0"></div>~;}
else { $foto_sm = qq~<div class="prev_img get_image" data-image="small" style="width:220px; height:140px;"><img src="/admin/img/gallery_no_photo_sm.png" border="0"></div>~; }

my $result_cat = $db->query("SELECT cat_category.c_id FROM cat_category LIMIT 1"); 
		
if (ref($result_cat) eq "ARRAY") {

$content_html=qq~$content_html
<script type="text/javascript" src="/admin/js/highslide/highslide.js"></script>
<link rel="stylesheet" type="text/css" href="/admin/js/highslide/highslide.css" />
<script type="text/javascript">
	hs.graphicsDir = '/admin/js/highslide/graphics/';
	hs.wrapperClassName = 'wide-border';
</script>~;	

if ($hide_products_multi_add ne "1"){
	$content_html .='<a title="Пакетное добавление товаров" class="multi-add" href="/cgi-bin/admin/engine/index.cgi?adm_act=products_multi">Пакетное добавление</a>';
}

$content_html .='<link rel="stylesheet" type="text/css" href="/admin/scripts/crop/css/imgareaselect-animated.css">
				 <script type="text/javascript" src="/admin/scripts/crop/jquery.imgareaselect.pack.js"></script>
				 <script type="text/javascript" src="/admin/scripts/crop/script.js"></script>';

$content_html=qq~$content_html<div class="clear"></div>
<script type="text/javascript" src="/admin/lib/help/catalog/products_edit.js"></script>	
<div id="pages_new" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="adm_save" value="save">
<input type="hidden" name="menu_act" value="ok">
<input type="hidden" name="imagebg_resize">
<input type="hidden" name="imagesm_resize">
<input type="hidden" name="imagebg_effect">
<input type="hidden" name="imagesm_effect">

<table style="float:left; margin-top:11px;">
	<tr>
		<td class="help_photo_big"><span class="p14 gray">Большая фотография</span> $foto_big</td>
	</tr>
	<tr>
		<td><input multiple="multiple" class="fileInput" type="file" name="imagebg" size="21" onchange="document.getElementById('fileInputbg').value = this.value;">
		<div class="browse">
			<input type="text" id="fileInputbg" class="browse_input"/>
		</div>
		<input type="text" foto_id="$num_edit" type_foto="big" value="" class="give_url_big">
		<p class="help_auto_small" style="margin-top:10px;"><input class="cb" type="checkbox" value="1" name="auto_small" checked><span> создать маленькую автоматически</span></p><br></td>
	</tr>
	<tr>
		<td class="help_photo_small"><span class="p14 gray">Малая фотография</span> $foto_sm</td>
	</tr>
	<tr>
		<td><input class="fileInput" type="file" name="imagesm" size="21" onchange="document.getElementById('fileInputsm').value = this.value;">
		<div class="browse">
			<input type="text" id="fileInputsm" class="browse_input"/>
		</div>
		<input type="text" foto_id="$num_edit" type_foto="small" value="" class="give_url_big">
		</td>
	<tr>
		<td style="padding-top:2px; padding-bottom:3px;"><span class="st">*</span> - для повышения качества плохих фото,<br> воспользуйтесь функциями справа</td>
	</tr>
	<tr>
		<td><input type="submit" class="button" value="Загрузить"></td>
	</tr>
</table>
			<link rel="stylesheet" type="text/css" href="/admin/scripts/hdr/style.css">
			<script type="text/javascript" src="/admin/scripts/hdr/script.js"></script>
			<table id="page_new" style="float:right; margin-right:15px;" class="add_product~;
if ($set_foto_hide ne "1"){
		$content_html.= qq~ open_set~;			
}
		$content_html.= qq~">
			<tr>
				<td class="name"></td><td class="name_main">Новый товар</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
			<tr>
				<td class="name">Выберите поставщика<em>*</em></td>
				<td>
					<select style="width:362px" name="supplier" class="category">
						<option value="1">Arlight</option>
						<option value="2">Geniled</option>
						<option value="100">Другой</option>
					</select>
				</td>
			</tr>			
			<tr class="help_parent">
$sel_category
			</tr>
$product_type_sel
			<tr>
				<td class="name">Добавить первым в категорию</td><td><input class="cb" type="checkbox" name="auto_first"></td>
			</tr>~;
		if ($hide_products_art ne "1"){
			$content_html.= qq~
			<tr class="help_art">
				<td class="name">Артикул товара<em>*</em></td><td><input class="price" type="text" name="article" value="" format=".+" notice="Введите артикул"></td>
			</tr>~;
		}			
		if ($hide_products_price ne "1"){
		$content_html.= qq~
			<tr class="help_price">
				<td class="name">Цена товара</td><td><input class="price" type="text" name="price" value="$ok_price"><input class="valut" type="text" readonly="readonly" value="$ok_valut"></td>
			</tr>
			<tr>
				<td class="name">Цена мелкий опт</td><td><input class="price" type="text" name="price_opt" value=""></td>
			</tr>
			<tr>
				<td class="name">Цена крупный опт</td><td><input class="price" type="text" name="price_opt_large" value=""></td>
			</tr>
			<tr>
				<td class="name">Цена закупки</td><td><input class="price" type="text" name="price_cost" value=""></td>
			</tr>~;
		}
		if ($hide_products_old_price ne "1"){
			$content_html.= qq~
			<tr class="help_price_old">
				<td class="name">Старая цена</td><td><input class="price" type="text" name="price_old" value=""></td>
			</tr>~;
		}		
		if ($hide_products_avail ne "1"){
			$content_html.= qq~
			<tr class="help_avail">
				<td class="name">Кол-во товара</td><td><input class="price" type="text" name="avail" value=""></td>
			</tr>~;
		}		
		if ($hide_products_param ne "1"){

			my $main_params=""; my $category_params=""; my $cat_id="";
			my $result = $db->query("SELECT * FROM cat_product_fields_set WHERE cat_id = '0' ORDER BY f_pos ASC");
			if ($result){
				foreach my $item(@$result){
					$main_params .='<tr><td class="name">'.$item->{'f_name'}.'</td><td><input type="text" name="fields_main_'.$item->{'f_name'}.'" value=""></td></tr>';
				}
			}
			$content_html .= '<tr><td class="name" colspan="2"><h3 style="margin-top:22px">Основные параметры</h3></td></tr>'.$main_params.'<tr><td></td><td><a href="#" class="add-param addMainParam">Добавить основной параметр</a></td></tr>';
			my $result = $db->query("SELECT c_id, c_name FROM cat_category WHERE c_pid = '0' ORDER BY c_pos ASC");
			foreach my $item(@$result){
				$category_params .='<option value="'.$item->{'c_id'}.'">'.$item->{'c_name'}.'</option>';
			}
			
			$content_html .= '<tr><td class="name" colspan="2"><h3 style="margin-top:22px">Уникальные параметры</h3></td></tr>
			<tr><td class="name">Выберите для категории<em>*</em></td><td><select class="selCategoryParam category"><option value="0">Выбрать</option>'.$category_params.'</select></td></tr>
			<tr><td colspan="2"></td></tr>';
			
		}
		$content_html .='</td>
			</tr>
			<tr>
				<td class="name">';
	if ($set_foto_hide eq "1"){		
		$content_html .='
				<a href="#" class="open_settings">Настройки изображения</a>';
	}	
		$content_html .='
				</td>
				<td></td>
			</tr>';
			
		$content_html .='	
			<tr>
				<td colspan="2" class="resize">
				
					<div class="foto_settings">
						<div class="test_image"><div class="container empty"><p>Перетащите изображение<br> в эту область</p></div></div>
						<div class="hdr_set"'.($ok_hdr_image > 0?' id="on"':' id="off"').'>
							<a href="#" class="control"></a>
							<div class="notic"></div>
							<div class="widget hdr">
								<span>Сила действия HDR</span>
								<div id="slider_hdr" class="slider"></div>
								<div class="value"><input name="hdr" value="'.$ok_hdr_image.'" type="text" readonly="readonly"></div>
							</div>
						</div>
						
						<div class="pointer1"></div>
						<div class="pointer2"></div>
							
						<div class="widget saturation">
							<span>Насыщенность</span><a href="#" class="reset">Сбросить</a>
							<div id="slider_saturation" class="slider"></div>
							<div class="value"><input name="saturation" value="'.$ok_saturation.'" type="text" readonly="readonly"></div>
						</div>
						
						<div class="widget contrast">
							<span>Прибавить контрастность</span>
							<div id="slider_contrast" class="slider"></div>
							<div class="value"><input name="contrast" value="'.$ok_contrast.'" type="text" readonly="readonly"></div>
						</div>	

						<div class="checkbox sharpness">
							<span>Добавить резкости</span>
							<input type="checkbox" name="sharpness"'.($ok_sharpness eq "1"?' checked':'').'>
						</div>
						
						<div class="checkbox normalize">
							<span>Нормализовать оттенки</span>
							<input type="checkbox" name="normalize"'.($ok_auto_normalize eq "1"?' checked':'').'>
						</div>	
						
						<div class="checkbox resize">
							<span>Авторазмер изображения</span>
							<input type="checkbox" name="resize"'.($ok_auto_resize eq "1"?' checked':'').'>
						</div>						
						
						<a href="#" class="test_image">Посмотреть результат</a>

						<a href="#" class="show_autoresize">Параметры изображения</a>
							
					</div>';
					
		$content_html.= qq~			
					<table id="page_new" class="autoresize">	
					<tr class="help_resize_big">
						<td class="name">Авторазмер для большой</td><td><input class="size" type="text" name="big_x" value="$big_x" size=10><input class="size" type="text" name="big_y" value="$big_y" size=10></td>
					</tr>
					<tr class="help_resize_small">
						<td class="name">Авторазмер для маленькой</td><td><input class="size" type="text" name="sm_x" value="$sm_x" size=10><input class="size" type="text" name="sm_y" value="$sm_y" size=10><span class="help_crop val"><input class="cb" type="checkbox" name="type_resize"~;
		if($ok_type_resize eq "full"){
			$content_html.= qq~ checked~;
		} 	

		my $photo_more="";	
		if ($count_more ne "" && $count_more > 0 && $hide_more_photo ne "1"){
			if ($count_more > 12){$count_more = 12;}		
			$rand_num=rand(1);	
			$photo_more .='<ul class="gallery_product">';
			my $num="";
			for ($num=1; $num<=$count_more; $num++) {
					$photo_more .='<li class="get_img" data-image="lite">
									<div class="foto"><img src="/admin/img/product_gallery_no_photo.png" alt=""></div>
									<input class="fileInputsm" type="file" name="image_lite'.$num.'" size="3" onchange="document.getElementById(\'fileInputLite'.$num.'\').value = this.value;">
									<div class="browse_sm">
										<input type="text" id="fileInputLite'.$num.'" class="browse_input_sm"/>
									</div>
									<input type="text" foto_id="" num_id="'.$num.'" type_foto="lite" value="" class="give_url_lite">						
								</li>';			
			}
			$photo_more .='</ul>';	
		}
			$content_html .=qq~ >обрезать края</span>
						</td>
					</tr>~;
			if ($hide_more_photo ne "1"){		
				$content_html .=qq~		
					<tr class="help_resize_more">
						<td class="name">Авторазмер для доп. фото</td><td><input class="size" type="text" name="lite_x" value="$lite_x" size=10><input class="size" type="text" name="lite_y" value="$lite_y" size=10></td>
					</tr>~;
			}
			$content_html .=qq~
					</table>
					
				</td>
			</tr>
			<tr class="help_desc_small">
				<td class="name">Краткое описание товара</td><td><textarea class="lite_desc" name="elm1_lite">@ok_elm_lite_old</textarea></td>
			</tr>	
			<tr class="help_add_params">
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>~;
		if ($count_more ne "" && $count_more > 0 && $hide_more_photo ne "1"){			
			$content_html .='
			<tr class="help_add_photo">
				<td colspan="2">
				<h3 style="margin:7px 0px 10px 187px; padding:0px;">Дополнительные фотографии</h3>
				
				'.$photo_more.'
				
				</td>
			</tr>';
		}	
		
			$content_html =qq~$content_html
			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param add_product" style="margin-bottom:-18px;">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr class="help_alias">
				<td class="name">Адрес товара</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>			
				$maket_list
			<tr>
				<td class="name">Дата создания </td><td><input name="date_add" readonly="readonly" value="$ok_date_add_old" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name">Дата изменения </td><td><input name="date_up" readonly="readonly" value="$today" type="text" class="date"></td>
			</tr>			
			<tr>
				<td class="name"></td><td class="show"></td>
			</tr>
			<tr>
				<td class="name"></td><td class="name_main">Настройки SEO</td>
			</tr>
			<tr class="help_meta-title">
				<td class="name">Meta Title</td><td><input name="title" value="$ok_title_old" type="text"></td>
			</tr>
			<tr class="help_meta-desc">
				<td class="name">Meta Description</td><td><input name="meta_desc" value="$ok_meta_desc_old" type="text"></td>
			</tr>
			<tr class="help_meta-key">
				<td class="name">Meta Keywords</td><td><input name="meta_key" value="$ok_meta_key_old" type="text"></td>
			</tr>	
			</table>
			
			</td>
			</tr>
			</table>

	<div class="clear"></div>~;
	
	if ($product_desc_ext eq "1"){
		$content_html.= qq~<h3>Анонс товара</h3>	
		<textarea id="elm1_sm" name="elm1_sm" rows="15" cols="80" class="tinymce">@ok_elm_sm_old</textarea>
		<h3>Полное описание</h3>
		<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>~;
	}
	else {
		$content_html.= qq~<h3>Полное описание</h3>
		<textarea id="elm1_sm" name="elm1_sm" rows="20" cols="80" class="tinymce">@ok_elm_sm_old</textarea>~;
	}	
	$content_html.= qq~
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<input type="submit" name="save" value="Сохранить" class="button" />
	<input type="reset" name="reset" value="Очистить" class="button" />
</form>
</div>
~;
}
else {	
	$content_html=qq~$content_html
	<div id="pages" style="margin-left:10px;">
		<div class="save_page">Добавьте категории к товарам</div>
	</div>~;
}


} else {

	if($num_edit eq ""){

		$catalog = new Core::DB::Catalog;
		my $products = $catalog->getAllProduct(10000);
		my $pages_amount="";
		foreach my $product(@{$products}){
			$pages_amount++;
		}
		
		my $pagess = $pages_amount/$count_pages;
		$pagess = $pagess+0.49;
		$pagess = sprintf("%.0f",$pagess); 
		my $i=1;
		my $pages="";
		while ($i <= $pagess) {
			my $style="";
			if ($i > 9 && $i < 100){$style=' style="padding:7px 8px 8px 7px;"';}
			elsif ($i > 99){$style=' style="padding:7px 4px 8px 4px;"';}		
			$pages .= '<a href="#" '.($i == 1?'id="current"':'').' class="page"'.$style.' id_page="'.$i.'">'.$i.'</a>&nbsp;&nbsp;&nbsp;';
			$i++;
		}
		if ($i == "2") {$pages ="";}

my $result_cat = $db->query("SELECT cat_category.c_id FROM cat_category LIMIT 1");
		
if (ref($result_cat) eq "ARRAY") {
$content_html .='
<link href="/admin/js/autocomplete/css/style.css" rel="stylesheet" />
<script type="text/javascript" src="/admin/js/autocomplete/jquery.autocomplete.mod.min.js"></script>
<div class="three_pages">';
	if ($hide_products_hit eq "0" or $hide_products_spec eq "0" or $hide_products_new eq "0"){
$content_html .='	
		<div class="main_button hits">
			<div><a>Хиты продаж</a></div>
		</div>';
	}
	else {
		$content_html .='<div class="main_button'.($view_all eq "all"?' active':'').'"><div><a href="#" class="cat_show_all" sort="'.($sort_pr eq "p_pos ASC"?'active':'no_sort').'">'.($content_wide eq "1"?'Все товары':'Показать все товары').'</a></div></div>';
	}
$content_html .='	
	<div class="search_catalog">
		<form>
			<input type="text" id="word_search" onblur="if (this.value==\'\'){this.value=\'Поиск:\'}" onfocus="if (this.value==\'Поиск:\') this.value=\'\';" value="Поиск:">
			<input type="submit" value="Поиск" id="search">
		</form>	
	</div>
	'.($content_wide eq "1"?'<div class="select_category"><span>Выберите категорию: </span>'.$select_category.'</div>':'<div style="display:none" class="select_category"><span>Выберите категорию: </span>'.$select_category.'</div>').'
	<div style="float:right; margin-left:10px;"><div class="main_button foto '.$show_foto.'"><div><a class="show_foto" href="#">Показать с фото</a></div></div></div>	
	<div style="float:right; margin-left:10px;"><div class="main_button list '.$show_list.'"><div><a class="show_list" href="#">Показать списком</a></div></div></div>
	<div class="clear"></div>
	<div id="category_products">'.$list_older.'</div>
</div>';
	if ($hide_products_multi_add ne "1"){
		$content_html .='<a title="Пакетное добавление товаров" class="multi-add" href="/cgi-bin/admin/engine/index.cgi?adm_act=products_multi">Пакетное добавление</a>';
	}
}
else {	
$content_html=qq~$content_html<div class="save_page">Добавьте категории к товарам</div>~;	
}	


if ($cat_show ne "") {

use Core::Config;
use Core::DB;

my $db = new Core::DB();

$rand_num=rand(1);

	my $product_page = $db->query("SELECT p.*, ".$sort_products_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_show."' ORDER BY ".$sort_products."");
	my $pages_amount="";
	foreach my $product(@$product_page){
		$pages_amount++;
	}

	my $pagess = $pages_amount/$count_pages;
	$pagess = $pagess+0.49;
	$pagess = sprintf("%.0f",$pagess); 
	my $i=1;
	my $pages="";
	while ($i <= $pagess) {
		my $style="";
		if ($i > 9 && $i < 100){$style=' style="padding:7px 8px 8px 7px;"';}
		elsif ($i > 99){$style=' style="padding:7px 4px 8px 4px;"';}	
		$pages .= '<a href="#" '.($curent_page == $i?'id="current"':'').' '.($curent_page == "" && $i == 1?'id="current"':'').''.$style.' class="page_cat" id_category="'.$cat_show.'" id_page="'.$i.'">'.$i.'</a>&nbsp;&nbsp;&nbsp;';
		$i++;
	}
	if ($i == "2") {$pages ="";}

	my $product = $db->query("SELECT p.*, ".$sort_products_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$cat_show."' ORDER BY ".$sort_products." ".($curent_page!=""?"LIMIT ".($curent_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");

	$content_html =qq~$content_html<div id="allProducts">
	<script>
		\$(document).ready(function(){
			\$("a.cat_show_all").parent().parent().removeClass("active");
			\$("div#category_products ul li a.show_cat").each(function(){
				if (\$(this).attr("cat_show") == $cat_show) {\$(this).addClass("active");};
			});	
		});
	</script>~;
	
	$content_html .= '<script type="text/javascript" src="/admin/lib/help/catalog/products.js"></script>';
	
	if ($show_set eq "foto") {
	
		$content_html .= '<ul id="product_foto" id_cat="'.$cat_show.'">';	
		
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

	} else {
		
		$content_html .= '<ul id="product_list" id_cat="'.$cat_show.'">';
		
		foreach my $line(@$product){
		$string = length($line->{p_name});
		if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}		
		$p_id = $line->{p_id};
		
		my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}		
		
		$content_html .= '<li p_id="'.$line->{p_id}.'" p_pos="'.$line->{p_pos}.'" '.($line->{p_show}==1?'':'class="off"').'><span class="move" '.($sort_pr eq "p_pos ASC"?'p_id="'.$line->{p_id}.'" cat_id="'.$line->{cat_id}.'" p_pos="'.$line->{p_pos}.'"><a class="up upper" href="#"></a><a class="down downer" href="#"></a>':'id="off">').'</span><a href="#" '.($line->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$line->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$line->{p_name}.'" href="#" class="product_del" del_id="'.$line->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$line->{p_id}.'">'.$line->{p_name}.'</a>'.($line->{p_price}!=""?'<span class="price"><span class="cost_list">'.$line->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';
		}	
	}

	if ($p_id eq "" && $result_cat) {$content_html .= "<div class=\"message\" style=\"margin-left:25px;\">В данной категории товаров нет.</div>";}
	
	$content_html .='</ul></div>';	
	
	if ($p_id ne "") {
		if ($pagess > 15){
			$content_html .= '<div class="pages wide"><a href="#" class="page_left">«</a><div class="container"><div class="width">'.$pages.'</div></div><a href="#" class="page_right">»</a></div>';
		}
		else {$content_html .= '<div class="pages"><div class="container">'.$pages.'</div></div>';}
	}	


} elsif ($adm_save eq "save") { $content_html .= '<div id="allProducts"></div>';}

else {

$catalog = new Core::DB::Catalog;
$rand_num=rand(1);
	
	if ($show_set eq "foto") {

		my $products = $catalog->getAllProduct($count_pages);
			$content_html .= '<div id="allProducts"><ul id="product_foto">';
		foreach my $product(@{$products}){
			$string = length($product->{p_name});
			if ($string > 35 and $string < 50){$size_name="small";} elsif ($string > 50 and $string < 60) {$size_name="lite";} elsif ($string > 60) {$size_name="very_lite";} else {$size_name="";}			
			$p_id = $product->{p_id};
			$img_id = $p_id+1000;
			
			my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
			if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$product->{p_art}.'.jpg?'.$rand_num;}			
			
			$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$line->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';
			$content_html .= '<li p_id="'.$product->{p_id}.'"><a href="?adm_act=products&num_edit='.$product->{p_id}.'">'.$img_sm.'</a><span class="name '.$size_name.'" '.($product->{p_show}==1?'':'style="color:#aaa"').' >'.$product->{p_name}.'</span>'.($product->{p_price}!=""?'<span class="price"><span class="cost">'.$product->{p_price}.'</span>,-</span>':'').'<a class="product_del" href="#" del_id="'.$product->{p_id}.'" title="Удалить товар"></a></li>';	}
			
		$content_html .='</div>';	
		
		if ($p_id ne "") {
			if ($pagess > 15){
				$content_html .= '</ul><div class="pages wide"><a href="#" class="page_left">«</a><div class="container"><div class="width">'.$pages.'</div></div><a href="#" class="page_right">»</a></div>';
			}
			else {$content_html .= '</ul><div class="pages"><div class="container">'.$pages.'</div></div>';}
		}	
		
	} else {
	
		my $products = $catalog->getAllProduct($count_pages);
		$content_html .= '<div id="allProducts"><ul id="product_list">';
		foreach my $product(@{$products}){
			$p_id = $product->{p_id};
			$string = length($product->{p_name});
			if ($string > 60){$size_name=qq~class="small"~;} else {$size_name="";}	

			my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
			if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{p_art}.'.jpg?'.$rand_num;}
			
			$content_html .= '<li p_id="'.$product->{p_id}.'" '.($product->{p_show}==1?'':'class="off"').'><span class="move" id="off"></span><a href="#" '.($product->{p_show}==1?'style="opacity:1" title="Скрыть товар"':'style="opacity:0.5" title="Сделать активным"').' lamp_id="'.$product->{p_id}.'" class="product_lamp"></a><a title="Удалить товар '.$product->{p_name}.'" href="#" class="product_del" del_id="'.$product->{p_id}.'"></a><a id="p_name" title="'.$img_link.'" '.$size_name.' href="?adm_act=products&num_edit='.$product->{p_id}.'">'.$product->{p_name}.'</a>'.($product->{p_price}!=""?'<span class="price"><span class="cost_list">'.$product->{p_price}.'</span>,-</span>':'<span class="price"><span class="cost_list">0</span>,-</span>').'</li>';}
			
		$content_html .='</div>';	
		
		if ($p_id ne "") {
			if ($pagess > 15){
				$content_html .= '</ul><div class="pages wide"><a href="#" class="page_left">«</a><div class="container"><div class="width">'.$pages.'</div></div><a href="#" class="page_right">»</a></div>';
			}
			else {$content_html .= '</ul><div class="pages"><div class="container">'.$pages.'</div></div>';}
		}	
	}
}		
	
} else {

$num_edit_old = $num_edit+1000;
$rand_num=rand(1);

my $p_art="";
if ($resize_photo_single eq "1"){
	
	my $res = $db->query("SELECT p_art FROM cat_product WHERE p_id ='".$num_edit."'");
	$p_art = $res->[0]->{'p_art'};
	if(-e "$dirs_catalog/$p_art\.jpg"){
		$foto_big =qq~<div class="prev_img get_image" data-image="big" style="max-width:220px; min-width:220px; min-height:140px;"><img style="max-width:220px; max-height:$big_y\px;" src="$dirs_catalog_www/$p_art\.jpg?$rand_num" border="0"><a href="#" class="del_foto" title="Удалить большую фотографию" id_del="$num_edit_old" size_foto="big"></a></div>~;
		$foto_sm =qq~<div class="prev_img get_image" data-image="small" style="max-width:220px; min-width:220px; min-height:140px;"><img style="max-width:220px; max-height:$sm_y\px;" src="$dirs_catalog_www/$p_art\.jpg?$rand_num" border="0"><a href="#" class="del_foto" title="Удалить малую фотографию" id_del="$num_edit_old" size_foto="small"></a></div>~;
	}
	else {	
		$foto_big = qq~<div class="prev_img get_image" data-image="big" style="width:220px; height:140px;"><img src="/admin/img/gallery_no_photo_sm.png" border="0"></div>~;
		$foto_sm = qq~<div class="prev_img get_image" data-image="small" style="width:220px; height:140px;"><img src="/admin/img/gallery_no_photo_sm.png" border="0"></div>~;
	}
}
else {
	if(-e "$dirs_catalog/$num_edit_old\_normal.jpg")
	{$foto_big =qq~<div class="prev_img get_image" data-image="big" style="max-width:220px; min-width:220px; min-height:140px;"><img style="max-width:220px; max-height:$big_y\px;" src="$dirs_catalog_www/$num_edit_old\_normal.jpg?$rand_num" border="0"><a href="#" class="del_foto" title="Удалить большую фотографию" id_del="$num_edit_old" size_foto="big"></a></div>~;}
	else {$foto_big = qq~<div class="prev_img get_image" data-image="big" style="width:220px; height:140px;"><img src="/admin/img/gallery_no_photo_sm.png" border="0"></div>~; }

	if(-e "$dirs_catalog/$num_edit_old\_small.jpg")
	{$foto_sm =qq~<div class="prev_img get_image" data-image="small" style="max-width:220px; min-width:220px; min-height:140px;"><img style="max-width:220px; max-height:$sm_y\px;" src="$dirs_catalog_www/$num_edit_old\_small.jpg?$rand_num" border="0"><a href="#" class="del_foto" title="Удалить малую фотографию" id_del="$num_edit_old" size_foto="small"></a></div>~;}
	else { $foto_sm = qq~<div class="prev_img get_image" data-image="small" style="width:220px; height:140px;"><img src="/admin/img/gallery_no_photo_sm.png" border="0"></div>~; }
}

$content_html=qq~$content_html
<script type="text/javascript" src="/admin/js/highslide/highslide.js"></script>
<link rel="stylesheet" type="text/css" href="/admin/js/highslide/highslide.css" />
<script type="text/javascript">
	hs.graphicsDir = '/admin/js/highslide/graphics/';
	hs.wrapperClassName = 'wide-border';
</script>~;	

if ($hide_products_multi_add ne "1"){
	$content_html .='<a title="Пакетное добавление товаров" class="multi-add" href="/cgi-bin/admin/engine/index.cgi?adm_act=products_multi">Пакетное добавление</a>';
}

$content_html .='<link rel="stylesheet" type="text/css" href="/admin/scripts/crop/css/imgareaselect-animated.css">
				 <script type="text/javascript" src="/admin/scripts/crop/jquery.imgareaselect.pack.js"></script>
				 <script type="text/javascript" src="/admin/scripts/crop/script.js"></script>';
	
$content_html=qq~$content_html
<div id="pages_old" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="adm_save" value="save">
<input type="hidden" name="menu_act" value="ok">
<input type="hidden" name="imagebg_resize">
<input type="hidden" name="imagesm_resize">
<input type="hidden" name="imagebg_effect" value="no">
<input type="hidden" name="imagesm_effect" value="no">

<table style="float:left; margin-top:11px;">
	<tr>
		<td class="help_photo_big"><span class="p14 gray">Большая фотография</span> $foto_big</td>
	</tr>
	<tr>
		<td><input multiple="multiple" class="fileInput" type="file" name="imagebg" size="21" onchange="document.getElementById('fileInputbg').value = this.value;">
		<div class="browse">
			<input type="text" id="fileInputbg" class="browse_input"/>
		</div>
		<input type="text" foto_id="$num_edit" type_foto="big" value="" class="give_url_big">
		<p class="help_auto_small" style="margin-top:10px;"><input class="cb" type="checkbox" value="1" name="auto_small" checked><span> создать маленькую автоматически</span></p><br></td>
	</tr>
	<tr>
		<td class="help_photo_small"><span class="p14 gray">Малая фотография</span> $foto_sm</td>
	</tr>
	<tr>
		<td><input class="fileInput" type="file" name="imagesm" size="21" onchange="document.getElementById('fileInputsm').value = this.value;">
		<div class="browse">
			<input type="text" id="fileInputsm" class="browse_input"/>
		</div>
		<input type="text" foto_id="$num_edit" type_foto="small" value="" class="give_url_big">
		</td>
	<tr>
		<td style="padding-top:2px; padding-bottom:3px;"><span class="st">*</span> - для повышения качества плохих фото,<br> воспользуйтесь функциями справа</td>
	</tr>
	<tr>
		<td><input type="submit" class="button" value="Загрузить"></td>
	</tr>~;	
if ($hide_products_recomend ne "1"){

	my $products_rec="";
	my $result = $db->query("SELECT p.p_show, pl.r_pos, pl.p_ids FROM cat_product AS p JOIN cat_product_recomend AS pl ON(pl.rec_id=p.p_id) WHERE p.p_id ='".$num_edit."' ORDER BY pl.r_pos ASC");
	if ($result){
		foreach my $line(@$result){
			my $p_id = $line->{p_ids};
			my $img_id = $p_id+1000;
			my $res = $db->query("SELECT p_img_url, p_art FROM cat_product WHERE p_id ='".$p_id."'");
			
			my $img_link = $dirs_catalog_www.'/'.$img_id.'_preview.jpg?'.$rand_num;
			if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$res->[0]->{p_art}.'.jpg?'.$rand_num;}
			
			$img_sm ='<div class="foto"><img onerror="this.src=\'/admin/img/product_no_photo_lite.png\'" src="'.(!$img_ext_url?$img_link:''.$res->[0]->{p_img_url}.'').'" '.($line->{p_show}==1?'':'style="opacity:0.5"').' alt=""></div>';
			
			$products_rec .='<li data-id="'.$p_id.'">'.$img_sm.'<a href="#" class="del_p"></a></li>';
		}
	}
	$content_html .='
		<tr class="help_recomend">
			<td>
				<div class="products_recomend products_select">
					<h3>Сопутствующие товары</h3>
					<div class="select">
						<span>Выберите категорию:</span>
						'.$select_category.'
					</div>
					<div class="container">
						<ul data-id="'.$num_edit.'">
							'.$products_rec.'
							<li class="add"><div class="foto"><span><em>Добавить товары</em></span></div></li>
						</ul>
					</div>
					<div class="add_product"><p>Перетащите товары<br> в эту область</p></div>
				</div>
			</td>
		</tr>';
}
$content_html.= qq~
</table>


			<script type="text/javascript" src="/admin/lib/help/catalog/products_edit.js"></script>
			<link rel="stylesheet" type="text/css" href="/admin/scripts/hdr/style.css">
			<script type="text/javascript" src="/admin/scripts/hdr/script.js"></script>
			<table id="page_new" style="float:right; margin-right:15px;" class="add_product~;
if ($set_foto_hide ne "1"){
		$content_html.= qq~ open_set~;			
}
		$content_html.= qq~">
			<tr>
				<td class="name"></td><td class="name_main">Редактирование товара</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>~;
	$content_html .=' 		
			<tr>
				<td class="name">Выберите поставщика<em>*</em></td>
				<td>
					<select style="width:362px" name="supplier" class="category">
						<option value="1"'.($ok_supplier == "1"?' selected':'').'>Arlight</option>
						<option value="2"'.($ok_supplier == "2"?' selected':'').'>Geniled</option>
						<option value="100"'.($ok_supplier == "100"?' selected':'').'>Другой</option>
					</select>
				</td>
			</tr>';
	$content_html .= qq~		
			<tr class="help_parent">
$sel_category
			</tr>
$product_type_sel
			~;
		if ($hide_products_art ne "1"){
			$content_html.= qq~
			<tr class="help_art">
				<td class="name">Артикул товара<em>*</em></td><td><input class="price" type="text" name="article" value="$ok_article_old" format=".+" notice="Введите артикул"></td>
			</tr>~;
		}			
		if ($hide_products_price ne "1"){
		$content_html.= qq~
			<tr class="help_price">
				<td class="name">Цена товара</td><td><input class="price" type="text" name="price" value="$ok_price"><input class="valut" type="text" readonly="readonly" value="$ok_valut"></td>
			</tr>
			<tr>
				<td class="name">Цена мелкий опт</td><td><input class="price" type="text" name="price_opt" value="$ok_price_opt"></td>
			</tr>
			<tr>
				<td class="name">Цена крупный опт</td><td><input class="price" type="text" name="price_opt_large" value="$ok_price_opt_large"></td>
			</tr>
			<tr>
				<td class="name">Цена закупки</td><td><input class="price" type="text" name="price_cost" value="$ok_price_cost"></td>
			</tr>~;
		}
		if ($hide_products_old_price ne "1"){
			$content_html.= qq~
			<tr class="help_price_old">
				<td class="name">Старая цена</td><td><input class="price" type="text" name="price_old" value="$ok_price_old"></td>
			</tr>~;
		}
		if ($hide_products_avail ne "1"){
			$content_html.= qq~
			<tr class="help_avail">
				<td class="name">Кол-во товара</td><td><input class="price" type="text" name="avail" value="$ok_avail_old"></td>
			</tr>~;
		}		
		$content_html.= qq~			
			<tr class="help_show">
				<td class="name">Показывать товар</td><td class="show"><input name="show" type="checkbox" class="cb"~;
		if($ok_show_old){
			$content_html.= qq~ checked ~;
		} 
		$content_html.= qq~></td></tr>~;
	}
	
		if ($num_edit){
		
		if ($hide_products_param ne "1"){
			my $main_params=""; my $unic_params=""; my $category_params="";
			my $result = $db->query("SELECT * FROM cat_product_fields WHERE p_id = '".$num_edit."' ORDER BY field ASC");
			foreach my $item(@$result){
				if ($item->{'unic'} eq "0"){
					$main_params .='<tr><td class="name">'.$item->{'field'}.'</td><td><input type="text" name="fields_main_'.$item->{'field'}.'" value="'.$item->{'value'}.'"></td></tr>';
				}
				if ($item->{'unic'} eq "1"){
					$unic_params .='<tr><td class="name">'.$item->{'field'}.'</td><td><input type="text" name="fields_unic_'.$item->{'field'}.'" value="'.$item->{'value'}.'"></td></tr>';
				}
			}
			if (!$main_params){
				my $result = $db->query("SELECT * FROM cat_product_fields_set WHERE cat_id = '0' ORDER BY f_pos ASC");
				if ($result){
					foreach my $item(@$result){
						$main_params .='<tr><td class="name">'.$item->{'f_name'}.'</td><td><input type="text" name="fields_main_'.$item->{'f_name'}.'" value=""></td></tr>';
					}
				}
			}
			$content_html .= '<tr><td class="name" colspan="2"><h3 style="margin-top:22px">Основные параметры</h3></td></tr>'.$main_params.'<tr><td></td><td><a href="#" class="add-param addMainParam">Добавить основной параметр</a></td></tr>';
			
			my $parent_cid = findParentCat($parent);
			my $result = $db->query("SELECT c_id, c_name FROM cat_category WHERE c_pid = '0' ORDER BY c_pos ASC");
			foreach my $item(@$result){
				$category_params .='<option value="'.$item->{'c_id'}.'"'.($parent_cid eq $item->{'c_id'}?' selected':'').'>'.$item->{'c_name'}.'</option>';
			}			
			if (!$unic_params){
				my $result = $db->query("SELECT f_name FROM cat_product_fields_set WHERE cat_id = '".$parent_cid."' ORDER BY f_pos ASC");
				if ($result){
					foreach my $item(@$result){
						$unic_params .='<tr><td class="name">'.$item->{'f_name'}.'</td><td><input name="fields_unic_'.$item->{'f_name'}.'" type="text" value="" autocomplete="off"></td></tr>';
					}
				}			
			}
			$content_html .= '<tr><td class="name" colspan="2"><h3 style="margin-top:22px">Уникальные параметры</h3></td></tr>
<tr><td class="name">Выберите для категории<em>*</em></td><td><select class="selCategoryParam category"><option value="0">Выбрать</option>'.$category_params.'</select></td></tr><tr><td colspan="2"><div id="addUnicParam-wrapper"><table>'.$unic_params.'<tr><td class="name"></td><td><a class="add-param addUnicParam" href="#">Добавить уникальный параметр</a></td></tr></table></div></td></tr>';
		}
		
			$content_html .='</td>
				</tr>
				<tr>
					<td class="name">';
		if ($set_foto_hide eq "1"){		
			$content_html .='
					<a href="#" class="open_settings">Настройки изображения</a>';
		}	
			$content_html .='
					</td>
					<td></td>
				</tr>';
		
		$content_html .='
			<tr>
				<td colspan="2" class="resize">
				
					<div class="foto_settings">

						<div class="test_image"><div class="container empty"><p>Перетащите изображение<br> в эту область</p></div></div>
						<div class="hdr_set"'.($ok_hdr_image > 0?' id="on"':' id="off"').'>
							<a href="#" class="control"></a>
							<div class="notic"></div>
							<div class="widget hdr">
								<span>Сила действия HDR</span>
								<div id="slider_hdr" class="slider"></div>
								<div class="value"><input name="hdr" value="'.$ok_hdr_image.'" type="text" readonly="readonly"></div>
							</div>
						</div>
						
						<div class="pointer1"></div>
						<div class="pointer2"></div>
							
						<div class="widget saturation">
							<span>Насыщенность</span><a href="#" class="reset">Сбросить</a>
							<div id="slider_saturation" class="slider"></div>
							<div class="value"><input name="saturation" value="'.$ok_saturation.'" type="text" readonly="readonly"></div>
						</div>
						
						<div class="widget contrast">
							<span>Прибавить контрастность</span>
							<div id="slider_contrast" class="slider"></div>
							<div class="value"><input name="contrast" value="'.$ok_contrast.'" type="text" readonly="readonly"></div>
						</div>	

						<div class="checkbox sharpness">
							<span>Добавить резкости</span>
							<input type="checkbox" name="sharpness"'.($ok_sharpness eq "1"?' checked':'').'>
						</div>
						
						<div class="checkbox normalize">
							<span>Нормализовать оттенки</span>
							<input type="checkbox" name="normalize"'.($ok_auto_normalize eq "1"?' checked':'').'>
						</div>	
						
						<div class="checkbox resize">
							<span>Авторазмер изображения</span>
							<input type="checkbox" name="resize"'.($ok_auto_resize eq "1"?' checked':'').'>
						</div>						
						
						<a href="#" class="test_image">Посмотреть результат</a>

						<a href="#" class="show_autoresize">Параметры изображения</a>					
							
					</div>';
					
		$content_html.= qq~			
					<table id="page_new" class="autoresize">
					<tr class="help_resize_big">
						<td class="name">Авторазмер для большой</td><td><input class="size" type="text" name="big_x" value="$big_x" size=10><input class="size" type="text" name="big_y" value="$big_y" size=10></td>
					</tr>
					<tr class="help_resize_small">
						<td class="name">Авторазмер для маленькой</td><td><input class="size" type="text" name="sm_x" value="$sm_x" size=10><input class="size" type="text" name="sm_y" value="$sm_y" size=10><span class="help_crop val"><input class="cb" type="checkbox" name="type_resize"~;
		if($ok_type_resize eq "full"){
			$content_html.= qq~ checked~;
		}

		my $photo_more="";
		if ($count_more ne "" && $count_more > 0 && $hide_more_photo ne "1"){
			if ($count_more > 12){$count_more = 12;}
			$rand_num=rand(1);	
			$photo_more .='<ul class="gallery_product">';
			my $num=""; my $img_lite=""; my $img_del="";
			for ($num=1; $num<=$count_more; $num++) {
					if(-e "$dirs_catalog/$num_edit_old\_$num\_small.jpg"){
						$img_lite = "<a class='highslide' href='$dirs_catalog_www/$num_edit_old\_$num\_big.jpg?$rand_num' title='Увеличить' onclick='return hs.expand(this)'><img style='max-height:90px; max-width:114px;' src='$dirs_catalog_www/$num_edit_old\_$num\_small.jpg?$rand_num' alt=''></a>";
						$img_del = '<a class="del_photo" title="Удалить фото" id_del="'.$num_edit_old.'" id_foto="'.$num.'" size_foto="lite" href="#"></a>';
					}
					else {$img_lite = "<img src='/admin/img/product_gallery_no_photo.png' alt=''>"; $img_del="";}
					$photo_more .='<li class="get_img" data-image="lite">
									<div class="foto">'.$img_lite.''.$img_del.'</div>
									<input class="fileInputsm" type="file" name="image_lite'.$num.'" size="3" onchange="document.getElementById(\'fileInputLite'.$num.'\').value = this.value;">
									<div class="browse_sm">
										<input type="text" id="fileInputLite'.$num.'" class="browse_input_sm"/>
									</div>
									<input type="text" foto_id="'.$num_edit.'" num_id="'.$num.'" type_foto="lite" value="" class="give_url_lite">						
								</li>';			
			}
			$photo_more .='</ul>';
		}
		
		my $products_reviews="";
		my $products_reviews_count="";
		if ($hide_products_reviews ne "1"){		
			my $reviews="";
			my $result = $db->query("SELECT *, DATE_FORMAT(v_date, \"%Y.%m.%d в %H:%i\") as date FROM cat_product_reviews WHERE p_id ='".$num_edit."' ORDER BY v_date DESC");
			foreach my $item(@$result){
				if ($result){
					 $reviews .='<div class="item'.($item->{'v_public'} eq "0"?' no_public':'').'" data-id="'.$item->{'v_id'}.'">
						<div class="name">
							<span>'.$item->{'v_name'}.'</span>
							<div class="raiting_star">
								<div class="raiting_blank"></div>
								<div class="raiting_votes" style="width:'.($item->{'v_raiting'}*19).'px;"></div>
							</div>
							<i title="Редактировать отзыв" class="edit_review fa fa-pencil"></i>
							'.($item->{'v_public'} eq "0"?'<a href="#" class="public_review">Опубликовать</a>':'').'
							<span class="date">'.$item->{'date'}.'</span>
							<i title="Удалить отзыв" class="delete_review fa fa-times"></i>
						</div>
						<div class="comments">
							'.$item->{'v_text'}.'
						</div>
					</div>';
					$products_reviews_count++;
				}
			}
			if (!$reviews){
				$reviews ='<div id="products_reviews_container"><p class="note">Пока нет отзывов</p></div>';
			}
			else {
				$reviews ='<div id="products_reviews_container">'.$reviews.'</div>';
			}
			$products_reviews ='<div id="products_reviews_wrap">
				'.$reviews.'
				<a href="#" class="add_show_reviews">Добавить отзыв</a>
				<div id="products_reviews_send">
					<div class="raiting"><span>Оцените товар</span>
						<div title="Поставить оценку" class="raiting_star" data-id="'.$num_edit.'" data-raiting="">
							<div class="raiting_blank"></div>
							<div class="raiting_hover"></div>
							<div class="raiting_votes"></div>
						</div>
					</div>
					<div class="head">Написать комментарий</div>
					<textarea></textarea>
					<div class="send">
						<label>Имя</label>
						<input type="text" name="name" class="normal" value="">
						<input type="button" value="Добавить" class="button">
					</div>
				</div>
			</div>';
		}		
			$content_html .=qq~ >обрезать края</span>
						</td>
					</tr>~;
			if ($hide_more_photo ne "1"){		
				$content_html .=qq~		
					<tr class="help_resize_more">
						<td class="name">Авторазмер для доп. фото</td><td><input class="size" type="text" name="lite_x" value="$lite_x" size=10><input class="size" type="text" name="lite_y" value="$lite_y" size=10></td>
					</tr>~;
			}
			$content_html .=qq~
					</table>
				</td>
			</tr>
			<tr class="help_desc_small">
				<td class="name">Краткое описание товара</td><td><textarea class="lite_desc" name="elm1_lite">@ok_elm_lite_old</textarea></td>
			</tr>
			<tr class="help_add_params">		
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>~;
		if ($count_more ne "" && $count_more > 0 && $hide_more_photo ne "1"){			
			$content_html .='
			<tr class="help_add_photo">
				<td colspan="2">
				<h3 style="margin:7px 0px 10px 187px; padding:0px;">Дополнительные фотографии</h3>
				
				'.$photo_more.'
				
				</td>
			</tr>';
		}
		if ($hide_products_reviews ne "1"){
			$content_html .='
			<tr class="help_products_reviews">
				<td colspan="2">
				<h3 style="margin:18px 0px 10px 27px; padding:0px;">Отзывы покупателей'.($products_reviews_count > 0?' <a href="#" class="show_reviews">Отзывы ('.$products_reviews_count.')</a>':'').'</h3>
				
				'.$products_reviews.'
				
				</td>
			</tr>';
		}		
			$content_html =qq~$content_html
			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param add_product" style="margin-bottom:-18px;">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr class="help_alias">
				<td class="name">Адрес товара</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>
				$maket_list
			<tr class="redirect">
				<td class="name">Редирект 301</td><td>
					<div>Например: <em><span>/</span>products<span>/</span>1001</em></div>
					<input name="redirect" type="text" value="$ok_redirect_old"></td>
			</tr>				
			<tr>
				<td class="name">Дата создания </td><td><input name="date_add" readonly="readonly" value="$ok_date_add_old" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name">Дата изменения </td><td><input name="date_up" readonly="readonly" value="$today" type="text" class="date"></td>
			</tr>			
			<tr class="help_header">
				<td class="name">Отображать заголовок товара</td><td class="show"><input name="show_head" type="checkbox" class="cb"~;
		if($ok_show_head_old){
			$content_html.= qq~ checked ~;
		} 
			$content_html.= qq~></td></tr> 
			<tr>
			<tr>
				<td class="name"></td><td class="name_main">Настройки SEO</td>
			</tr>
			<tr class="help_meta-title">
				<td class="name">Meta Title</td><td><input name="title" value="$ok_title_old" type="text"></td>
			</tr>
			<tr class="help_meta-desc">
				<td class="name">Meta Description</td><td><input name="meta_desc" value="$ok_meta_desc_old" type="text"></td>
			</tr>
			<tr class="help_meta-key">
				<td class="name">Meta Keywords</td><td><input name="meta_key" value="$ok_meta_key_old" type="text"></td>
			</tr>	
			</table>
			
			</td>
			</tr>
			</table>

	<div class="clear"></div>
	<img style="display:none;" src="/admin/js/tiny_mce/themes/advanced/skins/default/img/progress.gif" alt="">~;
	if ($product_desc_ext eq "1"){
		$content_html.= qq~<h3>Анонс товара</h3>	
		<textarea id="elm1_sm" name="elm1_sm" rows="15" cols="80" class="tinymce">@ok_elm_sm_old</textarea>
		<h3>Полное описание</h3>
		<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>~;
	}
	else {
		$content_html.= qq~<h3>Полное описание</h3>
		<textarea id="elm1_sm" name="elm1_sm" rows="20" cols="80" class="tinymce">@ok_elm_sm_old</textarea>~;
	}	
	my $result_cat = $db->query("SELECT cat_category.c_id, cat_category.c_alias FROM cat_category WHERE c_id = '".$parent."' LIMIT 1"); 
	my $cat_alias = $result_cat->[0]->{c_alias};	
	
	$content_html.= qq~
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<div class="save_content">$button_save
	<a class="preview_page" id="$num_edit" target="_blank" href="/products/$cat_alias/$ok_alias_old">Посмотреть</a><div class="check_save"><input type="checkbox" class="cb ajaxSave" $check_ajax>Быстрое сохранение контента</div></div>
</form>
</div>
~;
}
}

$content_html.= qq~
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;
}




-1;