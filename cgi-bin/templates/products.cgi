my $db = new Core::DB();


# Товары категорий каталога

#$script_product ='
#<script type="text/javascript" src="/js/fancybox/jquery.fancybox.pack.js"></script>
#<link rel="stylesheet" type="text/css" href="/js/fancybox/jquery.fancybox.css" />';
if ($hide_products_compare ne "1"){
$script_product .='
<script src="/js/jSbox/jquery.jSboxCompareProducts.js" type="text/javascript"></script>
<script type="text/javascript">
$(function(){
	$().jSboxCompareStatus({theme: "black"});
	$(".add_compare").jSboxAddCompare({theme: "black"});
});
</script>';
}
#$script_product .='
#<script type="text/javascript">
#$(function(){
#	$("a.fancybox, a.cloud-gallery, a#wrap-zoom").live("hover", function(){
#		$("a.fancybox, a.cloud-gallery, a#wrap-zoom").fancybox({
#			openEffect	: "elastic",
#			closeEffect	: "elastic",
#			padding     : 40,
#			helpers : {
#				overlay : {
#					opacity: 0.9
#				}
#			}
#		});
#	});
#});
#</script>
#'.($hide_products_zoom ne "1"?'<link href="/js/cloud-zoom/cloud-zoom.css" rel="stylesheet" type="text/css" />
#<script type="text/javascript" src="/js/cloud-zoom/cloud-zoom.1.0.2.js"></script>':'').'';	


