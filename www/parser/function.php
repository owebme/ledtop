<?php

function parsProducts($data, $category, $supplier = 1){

	if ($category > 0){}
	else if ($category){
		$res = mysql_query("SELECT c_id FROM cat_category WHERE c_name = '".cp1251($category)."' LIMIT 1");
		if (!mysql_num_rows($res)){
			mysql_query("INSERT INTO `cat_category` (`c_name`, `c_name_short`, `c_name_org`, `c_pos`, `c_pid`, `c_desc_top`, `c_desc_bottom`, `c_title`, `c_meta_desc`, `c_meta_key`, `c_date_add`, `c_date_up`, `c_show`, `c_show_head`, `c_show_menu`, `c_hide_child`, `c_show_child_count`, `c_mirror_id`, `c_mirror_link`, `c_alias`, `c_redirect`, `c_maket`) VALUES('".cp1251($item)."', '', '".cp1251($item)."', ".$pos.", ".$c_pid.", '', '', '', '', '', NOW(), NOW(), 1, 1, 1, 0, NULL, '', '', '".$alias."', NULL, 2)");		
		}
	}

	$cat_id=""; $c_pid="";
	$result = mysql_query("SELECT c_id, c_pid FROM cat_category WHERE ".($category > 0?"c_id = '".$category."'":"c_name = '".cp1251($category)."'")." LIMIT 1");
	while ($row = @mysql_fetch_array($result)){
		$cat_id = $row["c_id"];
		$c_pid = $row["c_pid"];
	}
	if ($cat_id > 0){
		mysql_query("UPDATE cat_category SET `c_date_up`=NOW() WHERE c_id='".$c_pid."' LIMIT 1");
		mysql_query("UPDATE cat_category SET `c_date_up`=NOW() WHERE c_id='".$cat_id."' LIMIT 1");
		if ($c_pid != "0"){
			$parent_id = findParentID($c_pid);
		}
		else {
			$parent_id = $c_pid;
		}
		
		$counts="0"; $updates="0";
		foreach ($data as $article => $array){
			#print "Артикуль:".$article."<br>";
			$techdata = array();
			if ($supplier == 2) {
				$color1=""; $color2=""; $color3="";
				foreach ($array as $key => $value){
					if ($key != "techdata"){
						#print $key.": ".$value."<br>";
						if ($key == "name"){$name = $value;}
						else if ($key == "price1"){$price = $value;}
						else if ($key == "price2"){$price_opt = $value;}
						else if ($key == "price3"){$price_opt_large = $value;}
						else if ($key == "price5"){$price_cost = $value;}
						else if ($key == "pack"){$pack = $value;}
						else if ($key == "packnorm"){$packnorm = $value;}
						else if ($key == "unit"){$unit = $value;}
						else if ($key == "color1"){$color1 = $value;}
						else if ($key == "color2"){$color2 = $value;}
						else if ($key == "color3"){$color3 = $value;}
						else if ($key == "pdf"){$pdf = $value;}
						else if ($key == "img"){$img = $value;}
						else if ($key == "descript"){$descript = $value;}
					}
					else if ($key == "techdata"){
						#print "Технические характеристики:<br>";
						foreach ($value as $field => $val){
							#print $field.": ".$val."<br>";
							$techdata[$field] = $val;
						}
					}	
				}
				$stock = 999;				
			}
			else {
				foreach ($array as $key => $value){
					if ($key != "techdata"){
						#print $key.": ".$value."<br>";
						if ($key == "name"){$name = $value;}
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
						#print "Технические характеристики:<br>";
						foreach ($value as $field => $val){
							#print $field.": ".$val."<br>";
							$techdata[$field] = $val;
						}
					}	
				}
				$price = $price1;
				$price_opt = $price1 - $price1*0.15;
				$price_opt_large = $price2;				
				$price_cost = $price2 - $price2*0.12;
			}
			$p_hit="0"; $p_spec="0"; $p_news="0";
			if ($advstatus == "1"){$p_news = "1";}
			else if ($advstatus == "2"){$p_spec = "1";}
			else if ($advstatus == "3"){$p_hit = "1";}
		
			$res = mysql_query("SELECT p_id FROM cat_product WHERE p_art = '".cp1251($article)."' LIMIT 1");
			if (!mysql_num_rows($res)){
				// Добавляем товар
				$p_id="";
				$result = mysql_query("SELECT p_id FROM cat_product ORDER BY p_id DESC LIMIT 1");
				while ($row = @mysql_fetch_array($result)){
					$p_id = $row["p_id"];
				}		
				$p_id += 1;
				
				$descript = preg_replace("%'%si", "\'", $descript);
			
				mysql_query("INSERT INTO `cat_product` (`p_id`, `p_name`, `p_price`, `p_price_opt`, `p_price_opt_large`, `p_price_cost`, `p_price_old`, `p_count`, `p_hit`, `p_spec`, `p_news`, `p_art`, `p_desc_sm`, `p_img_url`, `p_supplier`, `p_desc_top`, `p_desc_bottom`, `p_title`, `p_meta_desc`, `p_meta_key`, `p_date_add`, `p_date_up`, `p_show`, `p_show_head`, `p_alias`, `p_redirect`, `p_type_id`, `p_color_rel`, `p_raiting`, `p_raiting_count`, `p_maket`) VALUES(".$p_id.", '".cp1251($name)."', '".$price."', '".$price_opt."', '".$price_opt_large."', '".$price_cost."', NULL, ".$stock.", '".$p_hit."', '".$p_spec."', '".$p_news."', '".$article."', '".cp1251($descript)."', '".cp1251($img)."', '".$supplier."', NULL, NULL, NULL, NULL, NULL, NOW(), NOW(), 1, 1, '".cp1251(translit($name))."', NULL, NULL, NULL, '0.0', '0', 2)");
				
				$res = mysql_query("SELECT p_id FROM cat_product_fields WHERE p_id = '".($p_id+1000)."' LIMIT 1");
				if (!mysql_num_rows($res)){
				
					// Добавляем характеристики товара
					if ($supplier == 2) {
						mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Вид упаковки')."', '".cp1251($pack)."', '0')");
						mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Норма упаковки')."', '".cp1251($packnorm)."', '0')");
						mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Единица измерения')."', '".cp1251($unit)."', '0')");
						if ($color1){
							mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Цвет 1')."', '".cp1251($color1)."', '0')");
						}
						if ($color2){
							mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Цвет 2')."', '".cp1251($color2)."', '0')");
						}
						if ($color3){
							mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Цвет 3')."', '".cp1251($color3)."', '0')");
						}		
						if ($pdf){
							mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251('Ссылка на PDF')."', '".cp1251($pdf)."', '0')");			
						}
					}
					else {
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
					}
					
					// Добавляем уникальные характеристики товара
					foreach ($techdata as $field => $val){
						$res = mysql_query("SELECT id FROM cat_product_fields_set WHERE cat_id = '".$parent_id."' AND f_name = '".cp1251($field)."' LIMIT 1");
						if (!mysql_num_rows($res)){
							$f_pos="";
							$result = mysql_query("SELECT f_pos FROM cat_product_fields_set WHERE cat_id = '".$parent_id."' ORDER BY f_pos DESC LIMIT 1");
							while ($row = @mysql_fetch_array($result)){
								$f_pos = $row["f_pos"];
							}	
							$f_pos += 1;					
							mysql_query("INSERT INTO `cat_product_fields_set` (`cat_id`, `f_name`, `type`, `f_pos`) VALUES(".$parent_id.", '".cp1251($field)."', 'string', ".$f_pos.")");
						}				
						mysql_query("INSERT INTO `cat_product_fields` (`p_id`, `field`, `value`, `unic`) VALUES(".$p_id.", '".cp1251($field)."', '".cp1251($val)."', '1')");
					}
					$counts++;
				}
			}
			else {
				// Обновляем цены и прочие данные, если товар уже был
				mysql_query("UPDATE cat_product SET `p_price`='".$price."', `p_price_opt`='".$price_opt."', `p_price_opt_large`='".$price_opt_large."', `p_price_cost`='".$price_cost."', `p_count`='".$stock."', `p_hit`='".$p_hit."', `p_spec`='".$p_spec."', `p_news`='".$p_news."', `p_show`='1', `p_date_up`=NOW() WHERE p_art='".$article."' LIMIT 1");
				
				$res = mysql_query("SELECT p_id FROM cat_product WHERE p_art = '".cp1251($article)."' LIMIT 1");
				while ($row = @mysql_fetch_array($res)){
					$p_id = $row["p_id"];
				}
				if ($p_id){
					mysql_query("UPDATE cat_product_fields SET `value`='".cp1251($related)."' WHERE p_id='".$p_id."' AND field='".cp1251('Связанные товары')."' LIMIT 1");
				}
				$updates++;
			}
			
			$res = mysql_query("SELECT p_id, p_alias FROM cat_product WHERE p_art = '".cp1251($article)."' LIMIT 1");
			if (mysql_num_rows($res)){
				$p_id="";
				while ($row = @mysql_fetch_array($res)){
					$p_id = $row["p_id"];
					$p_alias = $row["p_alias"];
				}
				
				$p_pos="";
				$result = mysql_query("SELECT p_pos FROM cat_product_rel WHERE cat_id = '".$cat_id."' ORDER BY p_pos DESC LIMIT 1");
				while ($row = @mysql_fetch_array($result)){
					$p_pos = $row["p_pos"];
				}	
				$p_pos += 1;
				
				// Размещяем товар в соотвествии с сортировкой
				$res = mysql_query("SELECT cat_p_id FROM cat_product_rel WHERE cat_id != '".$cat_id."' AND cat_p_id = '".$p_id."' AND cat_main = '1' LIMIT 1");
				if (mysql_num_rows($res)){
					mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$p_id."' AND cat_id = '".$cat_id."' AND cat_main = '0'");
					mysql_query("INSERT INTO `cat_product_rel` (`cat_p_id`, `cat_id`, `cat_main`, `p_pos`) VALUES(".$p_id.", ".$cat_id.", '0', ".$p_pos.")");
				}				
				else {
					$res = mysql_query("SELECT cat_p_id FROM cat_product_rel WHERE cat_id = '".$cat_id."' AND cat_p_id = '".$p_id."' AND cat_main = '1' LIMIT 1");
					if (!mysql_num_rows($res)){
						mysql_query("INSERT INTO `cat_product_rel` (`cat_p_id`, `cat_id`, `cat_main`, `p_pos`) VALUES(".$p_id.", ".$cat_id.", '1', ".$p_pos.")");
					}
				}
				
				if ($c_pid > 0){
					$res = mysql_query("SELECT cat_p_id FROM cat_product_rel WHERE cat_id = '".$c_pid."' AND cat_p_id = '".$p_id."' LIMIT 1");
					if (!mysql_num_rows($res)){
						$p_pos="";
						$result = mysql_query("SELECT p_pos FROM cat_product_rel WHERE cat_id = '".$c_pid."' ORDER BY p_pos DESC LIMIT 1");
						while ($row = @mysql_fetch_array($result)){
							$p_pos = $row["p_pos"];
						}	
						$p_pos += 1;
						mysql_query("INSERT INTO `cat_product_rel` (`cat_p_id`, `cat_id`, `cat_main`, `p_pos`) VALUES(".$p_id.", ".$c_pid.", '0', ".$p_pos.")");
					}				
				}
				mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$p_id."' AND cat_id = '".$parent_id."'");
				$p_pos="";
				$result = mysql_query("SELECT p_pos FROM cat_product_rel WHERE cat_id = '".$parent_id."' ORDER BY p_pos DESC LIMIT 1");
				while ($row = @mysql_fetch_array($result)){
					$p_pos = $row["p_pos"];
				}	
				$p_pos += 1;
				mysql_query("INSERT INTO `cat_product_rel` (`cat_p_id`, `cat_id`, `cat_main`, `p_pos`) VALUES(".$p_id.", ".$parent_id.", '0', ".$p_pos.")");					
			}
		}
		$class1=' style="color:green"'; $class2=' style="color:green"';
		if (!$counts){$class1=' style="color:gray"';}
		if (!$updates){$class2=' style="color:gray"';}
		print '<h3'.$class1.'>Загружено новых: '.$counts.'</h3>';
		print '<h3'.$class2.'>Обновлено, количество: '.$updates.'</h3><br>';
	}
	else {
		print '<h3 style="color:red">Не найдена "'.$category.'" категория в БД</h3>';
	}
}

