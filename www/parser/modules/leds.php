<?php

	function parserLeds(){
	
		$response = file_get_contents(getDomen().'/parser/transistor_catalog_leds.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Светодиоды</h2>';
		
		parserCatalog($data, 1);
	}
	

?>