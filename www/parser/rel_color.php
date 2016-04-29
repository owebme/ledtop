<?php

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	mysql_query("UPDATE cat_product SET `p_color_rel` = NULL");
	
	cat_related(1, 1);
	cat_related(2, 1);
		cat_related(2, 2);
	cat_related(3, 1);
		cat_related(3, 2);
	cat_related(4, 1);
	cat_related(5, 1);
		cat_related(5, 2);
	cat_related(6, 1);
		cat_related(6, 2);

	function cat_related($id, $supplier){
	
		$products = array();
		$result = mysql_query("SELECT p.p_id, p.p_art, p.p_name, p.p_price, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id = '".$id."' AND p.p_supplier = '".$supplier."' AND p.p_show = '1'");
		while ($row = @mysql_fetch_array($result)){
		
			$colors=""; $param1=""; $param2=""; $param3=""; $param4=""; $param5=""; $param6="";
			$res = mysql_query("SELECT * FROM cat_product_fields WHERE p_id = '".$row["p_id"]."'");
			if (mysql_num_rows($res)){
				while ($row2 = @mysql_fetch_array($res)){
					if ($row2["value"]){
						if ($row2["field"] == "Цвет 1"){
							$colors .= $row2["value"];
						}				
						else if ($row2["field"] == "Цвет 2"){
							$colors .= "|".$row2["value"];
						}
						else if ($row2["field"] == "Цвет 3"){
							$colors .= "|".$row2["value"];
						}
						else {
							if ($row["cat_id"] == "1"){ // Светодиоды
								if ($row2["field"] == "Тип товара"){
									$param1 = $row2["value"];
								}
								if ($row2["field"] == "Прямой потребляемый ток, A"){
									$param2 = $row2["value"];
								}
								if ($row2["field"] == "Угол обзора, °"){
									$param3 = $row2["value"];
								}
								if ($row2["field"] == "Рассеиваемая мощность, W" || $row2["field"] == "Потребляемая мощность, W"){
									$param4 = $row2["value"];
								}			
							}
							else if ($row["cat_id"] == "2"){ // Ленты
								if ($row2["field"] == "Размер светодиодов"){
									$param1 = $row2["value"];
								}
								if ($row2["field"] == "Плотность светодиодов, шт/м"){
									$param2 = $row2["value"];
								}
								if ($row2["field"] == "Напряжение питания, V"){
									$param3 = $row2["value"];
								}
								if ($row2["field"] == "Потребляемая мощность, W"){
									$param4 = $row2["value"];
								}
								if ($row2["field"] == "Ширина, мм"){
									$param5 = $row2["value"];
								}
							}
							else if ($row["cat_id"] == "3"){ // Лампы
								if ($row2["field"] == "Напряжение питания, V"){
									$param1 = $row2["value"];
								}
								if ($row2["field"] == "Потребляемая мощность, W"){
									$param2 = $row2["value"];
								}
								if ($row2["field"] == "Цоколь"){
									$param3 = $row2["value"];
								}
							}
							else if ($row["cat_id"] == "4"){ // Светильники
								if ($row2["field"] == "Напряжение питания, V"){
									$param1 = $row2["value"];
								}
								if ($row2["field"] == "Потребляемая мощность, W"){
									$param2 = $row2["value"];
								}
								if ($row2["field"] == "Угол обзора, °"){
									$param3 = $row2["value"];
								}
								if ($row2["field"] == "Форма"){
									$param4 = $row2["value"];
								}
								if ($row2["field"] == "Цвет"){
									$param5 = $row2["value"];
								}
								if ($row2["field"] == "Диаметр отверстия, мм"){
									$param6 = $row2["value"];
								}							
							}
							else if ($row["cat_id"] == "5"){ // Модули
								if ($row2["field"] == "Размер светодиодов"){
									$param1 = $row2["value"];
								}
								if ($row2["field"] == "Кол-во св.диодов, шт"){
									$param2 = $row2["value"];
								}
								if ($row2["field"] == "Угол обзора, °"){
									$param3 = $row2["value"];
								}
								if ($row2["field"] == "Напряжение питания, V"){
									$param4 = $row2["value"];
								}
								if ($row2["field"] == "Потребляемая мощность, W"){
									$param5 = $row2["value"];
								}
								if ($row2["field"] == "Плотность светодиодов, шт/м"){
									$param6 = $row2["value"];
								}						
							}
							else if ($row["cat_id"] == "6"){ // Прожекторы
								if ($row2["field"] == "Угол обзора, °" or $row2["field"] == "Угол Обзора (гор/верт), °"){
									$param1 = $row2["value"];
								}
								if ($row2["field"] == "Напряжение питания, V"){
									$param2 = $row2["value"];
								}
								if ($row2["field"] == "Потребляемая мощность, W"){
									$param3 = $row2["value"];
								}
								if ($row2["field"] == "Длина, мм" || $row2["field"] == "Размер"){
									$param4 = $row2["value"];
								}
								if ($row2["field"] == "Ширина, мм"){
									$param5 = $row2["value"];
								}
								if ($row2["field"] == "Высота, мм"){
									$param6 = $row2["value"];
								}							
							}						
						}
					}				
				}
			}
			if ($colors){
				$md5 = md5($row["p_price"].$param1.$param2.$param3.$param4.$param5.$param6);
				$array = array(); 
				if ($products[$md5]){
					$array = $products[$md5];
				}			
				$item = $row["p_name"]."%%".$colors;
				$array[$row["p_art"]] = $item;
				$products[$md5] = $array;
			}
		}

		foreach ($products as $key){
			$counts = sizeof($key);
			if ($counts > 1){
				$colors=""; $i=0;
				foreach ($key as $art => $item){
					$value = explode("%%", $item);
					$name = $value[0]; $color = $value[1];
					$color1 = preg_replace("%\|%si", "\|", $color);
					if (!preg_match('%\['.$color1.'\]%', $colors)){
						$i++;
						if ($i > 1){$colors .= ";";}
						$colors .= $art."[".$color."]";
					}
				}
				foreach ($key as $article => $item){
					if ($i > 1){
						print $article." ".$colors."<br>";
						mysql_query("UPDATE cat_product SET `p_color_rel` = '".$colors."' WHERE p_art = '".$article."' LIMIT 1");
					}
				}
			}
		}
		//print_r($products);
	}

?>