function parserCategory($data, $name_org, $name, $c_pid, $concat=false){

	createCategory($name_org, $c_pid, 0, $name);

	$cat_id=""; $c_pid="";
	$result = mysql_query("SELECT c_id, c_pid FROM cat_category WHERE c_name = '".cp1251($name)."' LIMIT 1");
	while ($row = @mysql_fetch_array($result)){
		$cat_id = $row["c_id"];
		$c_pid = $row["c_pid"];
	}
	if ($cat_id > 0){
	
		$name = $name_org;
	
		mysql_query("UPDATE cat_category SET `c_date_up`=NOW() WHERE c_id='".$cat_id."' LIMIT 1");
		
		$name2 = $name;
		$name2 = preg_replace("%\[%si", "\[", $name2); $name2 = preg_replace("%\]%si", "\]", $name2);
		$name2 = preg_replace("%\+%si", "\+", $name2);
		$name2 = preg_replace("%\(%si", "\(", $name2); $name2 = preg_replace("%\)%si", "\)", $name2);
		
		$name2 = substr($name2, 2);
		
		$parents = array();
		if (!$concat){
			foreach ($data as $element){
				foreach ($element->childNodes as $item){
					if ($item->nodeName == "group"){
						$id = $item->getAttribute('id');
						$value = $item->nodeValue;
						if (preg_match('%'.$name2.'%ui', $value)){
							$category = preg_replace("%(.+?)/\s(.+?)\s/\s(.+?)$%si", "$3", $value);
							if (!in_array($category, $parents)){
								array_push($parents, $category);
							}
						}
					}
				}
			}
			$pos="";
		}
		else {
			array_push($parents, $name);
		}
		foreach ($parents as $item){
			if (!$concat){
				$pos++;
				$alias = translit($item);
				$res = mysql_query("SELECT c_id FROM cat_category WHERE c_pid ='".$cat_id."' AND c_name_org = '".cp1251($item)."' LIMIT 1");
				if (!mysql_num_rows($res)){
					mysql_query("INSERT INTO `cat_category` (`c_name`, `c_name_short`, `c_name_org`, `c_name_id`, `c_pos`, `c_pid`, `c_supplier`, `c_desc_top`, `c_desc_bottom`, `c_desc_sm`, `c_title`, `c_meta_desc`, `c_meta_key`, `c_date_add`, `c_date_up`, `c_show`, `c_show_head`, `c_show_menu`, `c_hide_child`, `c_show_child_count`, `c_mirror_id`, `c_mirror_link`, `c_alias`, `c_redirect`, `c_maket`) VALUES('".cp1251($item)."', '', '".cp1251($item)."', NULL, ".$pos.", ".$cat_id.", '1', '', '', '', '', '', '', NOW(), NOW(), 1, 1, 1, 0, NULL, '', '', '".$alias."', NULL, 2)");
				}
				else {
					mysql_query("UPDATE cat_category SET `c_date_up` = NOW() WHERE c_pid ='".$cat_id."' AND c_name_org='".cp1251($item)."' LIMIT 1");
				}
				
				$res = mysql_query("SELECT c_id, c_name_org FROM cat_category WHERE c_pid ='".$cat_id."' AND c_name_org = '".cp1251($item)."' LIMIT 1");
				while ($row = @mysql_fetch_array($res)){
					$c_id = $row["c_id"];
					$c_name = $row["c_name_org"];
				}
			}
			else {
				$c_id = $cat_id;
				$c_name = $name;
			}
			if ($c_id > 0){
			
				if (!$concat){
					$c_name = utf8($c_name);
					$c_name2 = $c_name;
					$c_name2 = preg_replace("%\[%si", "\[", $c_name2); $c_name2 = preg_replace("%\]%si", "\]", $c_name2);
					$c_name2 = preg_replace("%\+%si", "\+", $c_name2);
					$c_name2 = preg_replace("%\(%si", "\(", $c_name2); $c_name2 = preg_replace("%\)%si", "\)", $c_name2);					
					$c_name2 = substr($c_name2, 2);
				}
				else {
					$c_name2 = $name2;
				}				
				$products = array();
				foreach ($data as $element){
					$params = array(); $flag=""; $article="";
					foreach ($element->childNodes as $item){
						if ($item->nodeName == "group"){
							$value = $item->nodeValue;
							if (preg_match('%'.$c_name2.'%ui', $value)){
								$flag = true;
							}
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
					if ($flag){$products[$article] = $params;}
				}
				
				if (!sizeof($products)){
					print '<h3 style="color:red">Не найдена "'.$c_name.'" категория в XML</h3>';
				}
				else {
					mysql_query("UPDATE cat_category SET `c_date_up`=NOW() WHERE c_id='".$c_id."' LIMIT 1");
					
					print '<h3>'.$c_name.': '.sizeof($products).'</h3>';
					
					parsProducts($products, $c_id);
				}
			}
		}
		file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);
	}
	else {
		print '<h3 style="color:red">Не найдена "'.$name.'" категория в БД</h3>';
	}	
}

function parserCatalog($data, $c_pid){
	$result = mysql_query("SELECT c_id FROM cat_category WHERE c_id = '".$c_pid."' LIMIT 1");
	if (mysql_num_rows($result)){
		$parents = array();
		foreach ($data as $element){
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					$category = preg_replace("%(.+?)/\s(.+?)\s/\s(.+?)$%si", "$2", $value);
					if (!in_array($category, $parents)){
						array_push($parents, $category);
					}
				}
			}
		}
		$pos="";
		foreach ($parents as $item){
			$pos++;
			$alias = translit($item);
			$res = mysql_query("SELECT c_id FROM cat_category WHERE c_name_org = '".cp1251($item)."' LIMIT 1");			
			if (!mysql_num_rows($res)){
				mysql_query("INSERT INTO `cat_category` (`c_name`, `c_name_short`, `c_name_org`, `c_name_id`, `c_pos`, `c_pid`, `c_supplier`, `c_desc_top`, `c_desc_bottom`, `c_title`, `c_meta_desc`, `c_meta_key`, `c_date_add`, `c_date_up`, `c_show`, `c_show_head`, `c_show_menu`, `c_hide_child`, `c_show_child_count`, `c_mirror_id`, `c_mirror_link`, `c_alias`, `c_redirect`, `c_maket`) VALUES('".cp1251($item)."', '', '".cp1251($item)."', NULL, ".$pos.", ".$c_pid.", '1', '', '', '', '', '', NOW(), NOW(), 1, 1, 1, 0, NULL, '', '', '".$alias."', NULL, 2)");
			}
			else {
				mysql_query("UPDATE cat_category SET `c_date_up` = NOW() WHERE c_name_org='".cp1251($item)."' LIMIT 1");
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
						$pos=""; $parent_id="";
						$result = mysql_query("SELECT c_id FROM cat_category WHERE c_pid = '".$c_pid."' AND c_name_org = '".cp1251($parent)."' LIMIT 1");
						while ($row = @mysql_fetch_array($result)){		
							$parent_id = $row["c_id"];
						}
						$result = mysql_query("SELECT c_pos FROM cat_category WHERE c_pid = '".$parent_id."' ORDER BY c_pos DESC LIMIT 1");
						while ($row = @mysql_fetch_array($result)){		
							$pos = $row["c_pos"];
						}			
						$pos += 1;
						$alias = translit($category[$id]); $cat_id="";
						$res = mysql_query("SELECT c_id FROM cat_category WHERE c_name_id = '".$id."' LIMIT 1");
						if (!mysql_num_rows($res)){
							mysql_query("INSERT INTO `cat_category` (`c_name`, `c_name_short`, `c_name_org`, `c_name_id`, `c_pos`, `c_pid`, `c_supplier`, `c_desc_top`, `c_desc_bottom`, `c_title`, `c_meta_desc`, `c_meta_key`, `c_date_add`, `c_date_up`, `c_show`, `c_show_head`, `c_show_menu`, `c_hide_child`, `c_show_child_count`, `c_mirror_id`, `c_mirror_link`, `c_alias`, `c_redirect`, `c_maket`) VALUES('".cp1251($category[$id])."', '', '".cp1251($category[$id])."', ".$id.", ".$pos.", ".$parent_id.", '1', '', '', '', '', '', NOW(), NOW(), 1, 1, 1, 0, NULL, '', '', '".$alias."', NULL, 2)");
							$result = mysql_query("SELECT c_id FROM cat_category ORDER BY c_id DESC LIMIT 1");
							while ($row = @mysql_fetch_array($result)){		
								$cat_id = $row["c_id"];
							}
						}
						else {
							mysql_query("UPDATE cat_category SET `c_name` = '".cp1251($category[$id])."', `c_name_org` = '".cp1251($category[$id])."', `c_date_up` = NOW() WHERE c_name_id = '".$id."' LIMIT 1");
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
						
						parsProducts($products, $cat_id);
					}
				}
			}
		}
		file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);
	}
	else {
		print '<h3 style="color:red">Не найдена основная категория</h3>';
	}	
}

