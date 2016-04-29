<?php

	function parserLamp(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledbulbs.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Лампы</h2>';
		
		$c_pid = 3;
		
		parsLamp($data, 'G4 12V');
		parsLamp($data, 'G9 220V');
		createCategory('E27 220V', $c_pid);
			createCategory('Шар 220V E27', 'E27 220V');
			createCategory('Свеча 220V E27', 'E27 220V');
			createCategory('Шар с пультом 220V', 'E27 220V');
			createCategory('Кукуруза 220V', 'E27 220V');
			parsLamp($data, 'Шар 220V E27', false);
			parsLamp($data, 'Свеча 220V E27', false);
			parsLamp($data, 'Шар с пультом 220V', false);
			parsLamp($data, 'Кукуруза 220V', false);
		createCategory('E14 220V', $c_pid);
			createCategory('Шар 220V E14', 'E14 220V');
			createCategory('Свеча 220V E14', 'E14 220V');
			parsLamp($data, 'Шар 220V E14', false);
			parsLamp($data, 'Свеча 220V E14', false);
		parsLamp($data, 'MR16 GU5.3 12V');
		parsLamp($data, 'MR16 GU5.3 220V');
		parsLamp($data, 'GU10 220V');
		parsLamp($data, 'MR11 12V');
		createCategory('AR111 12/220V', $c_pid);
			createCategory('AR111 G53 12V', 'AR111 12/220V');
			createCategory('AR111 GU10 220V', 'AR111 12/220V');		
			parsLamp($data, 'AR111 G53 12V', false);
			parsLamp($data, 'AR111 GU10 220V', false);
		parsLamp($data, 'GX53 220V');
		createCategory('Т8 линейные', $c_pid);
			createCategory('Т8 600мм G13', 'Т8 линейные');
			createCategory('Т8 900мм G13', 'Т8 линейные');
			createCategory('Т8 1200мм G13', 'Т8 линейные');
			createCategory('Т8 1500мм G13', 'Т8 линейные');
			parsLamp($data, 'Т8 600мм G13', false);
			parsLamp($data, 'Т8 900мм G13', false);
			parsLamp($data, 'Т8 1200мм G13', false);
			parsLamp($data, 'Т8 1500мм G13', false);
	}
	
	
function parsLamp($xml, $name, $c_pid = 3){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'G4 12V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/g4/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'G9 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/g9/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'Шар 220V E27'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/шар/ui', $value) && preg_match('/e27/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'Свеча 220V E27'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/свеча/ui', $value) && preg_match('/e27/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}			
	}
	else if ($name == 'Шар с пультом 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/шар/ui', $value) && preg_match('/пульт/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	else if ($name == 'Кукуруза 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/corn/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	else if ($name == 'Шар 220V E14'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/шар/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}			
	}
	else if ($name == 'Свеча 220V E14'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/свеча/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'MR16 GU5.3 12V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/mr16/ui', $value) && preg_match('/12/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'MR16 GU5.3 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/mr16/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'GU10 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/gu10/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	else if ($name == 'MR11 12V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/mr11/ui', $value) && preg_match('/12/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	else if ($name == 'AR111 G53 12V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/ar111/ui', $value) && preg_match('/12/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'AR111 GU10 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/ar111/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'GX53 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/gx53/ui', $value) && preg_match('/220/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'Т8 600мм G13'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/t8/ui', $value) && preg_match('/600/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'Т8 900мм G13'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/t8/ui', $value) && preg_match('/900/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'Т8 1200мм G13'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/t8/ui', $value) && preg_match('/1200/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	else if ($name == 'Т8 1500мм G13'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/t8/ui', $value) && preg_match('/1500/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){$params['techdata'] = parsTechData($item);}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	
	print '<h3>'.$name.': '.$counts.'</h3>';
	
	parsProducts($products, $name);
	
	file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);
}

?>