sub build_TemplateProduct
{
	my $id = shift;
	my $art = shift;
	my $name = shift;
	my $alias = shift;
	my $c_alias = shift;
	my $price = shift;
	my $price_old = shift;
	my $desc_sm = shift;
	my $count = shift;
	my $label = shift;
	my $mark = shift;
	my $rait = shift;
	my $rait_count = shift;
	my $type = shift;
	my $img_url = shift;
	my $cat_name = shift;
	my $parent_id = shift;
	my $packnorm = shift;
	my $unit = shift;
	my $colors = shift;
	my $product="";
	if ($desc_sm ne "") {
		$desc_sm =~ s/\n/\<br \>/g;
	}	
	my $num_foto = $id+1000;
	$rand_num=rand(1); my $image="";
	if ($resize_photo_single eq "1"){
		$image = '<img onerror="this.src=\'/admin/site/img/no_photo.png\'" src="'.$dirs_catalog_www.'/'.$art.'.jpg" alt="'.$art.', '.$name.'">';
	}
	elsif (-e "".$dirs_catalog_www2."/".$num_foto."_small.jpg"){
		$image = '<img onerror="this.src=\'/admin/site/img/no_photo.png\'" src="'.$dirs_catalog_www.'/'.$num_foto.'_small.jpg?'.$rand_num.'" alt="'.$art.', '.$name.'">';
	}
	else {
		$image = '<img onerror="this.src=\'/admin/site/img/no_photo.png\'" src="/admin/site/img/no_photo.png" alt="'.$art.', '.$name.'">';
	}	
	
	if ($hide_products_old_price ne "1" && $price_old > 0){
		$price_old =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
		$price_old = $price_old." руб.";
	} else {$price_old="";}
	
	my $price_org = $price;
	if ($price > 0){
		$price = sprintf("%.0f",$price);
		$price =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
		$price = $price.' р';
	}
	else {$price="Цена по запросу";}
	
	my $compare="";
	if ($hide_products_compare ne "1"){
		if (cookie("compare_products") ne ""){
			my $compare_products = cookie("compare_products");
			while($compare_products =~ m/(\d+)\|/g){
				if ($id eq $1){$compare = "1";}
			}
		}
	}	
	
	# Верстка товаров //
	
	my $raiting="";
	if ($hide_products_raiting ne "1"){
		$raiting.='
		<div class="raiting_star">
			<div class="raiting" p_id="'.$id.'" p_raiting="'.$rait.'">
				<div class="raiting_blank"></div>
				<div class="raiting_hover"></div>
				<div class="raiting_votes"></div>
			</div>
			<div class="raiting_info">Всего голосов: <span>'.$rait_count.'</span></div>
		</div>';
	}
	if ($type ne "basket"){
	
		my ($label1, $label2, $label3, $label4, $pack, $packnorm, $unit) = build_ProductLabel($id, $parent_id);
		
		if ($type ne "related"){
			#$product ='<li'.($label eq "reflect"?' class="reflect"':'').'>';
			$product ='<li>';
		}	
		else {
			$product ='<div class="product-item">';
		}
		
		if ($packnorm =~/(\d+)\.5/){
			$packnorm = $packnorm*2;
		}		
		
		my $center="";		
		if ($mark eq "new" or $mark eq "hit"){$center = "center";}
		
		$product .='
						'.($mark eq "new"?'<span class="label">NEW</span>':'').'
						'.($mark eq "hit"?'<span class="label hit">ХИТ</span>':'').'
						'.($alias?'<a href="/products/'.$art.'/'.$alias.'" class="image"><span>'.$image.'</span></a>':'<a class="image"><span>'.$image.'</span></a>').'
						'.build_ColorItems($colors, $center).'
						<div class="text">
							'.($art?'<div class="art">Артикул: <em>'.$art.'</em></div>':'').'
							<div class="name">
								'.($alias?'<a href="/products/'.$art.'/'.$alias.'">'.$name.'</a>':$name).'
							</div>
							'.(!$label1 && !$label2 && !$label3 && !$label4?'<span>'.$cat_name.'</span>':'').'
							<div class="desc">'.$desc_sm.'</div>
							'.$label1.'
							'.$label2.'
							'.$label3.'
							'.$label4.'
						</div>
						<div class="holder">
							<strong class="price">'.$price.'</strong>										
							<a class="add buy_product" href="#" price="'.($price_org > 0?''.$price_org.'':'0').'" p_art="'.$art.'" data-pack="'.$packnorm.'">В корзину</a>
							'.($alias?'<a class="link" href="/products/'.$art.'/'.$alias.'">Подробнее</a>':'').'
							
						</div>';
						
		if ($type ne "related"){
			$product .='</li>';
		}
		else {
			$product .='</div>';
		}
		
		$product .="\r";
					
	} else {
		
		my $res_alias = $db->query("SELECT p_alias FROM cat_product WHERE p_art ='".$art."'");
		if ($res_alias){
			$alias = $res_alias->[0]->{'p_alias'};
		}
		
		if (!$packnorm && !$unit){
			($label1, $label2, $label3, $label4, $pack, $packnorm, $unit) = build_ProductLabel($id, $parent_id);
		}
		
		if (!$packnorm) {$packnorm = 1;}
		if (!$unit) {$unit = "шт";}
		
		if ($packnorm =~/(\d+)\.5/){
			$packnorm = $packnorm*2;
		}

		if ($price_org > 0){
			$price = $price_org;
			$price = $count*$price;
			$price = sprintf("%.2f",$price);
			$price =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
		}
		
		$product ='<div class="order-item" price="'.$price_org.'" p_art="'.$art.'">
					<div class="p-foto td">'.($alias?'<a href="/products/'.$art.'/'.$alias.'">'.$image.'</a>':$image).'</div>
					<div class="p-name td">
						'.($alias?'<a href="/products/'.$art.'/'.$alias.'">'.$name.'</a>':'<p>'.$name.'</p>').'
						<span class="p-type">'.$desc_sm.'</span>
						<span class="packnorm" data-pack="'.$packnorm.'">Норма отгрузки: '.$packnorm.' '.$unit.',&nbsp; цена за 1 '.$unit.': '.$price_org.' руб.</span>
					</div>
					<div class="p-col td">
						<span class="col-dec"></span>
						<em class="count">'.$count.'</em>
						<span class="col-inc"></span>
						<ul>
							<li class="active"><i>'.$packnorm.'</i></li>
							<li><i>'.($packnorm*2).'</i></li>
							<li><i>'.($packnorm*5).'</i></li>
							<li><i>'.($packnorm*10).'</i></li>
						</ul>
					</div>	
					<div class="p-price td">
						'.($price_org > 0?'<span class="cost">'.$price.'</span> <span>руб.</span>':'<span>Звоните</span>').'
					</div>
					<div class="p-delete td">
						<div class="p-delorder delete"></div>
					</div>
				</div>';
	}
				
	# / Верстка товаров //	

	return $product;
}

