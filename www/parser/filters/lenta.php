<?php

function getFilterLenta($gid = 1){

	getColors(706, $gid, 'ledribbon');

	$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledribbon.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");	
	
	$filter1 = 'developer';
	$filter2 = 'Размер светодиодов';
	$filter3 = 'Плотность светодиодов';
	$filter4 = 'Класс пыле-влагозащиты';
	$filter5 = 'Напряжение питания';
	$filter6 = 'Потребляемая мощность';
	
	$params_1 = array(); $params_2 = array();
	$params_3 = array(); $params_4 = array();
	$params_5 = array(); $params_6 = array();
	foreach ($data as $element){
		foreach ($element->childNodes as $item){
			if ($item->nodeName == $filter1 && !in_array($item->nodeValue, $params_1) && $item->nodeValue != "-"){
				array_push($params_1, $item->nodeValue);
			}
			if ($item->nodeName == "techdata"){
				foreach ($item->childNodes as $t){
					if ($t->nodeName == "param"){
						$n=""; $v="";
						foreach ($t->childNodes as $p){
							if ($p->nodeName == "name"){$n = $p->nodeValue;}
							if ($p->nodeName == "values"){$v = trim($p->nodeValue);}
						}
						if ($v != "-" && !preg_match('%\n%ui', $v)){
							if ($n == $filter2 && !in_array($v, $params_2)){
								array_push($params_2, $v);
							}						
							if ($n == $filter3 && !in_array($v, $params_3)){
								array_push($params_3, $v);
							}
							if ($n == $filter4 && !in_array($v, $params_4)){
								array_push($params_4, $v);
							}			
							if ($n == $filter5 && !in_array($v, $params_5)){
								array_push($params_5, $v);
							}						
							if ($n == $filter6 && !in_array($v, $params_6)){
								array_push($params_6, $v);
							}
						}
					}
				}
			}
		}
	}
	
	#print_r($params_1);
	$result = mysql_query("SELECT * FROM cat_product_filters WHERE f_pid = '0' ORDER BY filter_id ASC");
	while ($row = @mysql_fetch_array($result)){
		if ($row["gid"] == $gid){
			if ($row["filter_id"] == "1"){
				print "<h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_1 as $value){
					$name="";
					if ($value == "ARL"){$name = "Лента LUX";}
					else if ($value == "Norm"){$name = "Лента стандарт";}
					if ($name){
						addFilter($value, $name, $row["filter_id"], $gid);
					}
				}
			}		
			if ($row["filter_id"] == "2"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_2 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "3"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_3 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "4"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_4 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "5"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_5 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}	
			if ($row["filter_id"] == "6"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_6 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}			
		}
	}
}

?>