function getName($item){
	$value = $item->nodeValue;
	if ($item->getAttribute('prefix') != ""){$value = $item->getAttribute('prefix')." ".$value;}
	return $value;
}

function parsTechData($data){
	$techdata = array();
	foreach ($data->childNodes as $item){
		if ($item->nodeName == "param"){
			$name=""; $value="";
			foreach ($item->childNodes as $param){
				if ($param->nodeName == "name"){$name .= $param->nodeValue;}
				if ($param->nodeName == "unit" && $param->nodeValue){$name .= ', '.$param->nodeValue;}
				if ($param->nodeName == "values"){$value = trim($param->nodeValue);}
			}
			$techdata[$name] = $value;
		}
	}
	return $techdata;
}

function findParentID($c_pid){
	$res = mysql_query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$c_pid."'");
	if (mysql_num_rows($res)){
		while ($row = @mysql_fetch_array($res)){
			$result = $row["c_id"]; 
			if ($row["c_pid"] == "0"){
				return $result; break;
			}
			else {
				if ($ids = recSubParentCat($row["c_pid"])){
					$result = $ids;
				}
				if ($result){
					return $result; break;
				}
			}
		}
	}
}

function recSubParentCat($parent){
	$res = mysql_query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$parent."'");
	if (mysql_num_rows($res)){
		while ($row = @mysql_fetch_array($res)){
			$result = $row["c_id"]; 
			if ($row["c_pid"] == "0"){
				return $result; break;
			}
			else {
				if ($ids = recSubParentCat($row["c_pid"])){
					$result = $ids;
				}
				if ($result){
					return $result; break;
				}
			}
		}
	}
}

