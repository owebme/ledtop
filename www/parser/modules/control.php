<?php

	function parserControl(){

		$response = file_get_contents(getDomen().'/parser/transistor_catalog_lightcontrol.xml');	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("product");
		
		print '<h2 style="color:brown">Управление</h2>';
		
		$c_pid = 7;
		
		createCategory('RGB-контроллеры', $c_pid);
			createCategory('ИК - контроллеры', 'RGB-контроллеры');
			createCategory('RF-контроллеры (кнопочные)', 'RGB-контроллеры');
			createCategory('RF-контроллеры (сенсорные)', 'RGB-контроллеры');
			createCategory('Панели-контроллеры', 'RGB-контроллеры');
			parsControl($data, 'ИК - контроллеры', false);
			parsControl($data, 'RF-контроллеры (кнопочные)', false);
			parsControl($data, 'RF-контроллеры (сенсорные)', false);
			parsControl($data, 'Панели-контроллеры', false);
			createCategory('Профессиональные RGB/RGBW системы', 'RGB-контроллеры');
				$cid1 = createCategory('Мульти-пульт', 'Профессиональные RGB/RGBW системы', true);
				$cid2 = createCategory('Мульти-панель', 'Профессиональные RGB/RGBW системы', true);
				$cid3 = createCategory('Мульти-контроллер', 'Профессиональные RGB/RGBW системы', true);
				parsControl($data, 'Профессиональные RGB/RGBW системы => Мульти-пульт', false, $cid1);
				parsControl($data, 'Профессиональные RGB/RGBW системы => Мульти-панель', false, $cid2);
				parsControl($data, 'Профессиональные RGB/RGBW системы => Мульти-контроллер', false, $cid3);
			createCategory('WiFi контроллеры', 'RGB-контроллеры');
			createCategory('Аудио-контроллеры RGB', 'RGB-контроллеры');
			createCategory('RGB/RGB+W усилители', 'RGB-контроллеры');
			createCategory('Управление на корпусе (без пульта)', 'RGB-контроллеры');				
			parsControl($data, 'WiFi контроллеры', false);
			parsControl($data, 'Аудио-контроллеры RGB', false);
			parsControl($data, 'RGB/RGB+W усилители', false);
			parsControl($data, 'Управление на корпусе (без пульта)', false);
		createCategory('Белый MIX контроллеры', $c_pid);
			createCategory('Комплект с пультом', 'Белый MIX контроллеры');
			$cid4 = createCategory('Сенсорные панели-контроллеры', 'Белый MIX контроллеры', true);
			parsControl($data, 'Комплект с пультом', false);
			parsControl($data, 'Белый MIX контроллеры => Сенсорные панели-контроллеры', false, $cid4);
			createCategory('Профессиональные MIX системы', 'Белый MIX контроллеры');
				$cid5 = createCategory('Мульти-пульт', 'Профессиональные MIX системы', true);
				$cid6 = createCategory('Мульти-панель', 'Профессиональные MIX системы', true);
				$cid7 = createCategory('Мульти-контроллер', 'Профессиональные MIX системы', true);
				parsControl($data, 'Профессиональные MIX системы => Мульти-пульт', false, $cid5);
				parsControl($data, 'Профессиональные MIX системы => Мульти-панель', false, $cid6);
				parsControl($data, 'Профессиональные MIX системы => Мульти-контроллер', false, $cid7);
		createCategory('Диммеры', $c_pid);
			createCategory('Контроллер с пультом', 'Диммеры');
			$cid8 = createCategory('Сенсорные панели-контроллеры', 'Диммеры', true);
			createCategory('Без пульта управления', 'Диммеры');			
			parsControl($data, 'Контроллер с пультом', false);
			parsControl($data, 'Диммеры => Сенсорные панели-контроллеры', false, $cid8);
			parsControl($data, 'Без пульта управления', false);
			createCategory('Профессиональные DIM системы', 'Диммеры');
				$cid9 = createCategory('Мульти-пульт', 'Профессиональные DIM системы', true);
				$cid10 = createCategory('Мульти-панель', 'Профессиональные DIM системы', true);
				$cid11 = createCategory('Мульти-контроллер', 'Профессиональные DIM системы', true);			
				parsControl($data, 'Профессиональные DIM системы => Мульти-пульт', false, $cid9);
				parsControl($data, 'Профессиональные DIM системы => Мульти-панель', false, $cid10);
				parsControl($data, 'Профессиональные DIM системы => Мульти-контроллер', false, $cid11);
		parserCategory($data, 'Датчики управления освещением', 'Датчики управления освещением', $c_pid);
		parserCategory($data, 'Бегущие огни, SPI, флэш-модули', 'Бегущие огни, SPI, пиксели', $c_pid);
		parserCategory($data, 'Диммеры с управлением 0-10V', 'Диммеры с управлением 0-10V', $c_pid);
		parserCategory($data, 'Диммеры с управлением TRIAC', 'Диммеры с управлением TRIAC', $c_pid);
		parserCategory($data, 'Диммеры-выключатели с датчиком', 'Диммеры-выключатели с датчиком', $c_pid);
		parserCategory($data, 'Управление DMX', 'Управление DMX', $c_pid);
		parserCategory($data, 'Управление DALI', 'Управление DALI', $c_pid);
	}
	
	
