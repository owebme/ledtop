<?php

	function parserLenta(){
	
		$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledribbon.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Ленты</h2>';
		
		$c_pid = 2;
		
		parsLenta($data, 'Лента класса ЛЮКС');
		parsLenta($data, 'Лента на диодах 3528');
		parsLenta($data, 'Лента на диодах 5060 (5050)');
		parsLenta($data, 'Ленты LUX ультра 5630, 2835');
		parsLenta($data, 'Лента узкая 5 мм');
		parsLenta($data, 'Лента мультицветная RGBW (хамелеон)');
		parsLenta($data, 'Лента RGB «Бегущий огонь»');
		parsLenta($data, 'Ленты угловые и боковые');
		parsLenta($data, 'Гибкий неон ARL, NEO');
		parsLenta($data, 'Декоративные WR-нити');
		parsLenta($data, 'Коннекторы');
	}
	
	
function parsLenta($xml, $name, $c_pid = 2){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}

	$products = array(); $counts="";
	if ($name == 'Лента класса ЛЮКС'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/lux/ui', $value)){
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
	else if ($name == 'Лента на диодах 3528'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('/3528/ui', $value)){
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
	else if ($name == 'Лента на диодах 5060 (5050)'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('/5060/ui', $value) or preg_match('/5050/ui', $value)){
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
	else if ($name == 'Ленты LUX ультра 5630, 2835'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('/5630/ui', $value) or preg_match('/2835/ui', $value)){
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
	else if ($name == 'Лента узкая 5 мм'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){
						foreach ($item->childNodes as $t){
							if ($t->nodeName == "param"){
								$n=""; $v="";
								foreach ($t->childNodes as $p){
									if ($p->nodeName == "name"){$n = $p->nodeValue;}
									if ($p->nodeName == "values"){$v = trim($p->nodeValue);}
								}
								if ($n == 'Ширина' && $v == '5 мм'){
									$flag = true;
								}
							}
						}
						$params['techdata'] = parsTechData($item);
					}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}	
	else if ($name == 'Лента мультицветная RGBW (хамелеон)'){
		foreach ($xml as $element){
			$params = array(); $flag = true; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($item->nodeName == "color1" && $item->nodeValue == ""){$flag="";}
				if ($item->nodeName == "color2" && $item->nodeValue == ""){$flag="";}
				if ($item->nodeName == "color3" && $item->nodeValue == ""){$flag="";}
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
	else if ($name == 'Лента RGB «Бегущий огонь»'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/бегущий огонь/ui', $value)){
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
	else if ($name == 'Ленты угловые и боковые'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/боков/ui', $value)){
						$flag = true;
					}
				}
				if ($item->nodeName == "article"){$article = $item->nodeValue;}
				if ($article && $item->nodeName != "#text" && $item->nodeName != "article" && $item->nodeName != "category" && $item->nodeName != "group"){
					if ($item->nodeName == "techdata"){
						foreach ($item->childNodes as $t){
							if ($t->nodeName == "param"){
								$n=""; $v="";
								foreach ($t->childNodes as $p){
									if ($p->nodeName == "name"){$n = $p->nodeValue;}
									if ($p->nodeName == "values"){$v = trim($p->nodeValue);}
								}
								if ($n == 'Размер светодиодов' && !preg_match('/DIP 5мм/ui', $v) && !preg_match('/335/ui', $v)){
									$flag="";
								}
							}
						}
						$params['techdata'] = parsTechData($item);
					}
					else {$value = $item->nodeValue;
						if ($item->nodeName == "name"){$value = getName($item);}
						$params[$item->nodeName] = $value;
					}
				}
			}
			if ($flag){$products[$article] = $params; $counts++;}
		}		
	}
	else if ($name == 'Гибкий неон ARL, NEO'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/ибкий/ui', $value) or preg_match('/ибкие/ui', $value)){
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
	else if ($name == 'Декоративные WR-нити'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/ нить/ui', $value) or preg_match('/ нити/ui', $value)){
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
	else if ($name == 'Коннекторы'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/оннектор/ui', $value)){
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