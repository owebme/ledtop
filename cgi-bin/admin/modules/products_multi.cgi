use Core::DB;

$cat_edit=param('cat_edit');

if (!$cat_edit){
	open(BO, "../$dirs/set_cat_select"); @cat_current = <BO>; close(BO);
	foreach my $line(@cat_current){chomp($line);
	my ($cat_current_, $curent_page_) = split(/\|/, $line);
		$cat_edit=qq~$cat_current_~;
	}	
}

my $db = new Core::DB();

my $products_type="";
if ($hide_products_type ne "1"){
	$products_type ='<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_type&par=new"><span>'.$pr_type_name.'</span></a></li>';
}
$new_pages =qq~<li class="first activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category"><span>Категории</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Доб. товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category&par=new"><span>Доб. категорию</span></a></li>
$products_type~;

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
		<div id="content" style="position:relative;">
		<div id="multi">
		<a class="multi-add" href="/cgi-bin/admin/engine/index.cgi?adm_act=products">Вернуться в каталог</a>
		<div class="batch_csv"><span><em>Выгрузить CSV</em><div class="batch_csv_submenu"><a href="/export/csv/catalog" class="export_catalog">Выгрузить весь каталог</a><a href="/export/csv/category" class="export_category">Выгрузить данную категорию</a></div></span><span><input type="file"><em>Загрузить CSV</em></span></div>~;
		
