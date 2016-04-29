<?php

function getFilterModuli($gid = 4){

	$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledmodules.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");	
	
	$filter1 = 'Размер светодиодов';
	$filter2 = 'Кол-во св.диодов';
	$filter3 = 'Форма';
	$filter4 = 'Класс пыле-влагозащиты';
	$filter5 = 'Напряжение питания';
	$filter6 = 'Потребляемая мощность';

	$params_1 = array(); $params_2 = array();
	$params_3 = array(); $params_4 = array();
	$params_5 = array(); $params_6 = array();
	foreach ($data as $element){
		foreach ($element->childNodes as $item){
			if ($item->nodeName == "techdata"){
				foreach ($item->childNodes as $t){
					if ($t->nodeName == "param"){
						$n=""; $v="";
						foreach ($t->childNodes as $p){
							if ($p->nodeName == "name"){$n = $p->nodeValue;}
							if ($p->nodeName == "values"){$v = trim($p->nodeValue);}
						}
						if ($v != "-" && !preg_match('%\n%ui', $v)){
							if ($n == $filter1 && !in_array($v, $params_1)){
								array_push($params_1, $v);
							}						
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
			if ($row["filter_id"] == "18"){
				print "<h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_1 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}		
			if ($row["filter_id"] == "19"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_2 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "20"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_3 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "21"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_4 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "22"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_5 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}	
			if ($row["filter_id"] == "23"){
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