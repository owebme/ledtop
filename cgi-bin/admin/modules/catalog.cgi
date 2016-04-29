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
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog" class="btn active">Привязка</a>
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog" class="btn">Поставщики</a>
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=catalog" class="btn">Миграция</a>
			</div>	
		</div>
		<div id="control-primary" class="btn-group left">
			<button class="btn" data-action="expand-all">Раскрыть все</button>
			<button class="btn" data-action="collapse-all">Свернуть все</button>
		</div>
		<div id="control-secondary" class="btn-group right">
			<button class="btn" data-action="expand-all">Раскрыть все</button>
			<button class="btn" data-action="collapse-all">Свернуть все</button>
		</div>';
		
	my %data_providers=""; my $providers="";  my $provider_value=""; my $i=0;
	my $result = $db->query("SELECT * FROM catalog_providers ORDER BY date ASC");
	foreach my $item(@$result){
		$i++;
		$providers .= '<div class="toogle-menu-item catalog-b-'.$item->{color}.'" data-color="'.$item->{color}.'" data-id="'.$item->{id}.'" data-alias="'.$item->{alias}.'">'.$item->{name}.'</div>';
		if ($i == 1) {
			$provider_value = '<div data-id="'.$item->{id}.'" class="item catalog-b-'.$item->{color}.'">
						<span class="value">'.$item->{name}.'</span>
					</div>';
		}
		%data_providers = (%data_providers,
			$item->{"id"} => {
				"title" => $item->{"name"},
				"color" => $item->{"color"}		
			}
		);
	}
		
	my $tree = '<div class="dd" id="catalog-primary">
			<ol class="dd-list">';
			
	my $select="";
	my $result = $db->query("SELECT c_id, c_name FROM cat_category WHERE c_pid = '0' ORDER BY c_pos ASC");
	foreach my $item(@$result){
		$tree .= '<li class="dd-item dd3-item dd-collapsed" data-id="'.$item->{c_id}.'" data-links="'.getLinks($item->{c_id}).'">
			<div class="dd-handle dd3-handle"></div>
			<div class="dd3-content" data-pk="'.$item->{c_id}.'">
				<span class="dd-content-value">'.$item->{c_name}.'</span>
			</div>
			<div class="dd-badges"></div>';
		$select .= '<option data-level="0" class="option-strong" value="'.$item->{c_id}.'">'.$item->{c_name}.'</option>';
		if (my $sub = recMenuPrimary($item->{c_id}, 0) ){
			$tree .= $sub;
		}
		$tree .= '</li>';
	}
	
	sub getLinks {
		my $id = shift;
		my $result=""; my $p_id="";
		my $links = $db->query("SELECT * FROM cat_category_links WHERE id = '".$id."' ORDER BY p_id ASC");
		foreach my $link(@$links){
			if ($p_id == $link->{"p_id"}){$result .=',';}
			if ($p_id != $link->{"p_id"}){
				$result .= $p_id ? ']},' : '';
				$result .= '{"id":"'.$link->{"p_id"}.'","title":"'.$data_providers{$link->{"p_id"}}->{"title"}.'","color":"'.$data_providers{$link->{"p_id"}}->{"color"}.'","items":[';
			}
			$result .='{"id":"'.$link->{"p_cid"}.'","title":"'.$link->{"name"}.'"}';
			$p_id = $link->{"p_id"};
		}
		if ($result) {
			$result =~ s/"/&quot;/g;
			return '['.$result.']}]';
		}
	}
	
	sub recMenuPrimary {
		my $id = shift;
		my $level = shift;
		if ($level == 0) {$level = 1};
		sub nbsp { my $level = shift; my $t; my $n=3; if($level>1){$n=4} for(my $i=0;$i<=($level+1)*$n;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
		my $text = '<ol class="dd-list">';
		my $result = $db->query("SELECT c_id, c_name FROM cat_category WHERE c_pid='".$id."' ORDER BY c_pos ASC;");
		if ($result){
			foreach my $item(@$result){
				$text .= '<li class="dd-item dd3-item dd-collapsed" data-id="'.$item->{c_id}.'" data-links="'.getLinks($item->{c_id}).'">
					<div class="dd-handle dd3-handle"></div>
					<div class="dd3-content" data-pk="'.$item->{c_id}.'">
						<span class="dd-content-value">'.$item->{c_name}.'</span>
					</div>
					<div class="dd-badges"></div>';
				$select .= '<option data-level="'.$level.'" '.($level == 1?' class="option-blue"':'').' value="'.$item->{c_id}.'">'.nbsp($level).$item->{c_name}.'</option>';	
				if (my $sub = recMenuPrimary($item->{c_id}, $level + 1) ){
					$text .= $sub;
				}
				$text .= '</li>';
			}
		} else {
			return 0;
		}
		$text .= '</ol>';
		return $text;
	};

	$content_html .= '
		<div class="catalog-content">
			<div class="catalog-tab">
				<div class="catalog-header">
					<button class="button-flat button-flat-add category-add">Создать категорию</button>
					<div class="category-add-form">
						<select id="category-select" class="select">
							<option data-level="" class="option-strong" value="0">Верхний уровень</option>
							'.$select.'
						</select>
						<input type="text" class="input normal" placeholder="Название">
						<button class="button-flat button-flat-small button-flat-add"></button>
						<button class="button-flat button-flat-small button-flat-remove button-flat-gray">&times;</button>
					</div>
				</div>';	

	$content_html .= $tree.'</ol></div>';
	
	$content_html .= '</div>';

	$content_html .= '<div class="catalog-tab">
						<div class="catalog-header catalog-header-right">
							<div class="catalog-provider-select">
								'.$provider_value.'
								<div class="toogle-menu">
									'.$providers.'
								</div>
							</div>
							<button id="catalog-save" class="a-button light"><span>Сохранить все</span></button>
						</div>';

	my $tree = '<div class="dd dd-light" id="catalog-secondary">
			<ol class="dd-list">';
			
	my $result = $db->query("SELECT c_id, c_name FROM catalog_alright WHERE c_pid = '0'");
	foreach my $item(@$result){
		my $items = "";
		if (my $sub = recMenuSecondary($item->{c_id}) ){
			$items .= $sub;				
		}
		$tree .= '<li class="dd-item dd3-item dd3-item-handle dd-collapsed" data-id="'.$item->{c_id}.'">';
		if ($items){
			$tree .= '<button data-action="collapse" type="button" style="display: none;">Collapse</button>
				<button data-action="expand" type="button" style="display: block;">Expand</button>';
		}
		$tree .= '
			<div class="dd-handle dd3-content dd3-content-handle">
				<span class="dd-content-value">'.$item->{c_name}.'</span>
			</div>';
		if ($items) {$tree .= $items;}
		$tree .= '</li>';
	}
	
	sub recMenuSecondary {
		my $id = shift;
		my $text = '<ol class="dd-list">';
		my $result = $db->query("SELECT c_id, c_name FROM catalog_alright WHERE c_pid='".$id."'");
		if ($result){
			foreach my $item(@$result){
				my $items = "";
				if (my $sub = recMenuSecondary($item->{c_id}) ){
					$items .= $sub;				
				}
				$text .= '<li class="dd-item dd3-item dd3-item-handle dd-collapsed" data-id="'.$item->{c_id}.'">';
				if ($items){
					$text .= '<button data-action="collapse" type="button" style="display: none;">Collapse</button>
						<button data-action="expand" type="button" style="display: block;">Expand</button>';
				}
				$text .= '
					<div class="dd-handle dd3-content dd3-content-handle">
						<span class="dd-content-value">'.$item->{c_name}.'</span>
					</div>';
				if ($items) {$text .= $items;}
				$text .= '</li>';
			}
		} else {
			return 0;
		}
		$text .= '</ol>';
		return $text;
	};		

	$content_html .= $tree.'</ol></div>';
		
$content_html .='<script type="text/javascript" src="/admin/lib/catalog.js"></script>';

$content_html.= qq~</div>
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;

-1;