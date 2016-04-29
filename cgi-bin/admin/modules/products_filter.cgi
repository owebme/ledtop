use Core::DB::Catalog;
use Core::DB::Work;

my $catalog = new Core::DB::Catalog();
my $db = new Core::DB();

	my $products_type="";
	if ($hide_products_type ne "1"){
		$products_type ='<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_type&par=new"><span>'.$pr_type_name.'</span></a></li>';
	}	
	
if ($num_edit eq "") {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
$products_type~;
}
else {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
$products_type~;
}
if ($par) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Все товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Добавить товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
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
		<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />
		<div id="pages" class="products_filter indent">
<script type="text/javascript" src="/admin/lib/products_filter.js"></script>~;

	if ($hide_products_filter ne "1"){
		$content_html .='
			<div class="btn-group left">
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param" class="btn">Параметры</a>
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_filter" class="btn active">Фильтрация</a>
			</div>';	
	}
	
	my $group_filters="";
	my $result = $db->query("SELECT * FROM cat_product_filters_group ORDER BY g_id DESC;");
	foreach my $group(@$result){
		$group_filters .='<div class="group">';
		$group_filters .='<h4 class="name" data-ids="'.$group->{'c_ids'}.'"><span>'.$group->{'g_name'}.':</span> <em>';
		my $category=""; my $ids = $group->{'c_ids'}.",";
		while ($ids =~ m/(\d+),/g) {
			my $res_name = $db->query("SELECT c_name FROM cat_category WHERE c_id = '".$1."';");
			$category .= $res_name->[0]->{'c_name'}.', ';
		}
		$category =~ s/,\s$//g;
		$group_filters .= $category.'</em>&nbsp <a href="#" class="change">изменить</a>&nbsp <a href="#" class="show">показать фильтры</a><ins>&times;</ins></h4><div class="container hide" data-id="'.$group->{'g_id'}.'">';
		my $res = $db->query("SELECT * FROM cat_product_filters WHERE gid = '".$group->{'g_id'}."' AND f_pid ='0' ORDER BY f_pos ASC;");
		if ($res){
			foreach my $filter(@$res){
				$group_filters .='<div class="filter" data-id="'.$filter->{'filter_id'}.'">';
				$group_filters .='<h4>'.$filter->{'name'}.'<ins>&times;</ins></h4>';
				my $fields = $db->query("SELECT * FROM cat_product_filters WHERE f_pid = '".$filter->{'filter_id'}."' ORDER BY name ASC;");
				if ($fields){
					$group_filters .='<ul>';
					foreach my $item(@$fields){
						$group_filters .='<li data-id="'.$item->{'filter_id'}.'">'.$item->{'name'}.'</li>';
					}
					$group_filters .='</ul>';
				}
				$group_filters .='</div>';
			}
		}
		$group_filters .='</div></div>';
	}	
	
	my $box_filters="";
	my $result = $db->query("SELECT * FROM cat_product_filters_set WHERE f_pid = '0' ORDER BY filter_id DESC;");
	foreach my $item(@$result){
		$box_filters .='<div class="filter" data-id="'.$item->{'filter_id'}.'"><h4>'.$item->{'name'}.'<ins>&times;</ins></h4>';
		my $res = $db->query("SELECT * FROM cat_product_filters_set WHERE f_pid = '".$item->{'filter_id'}."' ORDER BY field ASC;");
		if ($res){
			$box_filters .='<ul>';
			foreach my $line(@$res){
				$box_filters .='<li data-id="'.$line->{'filter_id'}.'">'.$line->{'field'}.'</li>';
			}
			$box_filters .='</ul>';
		}
		$box_filters .='</div>';
	}

		$content_html .='<div class="tab_left">
			<h3>Группы фильтров</h3>
			<button id="add_group" class="a-button light"><span>Создать новую группу</span></button>
			<div class="filters group_filters">
				'.$group_filters.'
			</div>
		</div>';	
		
		$content_html .='<div class="tab_center">
			<h3>Создание фильтров</h3>
			<button id="add_filter" class="a-button light"><span>Добавить новый фильтр</span></button>
			<div class="filters box_filters">
				'.$box_filters.'
			</div>
		</div>';

		$content_html .='<div class="tab_right">
		</div>';
		
		
	my $sel_option_category="";
	my $result = $db->query("SELECT * FROM cat_category WHERE c_pid = '0' AND c_show = '1' ORDER BY c_pos ASC");
	foreach my $item(@$result){
		$sel_option_category .= '<option style="font-weight:bold" value="'.$item->{c_id}.'">'.$item->{c_name}.'</option>';
		if (my $sub = recMenuCategory($item->{c_id}, 0) ){
			$sel_option_category .= $sub;
		}
	}
	sub recMenuCategory {
		my $id = shift;
		my $level = shift;
		sub nbsp_cat { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
		my $result = $db->query("SELECT * FROM cat_category WHERE c_pid = '".$id."' AND c_show = '1' ORDER BY c_pos ASC");
		if ($result){
			foreach my $item(@$result){
				$sel_option_category .= '<option value="'.$item->{c_id}.'">'.nbsp_cat($level).$item->{c_name}.'</option>';
				if (my $sub = recMenuCategory($item->{c_id}, $level+1)){
					$sel_option_category .= $sub;
				}
			}
		}
		else {
			return 0;
		}
	}

	my $sel_option_params="";
	my $main_params=""; my $category_params=""; my $cat_id="";
	my $result = $db->query("SELECT * FROM cat_product_fields_set ORDER BY cat_id ASC, f_pos ASC;");
	$counts = @$result;
	foreach my $item(@$result){
		if ($item->{'cat_id'} eq "0"){
			$main_params .='<option value="'.$item->{'f_name'}.'">&nbsp;&mdash; '.$item->{'f_name'}.'</option>';
		}
		if ($item->{'cat_id'} > 0){
			if ($item->{'cat_id'} ne $cat_id or !$cat_id){
				my $res = $db->query("SELECT c_name FROM cat_category WHERE c_id = '".$item->{'cat_id'}."';");
				$category_params .= '<option style="font-weight:bold" disabled>'.$res->[0]->{c_name}.'</option>';
			}
			$category_params .='<option value="'.$item->{'f_name'}.'">&nbsp;&mdash; '.$item->{'f_name'}.'</option>';
			$cat_id = $item->{'cat_id'};
		}
	}
	
	if ($main_params or $category_params){
		if ($main_params){
			$main_params = '<option style="font-weight:bold" disabled>&nbsp;Для всех категорий</option>'.$main_params;
		}
		$sel_option_params = $main_params.$category_params;
	}
		
	if ($sel_option_category){
		$content_html.='
			<div class="select_category">
				<select class="category multi" multiple="multiple"><option value="0" disabled>Отметьте категории</option>'.$sel_option_category.'</select>
			</div>';
	}
	if ($sel_option_params){
		$content_html.='
			<div class="select_params">
				<select class="category"><option value="0">Выберите параметр</option>'.$sel_option_params.'</select>
			</div>';
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

-1;