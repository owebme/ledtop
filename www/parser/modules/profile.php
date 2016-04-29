<?php

	function parserProfile(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_profile.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Профили</h2>';
		
		parserCatalog($data, 9);
	}

?>