function parsControl($xml, $name, $c_pid = 7, $c_id = false){

	if ($c_pid > 0){
		createCategory($name, $c_pid);
	}

	$products = array(); $counts="";
	if ($name == 'ИК - контроллеры'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / комплекты с пультом%ui', $value) or $id == "133"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && (!preg_match('/IR/ui', $item->nodeValue) && !preg_match('/ИК-пульт/ui', $item->nodeValue))){
					$flag="";
				}		
				if ($item->nodeName == "descript" && (!preg_match('/IR/ui', $item->nodeValue) && !preg_match('/ИК-пульт/ui', $item->nodeValue))){
					$flag="";
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
	else if ($name == 'RF-контроллеры (кнопочные)'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / комплекты с пультом%ui', $value) or $id == "133"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/RF/ui', $item->nodeValue)){
					$flag="";
				}
				if ($item->nodeName == "name" && preg_match('/сенс/ui', $item->nodeValue) or preg_match('/sens/ui', $item->nodeValue)){
					$flag="";
				}
				if ($item->nodeName == "descript" && preg_match('/сенс/ui', $item->nodeValue) or preg_match('/sens/ui', $item->nodeValue)){
					$flag="";
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
	else if ($name == 'RF-контроллеры (сенсорные)'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / комплекты с пультом%ui', $value) or $id == "133"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/сенс/ui', $item->nodeValue) && !preg_match('/sens/ui', $item->nodeValue)){
					$flag="";
				}				
				if ($item->nodeName == "descript" && !preg_match('/сенс/ui', $item->nodeValue) && !preg_match('/sens/ui', $item->nodeValue)){
					$flag="";
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
	else if ($name == 'Панели-контроллеры'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / встраиваемые панели%ui', $value) or $id == "452"){
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
	else if ($name == 'Профессиональные RGB/RGBW системы => Мульти-пульт'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / пульты, контроллеры [раздельно]%ui', $value) or preg_match('%RGB-контроллеры / RGB/RGBW серия SR%ui', $value) or preg_match('%RGB-контроллеры / RGB/RGBW серия SR-434%ui', $value) or $id == "409" or $id == "367" or $id == "380"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/пульт/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Профессиональные RGB/RGBW системы => Мульти-панель'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / пульты, контроллеры [раздельно]%ui', $value) or preg_match('%RGB-контроллеры / RGB/RGBW серия SR%ui', $value) or preg_match('%RGB-контроллеры / RGB/RGBW серия SR-434%ui', $value) or $id == "409" or $id == "367" or $id == "380"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/панель/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Профессиональные RGB/RGBW системы => Мульти-контроллер'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / пульты, контроллеры [раздельно]%ui', $value) or preg_match('%RGB-контроллеры / RGB/RGBW серия SR%ui', $value) or preg_match('%RGB-контроллеры / RGB/RGBW серия SR-434%ui', $value) or $id == "409" or $id == "367" or $id == "380"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/контроллер/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}		
	else if ($name == 'WiFi контроллеры'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / управление телефоном \[Wi-Fi\]%ui', $value) or $id == "176"){
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
	else if ($name == 'Аудио-контроллеры RGB'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / аудио-вход%ui', $value) or $id == "135"){
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
	else if ($name == 'RGB/RGB+W усилители'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / RGB/RGBW-усилители%ui', $value) or $id == "540"){
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
	else if ($name == 'Управление на корпусе (без пульта)'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%RGB-контроллеры / кнопочные \[без пульта\]%ui', $value) or $id == "122"){
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
	else if ($name == 'Комплект с пультом'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%MIX-контроллеры для White лент / комплекты с пультом%ui', $value) or $id == "579"){
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
	else if ($name == 'Белый MIX контроллеры => Сенсорные панели-контроллеры'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%MIX-контроллеры для White лент / встраиваемые панели%ui', $value) or $id == "558"){
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Профессиональные MIX системы => Мульти-пульт'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%MIX-контроллеры для White лент / пульты, панели, контроллеры \[раздельно\]%ui', $value) or preg_match('%MIX-контроллеры для White лент / серия SR%ui', $value) or $id == "166" or $id == "496"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/пульт/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}	
	else if ($name == 'Профессиональные MIX системы => Мульти-панель'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%MIX-контроллеры для White лент / пульты, панели, контроллеры \[раздельно\]%ui', $value) or preg_match('%MIX-контроллеры для White лент / серия SR%ui', $value) or $id == "166" or $id == "496"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/панель/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}	
	else if ($name == 'Профессиональные MIX системы => Мульти-контроллер'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%MIX-контроллеры для White лент / пульты, панели, контроллеры \[раздельно\]%ui', $value) or preg_match('%MIX-контроллеры для White лент / серия SR%ui', $value) or $id == "166" or $id == "496"){
						$flag = true;
					}
				}
				if ($item->nodeName == "name" && !preg_match('/контроллер/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Контроллер с пультом'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%Диммеры / комплекты с пультом%ui', $value) or $id == "305"){
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
	else if ($name == 'Диммеры => Сенсорные панели-контроллеры'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%Диммеры / встраиваемые панели%ui', $value) or preg_match('%Диммеры / для светильников (токовые) с пультом%ui', $value) or $id == "169" or $id == "486"){
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Без пульта управления'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%Диммеры / кнопочные \[без пульта\]%ui', $value) or preg_match('%Диммеры / с потенциометром%ui', $value) or $id == "170" or $id == "118"){
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
	else if ($name == 'Профессиональные DIM системы => Мульти-пульт'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%Диммеры / пульты, диммеры \[раздельно\]%ui', $value) or preg_match('%Диммеры / серия SR%ui', $value) or $id == "560" or $id == "167"){
						$flag = true;
					}
				}	
				if ($item->nodeName == "name" && !preg_match('/пульт/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Профессиональные DIM системы => Мульти-панель'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%Диммеры / пульты, диммеры \[раздельно\]%ui', $value) or preg_match('%Диммеры / серия SR%ui', $value) or $id == "560" or $id == "167"){
						$flag = true;
					}
				}	
				if ($item->nodeName == "name" && !preg_match('/панель/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}
	else if ($name == 'Профессиональные DIM системы => Мульти-контроллер'){
		foreach ($xml as $element){
			$params = array(); $flag=""; $article="";
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "group"){
					$id = $item->getAttribute('id');
					$value = $item->nodeValue;
					if (preg_match('%Диммеры / пульты, диммеры \[раздельно\]%ui', $value) or preg_match('%Диммеры / серия SR%ui', $value) or $id == "560" or $id == "167"){
						$flag = true;
					}
				}	
				if ($item->nodeName == "name" && !preg_match('/контроллер/ui', $item->nodeValue)){
					$flag="";
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
		if ($c_id > 0){
			$name = $c_id;
		}
	}	
	
	print '<h3>'.$name.': '.sizeof($products).'</h3>';
	
	parsProducts($products, $name);
	
	file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?id='.$c_pid);
}

?>