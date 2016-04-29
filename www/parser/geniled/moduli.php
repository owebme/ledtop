<?php

ini_set('max_execution_time', 600);

function getDomen(){
	return 'http://ledtop2.ru';
}

include 'Class/simplexlsx.class.php';
include 'Class/simple_html_dom.php';

require_once 'db.php';
require_once '../function.php';

header("Content-type: text/html; charset=utf-8");

print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<style>html {width:988px; margin:25px auto 0; font-family: Arial, Helvetica;} body {margin:0;} h2, h3 {margin:0 0 10px;} h2 {font-size:1.7em; margin-bottom:12px;}</style>';

$arrLinks = parsGeniledLinks('/new/new_modul.php', '/new/sm_filter_modul_result.php');
$data = parsModuliXLS($arrLinks);

#print_r($data);

	print '<h2 style="color:brown">Модули</h2>';
	
	$c_pid = 5;

	parsModuli($data, 'Smd 3528 линейные', false);
	parsModuli($data, 'Smd 3528 квадратные', false);
	parsModuli($data, 'Smd 5050 линейные', false);
	parsModuli($data, 'Smd 5050 квадратные', false);
	createCategory('Smd 5630 квадратные', 'Модули герметичные');
		parsModuli($data, 'Smd 5630 квадратные', false);
	parsModuli($data, 'Пиксельные 9-12мм', false);

