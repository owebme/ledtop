<?php

ini_set('max_execution_time', 600);

function getDomen(){
	return 'http://ledtop-shop.ru';
}

$pars_xml = 0;
$clear = 1;
$pars_catalog = 1;
$pars_image = 1;
$backup_to = 0;
$backup_from = 0;

require_once 'db.php';
require_once '../function.php';

header("Content-type: text/html; charset=utf-8");

print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<style>html {width:988px; margin:25px auto 0; font-family: Arial, Helvetica;} body {margin:0;} h2, h3 {margin:0 0 10px;} h2 {font-size:1.7em; margin-bottom:12px;}</style>';

if ($backup_to){
	file_get_contents(getDomen().'/parser/backup.php?action=security&time=to');
}

require_once '../get_xml.php';

if ($pars_xml){
	getFile('ledribbon');
	getFile('supply');
	getFile('lightcontrol');
	getFile('profile');
	getFile('ledlamps');
	getFile('ledbulbs');
	getFile('ledmodules');
	getFile('ledprojectors');
	getFile('leds');
}

if ($clear){
	mysql_query("TRUNCATE TABLE `category_alright`");
	mysql_query("TRUNCATE TABLE `products_alright`");
	#sleep(2);
}

if ($pars_catalog){
	parsXML('leds');
	parsXML('ledribbon');
	parsXML('ledbulbs');
	parsXML('ledlamps');
	parsXML('ledmodules');
	parsXML('ledprojectors');
	parsXML('lightcontrol');
	parsXML('supply');
	parsXML('profile');
}

if ($pars_image){

	$result = mysql_query("SELECT p_name, p_art, p_image FROM products_alright WHERE p_image !=''");
	while ($row = @mysql_fetch_array($result)){
		$image = $row["p_image"];
		if ($image && !file_exists("../../files/catalog/".$row["p_art"].".jpg")){
			print $row["p_art"]." - ".cp1251($row["p_name"])."<br>";
			$file = file_get_contents($image);
			if ($file){
				$fp = fopen("../../files/catalog/".$row["p_art"].".jpg", 'w');
				fwrite($fp, $file);
				fclose($fp);
			}
		}
	}
}

if ($backup_from){
	file_get_contents(getDomen().'/parser/backup.php?action=security&time=from');
}

function parsXML($file_name){

	$response = file_get_contents(getDomen().'/parser/transistor_catalog_'.$file_name.'.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");

	$parents = array(); $c_pid="";
	foreach ($data as $element){
		foreach ($element->childNodes as $item){
			if ($item->nodeName == "group"){
				$id = $item->getAttribute('id');
				$value = $item->nodeValue;
				preg_match_all('%(.+?)/\s(.+?)\s/\s(.+?)$%', $value, $result);
				$parent = trim($result[1][0]);
				$result = mysql_query("SELECT c_id FROM category_alright WHERE c_name = '".cp1251($parent)."' AND c_pid = '0' LIMIT 1");
				if (!mysql_num_rows($result)){
					print '<h2 style="color:brown">'.$parent.'</h2>';
					mysql_query("INSERT INTO `category_alright` (`c_pid`, `c_name`) VALUES('0', '".cp1251($parent)."')");
				}
				$result = mysql_query("SELECT c_id FROM category_alright WHERE c_name = '".cp1251($parent)."' AND c_pid = '0' LIMIT 1");
				while ($row = @mysql_fetch_array($result)){		
					$c_pid = $row["c_id"];
				}
				$category = preg_replace("%(.+?)/\s(.+?)\s/\s(.+?)$%si", "$2", $value);
				if (!in_array($category, $parents)){
					array_push($parents, $category);
				}
			}
		}
	}
	
	if (sizeof($parents) > 0){
	
		foreach ($parents as $item){
			$res = mysql_query("SELECT c_id FROM category_alright WHERE c_name = '".cp1251($item)."' AND c_pid = '".$c_pid."' LIMIT 1");
			if (!mysql_num_rows($res)){
				mysql_query("INSERT INTO `category_alright` (`c_pid`, `c_name`) VALUES('".$c_pid."', '".cp1251($item)."')");
			}
		}
		
		$category = array();
		foreach ($data as $element){
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					if (!$category[$id]){
						$parent_xml = $item->nodeValue;
						$parent = preg_replace("%(.+?)/\s(.+?)\s/\s(.+?)$%si", "$2", $parent_xml);
						$category[$id] = preg_replace("%(.+?)/\s(.+?)\s/\s(.+?)$%si", "$3", $parent_xml);
						$parent_id="";
						$result = mysql_query("SELECT c_id FROM category_alright WHERE c_pid = '".$c_pid."' AND c_name = '".cp1251($parent)."' LIMIT 1");
						while ($row = @mysql_fetch_array($result)){
							$parent_id = $row["c_id"];
						}
						$cat_id="";
						$res = mysql_query("SELECT c_id FROM category_alright WHERE c_name = '".cp1251($category[$id])."' AND c_pid = '".$parent_id."' LIMIT 1");
						if (!mysql_num_rows($res)){
							mysql_query("INSERT INTO `category_alright` (`c_pid`, `c_name`) VALUES('".$parent_id."', '".cp1251($category[$id])."')");
							$result = mysql_query("SELECT c_id FROM category_alright ORDER BY c_id DESC LIMIT 1");
							while ($row = @mysql_fetch_array($result)){		
								$cat_id = $row["c_id"];
							}
						}
						else {
							while ($row = @mysql_fetch_array($res)){		
								$cat_id = $row["c_id"];
							}
						}
						
						$products = array();
						foreach ($data as $sub_element){
							$params = array(); $flag=""; $article="";
							foreach ($sub_element->childNodes as $sub_item){
								if ($sub_item->nodeName == "group"){
									$value = $sub_item->nodeValue;
									if ($parent_xml == $value){
										$flag = true;
									}									
								}
								if ($sub_item->nodeName == "article"){$article = $sub_item->nodeValue;}
								if ($article && $sub_item->nodeName != "#text" && $sub_item->nodeName != "article" && $sub_item->nodeName != "category" && $sub_item->nodeName != "group"){
									if ($sub_item->nodeName == "techdata"){$params['techdata'] = parsTechData($sub_item);}
									else {$value = $sub_item->nodeValue;
										if ($sub_item->nodeName == "name"){$value = getName($sub_item);}
										$params[$sub_item->nodeName] = $value;
									}
								}
							}
							if ($flag){$products[$article] = $params; $counts++;}
						}
						
						print '<h3>'.$category[$id].': '.sizeof($products).'</h3>';
						
						parsProductsXML($products, $cat_id);
					}
				}
			}
		}
	}
}