function createCategory($name_org, $c_pid, $return = false, $name = false){
	if ($name_org){
		if ($c_pid > 0){
			$res = mysql_query("SELECT c_id FROM cat_category WHERE c_name_org = '".cp1251($name_org)."' AND c_pid = '".$c_pid."' LIMIT 1");
		}
		else {
			$result = mysql_query("SELECT c_id FROM cat_category WHERE c_name_org = '".cp1251($c_pid)."' LIMIT 1");
			while ($row = @mysql_fetch_array($result)){		
				$c_pid = $row["c_id"];
			}
			$res = mysql_query("SELECT c_id FROM cat_category WHERE c_name_org = '".cp1251($name_org)."' AND c_pid = '".$c_pid."' LIMIT 1");
		}
		if (!mysql_num_rows($res) && $c_pid > 0){
			$result = mysql_query("SELECT c_pos FROM cat_category WHERE c_pid = '".$c_pid."' ORDER BY c_pos DESC LIMIT 1");
			while ($row = @mysql_fetch_array($result)){		
				$pos = $row["c_pos"];
			}			
			$pos += 1;
			$alias = translit($name);
			if (!$name){$name = $name_org;}
			mysql_query("INSERT INTO `cat_category` (`c_name`, `c_name_short`, `c_name_org`, `c_pos`, `c_pid`, `c_desc_top`, `c_desc_bottom`, `c_title`, `c_meta_desc`, `c_meta_key`, `c_date_add`, `c_date_up`, `c_show`, `c_show_head`, `c_show_menu`, `c_hide_child`, `c_show_child_count`, `c_mirror_id`, `c_mirror_link`, `c_alias`, `c_redirect`, `c_maket`) VALUES('".cp1251($name)."', '', '".cp1251($name_org)."', ".$pos.", ".$c_pid.", '', '', '', '', '', NOW(), NOW(), 1, 1, 1, 0, NULL, '', '', '".$alias."', NULL, 2)");		
			
			print '<h3 style="color:green">Создана категория: '.($name?$name:$name_org).'</h3>';
		}
		if ($return){
			$result = mysql_query("SELECT c_id FROM cat_category WHERE c_name = '".cp1251($name_org)."' AND c_pid = '".$c_pid."' LIMIT 1");
			while ($row = @mysql_fetch_array($result)){		
				return $row["c_id"];
			}
		}
	}
}

