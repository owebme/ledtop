<?php

function getFilterSvet($gid = 3){

	getColors(12, $gid, 'ledlamps');

	$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledlamps.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");	
	
	$filter1 = 'Форма';
	$filter2 = 'Способ установки';
	$filter3 = 'Диаметр отверстия';
	$filter4 = 'Напряжение питания';
	$filter5 = 'Потребляемая мощность';

	$params_1 = array(); $params_2 = array();
	$params_3 = array(); $params_4 = array();
	$params_5 = array();
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
			if ($row["filter_id"] == "13"){
				print "<h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_1 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "14"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_2 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "15"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_3 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "16"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_4 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}	
			if ($row["filter_id"] == "17"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_5 as $value){
					addFilter($value, $value, $row["filter_id"], $gid);
				}
			}			
		}
	}
}

?>