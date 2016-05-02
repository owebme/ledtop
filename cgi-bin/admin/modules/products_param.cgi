use Core::DB::Catalog;
use Core::DB::Work;

my $catalog = new Core::DB::Catalog();
my $db = new Core::DB();

	my $products_type="";
	if ($hide_products_type ne "1"){
		$products_type ='<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_type&par=new"><span>'.$pr_type_name.'</span></a></li>';
	}	
	
if ($num_edit eq "") {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category"><span>Категории</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Доб. товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category&par=new"><span>Доб. категорию</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Параметры</span></a></li>
$products_type~;
}
else {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category"><span>Категории</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Доб. товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category&par=new"><span>Доб. категорию</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Параметры</span></a></li>
$products_type~;
}
if ($par) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products"><span>Товары</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category"><span>Категории</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products&par=new"><span>Доб. товар</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=category&par=new"><span>Доб. категорию</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Параметры</span></a></li>
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
		<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />~;
	
	$content_html .='	
		<div id="pages" class="products_param'.($hide_products_filter ne "1"?' indent':'').'">
<script type="text/javascript" src="/admin/lib/products_param.js"></script>';

	if ($hide_products_filter ne "1"){
		$content_html .='
			<div class="btn-group left">
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param" class="btn active">Параметры</a>
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_filter" class="btn">Фильтрация</a>
			</div>';	
	}
	
	my $main_params=""; my $category_params=""; my $cat_id="";
	my $result = $db->query("SELECT * FROM cat_product_fields_set ORDER BY cat_id ASC, f_pos ASC;");
	my $counts = @$result;
	foreach my $item(@$result){
		if ($item->{'cat_id'} eq "0"){
			$main_params .='<button data-id="'.$item->{'id'}.'" class="a-button a-button-small not-active">'.$item->{'f_name'}.'<ins>&times;</ins></button>';
		}
		if ($item->{'cat_id'} > 0){
			if ($item->{'cat_id'} ne $cat_id && $cat_id){
				$category_params .='</div>';
			}
			if ($item->{'cat_id'} ne $cat_id or !$cat_id){
				my $res = $db->query("SELECT c_name FROM cat_category WHERE c_id = '".$item->{'cat_id'}."';");
				$category_params .= '<h4>'.$res->[0]->{c_name}.' &nbsp;<a href="#">показать</a></h4>';
				$category_params .='<div class="container hide">';
			}
			$category_params .='<button data-id="'.$item->{'id'}.'" class="a-button a-button-small not-active">'.$item->{'f_name'}.'<ins>&times;</ins></button>';
			$cat_id = $item->{'cat_id'};
		}
	}
	
	if ($category_params){
		$category_params = $category_params.'</div>';
	}

		$content_html .='<div class="tab_left">
			<h3>Для всех категорий</h3>
			<button id="add_param" class="a-button light"><span>Добавить параметр</span></button>
			<div class="params main_params">
				'.$main_params.'
			</div>
		</div>';	
		
		$content_html .='<div class="tab_center">
			<h3>Уникальные параметры</h3>
			<button id="add_cat_param" class="a-button light"><span>Добавить параметр</span></button>
			<div class="params category_params">
				'.$category_params.'
			</div>
		</div>';

		$content_html .='<div class="tab_right">
			<h3>Селекторы</h3>
			<button id="add_multi_param" class="a-button light"><span>Добавить селектор</span></button>
			<div class="params multi_params">
				
			</div>
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
		
	if ($sel_option_category){
		$content_html.='
		<div class="select_category">
			<select class="category"><option value="0">Выберите категорию</option>'.$sel_option_category.'</select>
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