function eqColor($color) {

	$K = explode("K", $color);
	$color = trim($K[0]);
	
	if ($color > 2000 && $color < 3300){return "Теплый белый";}
	else if ($color > 3600 && $color < 5000){return "Нейтральный белый";}
	else if ($color > 5000){return "Холодный белый";}
}

function eqKColor($color) {
	
	$K = explode("K", $color);
	$color = trim($K[0]);
	
	if ($color > 2000 && $color < 3300){return "warm_white";}
	else if ($color > 3600 && $color < 5000){return "day_white";}
	else if ($color > 5000){return "white";}
}
	
function parsGeniledLinks($url, $address) {
	
	$links = array();
	for ($page=1; $page<=20; $page++){

		$data = file_get_contents('http://geniled.ru'.$address.'?PAGEN_1='.$page.'&page_url=http://geniled.ru'.$url);
		
		if ($data){
		
			$html = new simple_html_dom();
			$html = str_get_html($data);
			
			$elements = $html->find(".orion_isp b");
			foreach($elements as $element) {
				if ($element->plaintext > 0 && $page != $element->plaintext){
					break 2;
				}
			}	
			
			$elements = $html->find(".catalog-section table table");
			foreach($elements as $table) {
				$links_ = $table->find("a");									
				foreach($links_ as $link_) {
					preg_match_all('/Артикул: (\d+)/', $table, $result);
					$article = $result[1][0];
					preg_match_all('/onclick="view_detail_item\(\'(.+)\',\'(\d+)\'\)">[^<img]/Uis', $link_, $result);
					$link = $result[1][0];
					if ($link){
						$links[$article] = $link;
					}
				}
			}

			$html->clear();
			unset($html);
		}
	}
	
	return $links;
}

