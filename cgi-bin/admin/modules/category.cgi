use Core::DB::Catalog;
use Core::DB::Work;

my $catalog = new Core::DB::Catalog();
my $db = new Core::DB();

	$menu_act=param('menu_act');
	$num_edit=param('num_edit');
	$settings=param('settings');
	$name=param('name');
	$name=Core::DB::Work::trans_new($name);		
	$name_short=param('name_short');
	$name_short=Core::DB::Work::trans_new($name_short);		
	$date_add=param('date_add');
	$date_up=param('date_up');
	$title=param('title');
	$meta_desc=param('meta_desc');	
	$meta_key=param('meta_key');		
	$elm1=param('elm1');
	$elm1=Core::DB::Work::trans_html($elm1);
	$elm1_sm=param('elm1_sm');
	$elm1_sm=Core::DB::Work::trans_html($elm1_sm);	
	$desc_sm=param('desc_sm');
	$desc_sm=Core::DB::Work::trans_html($desc_sm);		
	$parent=param('parent');
	$sort=param('sort');
	$alias=param('alias');
	if ($alias eq "") {$alias=Core::DB::Work::translit($name)}
	$redirect=param('redirect');
	if ($redirect ne "") {$redirect =~ s/^\///g; $redirect = "/".$redirect;}	
	$show=param('show');
	$show_menu=param('show_menu');
	$show_head=param('show_head');
	$par=param('par');
	$image=param('image');
	$img_ox=param('img_ox');
	$img_oy=param('img_oy');
	$maket=param('maket');
	$hide_child=param('hide_child');
	$show_child_count=param('show_child_count');

	if($show eq "on") {$show="0";} else {$show="1";};
	if($hide_child eq "on") {$hide_child="1";} else {$hide_child="0";};
	if($show_child_count == 0 or $show_child_count < 0) {$show_child_count="";};
	if($show_child_count ne "" && $hide_child == 1) {$hide_child="0";};	
	if($maket eq "") {$maket="1";};		
	
	my $products_type="";
	if ($hide_products_type ne "1"){
		$products_type ='<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_type&par=new"><span>'.$pr_type_name.'</span></a></li>';
	}

if ($num_edit eq "") {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
$products_type~;
} else {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
$products_type~;
}
if ($par) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
$products_type~;
}
if ($settings) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
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
		<div id="content" style="position:relative">
		<div id="pages">~;
		