sub build_ColorItems
{
	my $data = shift;
	my $param = shift;
	
	if ($data){
		my $result=""; my $i=0;
		$data .=";";
		while ($data =~ m/(\d+)\[(.+?)\]\;/g){
			$i++;
			my $art = $1;
			my $colors = $2;
			my $colors_ = $2;
			my $num = 0;
			if ($colors =~ /\|/){
				$data_colors = $colors .="|";
				$colors="";
				while ($data_colors =~ m/(.+?)\|/g){
					$num++;
					$colors .='<ins class="'.$1.'"></ins>';
				}
			}
			else {
				$num++;
				$colors = '<ins class="'.$colors.'"></ins>';
			}
			if ($num eq "1"){$num = "";}
			elsif ($num eq "2"){$num = " two";}
			elsif ($num eq "3"){$num = " three";}
			$result .='<a href="/products/'.$art.'" class="color-item'.$num.'" title="'.getColorRus($colors_).'">'.$colors.'<em>'.$art.'</em></a>';
		}
		if ($result){
			my $word = "цветов";
			if ($param eq "big"){
				--$i;
				$word = "цвете";
				if ($i > 1){$word = "цветах";}			
			}
			else {
				if ($i eq "1"){$word = "цвет";}
				elsif ($i < 5){$word = "цвета";}
			}
			$result ='<div class="colors-items'.($param eq "big"?' big':'').''.($param eq "center"?' center':'').'">
						<span class="colors-items-title">'.($param eq "big"?'Ещё в ':'').''.$i.' '.$word.'</span>
						<div class="colors-items-container">
							'.$result.'
						</div>
					</div>';
		
			return $result;
		}
	}
}

sub build_ProductTags
{
	my $tag_start = shift;
	my $tag_end = shift;
	my $type = shift;
	my $tag="";
	if ($tag_start){
		if ($type eq "basket"){
			$tag='<div class="order-list">';
		}
		else {
			$tag='<ul class="products-list'.(cookie("view_products")?' '.cookie("view_products").'':' list').''.($type?' '.$type.'':'').'">';
		}
	}
	elsif ($tag_end){
		if ($type eq "basket"){
			$tag='</div>';
		}
		else {
			$tag='</ul>';
		}
	}
	return $tag;		
}

