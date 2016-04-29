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

$q = 'ветодиодный прожектор';

$arrLinks = parsGeniledLinks2('/new/new_industry_light.php', $q);
$data = parsXLS($arrLinks, $q);

#print_r($data);

	print '<h2 style="color:brown">Прожекторы серии СДП</h2>';
	
	$c_pid = 6;

	parsProjectors($data, 'Floodlight, угол 120°', false);

function parsProjectors($data, $name, $c_pid = 6){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Floodlight, угол 120°'){
		foreach ($data as $article => $array){
			if (preg_match('/ветодиодный прожектор Geniled СДП/ui', $array['name'])){
				$products[$article] = $array; $counts++;
			}
		}		
	}
	
	print '<h3>'.$name.': '.$counts.'</h3>';
	
	//print_r($products);
	
	parsProducts($products, $name, 2);
	
	#file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);	
}

function parsXLS($arrLinks, $q) {

	$xlsx = new SimpleXLSX('price.xlsx');

	$products = array();
	list($num_cols, $num_rows) = $xlsx->dimension(2);

	$row = 0; $category="";
	//echo "<table>\n";
	foreach( $xlsx->rows(4) as $r ) {
		$row++;
		if ($row > 6){
			//echo "	<tr>\n";
			$params = array(); $article="";
			for( $i=0; $i < $num_cols; $i++ ) {
				if (!empty($r[$i])){
					if ($r[$i] == "Артикул"){break;}
					else if ($r[$i] == "* Замена:"){break 2;}
					else {
						if ($i == 0 && $r[$i] > 0){
							$article = trim($r[$i]);
							$params["category"] = trim($category);
						}
						else if ($i == 0 && $r[$i]){$category = $r[$i];}
						else if ($i == 2 && preg_match('%'.$q.'%', $r[$i])){
							$name = trim($r[$i]);
							$params["name"] = $name;	
						}
						else if ($i == 10 && $r[$i] > 0){$params["price1"] = $r[$i];}
						else if ($i == 11 && $r[$i] > 0){$params["price2"] = $r[$i];}
						else if ($i == 12 && $r[$i] > 0){$params["price3"] = $r[$i];}
						else if ($i == 13 && $r[$i] > 0){$params["price4"] = $r[$i];}
						else if ($i == 14 && $r[$i] > 0){$params["price5"] = $r[$i];}
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
	
	return parsGeniledTechData($products, $arrLinks);

	//foreach ($products as $article => $array){
	//	echo $article." => <br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['category']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['name']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['price1']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['link']."<br>";
	//}
}

function parsGeniledTechData($products, $arrLinks) {

	$i = 0;
	foreach ($products as $article => $array){
		$i++;		
		//if ($i == 20) break;
		$data = $arrLinks[$article];
		
		if ($data){
			$techdata = array();
			$techdata['Тип товара'] = 'Прожектор';
			
			preg_match_all('/Цветовая температура &ndash;(.+):\s(.+)\sК<\!--строка-->/', $data, $result);
			$param1 = trim($result[1][0]);
			$param2 = trim($result[2][0]);
			if ($param1) $techdata['Цвет свечения'] = $param1;
			if ($param2) $techdata['Цветовая температура, K'] = $param2." K";
			if (!$param1 && !$param2){
				preg_match_all('/Цветовая температура &ndash;(.+)К<\!--строка-->/', $data, $result);
				$param2 = trim($result[1][0]);
				if ($param2) $techdata['Цветовая температура, K'] = $param2." K";
			}
			
			if (!$techdata['Цвет свечения'] && $techdata['Цветовая температура, K']){
				$techdata['Цвет свечения'] = eqColor($techdata['Цветовая температура, K']);
			}			
			
			preg_match_all('/Световой поток &ndash;(.+)<\!--строка-->/', $data, $result);
			$param3 = trim($result[1][0]);
			if ($param3) $techdata['Световой поток, lm'] = $param3;
			
			preg_match_all('/Угол рассеивания &ndash;(.+)<\!--строка-->/', $data, $result);
			$param4 = trim($result[1][0]);
			if ($param4) $techdata['Угол обзора, °'] = $param4;				
			
			preg_match_all('/Входное напряжение &ndash;(.+)<\!--строка-->/', $data, $result);
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

			preg_match_all('/Потребляемая мощность &ndash;(.+)\sВт<\!--строка-->/', $data, $result);
			$param6 = trim($result[1][0]);
			if ($param6 && $param6 > 0) $techdata['Потребляемая мощность, W'] = $param6." W";
			
			preg_match_all('/Охлаждение &ndash;(.+)<\!--строка-->/', $data, $result);
			$param7 = trim($result[1][0]);
			if ($param7) $techdata['Охлаждение'] = $param7;

			preg_match_all('/Материал корпуса &ndash;(.+)<\!--строка-->/', $data, $result);
			$param8 = trim($result[1][0]);
			if ($param8) $techdata['Материал корпуса'] = $param8;

			preg_match_all('/Оптика &ndash;(.+)<\!--строка-->/', $data, $result);
			$param9 = trim($result[1][0]);
			if ($param9) $techdata['Оптика'] = $param9;			

			preg_match_all('/Размер прожектора &ndash;(.+)<\!--строка-->/', $data, $result);
			$param10 = trim($result[1][0]);
			if ($param10) $techdata['Размер'] = $param10;

			preg_match_all('/Срок службы &ndash;(.+)<\!--строка-->/', $data, $result);
			$param11 = trim($result[1][0]);
			if ($param11) $techdata['Срок службы'] = $param11;

			preg_match_all('/Степень защиты &ndash;(.+)<\!--строка-->/', $data, $result);
			$param12 = trim($result[1][0]);
			if ($param12) $techdata['Класс пыле-влагозащиты'] = $param12;

			preg_match_all('/<img.*src="(.+)" width/', $data, $result);
			$image = trim($result[1][0]);
			if ($image) $array['img'] = "http://geniled.ru".$image;	
			
			preg_match_all('/get\.php\?fid=Спецификация.*file=(.+)"/', $data, $result);
			$pdf = trim($result[1][0]);
			if ($pdf) $array['pdf'] = "http://geniled.ru/".$pdf;
			
			$array['color1'] = eqKColor($techdata['Цветовая температура, K']);
			
			$array['pack'] = "Коробка";
			$array['packnorm'] = "1";
			$array['unit'] = "шт";

			$array['descript'] = $array['name'].''.($techdata['Размер']?'. Размер '.$techdata['Размер'].'.':'').' Цвет свечения '.$techdata['Цвет свечения'].', св. поток '.$techdata['Световой поток, lm'].''.($techdata['Угол обзора, °']?', угол освещения '.$techdata['Угол обзора, °'].'.':'').' Питание '.$techdata['Напряжение питания, V'].', мощность '.$techdata['Потребляемая мощность, W'].'. Срок службы '.$techdata['Срок службы'];
			
			$array['techdata'] = $techdata;
			$products[$article] = $array;
		}
		else {
			unset($products[$article]);
		}
	}
	
	return $products;
}


?>