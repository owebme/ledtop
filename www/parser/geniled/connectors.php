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

$q = 'ксессуары для светодиодных лент';

$arrLinks = parsGeniledLinks('/new/new_lent.php', '/new/sm_filter_lent_result.php');
$data = parsLentaXLS($arrLinks, $q);

#print_r($data);

	print '<h2 style="color:brown">Коннекторы</h2>';
	
	$c_pid = 2;

	parsLenta($data, 'Коннекторы', false);

function parsLenta($data, $name, $c_pid = 2){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Коннекторы'){
		foreach ($data as $article => $array){
			$products[$article] = $array; $counts++;
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
						else if ($i == 3 && $r[$i] && preg_match('%'.$q.'%', $params["category"])){
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
			$techdata['Тип товара'] = 'Коннектор';
			
			preg_match_all('/Количество штук в наборе &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Количество штук в наборе'] = $param;
			
			preg_match_all('/Длина провода &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Длина провода'] = $param;				
			
			preg_match_all('/Количество разъемов &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Количество разъемов'] = $param;	

			preg_match_all('/Степень защиты &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Степень защиты'] = $param;				
			
			preg_match_all('/Состав набора &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Состав набора'] = $param;
			
			preg_match_all('/Тип соединяемой ленты &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Тип соединяемой ленты'] = $param;	

			preg_match_all('/Ширина ленты &ndash;(.+)<\!--строка-->/', $data, $result);
			$param = trim($result[1][0]);
			if ($param) $techdata['Ширина ленты'] = $param;	

			preg_match_all('/<img.*src="(.+)" width/', $data, $result);
			$image = trim($result[1][0]);
			if ($image) $array['img'] = "http://geniled.ru".$image;			
			
			$array['pack'] = "Упаковка";
			$array['packnorm'] = "20";
			$array['unit'] = "шт";

			$array['descript'] = $array['name'];
			
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