function parsGeniledLinks2($url, $section) {
	
	$links = array();
	for ($page=1; $page<=20; $page++){

		$data = file_get_contents('http://geniled.ru'.$url.'?PAGEN_1='.$page);
		
		if ($data){
		
			$html = new simple_html_dom();
			$html = str_get_html($data);
			
			$elements = $html->find(".orion_isp b");
			foreach($elements as $element) {
				if ($element->plaintext > 0 && $page != $element->plaintext){
					break 2;
				}
			}	
			
			$elements = $html->find(".wrap table table");
			foreach($elements as $table) {
				$links_ = $table->find("a");									
				foreach($links_ as $link_) {
					preg_match_all('/onclick="view_detail_item\(\'(.+)\',\'(\d+)\'\)">[^<img](.+)<\/a>/Uis', $link_, $result);
					$link = trim($result[1][0]);
					$name = trim($result[3][0]);
					$name = substr($name, 1);
					if ($link && preg_match('%'.$section.'%', $name)){					
						$article="";
						$data = file_get_contents('http://geniled.ru'.$link);						
						if ($data){
							preg_match_all('/<p>Артикул: (\d+)/', $data, $result);
							$article = trim($result[1][0]);	
						}
						if ($article){
							$links[$article] = $data;
						}
					}
				}
			}

			$html->clear();
			unset($html);
		}
	}
	
	return $links;
}