function parsProductsXML($data, $cat_id){

	if ($cat_id > 0){
		
		$counts="0";
		foreach ($data as $article => $array){
			#print "Артикуль:".$article."<br>";
			$techdata = array();
			foreach ($array as $key => $value){
				if ($key != "techdata"){
					#print $key.": ".$value."<br>";
					if ($key == "name"){$name = $value;}
					else if ($key == "stock"){$stock = $value;}
					else if ($key == "possible"){$possible = $value;}
					else if ($key == "waiting"){$waiting = $value;}
					else if ($key == "pack"){$pack = $value;}
					else if ($key == "packnorm"){$packnorm = $value;}
					else if ($key == "unit"){$unit = $value;}
					else if ($key == "price1"){$price1 = $value;}
					else if ($key == "price2"){$price2 = $value;}
					else if ($key == "color1"){$color1 = $value;}
					else if ($key == "color2"){$color2 = $value;}
					else if ($key == "color3"){$color3 = $value;}
					else if ($key == "related"){$related = $value;}
					else if ($key == "img"){$img = $value;}
					else if ($key == "descript"){$descript = $value;}
				}
			}
			$price = $price1;
			$price_opt = $price1 - $price1*0.15;
			$price_opt_large = $price2;				
			$price_cost = $price2 - $price2*0.12;
				
			$descript = preg_replace("%'%si", "\'", $descript);
			
			$colors = $color1."|".$color2."|".$color3;
			$colors = preg_replace("%(\|)+$%", "", $colors);
			
			// Добавляем товар
			mysql_query("INSERT INTO `products_alright` (`p_art`, `cat_id`, `p_name`, `p_image`, `p_price`, `p_price_opt`, `p_price_opt_large`, `p_price_cost`, `p_desc`, `p_stock`, `p_waiting`, `p_possible`, `p_color`, `p_pack`, `p_packnorm`, `p_unit`, `p_related`) VALUES('".$article."', '".$cat_id."', '".cp1251($name)."', '".$img."', '".$price."', '".$price_opt."', '".$price_opt_large."', '".$price_cost."', '".cp1251($descript)."', '".$stock."', '".$waiting."', '".$possible."', '".cp1251($colors)."', '".cp1251($pack)."', '".$packnorm."', '".cp1251($unit)."', '".($related?$related:'')."')");
			$counts++;
		}
		$class1=' style="color:green"'; $class2=' style="color:green"';
		if (!$counts){$class1=' style="color:gray"';}
		print '<h3'.$class1.'>Загружено товаров: '.$counts.'</h3>';
	}
	else {
		print '<h3 style="color:red">Не найдена "'.$category.'" категория в БД</h3>';
	}
}

?>