if (!$settings) {		
		$content_html .=qq~
			<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />
			<div class="catalog-btn-group">
				<div class="btn-group">
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog" class="btn">Привязка</a>
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog_providers" class="btn">Поставщики</a>
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=category" class="btn active">Категории</a>
				</div>	
			</div><br><br>
			<script type="text/javascript" src="/admin/js/ui-jquery/jquery.ui.nestedSortable.js"></script>		
			<script type="text/javascript" src="/admin/lib/category.js"></script>~;
}		

	if( param('posup') ne "" ){
		$catalog->PosUpCat($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";		
	}
	
	if( param('posdown') ne "" ){
		$catalog->PosDownCat($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";			
	}
	
	if( $lamp eq "on" ){
		$catalog->lamp_on_cat($num_edit);
		$num_edit="";
		$parents="";
		$list_older="";	
	}

	if( $lamp eq "off" ){
		$catalog->lamp_off_cat($num_edit);
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

	if ($menu_act eq "") {
		if($num_edit ne ""){
			my $category = $catalog->getCat($num_edit);
			$parent = $category->{c_pid};
			$ok_name_old = $category->{c_name};
			$ok_name_old=Core::DB::Work::trans_edit($ok_name_old);	
			$ok_name_short_old = $category->{c_name_short};
			$ok_name_short_old=Core::DB::Work::trans_edit($ok_name_short_old);
			$ok_title_old = $category->{c_title};
			$ok_meta_desc_old = $category->{c_meta_desc};
			$ok_meta_key_old = $category->{c_meta_key};				
			$ok_alias_old = $category->{c_alias};
			$ok_redirect_old = $category->{c_redirect};
			$ok_sort_old = $category->{c_pos};
			$ok_elm_old[0] = $category->{c_desc_bottom};
			$ok_elm_sm_old[0] = $category->{c_desc_top};
			$ok_desc_sm_old[0] = $category->{c_desc_sm};
			$ok_show_old = $category->{c_show};
			$ok_show_menu_old = $category->{c_show_menu};
			$ok_show_head_old = $category->{c_show_head};
			$ok_hide_child_old = $category->{c_hide_child};
			$ok_show_child_count_old = $category->{c_show_child_count};
			$ok_maket_old = $category->{c_maket};			
			$today=$category->{c_date_up};
			$ok_date_add_old=$category->{c_date_add};

			if ($ok_show_child_count_old eq "0") {$ok_show_child_count_old="";}	

		}

		open(BO, "../$dirs/set_catalog"); @set_catalog = <BO>; close(BO);
		foreach my $line(@set_catalog){chomp($line);
		my ($ajax_save_old_, $count_more_, $cat_desc_top_, $cat_desc_bottom_, $pr_desc_ext_, $content_wide_) = split(/\|/, $line);
		$category_desc_top =qq~$cat_desc_top_~;
		$category_desc_bottom =qq~$cat_desc_bottom_~;
		$content_wide =qq~$content_wide_~;}
		
	} elsif ($menu_act eq "ok") {
	
		if ($num_edit eq ""){
			my $db = new Core::DB();
			my $result = $db->query("SELECT c_alias FROM cat_category WHERE c_alias = '".$alias."';");
			if (ref($result) eq 'ARRAY'){$alias = $alias."2";}
			elsif ($parent ne "0"){
				my $p_alias ="";
				my $res = $db->query("SELECT c_id, c_alias FROM cat_category WHERE c_id = '".$parent."';");		
				foreach my $item(@$res){
					$p_alias = $item->{c_alias};
				}
				$alias = $p_alias."/".$alias;
			}
		}
	
		my %params = (
					'c_name' => "$name",
					'c_name_short' => "$name_short",
					'c_pos' => $sort,
					'c_pid' => $parent,
					'c_desc_bottom' => "$elm1",
					'c_desc_top' => "$elm1_sm",
					'c_desc_sm' => "$desc_sm",
					'c_title' => "$title",
					'c_meta_desc' => "$meta_desc",
					'c_meta_key' => "$meta_key",					
					'c_date_up' => "$today",
					'c_date_add' => "$date_add",			
					'c_show' => $show,
					'c_show_head' => $show_head,
					'c_show_menu' => $show_menu,
					'c_hide_child' => "$hide_child",
					'c_show_child_count' => "$show_child_count",						
					'c_alias' => $alias,
					'c_redirect' => $redirect,
					'c_maket' => "$maket",
			);
			
		if ($hide_category_photo ne "1"){
		
			open OUT, (">$dirs_catalog/category/settings.txt");
				print OUT "$img_ox|$img_oy"; 
			close(OUT);		
			
			if ($image ne ""){
		
				my $max_num=""; my $name_file_max="";
				my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'cat_category';");
				foreach my $item(@$result){	
					$max_num = $item->{Auto_increment};
					$name_file_max = $max_num+1000;			
				}

				if ($num_edit != "") {$name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$name_file_max="1001"}}

				open OUT, (">$dirs_catalog/category/$name_file_max\.png");
				 binmode (OUT);
				 while (<$image>) { print OUT "$_"; } 
				close(OUT);
				
				%configconsts = (
					'img_resize' => [$img_ox,$img_oy]	
				);

				use Image::Magick;
				
				my $image = Image::Magick->new;
				$image->Read("$dirs_catalog/category/$name_file_max\.png"); 
				($ox,$oy)=$image->Get('base-columns','base-rows'); 				
			
				$division = $configconsts{'img_resize'}[0]/$configconsts{'img_resize'}[1];
				
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
				$image->Write("$dirs_catalog/category/$name_file_max\.png");
			}
		}
		
		if($num_edit ne ""){
			$catalog->editCat($num_edit, \%params);
			ClearCache("../..");
		} else {
			%params = (%params,
				'c_name_org' => "$name"
			);
			$catalog->addCat(\%params);
			ClearCache("../..");
		}		
		
		my $res;
		if( ref($res) eq 'ARRAY' ){
			$content_html=qq~$content_html<div class="save_page">Категория "$name" сохранена.</div>~;
			$num_edit="";
			$parents="";
			$menu_act="";
			$list_older="";			
		} else {
			$content_html=qq~$content_html<div class="save_page">Категория "$name" сохранена.</div>~;
			$num_edit="";
			$parents="";
			$menu_act="";
			$list_older="";				
		}

	}	
	elsif ($menu_act eq "set_sort")  {
	
		$select_sort_cat=param('select_sort_cat');
		$select_sort_product=param('select_sort_product');
		$ajax_save=param('ajax_save');
		$img_url=param('img_url');
		$count_pages_admin=param('count_pages_admin');
		$count_pages_site=param('count_pages_site');
		$count_more_photo=param('count_more_photo');
		$category_desc_top=param('category_desc_top');
		$category_desc_bottom=param('category_desc_bottom');
		$product_desc_ext=param('product_desc_ext');
		$content_wide=param('content_wide');
		$set_foto_hide=param('set_foto_hide');
		$watermark_pos=param('watermark_pos');
		$watermark_opacity=param('watermark_opacity');
		$watermark_big=param('watermark_big');
		$watermark_normal=param('watermark_normal');
		$watermark_small=param('watermark_small');
		$watermark_text=param('watermark_text');
		$watermark_size=param('watermark_size');
		$watermark_color=param('watermark_color');
		
		if($ajax_save eq "on") {$ajax_save="1";} else {$ajax_save="0";};
		if($category_desc_top eq "on") {$category_desc_top="1";} else {$category_desc_top="0";};
		if($category_desc_bottom eq "on") {$category_desc_bottom="1";} else {$category_desc_bottom="0";};
		if($product_desc_ext eq "on") {$product_desc_ext="1";} else {$product_desc_ext="0";};
		if($category_desc_top eq "0" && $category_desc_bottom eq "0"){$category_desc_bottom="1";}
		if($count_more_photo eq "") {$count_more_photo="3";};
		if($content_wide eq "on") {$content_wide="1";} else {$content_wide="0";}
		if($set_foto_hide eq "on") {$set_foto_hide="1";} else {$set_foto_hide="0";}
		if($watermark_big eq "on") {$watermark_big="1";} else {$watermark_big="0";}
		if($watermark_normal eq "on") {$watermark_normal="1";} else {$watermark_normal="0";}
		if($watermark_small eq "on") {$watermark_small="1";} else {$watermark_small="0";}
		if($watermark_opacity eq "OFF"){$watermark_opacity = 0;}
		else {$watermark_opacity =~ s/\%//g;}		
		
		$watermark_color = "#".$watermark_color;
		
		open OUT, (">../$dirs/sort_catalog");
			print OUT "$select_sort_cat|$select_sort_product"; 
		close(OUT);	
		open OUT, (">$dirs_catalog/page_settings.txt");
			print OUT "$count_pages_admin|$count_pages_site"; 
		close(OUT);	
		open OUT, (">../$dirs/set_catalog");
			print OUT "$ajax_save|$count_more_photo|$category_desc_top|$category_desc_bottom|$product_desc_ext|$content_wide|$set_foto_hide|$img_url"; 
		close(OUT);
			
		if ($hide_products_watermark ne "1"){
			open OUT, (">$dirs_catalog/watermark.txt");
				print OUT "$watermark_pos|$watermark_opacity|$watermark_big|$watermark_normal|$watermark_small|$watermark_text|$watermark_size|$watermark_color"; 
			close(OUT);			
		}

		ClearCache("../..");
	
		$content_html=qq~$content_html<div class="save_page">Настройки сохранены.</div>~;	
	}
	
	if ($hide_category_photo ne "1"){
	open(BO, "$dirs_catalog/category/settings.txt"); my @categories = <BO>; close(BO);
		foreach my $linee(@categories)
			{
		chomp($linee);
		my ($img_ox_, $img_oy_) = split(/\|/, $linee);
		$img_ox=qq~$img_ox_~;
		$img_oy=qq~$img_oy_~;
			}		
	}

sub treeCat
{
	use Core::DB;
	my $self = new Core::DB();

	my $globalid = shift || undef;
	my $parent = shift || undef;
	
	my $sort="";
	open(BO, "../$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
	foreach my $line(@select_sort){chomp($line);
	my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
	$sort=qq~$select_sort_cat_~;}
	
	my $tree = "";
	$tree .= '<ul class="level0">';
	my $parents = "";
	my $result = $self->query("SELECT * FROM cat_category WHERE c_pid=0 ORDER BY ".$sort.";");
	foreach my $item(@$result){
		$tree .= '<li name="'.$item->{c_name}.'" c_id="'.$item->{c_id}.'" c_pid="'.$item->{c_pid}.'" c_pos="'.$item->{c_pos}.'" '.($item->{c_show_menu}==1?'':'class="off"').'><span class="move" '.($sort eq "c_pos ASC"?'><a class="up" href="#" title="Поднять вверх '.$item->{c_name}.'"></a><a class="down" href="#" title="Опустить вниз '.$item->{c_name}.'"></a>':'id="off">').'</span><a class="lamp" href="#" '.($item->{c_show_menu}==1?'title="Скрыть категорию"':'title="Сделать активной" style="opacity:0.5"').' '.$item->{c_name}.'"></a><a href="#" class="del" title="Удалить категорию '.$item->{c_name}.'"></a>';
		$tree .= '<a class="name" title="'.($item->{c_redirect} ne ""?'Редирект: /catalog/'.$item->{c_alias}.' на '.$item->{c_redirect}.'':'Страница: /catalog/'.$item->{c_alias}.'').'" href="?adm_act=category&num_edit='.$item->{c_id}.'">'.$item->{c_name}.'</a>';
		if ($num_edit == $item->{c_id}) {$parents .='';}
		else {$parents .= '<option value="'.$item->{c_id}.'" '.($parent==$item->{c_id}?'selected':'').' '.($globalid==$item->{c_id}?'disabled':'').'>'.$item->{c_name}.'</option>';}
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
		
			$result_parent = $db->query("SELECT * FROM cat_category WHERE c_id='".$id."'");
			my $hide_child="";
			my $show_child_count="";
			if($result_parent){ 
				foreach my $items(@$result_parent){
					$hide_child = $items->{c_hide_child};
					$show_child_count = $items->{c_show_child_count};
				}
			}
			if ($hide_child == 1) {$hide_child="class='hide'"} else {$hide_child=""};		
		
		my $result = $self->query("SELECT * FROM cat_category WHERE c_pid='".$id."' ORDER BY ".$sort.";");
		if($result){
			my $i_cat_old="";
			foreach my $item2(@$result){
				$i_cat_old++;
			}
			my $i_cat="";
			foreach my $item(@$result){
				$i_cat++;
				$text .= '<li name="'.$item->{c_name}.'" c_id="'.$item->{c_id}.'" c_pid="'.$item->{c_pid}.'" c_pos="'.$item->{c_pos}.'" '.($item->{c_show_menu}==1?'':'class="off"').'><span class="move" '.($sort eq "c_pos ASC"?'><a class="up" href="#" title="Поднять вверх '.$item->{c_name}.'"></a><a class="down" href="#" title="Опустить вниз '.$item->{c_name}.'"></a>':'id="off">').'</span><a class="lamp" href="#" '.($item->{c_show_menu}==1?'title="Скрыть категорию"':'title="Сделать активной" style="opacity:0.5"').' '.$item->{c_name}.'"></a><a href="#" class="del" title="Удалить категорию '.$item->{c_name}.'"></a><div class="point'.($i_cat==$i_cat_old?' last':'').'"></div>';
				$text .= '<a title="'.($item->{c_redirect} ne ""?'Редирект: /catalog/'.$item->{c_alias}.' на '.$item->{c_redirect}.'':'Страница: /catalog/'.$item->{c_alias}.'').'" '.$hide_child.' '.($show_child_count < $i_cat && $show_child_count !=0?'class="name hide"':'class="name"').' href="?adm_act=category&num_edit='.$item->{c_id}.'">'.$item->{c_name}.'</a>';
				if ($num_edit == $item->{c_id}) {$parents .='';}
				else {$parents .= '<option value="'.$item->{c_id}.'" '.($parent==$item->{c_id}?'selected':'').' '.($globalid==$item->{c_id}?'disabled':'').'>'.nbsp($level).$item->{c_name}.'</option>';}
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
    return ($tree, $parents);
}	

	my ($tree, $parents) = treeCat( $num_edit, $parent );
	$list_older .= $tree;
	menu_listing($parents);
	
	
sub old_sort {

		open(BO, "../$dirs/set_catalog"); @set_catalog = <BO>; close(BO);
		foreach my $line(@set_catalog){chomp($line);
		my ($ajax_save_old_, $count_more_, $cat_desc_top_, $cat_desc_bottom_, $pr_desc_ext_, $content_wide_, $set_foto_hide_, $img_url_) = split(/\|/, $line);
		$ok_ajax_save_old=qq~$ajax_save_old_~;
		$count_more =qq~$count_more_~;
		$ok_category_desc_top =qq~$cat_desc_top_~;
		$ok_category_desc_bottom =qq~$cat_desc_bottom_~;
		$ok_product_desc_ext =qq~$pr_desc_ext_~;
		$ok_content_wide =qq~$content_wide_~;
		$ok_set_foto_hide =qq~$set_foto_hide_~;
		$img_url_old =qq~$img_url_~;}

		open(BO, "../$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
		foreach my $line(@select_sort)
			{
		chomp($line);
		my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
		$select_sort_cat=qq~$select_sort_cat_~;
		$select_sort_product=qq~$select_sort_product_~;
			}	
			
		open(BO, "$dirs_catalog/page_settings.txt"); my @pages_count = <BO>; close(BO);
		foreach my $line(@pages_count)
			{
		chomp($line);
		my ($pages_admin_, $pages_site_) = split(/\|/, $line);
		$pages_admin=qq~$pages_admin_~;
		$pages_site=qq~$pages_site_~;
			}

		$sort_type_cat ='
		<option value="c_pos ASC" '.($select_sort_cat eq "c_pos ASC"?'selected':'').'>Позициям</option>
		<option value="c_name ASC" '.($select_sort_cat eq "c_name ASC"?'selected':'').'>Названию</option>
		<option value="c_date_add ASC" '.($select_sort_cat eq "c_date_add ASC"?'selected':'').'>Дате по возрастанию</option>
		<option value="c_date_add DESC" '.($select_sort_cat eq "c_date_add DESC"?'selected':'').'>Дате по убыванию</option>';
		$sort_type_product ='
		<option value="p_pos ASC" '.($select_sort_product eq "p_pos ASC"?'selected':'').'>Позициям</option>
		<option value="p_name ASC" '.($select_sort_product eq "p_name ASC"?'selected':'').'>Названию</option>
		<option value="p_date_add ASC" '.($select_sort_product eq "p_date_add ASC"?'selected':'').'>Дате по возрастанию</option>
		<option value="p_date_add DESC" '.($select_sort_product eq "p_date_add DESC"?'selected':'').'>Дате по убыванию</option>
		<option value="p_price ASC" '.($select_sort_product eq "p_price ASC"?'selected':'').'>Цене по возрастанию</option>
		<option value="p_price DESC" '.($select_sort_product eq "p_price DESC"?'selected':'').'>Цене по убыванию</option>';
}		
	
sub menu_listing {

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
				if ($ok_maket_old ne ""){$select = $ok_maket_old;} else {$select = $maket_catalog;}
				$maket_item .= '<option value="'.$num.'" '.($num==$select?'selected':'').'>'.$name_old.'</option>';
			}
		}
	}

	if ($maket_item ne "" && $hide_makets ne "1"){
		$maket_list = '
			<tr class="help_maket">
				<td class="name">Привязать категорию к макету</td>
				<td>
					<select class="category" name="maket" style="width:197px;">
						'.$maket_item.'
					</select>
				</td>
			</tr>';
	}	
	
	$img_load=""; $img_load_param="";
	if ($hide_category_photo ne "1"){
		$rand_num=rand(1);
		my $img_num = $num_edit+1000;
		if(-e "$dirs_catalog/category/$img_num.jpg")
		{$image =qq~<img src="$dirs_catalog_www/category/$img_num.jpg?$rand_num" border="0">~;}
		else { $image = "";}
		
		$img_load ='
				<tr class="help_image">
					<td class="name">'.($image ne ""?'Поменять картинку':'Загрузить картинку').'</td>
					<td class="img_load">
					'.($image ne ""?'<div class="prev_img get_image">'.$image.'</div>':'<div class="prev_img no_show get_image"></div>').'
					<input multiple="multiple" class="fileInput" type="file" name="image" size="21" onchange="document.getElementById(\'fileInputbg\').value = this.value;">
					<div class="browse" style="margin-left:2px;">
						<input type="text" id="fileInputbg" class="browse_input"/>
					</div>
					</td>
				</tr>
				<tr class="help_image_url">
					<td class="name">Загрузить картинку по ссылке</td>
					<td class="img_load">	
						<div class="b-help">
							<input type="text" cat_id="'.$num_edit.'" value="" class="give_url_big show">
							<div class="help">
								Для загрузки картинки из интернета скопируйте<br>
								адрес картинки в буфер и вставьте в это поле
							</div>
						</div>
					</td>
				</tr>';
				
		$img_load_param =qq~
				<tr class="autoresize">
					<td class="name">Авторазмер картинки</td><td><input class="size" type="text" name="img_ox" value="$img_ox" size=10><input class="size" type="text" name="img_oy" value="$img_oy" size=10></td>
				</tr>~;
	}

 my $parents = shift;
$dshfgkjdf=qq~<td class="name">Соответствие разделу<em>*</em></td><td><select name="parent" id="category"><option value="0">Верхний уровень</option>$parents</select></td>~;

if ($settings eq "set") {

	sub menu_settings {

		$list_older="";
		old_sort();

		$content_html.= qq~
		<script type="text/javascript" src="/admin/lib/help/catalog/category_settings.js"></script>
		<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
		<input type="hidden" name="adm_act" value="category">
		<input type="hidden" name="menu_act" value="set_sort">
					<table id="page_new" style="margin-bottom:0px;">
					<tr>
						<td class="name"></td><td class="name_main">Настройки модуля</td>
					</tr>
					<tr class="help_sort_category">
						<td class="name">Сортировать категории по</td><td><select name="select_sort_cat" class="category" style="width:358px;">$sort_type_cat</select></td>
					</tr>
					<tr class="help_sort_products">
						<td class="name">Сортировать товары по</td><td><select name="select_sort_product" class="category" style="width:358px;">$sort_type_product</select></td>
					</tr>
					<tr class="help_wide_review">
						<td class="name">Широкий режим просмотра товаров</td><td><input type="checkbox" class="cb" name="content_wide"~;
		if($ok_content_wide eq "1"){
			$content_html.= qq~ checked~;
		}			
		
	$content_html.= qq~></td>
					</tr>					
					<tr class="help_count_products_cms">
						<td class="name" title="Выводить количество товаров на странице">Количество товаров на стр. в CMS</td><td><input type="text" value="$pages_admin" name="count_pages_admin" class="normal"></td>
					</tr>
					<tr class="help_count_products_site">
						<td class="name" title="Выводить количество товаров на странице">Количество товаров на стр. на сайте</td><td><input type="text" value="$pages_site" name="count_pages_site" class="normal"></td>
					</tr>~;
					
		if ($hide_more_photo ne "1"){
			$content_html.= qq~		
					<tr class="help_add_photo">
						<td class="name">Доп. фотографии к товару</td><td><input type="text" value="$count_more" name="count_more_photo" class="normal"></td>
					</tr>~;
		}
		$content_html.= qq~
					<tr class="help_desc">
						<td class="name">Ред. текст категории над товарами</td><td><input class="cb" type="checkbox" name="category_desc_top"~;
		if($ok_category_desc_top eq "1"){
			$content_html.= qq~ checked~;
		} 			
			$content_html =qq~$content_html><div style="float:left; margin:0px 11px 0px 12px">под товарами</div><input class="cb" type="checkbox" name="category_desc_bottom"~;
		if($ok_category_desc_bottom eq "1"){
			$content_html.= qq~ checked~;
		} 			
			$content_html =qq~$content_html></td>
					</tr>
					<tr class="help_ext_desc_products">
						<td class="name">Расширить описание товара на 2-а поля</td><td><input type="checkbox" class="cb" name="product_desc_ext"~;
		if($ok_product_desc_ext eq "1"){
			$content_html.= qq~ checked~;
		}			
		
	$content_html.= qq~><div class="help_hide_photo_settings" style="padding-bottom:10px;"><div style="float:left; margin:0px 11px 0px 12px">Скрывать настройки изображения</div><input class="cb" type="checkbox" name="set_foto_hide"~;
		if($ok_set_foto_hide eq "1"){
			$content_html.= qq~ checked~;
		}			
		
	$content_html.= qq~></div></td>
					</tr>				
					<tr class="help_quick_save">
						<td class="name">Быстрое сохранение контента</td><td><input type="checkbox" class="cb" name="ajax_save"~;
		if($ok_ajax_save_old eq "1"){
			$content_html.= qq~ checked ~;
		}			
		
	$content_html.= qq~></td>
					</tr>
					<tr>
						<td class="name">Внешний адрес к картинкам</td>
						<td><input type="text" class="normal" name="img_url" value="$img_url_old"></td>
					</tr>~;

		if ($hide_products_watermark ne "1"){
		
		open(BO, "$dirs_catalog/watermark.txt"); my @categories = <BO>; close(BO);
		foreach my $linee(@categories)
			{
		chomp($linee);
		my ($watermark_pos_, $watermark_op_, $watermark_big_, $watermark_normal_, $watermark_small_, $watermark_text_, $watermark_size_, $watermark_color_) = split(/\|/, $linee);
		$ok_watermark_pos=qq~$watermark_pos_~;
		$ok_watermark_op=qq~$watermark_op_~;
		$ok_watermark_big=qq~$watermark_big_~;
		$ok_watermark_normal=qq~$watermark_normal_~;
		$ok_watermark_small=qq~$watermark_small_~;
		$ok_watermark_text=qq~$watermark_text_~;
		$ok_watermark_size=qq~$watermark_size_~;
		$ok_watermark_color=qq~$watermark_color_~;
			}
			
	my $img_exis=""; my $div_width = 520; my $div_height = 154; my $div_mLeft=""; my $img_mTop = 0; my $img_mLeft="";
	if (-e "$dirs_catalog/watermark.png"){
		use Image::Magick;
		my $img = Image::Magick->new;
		($width, $height, $size, $format) = $img->Ping("$dirs_catalog/watermark.png");
		if ($width > 1 && $height > 1){
			$img_exis ="1";
			$div_mLeft = -($div_width/2);
			if ($height > ($div_height-20)){$div_height = $height+30;}
			$img_mTop = -($height/2)+1;
			$img_mLeft = -($width/2)+1;
		}
	}
	
	if (!$width){$div_mLeft = -($div_width/2);}
		
	$content_html .='	
					<tr>
						<td class="name"></td><td class="name_main">Водяной знак<span style="color:#999999;">, загрузка файла</span></td>
					</tr>
					<tr>
						<td colspan="2">
							<link rel="stylesheet" type="text/css" href="/admin/css/font-face/watermark.css" />
							<script type="text/javascript" src="/admin/js/jscolor/jscolor.js"></script>
							<div class="watermark-fonts">
								<div class="container">
									<h4>Cвой текст</h4>
									<div class="item">
										<input type="text" class="normal" name="watermark_text" value="'.($ok_watermark_text ne ""?''.$ok_watermark_text.'':''.$ENV{'HTTP_HOST'}.'').'">
									</div>
									<h4>Размер и цвет</h4>
									<div class="item">
										<select data-value="'.$ok_watermark_size.'" style="width:82px;" class="category" name="watermark_size">
											<option value="10">10px</option>
											<option value="12">12px</option>
											<option value="14">14px</option>
											<option value="16">16px</option>
											<option value="18">18px</option>
											<option value="20">20px</option>
											<option value="24">24px</option>
											<option value="28">28px</option>
											<option value="30">30px</option>
											<option value="32">32px</option>
											<option value="36">36px</option>
											<option value="40">40px</option>
											<option value="48">48px</option>
											<option value="56">56px</option>
											<option value="60">60px</option>
											<option value="72">72px</option>
										</select>
										<input class="color jscolor-picker" value="'.$ok_watermark_color.'" name="watermark_color">
									</div>
									<input type="button" class="button create" value="Применить">
									<div class="clear"></div>
									<h5 class="test" style="font-size:'.$ok_watermark_size.'px; line-height:'.$ok_watermark_size.'px;">'.$ok_watermark_text.'</h5>
								</div>
							</div>						
							<div class="watermark-settings">';
					if ($img_exis eq "1"){	
						my $rand_num=rand(1);
						$content_html .='
							<div class="watermark-upload" data-height="154" style="height:'.$div_height.'px;">
								<div class="watermark-img" style="width:'.$div_width.'px; height:'.$div_height.'px; margin-left:'.$div_mLeft.'px;">
									<div class="img" style="width:'.$div_width.'px; height:'.$div_height.'px;">
										<img style="margin-top:'.$img_mTop.'px; margin-left:'.$img_mLeft.'px; opacity:'.($ok_watermark_op/100).'" src="'.$dirs_catalog_www.'/watermark.png?'.$rand_num.'" alt="">
									</div>
									<input type="file" class="file" title="Сменить картинку">
									<a title="Удалить водяной знак" href="#" class="del_watermark"></a>
								</div>
							</div>';
					}
					else {
					$content_html .='
							<div class="watermark-upload" style="height:'.$div_height.'px;">
								<div class="watermark-img add" style="width:'.$div_width.'px; height:'.$div_height.'px; margin-left:'.$div_mLeft.'px;">
									<div class="img" style="width:'.$div_width.'px; height:'.$div_height.'px;"><span><em>Загрузите файл в формате <ins>png, gif, jpg</ins></em></span></div>
									<input type="file" class="file" title="">
								</div>
							</div>';
					}
					$content_html .='
							</div>
						</td>
					</tr>
					<tr class="help_watermark_pos">
						<td class="name">
							<span class="p14">Выберите расположение</span>
						</td>
						<td>
							<select style="width:218px;" class="category" name="watermark_pos">
								<option value="top-left"'.($ok_watermark_pos eq "top-left"?' selected':'').'>Левый верхний угол</option>
								<option value="top-right"'.($ok_watermark_pos eq "top-right"?' selected':'').'>Правый верхний угол</option>
								<option value="center"'.($ok_watermark_pos eq "center"?' selected':'').'>По центру</option> 
								<option value="bottom-right"'.($ok_watermark_pos eq "bottom-right"?' selected':'').'>Правый нижний угол</option>
								<option value="bottom-left"'.($ok_watermark_pos eq "bottom-left"?' selected':'').'>Левый нижний угол</option>
							</select>						
						</td>
					</tr>
					<tr class="widget-slider help_opacity">
						<td class="name">
							<span class="p14">Прозрачность</span>
						</td>
						<td>
							<div class="widget-slider opacity">
								<div id="slider-opacity" class="slider"></div>
								<div class="value"><input name="watermark_opacity" value="'.$ok_watermark_op.'" type="text" readonly="readonly"></div>	
							</div>
						</td>
					</tr>
					<tr class="help_watermark_type">
						<td class="name">
							<span class="p14">Наносить на большую фотографию</span>
						</td>
						<td>
							<input class="cb" type="checkbox" name="watermark_big"'.($ok_watermark_big eq "1"?' checked':'').'><div style="float:left; margin:0px 11px 0px 12px"><span class="p14">среднюю</span></div><input class="cb" type="checkbox" name="watermark_normal"'.($ok_watermark_normal eq "1"?' checked':'').'><div style="float:left; margin:0px 11px 0px 12px"><span class="p14">малую</span></div><input class="cb" type="checkbox" name="watermark_small"'.($ok_watermark_small eq "1"?' checked':'').'>
						</td>
					</tr>';
		}
		$content_html.= qq~
					</table>
					
		<input style="margin-left:554px; margin-top:-15px;" type="submit" name="save" value="Сохранить" class="button" /><br><br>		
		</form>
		~;
	}
	menu_settings();
}

if ($par eq "new") {
$content_html.= qq~
<script type="text/javascript" src="/admin/lib/help/catalog/category_edit.js"></script>
<div class="three_pages" style="display:none;">$list_older</div>
<div id="pages_new" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">

			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Новая категория</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
			<tr>
				<td class="name">Краткое название</td><td><input type="text" name="name_short" value="$ok_name_short_old"></td>
			</tr>			
$img_load			
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>
			<tr>
$dshfgkjdf
			</tr>
			<tr>
				<td class="name">Краткое описание</td><td><textarea name="desc_sm" class="desc_sm"></textarea></td>
			</tr>			
			<tr>
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>

			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr class="help_alias">
				<td class="name">Адрес страницы</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>
				$maket_list
			<tr>
				<td class="name">Дата создания </td><td><input name="date_add" readonly="readonly" value="$ok_date_add_old" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name">Дата изменения </td><td><input name="date_up" readonly="readonly" value="$today" type="text" class="date"></td>
			</tr>
$img_load_param			
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
			</table>~;
			
	if ($category_desc_top eq "1" && $category_desc_bottom eq "1"){
		$content_html.= qq~<h3 style="margin-top:0px;">Анонс категории</h3>	
		<textarea id="elm1_sm" name="elm1_sm" rows="20" cols="80" class="tinymce">@ok_elm_sm_old</textarea>
		<h3>Полное описание</h3>
		<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>~;
	}
	elsif ($category_desc_top eq "1"){
		$content_html.= qq~<textarea id="elm1_sm" name="elm1_sm" rows="20" cols="80" class="tinymce">@ok_elm_sm_old</textarea>~;
	}	
	elsif ($category_desc_bottom eq "1"){
		$content_html.= qq~<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>~;
	}	
	$content_html.= qq~
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<input type="submit" name="save" value="Сохранить" class="button" />
	<input type="reset" name="reset" value="Очистить" class="button" />
</form>
</div>
~;
} else {


	if ($num_edit eq ""){
		if ($settings ne "set"){
			$content_html=qq~$content_html<script type="text/javascript" src="/admin/lib/help/catalog/category.js"></script>
<div class="three_pages">$list_older</div>~;	
		}
	} else {
	
	open(BO, "../$dirs/set_catalog"); @set_catalog = <BO>; close(BO);
	foreach my $line(@set_catalog){chomp($line);
	my ($ok_ajax_save_, $count_more_, $cat_desc_top_, $cat_desc_bottom_, $pr_desc_ext_, $content_wide_) = split(/\|/, $line);
	$ok_ajax_save=qq~$ok_ajax_save_~;}		

	if ($ok_ajax_save == "0" or $ok_ajax_save == "") {$button_save = '<input type="submit" name="save" value="Сохранить" class="button save" />'; $check_ajax='';}
	else {$button_save = '<a class="ajaxSave" href="#">Сохранить</a>'; $check_ajax='checked';}
	
$content_html=qq~$content_html
<script type="text/javascript" src="/admin/lib/help/catalog/category_edit.js"></script>
<div class="three_pages" style="display:none;">$list_older</div>
<div id="pages_old" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">

			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Редактирование категории</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
			<tr class="help_name">
				<td class="name">Краткое название</td><td><input type="text" name="name_short" value="$ok_name_short_old"></td>
			</tr>			
$img_load			
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>
			<tr class="help_parent">
$dshfgkjdf
			</tr>
			<tr class="help_show_menu">
		<td class="name">Показывать категорию в меню</td><td class="show"><input name="show_menu" type="checkbox" class="cb"~;
		if($ok_show_menu_old){
			$content_html.= qq~ checked~;
		}
		$content_html.= qq~></td></tr>~;
	}
	
		if($num_edit){
$content_html.= qq~
			<tr>
				<td class="name">Краткое описание</td><td><textarea name="desc_sm" class="desc_sm">@ok_desc_sm_old</textarea></td>
			</tr>
			<tr>
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>

			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr class="help_alias">
				<td class="name">Адрес страницы</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>

				$maket_list

			<tr class="redirect">
				<td class="name">Редирект 301</td><td>
					<div>Например: <em><span>/</span>catalog<span>/</span>new_category</em></div>
					<input name="redirect" type="text" value="$ok_redirect_old"></td>
			</tr>			
			<tr>
				<td class="name">Дата создания </td><td><input name="date_add" readonly="readonly" value="$ok_date_add_old" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name">Дата изменения </td><td><input name="date_up" readonly="readonly" value="$today" type="text" class="date"></td>
			</tr>
	$img_load_param			
			<tr class="help_header">
				<td class="name">Отображать заголовок категории</td><td class="show"><input name="show_head" type="checkbox" class="cb"~;
		if($ok_show_head_old){
			$content_html.= qq~ checked~;
		} 

		$content_html .= qq~></td></tr>
		<tr class="help_hide">
		<td class="name">Скрывать от поисковиков</td><td class="show"><input name="show" type="checkbox" class="cb" ~;
		if($ok_show_old eq "0"){
			$content_html.= qq~ checked ~;
		} 
		
$content_html.= qq~> </td></tr>~;			
		
			
	my $db = new Core::DB();
	my $res = $db->query("SELECT * FROM cat_category WHERE c_pid=".$num_edit.";");

	if(ref($res) eq "ARRAY") {			
		$content_html.= qq~
			<tr class="help_hide_child">
				<td class="name">Скрывать вложенные категории</td><td><input type="checkbox" class="cb" name="hide_child"~;
		if($ok_hide_child_old eq "1"){
			$content_html.= qq~ checked ~;
		}			
		
			$content_html.= qq~></td>
			</tr>
			<tr class="help_hide_child_count">
				<td class="name">Кол-во отображаемых категорий</td><td><input type="text" value="$ok_show_child_count_old" class="sort" name="show_child_count"></td>
			</tr>~;
	}
		
$content_html.= qq~			
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
			
	<img style="display:none;" src="/admin/js/tiny_mce/themes/advanced/skins/default/img/progress.gif" alt="">~;
	if ($category_desc_top eq "1" && $category_desc_bottom eq "1"){
		$content_html.= qq~<h3 style="margin-top:0px;">Анонс категории</h3>	
		<textarea id="elm1_sm" name="elm1_sm" rows="20" cols="80" class="tinymce">@ok_elm_sm_old</textarea>
		<h3>Полное описание</h3>
		<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>~;
	}
	elsif ($category_desc_top eq "1"){
		$content_html.= qq~<textarea id="elm1_sm" name="elm1_sm" rows="20" cols="80" class="tinymce">@ok_elm_sm_old</textarea>~;
	}	
	elsif ($category_desc_bottom eq "1"){
		$content_html.= qq~<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>~;
	}	
	$content_html.= qq~
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<div class="save_content">$button_save
	<a class="preview_page" id="$num_edit" target="_blank" href="/catalog/$ok_alias_old">Посмотреть</a><div class="check_save"><input type="checkbox" class="cb ajaxSave" $check_ajax>Быстрое сохранение контента</div></div>	
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