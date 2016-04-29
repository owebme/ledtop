<?php

function getColors($c_id, $gid, $url){

	$response = file_get_contents(getDomen().'/parser/transistor_catalog_'.$url.'.xml');	

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("product");
	
	$array = array();
	foreach ($data as $element){
		$id=""; $colors="";
		foreach ($element->childNodes as $item){
			if ($item->nodeName == "group"){
				if (!$id){
					if ($c1){$colors .= $c1;}
					if ($c2){$colors .= "|".$c2;}
					if ($c3){$colors .= "|".$c3;}
					if (!in_array($colors, $array) && $colors){
						array_push($array, $colors);
					}
					$c1=""; $c2=""; $c3="";
				}
				$id = $item->getAttribute('id');
			}
			if ($item->nodeName == 'color1' && $item->nodeValue){
				$c1 = $item->nodeValue;
			}						
			if ($item->nodeName == 'color2' && $item->nodeValue){
				$c2 = $item->nodeValue;
			}
			if ($item->nodeName == 'color3' && $item->nodeValue){
				$c3 = $item->nodeValue;
			}
		}
	}
	
	mysql_query("DELETE FROM cat_product_filters WHERE f_pid = '".$c_id."'");
	
	print "<br><h3>Цвет свечения</h3>";
	
	foreach ($array as $color){
		if ($url == "ledbulbs" && $color == "red"){
		}
		else {
			addColors($color, $color, $c_id, $gid);
		}
	}	
	
	print "<br>";
}

?>