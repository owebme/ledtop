<?php

	function parserPower(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_supply.xml');	
		
		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");	
		
		print '<h2 style="color:brown">Питание</h2>';
		
		parserCatalog($data, 8);
	}

?>