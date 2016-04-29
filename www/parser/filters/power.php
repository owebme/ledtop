<?php

function getFilterPower($gid = 5){

	$response = file_get_contents(getDomen().'/parser/transistor_catalog_supply.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");	
	
	$filter1 = 'Входное напряжение';
	$filter2 = 'Выходное напряжение';
	$filter3 = 'Выходная мощность';
	$filter4 = 'Выходной ток';
	$filter5 = 'Класс пыле-влагозащиты';

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
			if ($row["filter_id"] == "24"){
				print "<h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_1 as $value){
					$name = $value;
					$name = preg_replace("%min: (\d+) V; typ: (\d+) V; max: (\d+) V%si", "$1V - $3V, $2V", $name);
					$name = preg_replace("%min: (\d+)\s(\d+) V; max: (\d+) V%si", "$1$2V - $3V", $name);
					$name = preg_replace("%min: (\d+) V; max: (\d+) V%si", "$1V - $2V", $name);
					$name = preg_replace("%typ: (\d+) V%si", "$1V", $name);
					addFilter($value, $name, $row["filter_id"], $gid);
				}
			}		
			if ($row["filter_id"] == "25"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_2 as $value){
					$name = $value;
					$name = preg_replace("%min: (\d+) V; max: (\d+),(\d+) V%si", "$1V - $2.$3V", $name);
					$name = preg_replace("%min: (\d+) V; max: (\d+) V%si", "$1V - $2V", $name);
					$name = preg_replace("%max: (\d+) V%si", "$1V max", $name);
					$name = preg_replace("%typ: (\d+) V%si", "$1V", $name);
					addFilter($value, $name, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "26"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_3 as $value){
					$name = $value;
					$name = preg_replace("%typ: (\d+),(\d+) W; max: (\d+),(\d+) W%si", "$1.$2W - $3.$4W", $name);
					$name = preg_replace("%min: (\d+) W; max: (\d+) W%si", "$1W - $2W", $name);
					$name = preg_replace("%max: (\d+) W%si", "$1W max", $name);
					$name = preg_replace("%typ: (\d+),(\d+) W%si", "$1.$2W", $name);
					$name = preg_replace("%typ: (\d+)\s(\d+) W%si", "$1$2W", $name);
					$name = preg_replace("%typ: (\d+) W%si", "$1W", $name);
					addFilter($value, $name, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "27"){
				print "<br><h3>".utf8($row["name"])."</h3>";
				mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$row["filter_id"]."'");
				foreach ($params_4 as $value){
					$name = $value;
					$name = preg_replace("%min: (\d+),(\d+) A; max: (\d+),(\d+) A%si", "$1.$2A - $3.$4A", $name);
					$name = preg_replace("%min: (\d+),(\d+) A; max: (\d+) A%si", "$1.$2A - $3A", $name);
					$name = preg_replace("%min: (\d+) A; max: (\d+) A%si", "$1A - $2A", $name);
					$name = preg_replace("%max: (\d+),(\d+) A%si", "$1.$2A max", $name);
					$name = preg_replace("%max: (\d+) A%si", "$1A max", $name);
					$name = preg_replace("%typ: (\d+),(\d+) A%si", "$1.$2A", $name);
					$name = preg_replace("%typ: (\d+)\s(\d+) A%si", "$1$2A", $name);
					$name = preg_replace("%typ: (\d+) A%si", "$1A", $name);
					addFilter($value, $name, $row["filter_id"], $gid);
				}
			}
			if ($row["filter_id"] == "28"){
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