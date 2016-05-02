<?php

ini_set('max_execution_time', 600);

function getDomen(){
	return 'http://ledtop2.ru';
}

$clear = 1;
$pars_catalog = 1;
$pars_xml = 0;
$pars_image = 0;
$pars_pdf = 0;
$backup_to = 0;
$backup_from = 0;
$arhive_products = 1;

require_once 'db.php';
require_once '../function.php';

header("Content-type: text/html; charset=utf-8");

print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<style>html {width:988px; margin:25px auto 0; font-family: Arial, Helvetica;} body {margin:0;} h2, h3 {margin:0 0 10px;} h2 {font-size:1.7em; margin-bottom:12px;}</style>';

if ($backup_to){
	file_get_contents(getDomen().'/parser/backup.php?action=security&time=to');
}

require_once '../get_xml.php';

if ($clear){
	mysql_query("TRUNCATE TABLE `catalog_alright`");
}

if ($pars_catalog){
	parsCategories($pars_xml);
}

if ($pars_image){

	$result = mysql_query("SELECT p_name, p_art, p_image FROM products_alright WHERE p_image !=''");
	while ($row = @mysql_fetch_array($result)){
		$image = $row["p_image"];
		if ($image && !file_exists("../../files/catalog/".$row["p_art"].".jpg")){
			print $row["p_art"]." - ".cp1251($row["p_name"])." картинка загружена<br>";
			$file = file_get_contents($image);
			if ($file){
				$fp = fopen("../../files/catalog/".$row["p_art"].".jpg", 'w');
				fwrite($fp, $file);
				fclose($fp);
			}
		}
	}
}

if ($pars_pdf){

	$result = mysql_query("SELECT p.p_name, p.p_art, f.value FROM cat_product AS p JOIN cat_product_fields AS f ON(f.p_id=p.p_id) WHERE f.field = 'Ссылка на PDF' AND f.value !='' ORDER BY p.p_id ASC");
	while ($row = @mysql_fetch_array($result)){
		$pdf = $row["value"];
		if ($pdf && !file_exists("../../files/catalog/pdf/".$row["p_art"].".pdf")){
			print $row["p_art"]." - ".$row["p_name"]." pdf загружен<br>";
			$file = file_get_contents($pdf);
			if ($file){
				$fp = fopen("../../files/catalog/pdf/".$row["p_art"].".pdf", 'w');
				fwrite($fp, $file);
				fclose($fp);
			}
		}
	}
}

if ($arhive_products){

	$result = mysql_query("SELECT p_art, p_name, p_id, p_alias FROM cat_product WHERE DAY(p_date_up) != DAY(NOW()) AND p_supplier = '1' AND p_show = '1' ORDER BY p_id ASC");
	while ($row = @mysql_fetch_array($result)){
		mysql_query("UPDATE cat_product SET `p_show` = '0' WHERE p_id='".$row["p_id"]."' LIMIT 1");
		print "<b>".utf8($row["p_art"]).":</b> ".utf8($row["p_name"])." - <span style='color:red'>в архив</span><br>";
	}
}

if ($backup_from){
	file_get_contents(getDomen().'/parser/backup.php?action=security&time=from');
}

function parsCategories($pars_xml){

	if ($pars_xml){
		getFile("group-descriptions");
	}
	
	$xml = simplexml_load_file('../xml/transistor_catalog_group-descriptions.xml');
	
	$parents = array();
	foreach ($xml->categories->category as $item) {
		array_push($parents, $item->xmlurl);
	}
	
	foreach ($xml->groups->group as $item) {
		if ($item->id > 1){
			mysql_query("INSERT INTO `catalog_alright` (`c_id`, `c_pid`, `c_name`) VALUES('".$item->id."', '".($item->parent == 1 ? 0 : $item->parent)."', '".cp1251($item->name)."')");
			if ($item->parent == 1) {print '<h2>'.$item->name.'</h2>';}
			else {print '<h3>'.$item->name.'</h3>';}
		}
	}	
	
	print '<br>';
	
	foreach ($parents as $file){
		if ($pars_xml){
			getFile($file);
		}
		$name = preg_replace("%http.+\?category=(.+?)%si", "$1", $file);
		if ($name) {parsXML($name);}
	}
}

