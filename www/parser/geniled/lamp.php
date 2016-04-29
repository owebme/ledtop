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

$q = 'ветодиодная лампа';

$arrLinks = parsGeniledLinks('/new/new_lamps.php', '/new/sm_filter_result.php');
$data = parsLampXLS($arrLinks, $q);

	print '<h2 style="color:brown">Лампы</h2>';
	
	$c_pid = 3;

	parsLamp($data, 'Свеча 220V E14', false);
	parsLamp($data, 'Груша 220V E27', false);
	parsLamp($data, 'Грибок 220V E27', false);
	parsLamp($data, 'Грибок 220V E14', false);
	parsLamp($data, 'Шар 220V E14', false);
	parsLamp($data, 'Шар 220V E27', false);
	parsLamp($data, 'MR16 GU5.3 12V', false);
	parsLamp($data, 'MR16 GU5.3 220V', false);
	parsLamp($data, 'GU10 220V', false);
	parsLamp($data, 'AR111 G53 12V', false);
	createCategory('AR111 G53 220V', 'AR111 12/220V');
		parsLamp($data, 'AR111 G53 220V', false);
	parsLamp($data, 'Geniled EVO Е27', false);
	parsLamp($data, 'Geniled EVO Е14 G45', false);
	parsLamp($data, 'Geniled EVO Е14 С37', false);
	parsLamp($data, 'G4 12V', false);
	createCategory('G4 220V', $c_pid);
		parsLamp($data, 'G4 220V', false);
	parsLamp($data, 'G9 220V', false);
	parsLamp($data, 'GX53 220V', false);
	parsLamp($data, 'Т8 600мм G13', false);
	parsLamp($data, 'Т8 1200мм G13', false);
	parsLamp($data, 'Т8 1500мм G13', false);