function translit($string, $gost=true){
	$string = strrtolower($string);
	$string = str_replace("'", "", $string);
	$string = str_replace("\"", "", $string);
	$string = str_replace(" – ", "-", $string);
	$string = str_replace(" - ", "-", $string);
	$string = str_replace(" — ", "-", $string);
	$string = str_replace("_", "-", $string);	
    if ($gost)
    {
        $replace = array("А"=>"A","а"=>"a","Б"=>"B","б"=>"b","В"=>"V","в"=>"v","Г"=>"G","г"=>"g","Д"=>"D","д"=>"d",
                "Е"=>"E","е"=>"e","Ё"=>"E","ё"=>"e","Ж"=>"Zh","ж"=>"zh","З"=>"Z","з"=>"z","И"=>"I","и"=>"i",
                "Й"=>"I","й"=>"i","К"=>"K","к"=>"k","Л"=>"L","л"=>"l","М"=>"M","м"=>"m","Н"=>"N","н"=>"n","О"=>"O","о"=>"o",
                "П"=>"P","п"=>"p","Р"=>"R","р"=>"r","С"=>"S","с"=>"s","Т"=>"T","т"=>"t","У"=>"U","у"=>"u","Ф"=>"F","ф"=>"f",
                "Х"=>"Kh","х"=>"kh","Ц"=>"Tc","ц"=>"tc","Ч"=>"Ch","ч"=>"ch","Ш"=>"Sh","ш"=>"sh","Щ"=>"Shch","щ"=>"shch",
                "Ы"=>"Y","ы"=>"y","Э"=>"E","э"=>"e","Ю"=>"Iu","ю"=>"iu","Я"=>"Ia","я"=>"ia","ъ"=>"","ь"=>"");
    }
    else
    {
        $arStrES = array("ае","уе","ое","ые","ие","эе","яе","юе","ёе","ее","ье","ъе","ый","ий");
        $arStrOS = array("аё","уё","оё","ыё","иё","эё","яё","юё","ёё","её","ьё","ъё","ый","ий");        
        $arStrRS = array("а$","у$","о$","ы$","и$","э$","я$","ю$","ё$","е$","ь$","ъ$","@","@");
                    
        $replace = array("А"=>"A","а"=>"a","Б"=>"B","б"=>"b","В"=>"V","в"=>"v","Г"=>"G","г"=>"g","Д"=>"D","д"=>"d",
                "Е"=>"Ye","е"=>"e","Ё"=>"Ye","ё"=>"e","Ж"=>"Zh","ж"=>"zh","З"=>"Z","з"=>"z","И"=>"I","и"=>"i",
                "Й"=>"Y","й"=>"y","К"=>"K","к"=>"k","Л"=>"L","л"=>"l","М"=>"M","м"=>"m","Н"=>"N","н"=>"n",
                "О"=>"O","о"=>"o","П"=>"P","п"=>"p","Р"=>"R","р"=>"r","С"=>"S","с"=>"s","Т"=>"T","т"=>"t",
                "У"=>"U","у"=>"u","Ф"=>"F","ф"=>"f","Х"=>"Kh","х"=>"kh","Ц"=>"Ts","ц"=>"ts","Ч"=>"Ch","ч"=>"ch",
                "Ш"=>"Sh","ш"=>"sh","Щ"=>"Shch","щ"=>"shch","Ъ"=>"","ъ"=>"","Ы"=>"Y","ы"=>"y","Ь"=>"","ь"=>"",
                "Э"=>"E","э"=>"e","Ю"=>"Yu","ю"=>"yu","Я"=>"Ya","я"=>"ya","@"=>"y","$"=>"ye");
                
        $string = str_replace($arStrES, $arStrRS, $string);
        $string = str_replace($arStrOS, $arStrRS, $string);
    }
	
	$string = str_replace(" ", "-", $string);
	$string = str_replace(".", "", $string);
	$string = str_replace(",", "", $string);
	$string = str_replace(":", "", $string);
	$string = str_replace(";", "", $string);
	$string = str_replace("?", "", $string);
	$string = str_replace("!", "", $string);
	$string = str_replace("@", "", $string);
	$string = str_replace("%", "", $string);
	$string = str_replace("№", "", $string);
	$string = str_replace("«", "", $string);
	$string = str_replace("»", "", $string);
	$string = str_replace("_", "", $string);
	$string = str_replace("(", "", $string);
	$string = str_replace(")", "", $string);
	$string = str_replace("[", "", $string);
	$string = str_replace("]", "", $string);
	$string = str_replace("{", "", $string);
	$string = str_replace("}", "", $string);
	$string = str_replace("°", "", $string);
	$string = str_replace("+", "-", $string);
	$string = str_replace("/", "-", $string);
	$string = preg_replace("%(-)+%", "-", $string);
        
    return iconv("UTF-8","UTF-8//IGNORE",strtr($string,$replace));
}

