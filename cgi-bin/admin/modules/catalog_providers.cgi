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
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog"><span>Работа с каталогом</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=products_param"><span>Характеристики</span></a></li>
$products_type~;
}
else {
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
		<div id="pages" class="clients">
			<script type="text/javascript" src="/admin/js/modernizr.custom.js"></script>
			<script type="text/javascript" src="/admin/js/jquery.isJSON.js"></script>
			<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap.css" />
			<link rel="stylesheet" type="text/css" href="/admin/js/nestable/jquery.nestable.css" />
			<script type="text/javascript" src="/admin/js/nestable/jquery.nestable.js"></script>
			<link rel="stylesheet" type="text/css" href="/admin/js/x-editable/bootstrap-editable.css" />
			<script type="text/javascript" src="/admin/js/x-editable/bootstrap-tooltip.js"></script>
			<script type="text/javascript" src="/admin/js/x-editable/bootstrap-popover.js"></script>
			<script type="text/javascript" src="/admin/js/x-editable/bootstrap-editable.min.js"></script>
			<link href="/admin/js/select2/select2.css" rel="stylesheet" type="text/css" />
			<script src="/admin/js/select2/select2.min.js" type="text/javascript"></script>';	

	$content_html .='
		<div class="catalog-btn-group">
			<div class="btn-group">
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog" class="btn">Привязка</a>
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog_providers" class="btn active">Поставщики</a>
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=category" class="btn">Категории</a>
			</div>	
		</div>';
		
	my $providers="";
	my $result = $db->query("SELECT * FROM catalog_providers ORDER BY date ASC");
	foreach my $item(@$result){
		$providers .= '<div class="toogle-menu-item catalog-b-'.$item->{color}.'" data-color="'.$item->{color}.'" data-id="'.$item->{id}.'" data-alias="'.$item->{alias}.'">'.$item->{name}.'</div>';
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