function parsXML($file_name){

	$response = file_get_contents(getDomen().'/parser/xml/transistor_catalog_'.$file_name.'.xml');	
	
	if (!$response) {print '<h3 style="color:red">file not found: '.getDomen().'/parser/xml/transistor_catalog_'.$file_name.'.xml</h3>';}

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");

	$products = array();
	foreach ($data as $element){
		$params = array(); $article="";
		foreach ($element->childNodes as $item){
			if ($item->nodeName == "group"){
				$params["cat_id"] = $item->getAttribute('id');
				$value = $item->nodeValue;		
			}
			if ($item->nodeName == "article"){$article = $item->nodeValue;}
			if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
				if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
				else {$value = $item->nodeValue;
					if ($item->nodeName == "name"){$value = getName($item);}
					$params[$item->nodeName] = $value;
				}
			}
		}
		$products[$article] = $params; $counts++;
	}
	
	print '<h3>'.$file_name.': '.sizeof($products).'</h3>';
	
	parsProductsXML($products);
}


function parsProductsXML($data, $supplier = 1){
		
	$counts="0"; $updates="0";
	foreach ($data as $article => $array){
		$techdata = array();
		foreach ($array as $key => $value){			
			if ($key != "techdata"){
				if ($key == "cat_id"){$cat_id = $value;}
				else if ($key == "name"){$name = $value;}
				else if ($key == "developer"){$developer = $value;}
				else if ($key == "case"){$case = $value;}
				else if ($key == "advstatus"){$advstatus = $value;}
				else if ($key == "status"){$status = $value;}
				else if ($key == "archive"){$archive = $value;}
				else if ($key == "stock"){$stock = $value;}
				else if ($key == "possible"){$possible = $value;}
				else if ($key == "waiting"){$waiting = $value;}
				else if ($key == "pack"){$pack = $value;}
				else if ($key == "packnorm"){$packnorm = $value;}
				else if ($key == "unit"){$unit = $value;}
				else if ($key == "pricestatus"){$pricestatus = $value;}
				else if ($key == "price1"){$price1 = $value;}
				else if ($key == "price2"){$price2 = $value;}
				else if ($key == "color1"){$color1 = $value;}
				else if ($key == "color2"){$color2 = $value;}
				else if ($key == "color3"){$color3 = $value;}
				else if ($key == "related"){$related = $value;}
				else if ($key == "techinfo"){$techinfo = $value;}
				else if ($key == "pdf"){$pdf = $value;}
				else if ($key == "img"){$img = $value;}
				else if ($key == "descript"){$descript = $value;}
			}
			else if ($key == "techdata"){
				foreach ($value as $field => $val){
					$techdata[$field] = $val;
				}
			}	
		}
		$price = $price1;
		$price_opt = $price1 - $price1*0.15;
		$price_opt_large = $price2;				
		$price_cost = $price2 - $price2*0.12;
			
		$name = preg_replace("%'%si", "\'", $name);
		$descript = preg_replace("%'%si", "\'", $descript);
		
		$colors = $color1."|".$color2."|".$color3;
		$colors = preg_replace("%(\|)+$%", "", $colors);
		
		$res = mysql_query("SELECT p_id FROM cat_product WHERE p_art = '".cp1251($article)."' AND p_supplier = '".$supplier."' LIMIT 1");
		if (!mysql_num_rows($res)){
			// Добавляем товар в единый каталог
			$p_id="";
			$result = mysql_query("SELECT p_id FROM cat_product ORDER BY p_id DESC LIMIT 1");
			while ($row = @mysql_fetch_array($result)){
				$p_id = $row["p_id"];
			}		
			$p_id += 1;
		
			mysql_query("INSERT INTO `cat_product` (`p_id`, `p_name`, `cat_id`, `p_price`, `p_price_opt`, `p_price_opt_large`, `p_price_cost`, `p_price_old`, `p_count`, `p_hit`, `p_spec`, `p_news`, `p_art`, `p_desc_sm`, `p_img_url`, `p_supplier`, `p_desc_top`, `p_desc_bottom`, `p_title`, `p_meta_desc`, `p_meta_key`, `p_date_add`, `p_date_up`, `p_show`, `p_show_head`, `p_alias`, `p_redirect`, `p_type_id`, `p_color_rel`, `p_stock`, `p_waiting`, `p_possible`, `p_color`, `p_pack`, `p_packnorm`, `p_unit`, `p_related`, `p_raiting`, `p_raiting_count`, `p_maket`) VALUES(".$p_id.", '".cp1251($name)."', '".$cat_id."', '".$price."', '".$price_opt."', '".$price_opt_large."', '".$price_cost."', NULL, ".$stock.", '".$p_hit."', '".$p_spec."', '".$p_news."', '".$article."', '".cp1251($descript)."', '".cp1251($img)."', '".$supplier."', NULL, NULL, NULL, NULL, NULL, NOW(), NOW(), 1, 1, '".cp1251(translit($name))."', NULL, NULL, NULL, '".$stock."', '".$waiting."', '".$possible."', '".cp1251($colors)."', '".cp1251($pack)."', '".$packnorm."', '".cp1251($unit)."', '".($related ? $related : '')."', '0.0', '0', 2)");
			
			$res = mysql_query("SELECT p_id FROM cat_product_fields WHERE p_id = '".($p_id+1000)."' LIMIT 1");
			if (!mysql_num_rows($res)){
			
				// Добавляем характеристики товара
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Производитель')."', '".cp1251($developer)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Корпус')."', '".cp1251($case)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Выводится из продажи')."', '".cp1251($status)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Ожидание товара')."', '".cp1251($waiting)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Вид упаковки')."', '".cp1251($pack)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Норма упаковки')."', '".cp1251($packnorm)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Единица измерения')."', '".cp1251($unit)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Изменение цены')."', '".cp1251($pricestatus)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Цвет 1')."', '".cp1251($color1)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Цвет 2')."', '".cp1251($color2)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Цвет 3')."', '".cp1251($color3)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Ссылка на описание')."', '".cp1251($techinfo)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Ссылка на PDF')."', '".cp1251($pdf)."', '0')");
				mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Связанные товары')."', '".cp1251($related)."', '0')");
				
				// Добавляем уникальные характеристики товара
				foreach ($techdata as $field => $val){
					mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251($field)."', '".cp1251($val)."', '1')");
				}
				$counts++;
			}
		}
		else {
			// Обновляем цены и прочие данные, если товар уже был
			mysql_query("UPDATE cat_product SET `cat_id`='".$cat_id."', `p_price`='".$price."', `p_price_opt`='".$price_opt."', `p_price_opt_large`='".$price_opt_large."', `p_price_cost`='".$price_cost."', `p_count`='".$stock."', `p_stock`='".$stock."', `p_waiting`='".$waiting."', `p_possible`='".$possible."', `p_color`='".cp1251($colors)."', `p_pack`='".cp1251($pack)."', `p_packnorm`='".$packnorm."', `p_unit`='".cp1251($unit)."', `p_related`='".($related ? $related : '')."', `p_show`='1', `p_date_up`=NOW() WHERE p_art='".$article."' AND p_supplier = '".$supplier."' LIMIT 1");	
			$res = mysql_query("SELECT p_id FROM cat_product WHERE p_art = '".cp1251($article)."' AND p_supplier = '".$supplier."' LIMIT 1");
			while ($row = @mysql_fetch_array($res)){
				$p_id = $row["p_id"];
			}
			if ($p_id){
				mysql_query("UPDATE cat_product_fields SET `value`='".cp1251($related)."' WHERE p_id='".$p_id."' AND field='".cp1251('Связанные товары')."' LIMIT 1");
			}
			$updates++;
		}
	}
	$class1=' style="color:green"'; $class2=' style="color:green"';
	if (!$counts){$class1=' style="color:gray"';}
	if (!$updates){$class2=' style="color:gray"';}
	print '<h3'.$class1.'>Загружено новых: '.$counts.'</h3>';
	print '<h3'.$class2.'>Обновлено, количество: '.$updates.'</h3><br>';
}

?>