my $sort_category=""; my $sort_products="";
open(BO, "../$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
foreach my $line(@select_sort){chomp($line);
my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
$sort_category=qq~$select_sort_cat_~;
$sort_products=qq~$select_sort_product_~;}

my $select_category=""; my $first_category="";
my $result = $db->query("SELECT cat_category.c_id, cat_category.c_name FROM cat_category WHERE c_pid=0 ORDER BY ".$sort_category.";");
foreach my $item(@$result){
	if (!$first_category){
		$first_category = $item->{c_id};
		if ($cat_edit > 0){$cat_edit = $cat_edit;}
		else {$cat_edit = $first_category}
	}
	$select_category .= '<option value="'.$item->{c_id}.'"'.($cat_edit==$item->{c_id}?' selected':'').'>'.$item->{c_name}.'</option>';
	if (my $sub = recMenu($item->{c_id}, 0)){
		$select_category .= $sub;
	}	
}
sub recMenu {
	my $id = shift;
	my $level = shift;
	my $select_cat="";
	sub nbsp {my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';} return $t.'&mdash; ';}
	my $result = $db->query("SELECT cat_category.c_id, cat_category.c_name FROM cat_category WHERE c_pid='".$id."' ORDER BY ".$sort_category.";");
	if ($result){
		foreach my $item(@$result){
			$select_cat .= '<option value="'.$item->{c_id}.'"'.($cat_edit==$item->{c_id}?' selected':'').'>'.nbsp($level).$item->{c_name}.'</option>';
			if (my $sub = recMenu($item->{c_id}, $level+1) ){
				$select_cat .= $sub;
			}
		}		
	}
	else {
		return 0;
	}	
	return $select_cat;
}

mkdir "$dirs_catalog/multi", 0755;
mkdir "$dirs_catalog/multi/upload", 0755;

$content_html .='<div class="products_add_table" data-cat="'.$cat_edit.'"><table>';
$content_html .='<thead><tr><th class="del"></th><th class="art">Артикул</th><th class="name">Название</th><th class="price">Цена</th><th class="count">Кол-во</th><th class="foto">Фотография</th><th class="size"></th></tr></thead>';
$content_html .='<tbody>';

use Image::Magick;

my $sort_ = $sort_products;
$sort_=~ s/\sASC$//g;
$sort_=~ s/\sDESC$//g;
if ($sort_ eq "p_pos"){$sort_products = "pl.".$sort_products; $sort_ = "pl.".$sort_;}
else {$sort_products = "p.".$sort_products; $sort_ = "p.".$sort_;}

my $num=""; my $field="";
if ($cat_edit){
	my $result = $db->query("SELECT p.*, ".$sort_.", c.c_name FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id = '".$cat_edit."' AND pl.cat_main = '1' ORDER BY ".$sort_products);
	if ($result){
		foreach my $item(@$result){
			$num++;
			my $rand_num=rand(1);
			my $image=""; my $img_small=""; my $img_big="";
			if ($resize_photo_single){
				if (-e "$dirs_catalog/".$item->{p_art}.".jpg"){
					$image = 1;
				}			
				$img_small = $img_big = $dirs_catalog_www.'/'.$item->{p_art}.'.jpg?'.$rand_num;
			}
			else {
				if (-e "$dirs_catalog/".($item->{p_id}+1000)."_small.jpg"){
					$image = 1;
				}			
				$img_small = $dirs_catalog_www.'/'.($item->{p_id}+1000).'_small.jpg?'.$rand_num;
				$img_big = $dirs_catalog_www.'/'.($item->{p_id}+1000).'_small.jpg?'.$rand_num;
			}
			
			$field .='<tr data-id="'.$item->{p_id}.'" data-index="'.$num.'">
						<td></td>
						<td class="art"><input type="text" value="'.$item->{p_art}.'"></td>
						<td class="name"><input type="text" value="'.$item->{p_name}.'">'.($item->{p_desc_sm} ne ""?'<div class="desc"><a href="#" class="desc_add" id="close">Показать описание</a></div><textarea>'.$item->{p_desc_sm}.'</textarea>':'<div class="desc"><a class="desc_add" href="#">Добавить описание товара</a></div">').'</td>
						<td class="price"><input type="text" value="'.$item->{p_price}.'"></td>
						<td class="count"><input type="text" value="'.$item->{p_count}.'"></td>
						<td class="foto"><img '.($image?'src="'.$img_small.'" style="height:52px;"':'src="/admin/img/product_gallery_no_photo.png" style="height:52px; border-radius:5px"').' alt=""><div class="container"><div class="input img" title="Кликните для смены картинки"><input type="file" class="file"></div><div class="foto'.($num eq "1"?' help_foto':'').'"></div></div></td>
						<td class="size"><div class="size"><a href="'.$img_big.'" onclick="return hs.expand(this)" class="highslide">'.($image?'Увеличить':'').'</a></div></td>
					</tr>';			
		}
	}
}

opendir (DBDIR, "$dirs_catalog/multi"); @list_dir = readdir(DBDIR); close DBDIR;
foreach $line_wall(@list_dir) {
	chomp ($line_wall);
	if ($line_wall ne "." && $line_wall ne "..") {
		my ($name, $exec) = split(/\./, $line_wall);
		if ($name ne "" && $exec ne ""){
			$num++;
			my $rand_num=rand(1);
			my $img = Image::Magick->new;
			my ($width, $height, $size, $format) = $img->Ping($dirs_catalog."/multi/".$name.".".$exec);			
			$field .='<tr data-index="'.$name.'">
						<td></td>
						<td class="art"><input type="text"></td>
						<td class="name"><input type="text"><div class="desc"><a class="desc_add" href="#">Добавить описание товара</a></div></td>
						<td class="price"><input type="text"></td>
						<td class="count"><input type="text"></td>
						<td class="foto"><img style="height:52px;" src="'.$dirs_catalog_www.'/multi/'.$name.'.'.$exec.'?'.$rand_num.'" alt=""><div class="container"><div class="input img" title="Кликните для смены картинки"><input type="file" class="file"></div><div class="foto'.($num eq "1"?' help_foto':'').'"></div></div></td>
						<td class="size"><div class="size"><a href="'.$dirs_catalog_www.'/multi/'.$name.'.'.$exec.'?'.$rand_num.'" onclick="return hs.expand(this)" class="highslide">'.($width > 0 && $height > 0?''.$width.' x '.$height.'':'не определено').'</a>'.($width < 250 && $width > 0?'<p class="red">(изображение малого размера)</p>':'').'</div></td>
					</tr>';
		}
	}
}


$content_html .='<tr data-index="0" class="copy">
					<td></td>
					<td class="art"><input type="text"></td>
					<td class="name"><input type="text"><div class="desc"><a class="desc_add" href="#">Добавить описание товара</a></div></td>
					<td class="price"><input type="text"></td>
					<td class="count"><input type="text"></td>
					<td class="foto"><span><em>Перетащите картинку сюда</em></span><div class="container"><div class="input"><input type="file" class="file"></div><div class="foto"></div></div></td>
					<td class="size"></td>
				</tr>';

if ($field ne ""){
	$content_html .= $field;
}
if ($field eq "" or !$line_wall){
$content_html .='<tr data-index="'.($num?''.($num+1).'':'1').'">
					<td></td>
					<td class="art"><input type="text"></td>
					<td class="name"><input type="text"><div class="desc"><a class="desc_add" href="#">Добавить описание товара</a></div></td>
					<td class="price"><input type="text"></td>
					<td class="count"><input type="text"></td>
					<td class="foto help_foto"><span><em>Перетащите картинку сюда</em></span><div class="container"><div class="input"><input type="file" class="file"></div><div class="foto"></div></div></td>
					<td class="size"></td>
				</tr>';
}

$content_html .='</tbody></table><a href="#" class="add_tr">+ <span>Добавить поле</span></a>';

if ($select_category ne ""){
$content_html .='<div class="batch_add"><div class="select_category"><select class="category">'.$select_category.'</select></div><input type="button" class="button" value="Сохранить"></div>';
}

$content_html .='</div><div class="clear"></div>
<script type="text/javascript" src="/admin/lib/help/catalog/products_multi.js"></script>	
<script type="text/javascript" src="/admin/js/jquery.mousewheel.min.js"></script>
<script type="text/javascript" src="/admin/scripts/yaimages/jcarousellite.mod.js"></script>
<script type="text/javascript" src="/admin/scripts/yaimages/yaimages.js"></script>
<script type="text/javascript" src="/admin/js/highslide/highslide.js"></script>
<link rel="stylesheet" type="text/css" href="/admin/js/highslide/highslide.css" />
<script type="text/javascript">
	hs.graphicsDir = "/admin/js/highslide/graphics/";
	hs.wrapperClassName = "wide-border";
</script>';

if ($hide_products_yaimages ne "1"){
$content_html .='
	<div class="yaimages">
		<div class="search">
			<form>
				<input type="text" id="word_search" onblur="if (this.value==\'\'){this.value=\'Поиск:\'}" onfocus="if (this.value==\'Поиск:\') this.value=\'\';" value="Поиск:">
				<input type="submit" value="Поиск" id="search">
			</form>
		</div>';
}
else {
$content_html .='	
	<div class="yaimages" id="buffer">';
}
$content_html .='
		<div class="add_images">
			<div class="input"><input type="file" name="file" class="add_images" multiple="true" /><span>картинки</span></div>
		</div>
		<div class="clear"></div>
		<div class="container_slider">
			<i class="bg_left"></i>
			<i class="bg_right"></i>
			<span class="arrow_left"></span>						
			<span class="arrow_right"></span>
			<div class="images">
				<ul>
					'.($hide_products_yaimages ne "1"?'':'<li class="buffer">Буфер изображений</li>').'
				</ul>
			</div>
		</div>
	</div>';

$content_html.= qq~
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;


-1;