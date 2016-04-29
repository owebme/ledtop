<?php

ini_set('max_execution_time', 600);

require_once 'db.php';

header("Content-type: text/html; charset=utf-8");

print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<style>html {width:988px; margin:25px auto 0; font-family: Arial, Helvetica;} body {margin:0;} * {margin:0; padding:0;} h2, h3 {margin:20px 0 10px;} h2 {font-size:1.7em; margin-bottom:12px;} p {margin-bottom:7px;} .name {display:inline-block; width:40%;} em {font-style:normal; display:inline-block; margin-right:2px; position:relative; top:-3px;} h2:first-child {margin-top:0px;}</style>';

require_once 'get_xml.php';

	getFile('ledribbon');
	getFile('supply');
	getFile('lightcontrol');
	getFile('profile');
	getFile('ledlamps');
	getFile('ledbulbs');
	getFile('ledmodules');
	getFile('ledprojectors');
	getFile('leds');

	parserPriceXML('Светодиоды', 'leds');
	
	parserPriceXML('Ленты', 'ledribbon');
	
	parserPriceXML('Лампы', 'ledbulbs');
	
	parserPriceXML('Светильники', 'ledlamps');
	
	parserPriceXML('Модули', 'ledmodules');
	
	parserPriceXML('Прожекторы', 'ledprojectors');
	
	parserPriceXML('Управление', 'lightcontrol');
	
	parserPriceXML('Питание', 'supply');
	
	parserPriceXML('Профили', 'profile');
	
	
	function parserPriceXML($name, $file){
	
		$response = file_get_contents('http://ledtop-shop.ru/parser/transistor_catalog_'.$file.'.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">'.$name.'</h2>';
		
		foreach ($data as $element){
			$article=""; $price1=""; $price2=""; $stock=""; $possible=""; $waiting="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($item->nodeName == "price1"){$price1 = $item->nodeValue;}
				if ($item->nodeName == "price2"){$price2 = $item->nodeValue;}
				if ($item->nodeName == "stock"){$stock = $item->nodeValue;}
				if ($item->nodeName == "possible"){$possible = $item->nodeValue;}
				if ($item->nodeName == "waiting"){$waiting = $item->nodeValue;}
			}
			$result = mysql_query("SELECT p_name, p_price, p_price_cost FROM cat_product WHERE p_art = '".$article."' LIMIT 1");
			if (mysql_num_rows($result)){
				while ($row = @mysql_fetch_array($result)){
					$p_name = $row["p_name"];
					$price = $row["p_price"];
					$price_opt = $row["p_price_opt"];					
				}
				$item = '<p><span class="name">'.utf8($p_name).'</span>';
				if ($price1 > $price){$item .= ' <span style="color:red">розн. <em>&uarr;</em>'.($price1 - $price).' руб.</span>';}
				else if ($price1 < $price){$item .= ' <span style="color:green">розн. <em>&darr;</em>'.($price - $price1).' руб.</span>';}
				if ($price2 > $price_opt){$item .= ' <span style="color:red">опт. <em>&uarr;</em>'.($price2 - $price_opt).' руб.</span>';}
				else if ($price2 < $price_opt){$item .= ' <span style="color:green">опт. <em>&darr;</em>'.($price_opt - $price2).' руб.</span>';}
				$item .= '</p>';
				
				$price_opt = $price1 - $price1*0.15;
				$price_opt_large = $price2;
				
				$price_cost = $price2 - $price2*0.12;
				
				print $item;
				
				mysql_query("UPDATE cat_product SET `p_price`='".$price1."', `p_price_opt`='".$price_opt."', `p_price_opt_large`='".$price_opt_large."', `p_price_cost`='".$price_cost."', `p_count`='".$stock."', `p_date_up`=NOW() WHERE p_art='".$article."' LIMIT 1");
				
				mysql_query("UPDATE products_alright SET `p_price`='".$price1."', `p_price_opt`='".$price_opt."', `p_price_opt_large`='".$price_opt_large."', `p_price_cost`='".$price_cost."', `p_stock`='".$stock."', `p_possible`='".$possible."', `p_waiting`='".$waiting."' WHERE p_art='".$article."' LIMIT 1");
			}
		}
	}

function utf8($data){
	$data = iconv("WINDOWS-1251","UTF-8", $data);
	return $data;
}

?>		
	
	