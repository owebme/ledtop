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

$q = 'лок питания';

$arrLinks = parsGeniledLinks2('/new/new_bp.php', $q);
$data = parsXLS($arrLinks, $q);

#print_r($data);

	print '<h2 style="color:brown">Блоки питания</h2>';
	
	$c_pid = 8;

	parsSupply($data, 'Блоки питания 5V => Герметичные [IP67, металл]', false);
	parsSupply($data, 'Блоки питания 12V => Герметичные [IP67, металл]', false);
	parsSupply($data, 'В защитном кожухе', false);

function parsSupply($data, $name, $c_pid = 8){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Блоки питания 5V => Герметичные [IP67, металл]'){
		foreach ($data as $article => $array){
			if (preg_match('/сточники питания 5V/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
		$name = 264;
	}
	else if ($name == 'Блоки питания 12V => Герметичные [IP67, металл]'){
		foreach ($data as $article => $array){
			if (preg_match('/сточники питания 12V  влагозащищенные/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
		$name = 268;
	}
	else if ($name == 'В защитном кожухе'){
		foreach ($data as $article => $array){
			if (preg_match('/сточники питания 12V интерьерные/ui', $array['category'])){
				$products[$article] = $array; $counts++;
			}
		}
		$name = 270;
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
	foreach( $xlsx->rows(9) as $r ) {
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
	
	return parsGeniledTechData($products, $arrLinks);

	#foreach ($products as $article => $array){
	#	echo $article." => <br>";
	#	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['category']."<br>";
	#	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['name']."<br>";
	#	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['price1']."<br>";
	#	echo "&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;".$array['link']."<br>";
	#}
}

function parsGeniledTechData($products, $arrLinks) {

	$i = 0;
	foreach ($products as $article => $array){
		$i++;		
		//if ($i == 20) break;
		$data = $arrLinks[$article];
		
		if ($data){
			$techdata = array();
			$techdata['Тип товара'] = 'Источник напряжения';
			
			preg_match_all('/Выход.+мощность(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) {
				if (preg_match('%(\d+) - (\d+)%', $param)){
					preg_match_all('/(\d+) - (\d+)/', $param, $result);
					$param1 = $result[1][0]."W - ".$result[2][0]."W";
					if ($param1) $techdata['Выходная мощность, W'] = $param1;
				}
				else if (preg_match('%(\d+)%', $param)){
					preg_match_all('/(\d+)/', $param, $result);
					$param1 = $result[1][0]."W";
					if ($param1) $techdata['Выходная мощность, W'] = $param1;
				}
			}
			
			preg_match_all('/Вход.+напряжение(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) {
				if (preg_match('%(\d+) - (\d+)%', $param)){
					preg_match_all('/(\d+) - (\d+)/', $param, $result);
					$param1 = $result[1][0]."V - ".$result[2][0]."V";
					if ($param1) $techdata['Входное напряжение, V'] = $param1;
				}
				else if (preg_match('%(\d+)%', $param)){
					preg_match_all('/(\d+)/', $param, $result);
					$param1 = $result[1][0]."V";
					if ($param1) $techdata['Входное напряжение, V'] = $param1;
				}
			}

			preg_match_all('/Выход.+напряжение(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) {
				if (preg_match('%(\d+) - (\d+)%', $param)){
					preg_match_all('/(\d+) - (\d+)/', $param, $result);
					$param1 = $result[1][0]."V - ".$result[2][0]."V";
					if ($param1) $techdata['Выходное напряжение, V'] = $param1;
				}
				else if (preg_match('%(\d+)%', $param)){
					preg_match_all('/(\d+)/', $param, $result);
					$param1 = $result[1][0]."V";
					if ($param1) $techdata['Выходное напряжение, V'] = $param1;
				}
			}

			preg_match_all('/Выход.+ток(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) {
				if (preg_match('%(\d+) - (\d+)%', $param)){
					preg_match_all('/(\d+) - (\d+)/', $param, $result);
					$param1 = $result[1][0]."A - ".$result[2][0]."A";
					if ($param1) $techdata['Выходной ток, A'] = $param1;
				}
				else if (preg_match('%(\d+)%', $param)){
					preg_match_all('/(\d+)/', $param, $result);
					$param1 = $result[1][0]."A";
					if ($param1) $techdata['Выходной ток, A'] = $param1;
				}
			}			

			preg_match_all('/Степень защиты(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param && preg_match('%(\d+)%', $param)) {
				preg_match_all('/(\d+)/', $param, $result);
				$param1 = $result[1][0];
				if ($param1) $techdata['Класс пыле-влагозащиты'] = "IP".$param1;
			}
			
			preg_match_all('/Габаритные размеры &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Габаритные размеры'] = $param;

			preg_match_all('/Материал корпуса &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Материал корпуса'] = $param;			

			preg_match_all('/<img.*src="(.+)" width/', $data, $result);
			$image = trim($result[1][0]);
			if ($image) $array['img'] = "http://geniled.ru".$image;	
			
			preg_match_all('/get\.php\?fid=Спецификация.*file=(.+)"/', $data, $result);
			$pdf = trim($result[1][0]);
			if ($pdf) $array['pdf'] = "http://geniled.ru/".$pdf;
			
			$array['pack'] = "Коробка";
			$array['packnorm'] = "1";
			$array['unit'] = "шт";
			
			$array['link'] = "";

			$array['descript'] = $array['name']." ".$techdata['Выходное напряжение, V'].", ток ".$techdata['Выходной ток, A'].", ".$techdata['Выходная мощность, W'].",".($techdata['Материал корпуса']?" материал корпуса ".$techdata['Материал корпуса']."":"")." ".$techdata['Класс пыле-влагозащиты'].", входное напряжение ".$techdata['Входное напряжение, V'].", размеры ".$techdata['Габаритные размеры'];
			
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