<?php

ini_set('max_execution_time', 600);

require_once 'db.php';

header("Content-type: text/html; charset=utf-8");

	$response = file_get_contents('http://ledtop-shop.ru/parser/transistor_catalog_supply.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");
	
	foreach ($data as $element){
		$article=""; $unit="";
		foreach ($element->childNodes as $item){
			if ($item->nodeName == "article"){$article = $item->nodeValue;}
			if ($item->nodeName == "unit"){$unit = $item->nodeValue;}
		}
		if ($article && $unit){
			$p_id="";
			$result = mysql_query("SELECT p_id FROM cat_product WHERE p_art = '".$article."' LIMIT 1");
			while ($row = @mysql_fetch_array($result)){
				$p_id = $row["p_id"];
			}	
			if ($p_id > 0){
				print $article." - ".$unit."<br>";
				mysql_query("UPDATE cat_product_fields SET `value`='".cp1251($unit)."' WHERE p_id = '".$p_id."' AND field = '".cp1251('Единица измерения')."' AND unic = '0' LIMIT 1");
			}
		}
	}
	
function cp1251($data){
	$data = iconv("UTF-8","WINDOWS-1251", $data);
	return $data;
}	
	
?>