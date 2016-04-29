<?php

	function parserProjectors(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledprojectors.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");	
		
		print '<h2 style="color:brown">Прожекторы</h2>';
		
		parserCatalog($data, 6);
	}

?>