function strrtolower($str) {
    $trans=array(
    "Б" => "б",
    "В" => "в",
    "Ч" => "ч",
    "З" => "з",
    "Д" => "д",
    "Е" => "е",
    "_" => "_",
    "Ц" => "ц",
    "Ъ" => "ъ",
    "Й" => "й",
    "К" => "к",
    "Л" => "л",
    "М" => "м",
    "Н" => "н",
    "О" => "о",
    "П" => "п",
    "Р" => "р",
    "Т" => "т",
    "У" => "у",
    "Ф" => "ф",
    "Х" => "х",
    "Ж" => "ж",
    "И" => "и",
    "Г" => "г",
    "Ю" => "ю",
    "Ы" => "ы",
    "Э" => "э",
    "Ш" => "ш",
    "Щ" => "щ",
    "Я" => "я",
    "Ь" => "ь",
    "А" => "а",
    "С" => "с",
	"A" => "a",
	"B" => "b",
	"C" => "c",
	"D" => "d",
	"E" => "e",
	"F" => "f",
	"G" => "g",
	"H" => "h",
	"I" => "i",
	"J" => "j",
	"K" => "k",
	"L" => "l",
	"M" => "m",
	"N" => "n",
	"O" => "o",
	"P" => "p",
	"Q" => "q",
	"R" => "r",
	"S" => "s",
	"T" => "t",
	"U" => "u",
	"V" => "v",
	"W" => "w",
	"X" => "x",
	"Y" => "y",
	"Z" => "z",
    );
    $str=strtr($str, $trans);
    return($str);
}

function addFilter($field, $name, $id, $gid){
	mysql_query("INSERT INTO `cat_product_filters` (`field`, `name`, `f_pid`, `gid`, `f_alias`, `f_pos`) VALUES('".cp1251($field)."', '".cp1251($name)."', ".$id.", ".$gid.", NULL, NULL)");
	print $name."<br>";
}

function addColors($field, $name, $id, $gid){	
	mysql_query("INSERT INTO `cat_product_filters` (`field`, `name`, `f_pid`, `gid`, `f_alias`, `f_pos`) VALUES('".cp1251($field)."', '".cp1251($name)."', ".$id.", ".$gid.", NULL, NULL)");
	print $name."<br>";
}

function cp1251($data){
	$data = iconv("UTF-8","WINDOWS-1251", $data);
	return $data;
}

function utf8($data){
	$data = iconv("WINDOWS-1251","UTF-8", $data);
	return $data;
}

?>