function parsLamp($data, $name, $c_pid = 3){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Свеча 220V E14'){
		foreach ($data as $article => $array){
			if (preg_match('/Свеча/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е14" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}		
	}
	else if ($name == 'Груша 220V E27'){
		foreach ($data as $article => $array){
			if (preg_match('/Груша/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е27" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
		$name = "Шар 220V E27";
	}
	else if ($name == 'Грибок 220V E27'){
		foreach ($data as $article => $array){
			if (preg_match('/Грибок/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е27" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
		$name = "Шар 220V E27";
	}
	else if ($name == 'Грибок 220V E14'){
		foreach ($data as $article => $array){
			if (preg_match('/Грибок/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е14" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
		$name = "Шар 220V E14";
	}
	else if ($name == 'Шар 220V E14'){
		foreach ($data as $article => $array){
			if (preg_match('/Шарик/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е14" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Шар 220V E27'){
		foreach ($data as $article => $array){
			if (preg_match('/Шарик/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е27" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'MR16 GU5.3 12V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "GU5.3" && $array['techdata']['Напряжение питания, V'] == "12 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'MR16 GU5.3 220V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "GU5.3" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'GU10 220V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "GU10" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'AR111 G53 12V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G53" && $array['techdata']['Напряжение питания, V'] == "12 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'AR111 G53 220V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G53" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}	
	else if ($name == 'Geniled EVO Е27'){
		foreach ($data as $article => $array){
			if (preg_match('/Geniled EVO/ui', $array['category']) && $array['techdata']['Цоколь'] == "Е27" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
		$name = "Шар 220V E27";
	}
	else if ($name == 'Geniled EVO Е14 G45'){
		foreach ($data as $article => $array){
			if (preg_match('/Geniled EVO/ui', $array['category']) && preg_match('/Geniled EVO Е14 G45/ui', $array['name']) && $array['techdata']['Цоколь'] == "Е14" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
		$name = "Шар 220V E14";
	}
	else if ($name == 'Geniled EVO Е14 С37'){
		foreach ($data as $article => $array){
			if (preg_match('/Geniled EVO/ui', $array['category']) && preg_match('/Geniled EVO Е14 С37/ui', $array['name']) && $array['techdata']['Цоколь'] == "Е14" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
		$name = "Свеча 220V E14";
	}
	else if ($name == 'G4 12V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G4" && $array['techdata']['Напряжение питания, V'] == "12 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'G4 220V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G4" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}	
	else if ($name == 'G9 220V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G9" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'GX53 220V'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "GX53" && $array['techdata']['Напряжение питания, V'] == "220 V"){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Т8 600мм G13'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G13" && preg_match('/Т8 600мм/ui', $array['name'])){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Т8 1200мм G13'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G13" && preg_match('/Т8 1200мм/ui', $array['name'])){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Т8 1500мм G13'){
		foreach ($data as $article => $array){
			if ($array['techdata']['Цоколь'] == "G13" && preg_match('/Т8 1500мм/ui', $array['name'])){
				$products[$article] = $array; $counts++;
			}
		}
	}	
	
	print '<h3>'.$name.': '.$counts.'</h3>';
	
	//print_r($products);
	
	parsProducts($products, $name, 2);
	
	#file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);	
}

function parsLampXLS($arrLinks, $q) {

	$xlsx = new SimpleXLSX('price.xlsx');

	$products = array();
	list($num_cols, $num_rows) = $xlsx->dimension(2);

	$row = 0; $category="";
	//echo "<table>\n";
	foreach( $xlsx->rows(2) as $r ) {
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
							$article = $r[$i];
							$params["category"] = $category;
							if ($arrLinks[$article]){
								$params["link"] = $arrLinks[$article];
							}							
						}
						else if ($i == 0 && $r[$i]){$category = $r[$i];}
						else if ($i == 2 && preg_match('%'.$q.'%', $r[$i])){
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
	
	return parsLampTechData($products);

	//foreach ($products as $article => $array){
	//	echo $article." => <br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['category']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['name']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['price1']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['link']."<br>";
	//}
}

function parsLampTechData($products) {

	$i = 0;
	foreach ($products as $article => $array){
		$i++;	
		//if ($i == 20) break;
		$data = file_get_contents('http://geniled.ru'.$array['link']);
		
		if ($data){
			$techdata = array();
			$techdata['Тип товара'] = 'Лампа';
			
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

			preg_match_all('/Тип цоколя &ndash;(.+)<\!--строка-->/', $data, $result);
			$param7 = trim($result[1][0]);
			if ($param7) {
				$param7_ = explode(" ", $param7);
				if ($param7_[0]){$param7 = $param7_[0];}
				$techdata['Цоколь'] = $param7;	
			}	

			preg_match_all('/Возможность диммирования &ndash;(.+)<\!--строка-->/', $data, $result);
			$param8 = trim($result[1][0]);
			if ($param8) $techdata['Возможность диммирования'] = $param8;	

			preg_match_all('/Срок службы &ndash;(.+)<\!--строка-->/', $data, $result);
			$param9 = trim($result[1][0]);
			if ($param9) $techdata['Срок службы'] = $param9;

			preg_match_all('/Замена лампы накаливания &ndash;(.+)<\!--строка-->/', $data, $result);
			$param10 = trim($result[1][0]);
			if ($param10) $techdata['Замена лампы накаливания'] = $param10;

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

			$array['descript'] = $techdata['Цоколь'].' светодиодная лампа.'.($techdata['Замена лампы накаливания']?'Эквивалента лампе накаливания '.$techdata['Замена лампы накаливания'].'.':'').' Цвет свечения '.$techdata['Цвет свечения'].', св. поток '.$techdata['Световой поток, lm'].''.($techdata['Угол обзора, °']?', угол освещения '.$techdata['Угол обзора, °'].'.':'').' Питание '.$techdata['Напряжение питания, V'].', мощность '.$techdata['Потребляемая мощность, W'].'. Срок службы '.$techdata['Срок службы'].' '.($techdata['Возможность диммирования'] == "Да"?' Возможность диммирования: Да':'');
			
			$array['techdata'] = $techdata;
			$products[$article] = $array;
		}
	}
	
	return $products;
}


?>