function parsModuli($data, $name, $c_pid = 5){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Smd 3528 линейные'){
		foreach ($data as $article => $array){
			if ((preg_match('/3528/ui', $array['category']) or preg_match('/3535/ui', $array['techdata']['Размер светодиодов'])) && $array['techdata']['Форма'] == "Линейный"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Smd 3528 квадратные'){
		foreach ($data as $article => $array){
			if ((preg_match('/3528/ui', $array['category']) or preg_match('/3535/ui', $array['techdata']['Размер светодиодов'])) && $array['techdata']['Форма'] == "Квадратный"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Smd 5050 линейные'){
		foreach ($data as $article => $array){
			if (preg_match('/5050/ui', $array['category']) && $array['techdata']['Форма'] == "Линейный"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Smd 5050 квадратные'){
		foreach ($data as $article => $array){
			if (preg_match('/5050/ui', $array['category']) && $array['techdata']['Форма'] == "Квадратный"){
				$products[$article] = $array; $counts++;
			}
		}
	}	
	else if ($name == 'Smd 5630 квадратные'){
		foreach ($data as $article => $array){
			if (preg_match('/5630/ui', $array['category']) && $array['techdata']['Форма'] == "Квадратный"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Smd 5630 квадратные'){
		foreach ($data as $article => $array){
			if (preg_match('/5630/ui', $array['category']) && $array['techdata']['Форма'] == "Квадратный"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Пиксельные 9-12мм'){
		foreach ($data as $article => $array){
			if (preg_match('/иксельные/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
	}
	
	print '<h3>'.$name.': '.$counts.'</h3>';
	
	//print_r($products);
	
	parsProducts($products, $name, 2);
	
	#file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);	
}

function parsModuliXLS($arrLinks) {

	$xlsx = new SimpleXLSX('price.xlsx');

	$products = array();
	list($num_cols, $num_rows) = $xlsx->dimension(2);

	$row = 0; $category="";
	//echo "<table>\n";
	foreach( $xlsx->rows(8) as $r ) {
		$row++;
		if ($row > 5){
			//echo "	<tr>\n";
			$params = array(); $article="";
			for( $i=0; $i < $num_cols; $i++ ) {
				if (!empty($r[$i])){
					if ($r[$i] == "Артикул"){break;}
					else if ($r[$i] == "* Замена:"){break 2;}
					else {
						if ($i == 0 && $r[$i] > 0){
							$article = $r[$i];
							$params["category"] = $category;
							if ($arrLinks[$article]){
								$params["link"] = $arrLinks[$article];
							}							
						}
						else if ($i == 0 && $r[$i]){$category = $r[$i];}
						else if ($i == 2 && $r[$i]){
							$params["name"] = trim($r[$i]);
						}
						else if ($i == 7 && $r[$i] > 0){$params["price1"] = $r[$i];}
						else if ($i == 8 && $r[$i] > 0){$params["price2"] = $r[$i];}
						else if ($i == 9 && $r[$i] > 0){$params["price3"] = $r[$i];}
						else if ($i == 10 && $r[$i] > 0){$params["price4"] = $r[$i];}
						else if ($i == 11 && $r[$i] > 0){$params["price5"] = $r[$i];}
						//echo "		<td>".$r[$i]."</td>\n";
					}
				}
			}
			if (sizeof($params) > 0){
				if ($params["name"]){
					$products[$article] = $params;
				}
			}
			//echo "	</tr>\n";
		}
	}
	//echo "</table>";
	
	return parsModuliTechData($products);

	//foreach ($products as $article => $array){
	//	echo $article." => <br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['category']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['name']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['price1']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['link']."<br>";
	//}
}

function parsModuliTechData($products) {

	$i = 0;
	foreach ($products as $article => $array){
		$i++;	
		//if ($i == 2) break;
		$data = file_get_contents('http://geniled.ru'.$array['link']);
		
		if ($data){
			$techdata = array();
			$techdata['Тип товара'] = 'Модуль';
			
			preg_match_all('/Цвет свечения &ndash;(.+)<\!--строка-->/', $data, $result);
			$param1 = trim($result[1][0]);
			if ($param1) $techdata['Цвет свечения'] = $param1;
			if (preg_match('%(\d+)%', $techdata['Цвет свечения'])){
				preg_match_all('/(\d+)К/', $techdata['Цвет свечения'], $result);
				$param2 = trim($result[1][0])." K";
				if ($param2) $techdata['Цветовая температура, K'] = $param2;
				preg_match_all('/^(.+)\s/', $techdata['Цвет свечения'], $result);
				$param1 = trim($result[1][0]);
				$techdata['Цвет свечения'] = $param1;
			}
			if (!$techdata['Цвет свечения']){
				preg_match_all('/Цвет &ndash;(.+)<\!--строка-->/', $data, $result);
				$param1 = trim($result[1][0]);
				if ($param1) $techdata['Цвет свечения'] = $param1;
				preg_match_all('/Цветовая температура &ndash;(.+)<\!--строка-->/', $data, $result);
				$param2 = trim($result[1][0]);
				if ($param2) $techdata['Цветовая температура, K'] = $param2;
			}
			
			if ($techdata['Цвет свечения'] == "Белый" or $techdata['Цвет свечения'] == "белый") $array['color1'] = "white";
			else if ($techdata['Цвет свечения'] == "Теплый белый") $array['color1'] = "warm_white";
			else if ($techdata['Цвет свечения'] == "Красный") $array['color1'] = "red";
			else if ($techdata['Цвет свечения'] == "Зеленый") $array['color1'] = "green";
			else if ($techdata['Цвет свечения'] == "Синий" or $techdata['Цвет свечения'] == "Cиний") $array['color1'] = "blue";
			else if ($techdata['Цвет свечения'] == "Голубой") $array['color1'] = "cool_white";
			else if ($techdata['Цвет свечения'] == "Желтый") $array['color1'] = "yellow";
			else if ($techdata['Цвет свечения'] == "Оранжевый") $array['color1'] = "orange";
			else if ($techdata['Цвет свечения'] == "Розовый") $array['color1'] = "pink";
			else if ($techdata['Цвет свечения'] == "Фиолетовый") $array['color1'] = "violet";
			else if (preg_match('%RGB%', $techdata['Цвет свечения'])){
				$array['color1'] = "red";
				$array['color2'] = "green";
				$array['color3'] = "blue";
			}
			
			preg_match_all('/Световой поток.+&ndash;(.+)<\!--строка-->/', $data, $result);
			$param3 = trim($result[1][0]);
			if ($param3) $techdata['Световой поток, lm'] = $param3;
			
			preg_match_all('/Рабочий ток &ndash;(.+)<\!--строка-->/', $data, $result);
			$param3 = trim($result[1][0]);
			if ($param3) $techdata['Рабочий ток'] = $param3;
			
			preg_match_all('/Угол рассеивания &ndash;(.+)<\!--строка-->/', $data, $result);
			$param4 = trim($result[1][0]);
			if ($param4) $techdata['Угол обзора, °'] = $param4;
			if (!$techdata['Угол обзора, °']){
				preg_match_all('/Угол рассеивая &ndash;(.+)<\!--строка-->/', $data, $result);
				$param4 = trim($result[1][0]);
				if ($param4) $techdata['Угол обзора, °'] = $param4;		
			}

			if (preg_match('%2835%', $array['category'])){
				$techdata['Размер светодиодов'] = '2835 (2.8x3.5мм)';
			}			
			else if (preg_match('%3528%', $array['category'])){
				$techdata['Размер светодиодов'] = '3528 (3.5x2.8мм)';
			}
			else if (preg_match('%3535%', $array['category'])){
				$techdata['Размер светодиодов'] = '3535 (3.5x3.5мм)';
			}
			else if (preg_match('%3014%', $array['category'])){
				$techdata['Размер светодиодов'] = '3014 (3x1.4мм)';
			}
			else if (preg_match('%5050%', $array['category'])){
				$techdata['Размер светодиодов'] = '5050/5060 (5x5мм)';
			}
			else if (preg_match('%5630%', $array['category'])){
				$techdata['Размер светодиодов'] = '5630 (5.6x3мм)';
			}			
			else if (preg_match('%5730%', $array['category'])){
				$techdata['Размер светодиодов'] = '5730 (5.7x3мм)';
			}
			if ($article == "02097" or $article == "02098"){
				$techdata['Размер светодиодов'] = "3535 (3.5x3.5мм)";
			}			

			preg_match_all('/Диаметр светодиода &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Диаметр светодиода'] = $param;

			preg_match_all('/Наружный диаметр &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Наружный диаметр'] = $param;

			preg_match_all('/Диаметр монтажного отверстия &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Диаметр монтажного отверстия'] = $param;

			preg_match_all('/Толщина листового материала для монтажа &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Толщина листового материала для монтажа'] = $param;

			preg_match_all('/Тип линзы &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Тип линзы'] = $param;

			preg_match_all('/Светодиоды &ndash;.+, (\d+)шт<\!--строка-->/', $data, $result);
			$param5 = trim($result[1][0]);
			if ($param5) $techdata['Кол-во св.диодов, шт'] = $param5." шт";
			
			if ($article == "02097" or $article == "02098"){
				$techdata['Кол-во св.диодов, шт'] = "1 шт";
			}			
			
			if (preg_match('%пиксельные%', $array['category'])){
				$techdata['Форма'] = "Круглый";
				$techdata['Кол-во св.диодов, шт'] = "1 шт";
			}
			else {
				if ($article == "02091" or $article == "02113" or $param5 == "4"){
					$techdata['Форма'] = "Квадратный";
				}
				else if ($param5 < 4){
					$techdata['Форма'] = "Линейный";
				}					
			}			
			
			preg_match_all('/апряжение(.+)<\!--строка-->/', $data, $result);
			$param5 = trim($result[1][0]);
			if ($param5 && (preg_match('%240%', $param5) or preg_match('%230%', $param5) or preg_match('%220%', $param5))){
				$techdata['Напряжение питания, V'] = '220 V';
			}
			else if ($param5 && (preg_match('%120%', $param5) or preg_match('%110%', $param5) or preg_match('%100%', $param5))){
				$techdata['Напряжение питания, V'] = '110 V';
			}
			else if ($param5 && preg_match('%12%', $param5)){
				$techdata['Напряжение питания, V'] = '12 V';
			}
			else if ($param5 && preg_match('%5%', $param5)){
				$techdata['Напряжение питания, V'] = '5 V';
			}			
			if (!$techdata['Напряжение питания, V']){
				preg_match_all('/напряжение &ndash;(.+)<\!--строка-->/', $data, $result);
				$param5 = trim($result[1][0]);
				if ($param5 && (preg_match('%240%', $param5) or preg_match('%230%', $param5) or preg_match('%220%', $param5))){
					$techdata['Напряжение питания, V'] = '220 V';
				}
				else if ($param5 && (preg_match('%120%', $param5) or preg_match('%110%', $param5) or preg_match('%100%', $param5))){
					$techdata['Напряжение питания, V'] = '110 V';
				}
				else if ($param5 && preg_match('%12%', $param5)){
					$techdata['Напряжение питания, V'] = '12 V';
				}
				else if ($param5 && preg_match('%5%', $param5)){
					$techdata['Напряжение питания, V'] = '5 V';
				}				
			}			

			preg_match_all('/Потребляемая мощность &ndash; (.+)\sВт<\!--строка-->/', $data, $result);
			$param6 = trim($result[1][0]);
			if ($param6) $techdata['Потребляемая мощность, W'] = ($param6)." W";
			
			if ($article == "02098") $techdata['Потребляемая мощность, W'] = "2 W";
			if ($article == "02078") $techdata['Потребляемая мощность, W'] = "0,72 W";
			
			preg_match_all('/Степень защиты &ndash;(.+)<\!--строка-->/', $data, $result);
			$param7 = trim($result[1][0]);
			if ($param7) $techdata['Класс пыле-влагозащиты'] = $param7;

			preg_match_all('/Размер модуля &ndash;(.+)<\!--строка-->/', $data, $result);
			$param8 = trim($result[1][0]);
			if ($param8) $techdata['Размер модуля'] = $param8;			

			preg_match_all('/Срок службы &ndash;(.+)<\!--строка-->/', $data, $result);
			$param9 = trim($result[1][0]);
			if ($param9) $techdata['Срок службы'] = $param9;

			preg_match_all('/<img.*src="(.+)" width/', $data, $result);
			$image = trim($result[1][0]);
			if ($image) $array['img'] = "http://geniled.ru".$image;	
			
			preg_match_all('/get\.php\?fid=Спецификация.*file=(.+)"/', $data, $result);
			$pdf = trim($result[1][0]);
			if ($pdf) $array['pdf'] = "http://geniled.ru/".$pdf;
			
			$array['pack'] = "Упаковка";
			$array['packnorm'] = "100";
			$array['unit'] = "шт";

			$array['descript'] = 'Светодиодный модуль'.($techdata['Форма']?' ('.$techdata['Форма'].')':'').''.($techdata['Размер светодиодов']?', '.$techdata['Размер светодиодов'].'':'').''.($techdata['Класс пыле-влагозащиты']?', '.$techdata['Класс пыле-влагозащиты'].'':'').', цвет '.$techdata['Цвет свечения'].''.($techdata['Световой поток, lm']?', cвет. поток '.$techdata['Световой поток, lm'].'':'').'. Питание '.$techdata['Напряжение питания, V'].', мощность '.$techdata['Потребляемая мощность, W'].'. '.($techdata['Размер модуля']?'Размер модуля '.$techdata['Размер модуля'].'':'').'';
			
			$array['techdata'] = $techdata;
			$products[$article] = $array;
			
			if (!$techdata['Напряжение питания, V']) {
				unset($products[$article]);
			}			
		}
		else {
			unset($products[$article]);
		}
	}
	
	return $products;
}


?>