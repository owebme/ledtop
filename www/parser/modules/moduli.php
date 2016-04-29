<?php

	function parserModuli(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledmodules.xml');
		
		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Модули</h2>';
		
		parserCatalog($data, 5);
	}

?>