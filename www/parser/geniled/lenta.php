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

$q = 'ента Geniled';

$arrLinks = parsGeniledLinks('/new/new_lent.php', '/new/sm_filter_lent_result.php');
$data = parsLentaXLS($arrLinks, $q);

#print_r($data);

	print '<h2 style="color:brown">Ленты</h2>';
	
	$c_pid = 2;

	parsLenta($data, 'Лента на диодах 3528', false);
	parsLenta($data, 'Ленты LUX ультра 5630, 2835', false);
	parsLenta($data, 'Лента на диодах 5060 (5050)', false);

function parsLenta($data, $name, $c_pid = 2){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Лента на диодах 3528'){
		foreach ($data as $article => $array){
			if (preg_match('/3528/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Ленты LUX ультра 5630, 2835'){
		foreach ($data as $article => $array){
			if (preg_match('/3014/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
	}
	else if ($name == 'Лента на диодах 5060 (5050)'){
		foreach ($data as $article => $array){
			if (preg_match('/5050/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
	}	
	
	print '<h3>'.$name.': '.$counts.'</h3>';
	
	//print_r($products);
	
	parsProducts($products, $name, 2);
	
	#file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);	
}

function parsLentaXLS($arrLinks, $q) {

	$xlsx = new SimpleXLSX('price.xlsx');

	$products = array();
	list($num_cols, $num_rows) = $xlsx->dimension(2);

	$row = 0; $category="";
	//echo "<table>\n";
	foreach( $xlsx->rows(7) as $r ) {
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
						else if ($i == 3 && preg_match('%'.$q.'%', $r[$i])){
							$params["name"] = trim($r[$i]);
						}
						else if ($i == 7 && $r[$i] > 0){$params["price1"] = $r[$i]/5;}
						else if ($i == 8 && $r[$i] > 0){$params["price2"] = $r[$i]/5;}
						else if ($i == 9 && $r[$i] > 0){$params["price3"] = $r[$i]/5;}
						else if ($i == 10 && $r[$i] > 0){$params["price4"] = $r[$i]/5;}
						else if ($i == 11 && $r[$i] > 0){$params["price5"] = $r[$i]/5;}
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
	
	return parsLentaTechData($products);

	//foreach ($products as $article => $array){
	//	echo $article." => <br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['category']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['name']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['price1']."<br>";
	//	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['link']."<br>";
	//}
}

function parsLentaTechData($products) {

	$i = 0;
	foreach ($products as $article => $array){
		$i++;	
		//if ($i == 2) break;
		$data = file_get_contents('http://geniled.ru'.$array['link']);
		
		if ($data){
			$techdata = array();
			$techdata['Тип товара'] = 'Лента';
			
			preg_match_all('/Цвет свечения &ndash;(.+)<\!--строка-->/', $data, $result);
			$param1 = trim($result[1][0]);
			if ($param1) $techdata['Цвет свечения'] = $param1;
			if (preg_match('%(\d+)%', $techdata['Цвет свечения'])){
				preg_match_all('/(\d+)\sК/', $techdata['Цвет свечения'], $result);
				$param2 = trim($result[1][0])." K";
				$techdata['Цветовая температура, K'] = $param2;
				preg_match_all('/^(.+)\s&#40;/', $techdata['Цвет свечения'], $result);
				$param1 = trim($result[1][0]);
				$techdata['Цвет свечения'] = $param1;
			}
			
			if ($techdata['Цвет свечения'] == "Белый") $array['color1'] = "white";
			else if ($techdata['Цвет свечения'] == "Теплый белый") $array['color1'] = "warm_white";
			else if ($techdata['Цвет свечения'] == "Красный") $array['color1'] = "red";
			else if ($techdata['Цвет свечения'] == "Зеленый") $array['color1'] = "green";
			else if ($techdata['Цвет свечения'] == "Синий") $array['color1'] = "blue";
			else if ($techdata['Цвет свечения'] == "Желтый") $array['color1'] = "yellow";
			else if ($techdata['Цвет свечения'] == "Оранжевый") $array['color1'] = "orange";
			else if ($techdata['Цвет свечения'] == "Розовый") $array['color1'] = "pink";
			else if ($techdata['Цвет свечения'] == "Фиолетовый") $array['color1'] = "violet";
			else if ($techdata['Цвет свечения'] == "RGB"){
				$array['color1'] = "red";
				$array['color2'] = "green";
				$array['color3'] = "blue";
			}
			
			preg_match_all('/Световой поток.+&ndash;(.+)<\!--строка-->/', $data, $result);
			$param3 = trim($result[1][0]);
			if ($param3) $techdata['Световой поток, lm'] = $param3;
			
			preg_match_all('/Угол рассеивания &ndash;(.+)<\!--строка-->/', $data, $result);
			$param4 = trim($result[1][0]);
			if ($param4) $techdata['Угол обзора, °'] = $param4;
			
			if (preg_match('%3528%', $array['category'])){
				$techdata['Размер светодиодов'] = '3528 (3.5x2.8мм)';
			}
			else if (preg_match('%3014%', $array['category'])){
				$techdata['Размер светодиодов'] = '3014 (3x1.4мм)';
			}
			else if (preg_match('%5050%', $array['category'])){
				$techdata['Размер светодиодов'] = '5050/5060 (5x5мм)';
			}

			preg_match_all('/Светодиоды &ndash;.+, (\d+) шт\/м<\!--строка-->/', $data, $result);
			$param5 = trim($result[1][0]);
			if ($param5) $techdata['Плотность светодиодов, шт/м'] = $param5." шт/м";			
			
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

			preg_match_all('/Потребляемая мощность &ndash;(.+)\sВт\/м<\!--строка-->/', $data, $result);
			$param6 = trim($result[1][0]);
			if ($param6 && $param6 > 0) $techdata['Потребляемая мощность, W'] = ($param6*5)." W";
			
			preg_match_all('/Степень защиты &ndash;(.+)<\!--строка-->/', $data, $result);
			$param7 = trim($result[1][0]);
			if ($param7) {
				preg_match_all('/^(.+)\s&#40;/', $param7, $result);
				$techdata['Класс пыле-влагозащиты'] = trim($result[1][0]);
			}			

			preg_match_all('/Срок службы &ndash;(.+)<\!--строка-->/', $data, $result);
			$param8 = trim($result[1][0]);
			if ($param8) $techdata['Срок службы'] = $param8;

			preg_match_all('/<img.*src="(.+)" width/', $data, $result);
			$image = trim($result[1][0]);
			if ($image) $array['img'] = "http://geniled.ru".$image;	
			
			preg_match_all('/get\.php\?fid=Спецификация.*file=(.+)"/', $data, $result);
			$pdf = trim($result[1][0]);
			if ($pdf) $array['pdf'] = "http://geniled.ru/".$pdf;
			
			$array['pack'] = "Катушка";
			$array['packnorm'] = "5";
			$array['unit'] = "м";

			$array['descript'] = 'Лента цвет свечения '.$techdata['Цвет свечения'].''.($techdata['Световой поток, lm']?', св. поток '.$techdata['Световой поток, lm'].'':'').''.($techdata['Угол обзора, °']?', угол освещения '.$techdata['Угол обзора, °'].'.':'').' Питание '.$techdata['Напряжение питания, V'].', мощность '.$techdata['Потребляемая мощность, W'].'. Срок службы '.$techdata['Срок службы'].'. Длина 5м. Цена указана за 1м. Разрезается на сегменты (мин.50мм).';
			
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