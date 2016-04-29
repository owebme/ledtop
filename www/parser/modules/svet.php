<?php

	function parserSvet(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_ledlamps.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Светильники</h2>';
		
		$c_pid = 4;
		
		createCategory('Ультратонкие светильники', $c_pid);
			createCategory('Встраиваемые круглые 220V', 'Ультратонкие светильники');
			createCategory('Встраиваемые квадратные 220V', 'Ультратонкие светильники');
			createCategory('Универсальные панели 220V', 'Ультратонкие светильники');
			createCategory('Мультицветные RGB панели 12V', 'Ультратонкие светильники');	
			createCategory('Драйверы для светильников', 'Ультратонкие светильники');
			parsSvet($data, 'Встраиваемые круглые 220V', false);
			parsSvet($data, 'Встраиваемые квадратные 220V', false);
			parsSvet($data, 'Универсальные панели 220V', false);
			parsSvet($data, 'Мультицветные RGB панели 12V', false);
			parsSvet($data, 'Драйверы для светильников', false);
		createCategory('Стекляные светильники', $c_pid);
			createCategory('Квадратные стекляные 220V', 'Стекляные светильники');
			createCategory('Круглые стекляные 220V', 'Стекляные светильники');
			createCategory('Со световым контуром 220V', 'Стекляные светильники');
			parsSvet($data, 'Квадратные стекляные 220V', false);
			parsSvet($data, 'Круглые стекляные 220V', false);
			parsSvet($data, 'Со световым контуром 220V', false);
		createCategory('Потолочные Downlight', $c_pid);	
			createCategory('Широкий угол 220V', 'Потолочные Downlight');	
			createCategory('Направленный свет 220V', 'Потолочные Downlight');		
			parsSvet($data, 'Широкий угол 220V', false);
			parsSvet($data, 'Направленный свет 220V', false);
		createCategory('Точечные светильники SPOT', $c_pid);		
			createCategory('Точечные 220V', 'Точечные светильники SPOT');	
			createCategory('Точечные токовые 350mA', 'Точечные светильники SPOT');		
			parsSvet($data, 'Точечные 220V', false);
			parsSvet($data, 'Точечные токовые 350mA', false);
		parserCategory($data, 'Светильники мебельные', 'Мебельные светильники', $c_pid);
		parserCategory($data, 'Светильники трековые', 'Трековые светильники', $c_pid);
	}
	
function parsSvet($xml, $name, $c_pid = 4){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}
	
	$products = array(); $counts="";
	if ($name == 'Встраиваемые круглые 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/тонкие/ui', $value) && preg_match('/круглые/ui', $value) && preg_match('/220/ui', $value)){
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
	else if ($name == 'Встраиваемые квадратные 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/тонкие/ui', $value) && preg_match('/квадрат/ui', $value) && preg_match('/220/ui', $value)){
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
	else if ($name == 'Универсальные панели 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if ((preg_match('/300..1200/ui', $value) or preg_match('/600..1200/ui', $value)) && preg_match('/220/ui', $value)){
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
	else if ($name == 'Мультицветные RGB панели 12V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/мультицвет/ui', $value) && preg_match('/12/ui', $value)){
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
	else if ($name == 'Драйверы для светильников'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/драйвер/ui', $value)){
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
	else if ($name == 'Квадратные стекляные 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/квадрат/ui', $value) && preg_match('/стекл/ui', $value) && preg_match('/220/ui', $value)){
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
	else if ($name == 'Круглые стекляные 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/круг/ui', $value) && preg_match('/стекл/ui', $value) && preg_match('/220/ui', $value)){
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
	else if ($name == 'Со световым контуром 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/контур/ui', $value) && preg_match('/220/ui', $value)){
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
	else if ($name == 'Широкий угол 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article=""; $group="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if ((preg_match('/потолоч/ui', $value) or preg_match('/downlight/ui', $value)) && preg_match('/220/ui', $value)){
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
								if ($n == 'Угол обзора' && $v != '120 °'){
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
	else if ($name == 'Направленный свет 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article=""; $group="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if ((preg_match('/потолоч/ui', $value) or preg_match('/downlight/ui', $value)) && preg_match('/220/ui', $value)){
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
								if ($n == 'Угол обзора' && $v == '120 °'){
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
	else if ($name == 'Точечные 220V'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article=""; $group="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if ((preg_match('/потолоч/ui', $value) or preg_match('/downlight/ui', $value) or (preg_match('/мебел/ui', $value) && preg_match('/ltm/ui', $value))) && preg_match('/220/ui', $value)){
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
								if ($n == 'Угол обзора' && $v == '120 °'){
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
	else if ($name == 'Точечные токовые 350mA'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = strrtolower($item->nodeValue);
					if (preg_match('/токов/ui', $value) && preg_match('/350/ui', $value)){
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
	
	print '<h3>'.$name.': '.sizeof($products).'</h3>';
	
	parsProducts($products, $name);
	
	file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);
}

?>