sub build_ProductCat
{
	my $id = shift;
	my $current_page = shift;	
	my $count_pages = shift;
	my $cat_name = shift;
	my $c_alias = shift;		
	my $pagess = shift;	
	my $sort = shift;
	my $parent_id = shift;
	my $ajax = shift;
	my $brand_ajax = shift;
	if (cookie("sort_products")){$sort = cookie("sort_products");}
	my $sort_ = $sort;
	$sort_=~ s/\sASC$//g;
	$sort_=~ s/\sDESC$//g;
	if ($sort_ eq "p_pos"){$sort = "pl.".$sort; $sort_ = "pl.".$sort_;}
	else {$sort = "p.".$sort; $sort_ = "p.".$sort_;}
	if ($brand_ajax ne ""){$brand_alias = $brand_ajax;}
	my $filter_price = cookie("filter_price");	
	if (cookie("filter_price")){
		if (cookie("filter_price") eq "ASC"){$sort = "p.p_price ASC";}
		elsif (cookie("filter_price") eq "DESC"){$sort = "p.p_price DESC";}
	}
	my $products_cat="";
	my $count="";
	my $result="";
	if ($id eq "all"){
		$c_alias = "all";
		if ($current_page eq "all"){
			$result = $db->query("SELECT * FROM cat_product");
		}
		else {
			$result = $db->query("SELECT * FROM cat_product ".($current_page!=""?"LIMIT ".($current_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");
		}
	}
	else {
		if ($current_page eq "all"){
			$result = $db->query("SELECT p.*, ".$sort_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$id."' AND p.p_show != '0' ORDER BY ".$sort);
		}
		else {
			$result = $db->query("SELECT p.*, ".$sort_.", pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$id."' AND p.p_show != '0' ORDER BY ".$sort." ".($current_page!=""?"LIMIT ".($current_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");
			#$result = $db->query("SELECT p.* FROM cat_category AS cat JOIN cat_category_links AS link ON(cat.c_id=link.id) JOIN products_alright AS p ON(link.p_cid = p.cat_id) WHERE cat.c_id ='".$id."'");
		}
	}
	foreach my $line(@$result){
		if($line->{'p_show'} ne "0"){
			$count++; my $mark="";
			if ($line->{'p_news'} eq "1"){$mark="new";}
			if ($line->{'p_hit'} eq "1"){$mark="hit";}
			if ($line->{'p_spec'} eq "1"){$mark="spec";}
			my $label = 0;
			if ($count == 3) {$label = "reflect"; $count="";}
			$products_cat .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, $c_alias, $line->{'p_price'}, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, $label, $mark, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "catalog", $line->{'p_img_url'}, $cat_name, $parent_id, "", "", $line->{'p_color_rel'});
		
		} else {$products_cat .="";}
	}

	# Страницы категории //
	
	my $i=1; my $p=""; my $pages="";
	while ($i <= $pagess) {
		if ($i > ($current_page-4) && $i < ($current_page-2)){
			$pages .= '<li><a href="/catalog/'.$c_alias.'/'.($i > 1?'page_'.$i.'':'').''.($brand_id > 0?'?brand='.$brand_id.'':'').'">'.$i.'</a></li>';
		}			
		elsif ($i > ($current_page-3) && $i < ($current_page+3) && $current_page > 2 or $current_page < 3 && $i < 6){
			if ($i == $current_page) {$p = '<li class="active"><a href="#">'.$current_page.'</a></li>&nbsp;';}
			elsif ($current_page == "" && $current_page ne "all") {$p = ''.($i == 1?'<li class="active"><a href="#">'.$i.'</a></li>&nbsp;':'<li><a href="/catalog/'.$c_alias.'/page_'.$i.''.($brand_id > 0?'?brand='.$brand_id.'':'').'">'.$i.'</a></li>&nbsp;').'';}
			else {$p = ''.($i == 1?'<li><a href="/catalog/'.$c_alias.''.($brand_id > 0?'?brand='.$brand_id.'':'').'">'.$i.'</a></li>&nbsp;':'<li><a href="/catalog/'.$c_alias.'/page_'.$i.''.($brand_id > 0?'?brand='.$brand_id.'':'').'">'.$i.'</a></li>&nbsp;').'';}
			$pages .= $p;
		}
		elsif ($i > ($current_page+2) && $i < ($current_page+4) && $current_page > 2 or $current_page < 3 && $i == 6){
			$pages .= '<li><a href="/catalog/'.$c_alias.'/page_'.$i.''.($brand_id > 0?'?brand='.$brand_id.'':'').'">'.$i.'</a></li>';
		}
		$i++;
	}
	
	if ($pagess < 2){
		$pages_show_bottom ='';
	}
	else {
		if (!$current_page){$current_page = 1;}
		$pages_show_bottom ='<ul class="pag">'.($current_page > 1?'<li class="prev"><a href="/catalog/'.$c_alias.'/page_'.($current_page-1).''.($brand_id > 0?'?brand='.$brand_id.'':'').'">Предыдущая</a></li>':'<li class="space"><span></span></li>').''.$pages.''.($current_page < ($pagess-3) && $pagess > 6?'<li><span>...</span></li><li><a href="/catalog/'.$c_alias.'/page_'.$pagess.''.($brand_id > 0?'?brand='.$brand_id.'':'').'">'.$pagess.'</a></li>':'').''.($current_page ne $pagess?'<li class="next"><a href="/catalog/'.$c_alias.'/page_'.($current_page+1).''.($brand_id > 0?'?brand='.$brand_id.'':'').'">Следующая</a></li>':'<li class="space"><span></span></li>').'</ul>';
	}
	
	# / Страницы категории //

	my $sort_price='<a href="#" class="price" sort="">Цене</a>';
	my $sort_update='<a href="#" class="update" sort="">Обновлению</a>';
	if ($sort_ eq "p.p_price"){
		$sort_price = '<a href="#" id="active" class="price" '.($sort eq "p.p_price ASC"?'sort="p_price ASC">Цене</a> <i>&uarr;</i>':'sort="p_price DESC">Цене</a> <i>&darr;</i>').'';
	}
	elsif ($sort_ eq "p.p_date_add"){
		$sort_update = '<a href="#" id="active" class="update" '.($sort eq "p.p_date_add ASC"?'sort="p_date_add ASC">Обновлению</a> <i>&uarr;</i>':'sort="p_date_add DESC">Обновлению</a> <i>&darr;</i>').'';		
	}	
	
	my $tabs_view="";
	if ($hide_products_view ne "1"){
		my $view_default="";
		if (cookie("view_products") eq ""){$view_default = ' class="active"';}	
		$tabs_view = '<ul class="tabs-view">
							<li class="view1"><a href="#"'.(cookie("view_products") eq "view1"?' class="active"':'').'>&nbsp;</a></li>
							<li class="view2"><a href="#"'.(cookie("view_products") eq "view2"?' class="active"':''.$view_default.'').'>&nbsp;</a></li>
						</ul>';
	}
	my $filter_price="";
	if ($hide_products_f_price ne "1"){
		$filter_price = '<div class="filter_price">
							<span class="name">Фильтр по цене:</span>
							<select name="f_price" onchange="jSboxFilterPrice();">
								<option class="0" value="0">Выбрать</option>
								<option class="to_1000" value="to_1000">до 1000 руб</option>
								<option class="to_3000" value="to_3000">до 3000 руб</option>
								<option class="to_5000" value="to_5000">до 5000 руб</option>
								<option class="to_10000" value="to_10000">до 10000 руб</option>
								<option class="from_10000" value="from_10000">от 10000 руб</option>
							</select>
						</div>';
	}
	
	# Вывод товаров //
	
	if ($ajax eq "ajax"){
		$products_list = build_ProductTags(1,0,"catalog").''.$products_cat.''.build_ProductTags(0,1,"catalog");
		if (cookie("filter_price") ne "" && cookie("filter_price_pointer") ne "" && $current_page eq "1"){
			if ($pages_show_bottom ne ""){$products_list .= '<div class="pages-bottom pages-double" style="display:none;">'.$pages_show_bottom.'</div>';}
		}
	}
	else {
		$products_list = build_ProductTags(1,0,"catalog").''.$products_cat.''.build_ProductTags(0,1,"catalog").''.$pages_show_bottom.''.$script_product;
	}
	
	if (ref($result) ne 'ARRAY') {
		if ($ajax eq "ajax" && cookie("filter_price") ne "" && cookie("filter_price_pointer") ne ""){
			$products_list='<div class="no_result" style="display:none;"><div class="clear"></div><p>Товаров нет удовлетворяющих параметрам фильтра.</p></div>';
		}
		else {$products_list='<div class="no_result"><div class="clear"></div><p>Товаров пока нет в данной категории.</p></div>';}
	}
	
	# / Вывод товаров //
	
    return $products_list;
}


# Подробная карточка товара

sub build_Product
{
	my $id = shift;
	my $parent_id = shift;
	my $sort = shift;
	my $product = "";
	$result = $db->query("SELECT * FROM cat_product WHERE p_id ='".$id."' LIMIT 1");
	foreach my $line(@$result){	
		my $desc_sm="";
		if ($line->{'p_desc_sm'} ne "") {
			$desc_sm = $line->{'p_desc_sm'};
		}
		
		my ($label1, $label2, $label3, $label4) = build_ProductLabel($id, $parent_id);
		
		$rand_num=rand(1);
		my $num_foto = 1000+$line->{'p_id'};	
		
		my $img_link = $dirs_catalog_www.'/'.$num_foto.'_preview.jpg?'.$rand_num;
		if ($resize_photo_single){$img_link = $dirs_catalog_www.'/'.$line->{'p_art'}.'.jpg?'.$rand_num;}
				
		my $image="";
		$image = '<div class="image">
				<div class="labels">'.$label1.''.$label2.''.$label3.''.$label4.''.build_ColorItems($line->{'p_color_rel'}, "big").'</div>
				'.($line->{'p_news'}?'<em class="label">NEW</em>':'').'
				'.($line->{'p_hit'}?'<em class="label hit">ХИТ</em>':'').'
				<span class="photo"><img onerror="this.src=\'/admin/site/img/no_photo_big.png\'" src="'.$img_link.'" alt="'.$line->{'p_art'}.', '.$line->{'p_name'}.'"></span>
			</div>';

		my $zoom="";
		if ($hide_products_zoom ne "1" && -e "$dirs_catalog_www2/$num_foto\_big.jpg" && -e "$dirs_catalog_www2/$num_foto\_normal.jpg"){			
			use Image::Magick;
			my $img = Image::Magick->new;		
			$img->Read("$dirs_catalog_www2/$num_foto\_big.jpg"); 
			my ($ox_big,$oy_big)=$img->Get('base-columns','base-rows');				
			if ($ox_big > 600 or $oy_big > 600){
				$zoom = "checked";
				my $img = Image::Magick->new;
				$img->Read("$dirs_catalog_www2/$num_foto\_normal.jpg"); 
				my ($ox,$oy)=$img->Get('base-columns','base-rows');
				$image = '<div class="foto zoom" style="width:'.$div_ox.'px; height:'.$div_oy.'px;"><a style="width:'.$ox.'px; height:'.$oy.'px;" title="'.$line->{'p_name'}.'" href="/files/catalog/'.$num_foto.'_big.jpg?'.$rand_num.'" id="zoom_big" class="cloud-zoom" rel="'.($pr_zoom_color eq "black"?'tint:\'#000000\', tintOpacity:0.2, ':'').'smoothMove:5, zoomWidth:'.$ox.', adjustY:0, adjustX:10"><img src="/files/catalog/'.$num_foto.'_normal.jpg?'.$rand_num.'" alt="'.$desc_sm.'"></a></div>';
			}
		}
		
		my $price_old="";
		if ($line->{'p_price_old'}){$price_old = $line->{'p_price_old'};}
		else {
			$price_old = $line->{'p_price'}*1.15;
		}
		
		my $desc_full = $line->{'p_desc_bottom'};
		if ($desc_full ne "" && $product_desc_ext eq "1"){
			$desc_full = '<div class="clear"></div><br>
			<div class="descript_full">
				'.($line->{'p_show_head'} eq "1"?'<h3>Подробное описание '.$line->{'p_name'}.'</h3>':'').'					
				'.$line->{'p_desc_bottom'}.'
			</div>';			
		} else {$desc_full="";}

		my $products_reviews="";
		if ($hide_products_reviews ne "1"){
			require "templates/products_reviews.cgi";
			$products_reviews = build_ProductReviews($line->{'p_id'});
		}			
		my $products_recomend="";
		if ($hide_products_recomend ne "1"){
			require "templates/products_recomend.cgi";
			$products_recomend = build_ProductRecomend($line->{'p_id'});
		}			
		my $navigation=""; my $neighboring="";
		if ($hide_products_navigation ne "1" or $hide_products_related ne "1"){
			require "templates/products_related.cgi";
			($navigation, $neighboring) = build_ProductRelated($sort, $line->{'p_alias'});
		}			
		my $products_viewed="";
		if ($hide_products_viewed ne "1"){
			require "templates/products_viewed.cgi";
			$products_viewed = build_ProductViewed();
		}
		
		my $social="";
		if ($hide_products_social ne "1"){
			$social = '<script type="text/javascript" src="//yandex.st/share/share.js" charset="utf-8"></script>
			<div class="yashare-auto-init social" data-yashareL10n="ru"
data-yashareType="link" data-yashareQuickServices="vkontakte,facebook,twitter,odnoklassniki,moimir,lj,gplus"></div>';			
		}
		
		my $techdata=""; my $related=""; my $pdf=""; my $num=""; my $pack=""; my $packnorm=""; my $unit="";
		my $res = $db->query("SELECT * FROM cat_product_fields WHERE p_id ='".$id."'");
		foreach my $item(@$res){
			if ($item->{'unic'} eq "1" && $item->{'field'} ne "Чертеж"){
				$num++;
				$techdata .='
				<tr'.($num == 1?' class="silver"':'').'>
					<td>'.$item->{'field'}.':</td>
					<td>'.$item->{'value'}.'</td>
				</tr>';
				if ($num == 2){$num="";}
			}
			if ($item->{'field'} eq "Связанные товары"){$related = $item->{'value'};}
			if ($item->{'field'} eq "Ссылка на PDF"){$pdf = $item->{'value'};}
			if ($item->{'field'} eq "Вид упаковки"){$pack = $item->{'value'};}
			if ($item->{'field'} eq "Норма упаковки"){$packnorm = $item->{'value'};}
			if ($item->{'field'} eq "Единица измерения"){$unit = $item->{'value'};}
		}			
		if (!$packnorm) {$packnorm = 1;}
		if (!$unit) {$unit = "шт";}
		
		if ($packnorm =~/(\d+)\.5/){
			$packnorm = $packnorm*2;
		}		
		
		# // Наличие на складе //
		
		my $p_count="";
		if ($hide_products_avail ne "1"){
			$p_count = '<div class="art">Наличие на складе: <em>'.($line->{'p_count'} ne ""?''.$line->{'p_count'}.' шт.':'отсутствует').'</em></div>';
		}						
		
		# Верстка карточки товара //
		
		$product .='<div class="product-info">
						'.$image.'
						<div class="info-box">
							<div class="info">
								<div class="price-holder">
									<strong class="price"><span>'.price_trans($line->{'p_price'}).'</span> р.</strong>
									'.(!$price_old?'<span class="old-price">Старая цена: <strong>'.price_old_trans($price_old).'</strong></span>':'').'
									'.($unit?'<span class="price-title">Цена за 1 '.$unit.'</span>':'').'
								</div>
								'.($line->{'p_art'}?'<span class="art">Артикул: <strong>'.$line->{'p_art'}.'</strong></span>':'').'
								<p>'.$desc_sm.'
								   '.($packnorm > 0?'<br><span class="packnorm center">Норма отгрузки: <strong>'.$packnorm.' '.$unit.'</strong></span>':'').'
								</p>';
								
		if ($line->{'p_show'} eq "1"){
		
							$product .='
								<form class="number">
									<fieldset>
										<a class="minus" href="#">-</a>
										<input class="text count" type="text" value="1" autocomplete="off">
										<a class="plus" href="#">+</a>
									</fieldset>
									<ul>
										<li class="active"><span>'.$packnorm.'</span></li>
										<li><span>'.($packnorm*2).'</span></li>
										<li><span>'.($packnorm*5).'</span></li>
										<li><span>'.($packnorm*10).'</span></li>
									</ul>
								</form>
								<a href="#" class="add buy_product" data-pack="'.$packnorm.'" data-unit="'.$unit.'" price="'.($line->{'p_price'} > 0?''.$line->{'p_price'}.'':'0').'" p_art="'.$line->{'p_art'}.'">В корзину</a>
								<a href="#" class="fast buy_quick" p_id="'.$line->{'p_id'}.'">Купить быстро в 1 клик</a>';
		}
		elsif ($line->{'p_show'} ne "1"){
			$product .='<div class="arhive">Нет на складе</div>';
		}
					$product .='			
							</div>
							<div class="prev-list">
								<ul>
									<li class="list01 city">
										<div class="ico"><img src="/img/ico22.png" alt="#" width="64" height="52" /></div>
										<div class="text">11 городов<br />филиалов<br><a id="cityContacts" href="#">найти свой</a></div>
									</li>
									<li class="list02">
										<div class="ico"><img src="/img/ico16.png" alt="#" width="64" height="52" /></div>
										<div class="text">Доставка <br />По России</div>
									</li>
									<li class="list03">
										<div class="ico"><img src="/img/ico17.png" alt="#" width="64" height="56" /></div>
										<div class="text">Прямые<br /> поставки <span>производителя</span></div>
									</li>
									<li class="list04">
										<div class="ico"><img src="/img/ico18.png" alt="#" width="64" height="55" /></div>
										<div class="text"><span>Постоянным</span> клиентам скидки</div>
									</li>
								</ul>
								<span class="registration">Для получения скидок <br />пройдите <a href="#" id="reg" data-tag="register">регистрацию</a><br /> не более минуты!</span>
								<div class="sales-link">
									<a target="_blank" href="/pages/sales">
										<i>Хочу скидку</i>
										Перейти к условиям
									</a>
								</div>
							</div>
							'.($pdf?'<a class="pdf" target="_blank" href="'.$dirs_catalog_www.'/pdf/'.$line->{'p_art'}.'.pdf">Посмотреть описание<br> в формате PDF</a>':'').'
						</div>
					</div>';
				
					#if ($hide_products_navigation ne "1"){$product .= $navigation;}

					# Фотогалерея						
					open(BO, "admin/$dirs/set_catalog"); @set_catalog = <BO>; close(BO);
					foreach my $line(@set_catalog){chomp($line);
					my ($ajax_save_old_, $count_more_, $cat_desc_top_, $cat_desc_bottom_, $pr_desc_ext_, $content_wide_, $set_foto_hide_) = split(/\|/, $line);
					$count_more =qq~$count_more_~;
					$product_desc_ext =qq~$pr_desc_ext_~;}			
					
					my $gallery="";	
					if ($hide_more_photo ne "1"){
						my $num="";
						for ($num=1; $num < $count_more+1; $num++) {
							if(-e "$dirs_catalog_www2/$num_foto\_$num\_big.jpg"){
								$gallery .='<div class="item"><a href="/files/catalog/'.$num_foto.'_'.$num.'_big.jpg"><img src="/files/catalog/'.$num_foto.'_'.$num.'_small.jpg" alt="'.$line->{'p_name'}.'"/></a></div>';
							}
						}
						if ($photo_more ne ""){$photo_more = '<br><br><div class="photo_more">'.$photo_more.'</div>';}
					}
					if (!$gallery && ($parent_id eq "2" or $parent_id eq "3" or $parent_id eq "4")){
						my $folder=""; my $counts="";
						if ($parent_id eq "2"){$folder="lenta"; $counts = 27;}
						elsif ($parent_id eq "3"){$folder="lampa"; $counts = 15;}
						elsif ($parent_id eq "4"){$folder="svet"; $counts = 14;}
						for ($num=1001; $num < ($counts+1001); $num++) {
							$gallery .='<div class="item"><a href="/files/catalog/'.$folder.'/'.$num.'_big.jpg"><img src="/files/catalog/'.$folder.'/'.$num.'_small.jpg" alt=""/></a></div>';
						}
					}
					if ($gallery){
						$product .= '
						<div class="product-gallery-wrap">
							<h2>Продукция в интерьере</h2>
							<div class="product-gallery scroller">
								<div class="product-gallery-list owl-carousel">	
								'.$gallery.'
								</div>
							</div>
						</div>';
					}

					# Обратный звонок
					$product .= '
					<div class="phone-holder">
						<div class="phone-box">
							<strong>Уточняйте оптовые цены!</strong>
							<a href="#" id="callback">Уточнить оптовую цену</a>
							<a class="phone" href="tel:88007004734">8 800 700-47-34</a>
						</div>
						<a class="callback02" href="#">Заказать обратный звонок</a>
					</div>';
					
					if ($line->{'p_desc_top'}){
						$product .= '<div class="desc_product">'.$line->{'p_desc_top'}.'</div>';						
					}

					# Связанные по цвету товары				
					if ($line->{'p_color_rel'} && $line->{'p_show'} eq "1"){
						$product .= build_ProductColorRelated($line->{'p_color_rel'}, $line->{'p_price'}, $pack, $packnorm, $unit);
					}	

					# Технические характеристики						
					if ($techdata){
						$product .= '
							<div class="characteristics">
								<h2>Посмотреть технические характеристики<span>'.$line->{'p_name'}.'</span>:</h2>
								<table>
									<tbody>
										'.$techdata.'
									</tbody>
								</table>
							</div>';
					}					
					
					if ($hide_products_recomend ne "1"){$product .= $products_recomend;}
					
					if (!$products_recomend){
						require "templates/products_related.cgi";
						($navigation, $neighboring) = build_ProductRelated($sort, $line->{'p_art'}, $related);
						$product .= $neighboring;
					}
					
					#if ($hide_products_reviews ne "1"){$product .= $products_reviews;}

					#if ($hide_products_related ne "1"){$product .= $neighboring;}

					#if ($hide_products_viewed ne "1"){$product .= $products_viewed;}
					
					
		# / Верстка карточки товара //
	}
	
	if (ref($result) eq 'ARRAY' ){	
		$product = $product.''.$script_product;
	} else {$product='<p>Товар не найден.</p>';}
	
    return $product;
}

sub price_old_trans {
	my $price_old = shift;
	if ($hide_products_old_price ne "1" && $price_old > 0){
		$price_old = sprintf("%.0f",$price_old);
		$price_old = $price_old." руб.";
	} else {$price_old="";}	
	return $price_old;				
}			

sub price_trans {
	my $price = shift;
	my $fraction = shift;
	if ($price > 0){
		if ($fraction){
			$price = sprintf("%.2f",$price);
		}
		else {
			$price = sprintf("%.0f",$price);
		}
		$price =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
	}
	else {$price="Цена по запросу";}	
	return $price;
}

sub build_ProductColorRelated
{
	my $data = shift;
	my $price = shift;
	my $pack = shift;
	my $packnorm = shift;
	my $unit = shift;
	
	if ($data){
		my $result=""; my $i=0;
		$data .=";";
		while ($data =~ m/(\d+)\[(.+?)\]\;/g){
			$i++;
			my $art = $1;
			my $colors = $2;
			my $colors_ = $2;
			my $num = 0;
			if ($colors =~ /\|/){
				$data_colors = $colors .="|";
				$colors="";
				while ($data_colors =~ m/(.+?)\|/g){
					$num++;
					$colors .='<ins class="'.$1.'">&nbsp;</ins>';
				}
			}
			else {
				$num++;
				$colors = '<ins class="'.$colors.'">&nbsp;</ins>';
			}
			if ($num eq "1"){$num = "one";}
			elsif ($num eq "2"){$num = "two";}
			elsif ($num eq "3"){$num = "three";}
			
			$result .='<tr data-price="'.$price.'" data-art="'.$art.'">
							<td class="art">'.$art.'</td>								
							<td class="name">'.getColorRus($colors_, "bold").'</td>
							<td class="color"><label class="color-related color '.$num.'">'.$colors.'</label></td>
							<td class="price"><span>'.price_trans($price, 1).'</span> руб.<em>&times;</em></td>
							<td class="count">
								<div class="p-count">
									<input name="'.$art.'" data-value="'.$packnorm.'" value="'.$packnorm.'" class="count" autocomplete="off">
									<em>'.$pack.' '.$packnorm.' '.$unit.'</em>
								</div>
							</td>
							<td class="price"><span class="price-total">'.price_trans(($price*$packnorm), 1).'</span> руб.</td>
							<td class="add_basket"><span class="add_basket_related">В корзину</span></td>
						</tr>';
		}
		if ($result){
			$result = '<div id="products-table" class="related">
						<table>
							<tbody>
								'.$result.'
							</tbody>
						</table>
					   </div>';					   
			return $result;
		}
	}
}

1;