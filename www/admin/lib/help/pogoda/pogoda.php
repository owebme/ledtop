<?php

header("Content-type: text/html; charset=windows-1251");

$cook = $_COOKIE['uplecms'];

if ($cook){
	list($_login, $_pass) = preg_split("%\|%",$cook);
	list($_var, $login) = preg_split("%\:%",$_login);
	list($_var, $pass) = preg_split("%\:%",$_pass);
	
	$path="";
	$path1 = $_SERVER['DOCUMENT_ROOT'].'/cgi-bin/';
	$path2 = $_SERVER['DOCUMENT_ROOT'].'/../cgi-bin/';
	
	if (file_exists($path1)) {
		$path = $path1;
	}
	else if (file_exists($path2)) {
		$path = $path2;
	}
	if ($path){
		$file = $path."admin/engine/password-settings/".$login;
		if ($pass && $login && file_exists($file) && $pass == file_get_contents($file) && file_get_contents($file) != "") {
		}
		else {
			exit();
		}
	}
}
else {
	exit();
}

	$arrCity = array(
		"Беларусь" => 4,
		"Борисов" => 9,
		"Минск" => 34,
		"Могилев" => 35,
		"Орша" => 58,
		"Казахстан" => 2,
		"Алматы" => 6,
		"Астана" => 2,
		"Актау" => 215,
		"Россия" => 1,
		"Москва" => 37,
		"Орел" => 115,
		"Волжский" => 127,
		"Зеленоград" => 101,
		"Пермь" => 59,
		"Чита" => 121,
		"Санкт-Петербург" => 69,
		"Краснодар" => 199,
		"Нижнекамск" => 147,
		"Самара" => 125,
		"Хабаровск" => 21,
		"Архангельск" => 4,
		"Вологда" => 132,
		"Новосибирск" => 99,
		"Брянск" => 104,
		"Ачинск" => 185,
		"Курск" => 107,
		"Белгород" => 112,
		"Псков" => 102,
		"Абакан" => 156,
		"Саратов" => 149,
		"Оренбург" => 167,
		"Сочи" => 116,
		"Рязань" => 65,
		"Ульяновск" => 90,
		"Пенза" => 169,
		"Ярославль" => 92,
		"Саранск" => 129,
		"Тольятти" => 86,
		"Димитровград" => 178,
		"Красноярск" => 146,
		"Первоуральск" => 60,
		"Чебоксары" => 10,
		"Новочеркасск" => 154,
		"Махачкала" => 32,
		"Обнинск" => 191,
		"Астрахань" => 5,
		"Тамбов" => 130,
		"Калининград" => 105,
		"Иваново" => 100,
		"Сызрань" => 85,
		"Комсомольск-на-Амуре" => 27,
		"Улан-Удэ" => 109,
		"Челябинск" => 11,
		"Владивосток" => 98,
		"Ангарск" => 144,
		"Сарапул" => 196,
		"Тула" => 177,
		"Екатеринбург" => 122,
		"Барнаул" => 160,
		"Находка" => 168,
		"Иркутск" => 163,
		"Нижний Новгород" => 120,
		"Братск" => 141,
		"Сергиев Посад" => 71,
		"Ковров" => 164,
		"Уссурийск" => 162,
		"Лучегорск" => 201,
		"Кисловодск" => 180,
		"Ижевск" => 182,
		"Омск" => 128,
		"Петрозаводск" => 137,
		"Уфа" => 140,
		"Коломна" => 166,
		"Сургут" => 133,
		"Ставрополь" => 75,
		"Мурманск" => 113,
		"Волгоград" => 198,
		"Воронеж" => 148,
		"Ростов-на-Дону" => 135,
		"Миасс" => 159,
		"Южно-Сахалинск" => 94,
		"Старый Оскол" => 74,
		"Липецк" => 173,
		"Мытищи" => 47,
		"Томск" => 175,
		"Северск" => 190,
		"Тверь" => 87,
		"Кемерово" => 176,
		"Владимир" => 123,
		"Благовещенск" => 8,
		"Йошкар-Ола" => 142,
		"Таганрог" => 134,
		"Майкоп" => 158,
		"Череповец" => 126,
		"Альметьевск" => 3,
		"Новороссийск" => 54,
		"Химки" => 24,
		"Казань" => 486,
		"Одинцово" => 172,
		"Люберцы" => 30,
		"Балашиха" => 7,
		"Королев" => 170,
		"Щелково" => 70,
		"Железнодорожный" => 96,
		"Новокузнецк" => 165,
		"Подольск" => 62,
		"Калуга" => 114,
		"Магнитогорск" => 106,
		"Великий Новгород" => 151,
		"Курган" => 110,
		"Златоуст" => 117,
		"Тюмень" => 88,
		"Сыктывкар" => 84,
		"Черкесск" => 189,
		"Нальчик" => 48,
		"Элиста" => 194,
		"Новокуйбышевск" => 53,
		"Артем" => 197,
		"Пятигорск" => 171,
		"Ногинск" => 186,
		"Серпухов" => 72,
		"Шахты" => 73,
		"Киров" => 179,
		"Петропавловск-Камчатский" => 111,
		"Камышин" => 20,
		"Назрань" => 49,
		"Электросталь" => 15,
		"Стерлитамак" => 138,
		"Кострома" => 136,
		"Владикавказ" => 124,
		"Нижневартовск" => 145,
		"Якутск" => 202,
		"Смоленск" => 118,
		"Энгельс" => 16,
		"Бийск" => 150,
		"Каменск-Уральский" => 19,
		"Новомосковск" => 174,
		"Набережные Челны" => 12,
		"Нижний Тагил" => 108,
		"Выборг" => 91,
		"Норильск" => 51,
		"Ухта" => 89,
		"Арзамас" => 184,
		"Рыбинск" => 67,
		"Балаково" => 103,
		"Нефтеюганск" => 187,
		"Орехово-Зуево" => 57,
		"Ленинск-Кузнецкий" => 195,
		"Спасск-Дальний" => 221,
		"Кавалерово" => 228,
		"Дальнегорск" => 222,
		"Муром" => 181,
		"Грозный" => 18,
		"Кызыл" => 29,
		"Нефтекамск" => 183,
		"Славянка" => 219,
		"Ольга" => 224,
		"Дальнереченск" => 223,
		"Лесозаводск" => 200,
		"Яковлевка" => 227,
		"Кировский" => 229,
		"Арсеньев" => 217,
		"Рубцовск" => 157,
		"Прокопьевск" => 63,
		"Волгодонск" => 155,
		"Дзержинск" => 139,
		"Северодвинск" => 152,
		"Орск" => 143,
		"Новотроицк" => 192,
		"Салават" => 161,
		"Березники" => 153,
		"Батайск" => 188,
		"Великие Луки" => 193,
		"Армавир" => 119,
		"Хасавюрт" => 23,
		"Елец" => 93,
		"Октябрьский" => 56,
		"Киселевск" => 26,
		"Могилева" => 36,
		"Невиномысск" => 50,
		"Новочебоксарск" => 52,
		"Петергоф" => 61,
		"Пушкин" => 64,
		"Партизанск" => 216,
		"Терней" => 218,
		"Байкальск" => 220,
		"Большой Камень" => 225,
		"Посьет" => 226,
		"Астраханка" => 436,
		"Ливадия" => 437,
		"Украина" => 5,
		"Днепропетровск" => 13,
		"Донецк" => 14,
		"Харьков" => 22,
		"Киев" => 25,
		"Кривой Рог" => 28,
		"Львов" => 31,
		"Мариуполь" => 33,
		"Одесса" => 55,
		"Запорожье" => 95,
		"Житомир" => 97,
		"Симферополь" => 434
	); 
	
	if(!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest'){

		$day = $_GET['day'];
		if (!$day){$day = 2;}
		
		$link = 'http://ipgeobase.ru:7020/geo?ip='.get_ip();
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $link);
		curl_setopt($ch, CURLOPT_HEADER, false);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
		curl_setopt($ch, CURLOPT_TIMEOUT, 3);
		curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 3);
		$string = curl_exec($ch);

		$data = parse_string($string);
		$city = $data['city'];
		
		$id_city="";
		if ($city){
			foreach($arrCity as $key => $value)
			{
			   if ($city == $key){$id_city = $value; break;}
			}
		}
		
		if (!$id_city){$id_city = 37; $city = "Москва";}
		
		$xml_file="http://xml.meteoservice.ru/export/gismeteo/point/".$id_city.".xml"; 

		$xml = file_get_contents($xml_file);
		$dom = new DOMDocument();
		$dom->loadXML($xml);
		$dom->validateOnParse = true;
		$data = $dom->getElementsByTagName('FORECAST');
		$tod = array(0=>"Ночь", 1=>"Утро", 2=>"День", 3=>"Вечер");
		$direction = array(0=>"Северный", 1=>"Северо-восточный", 2=>"Восточный", 3=>"Юго-восточный", 4=>"Южный", 5=>"Юго-западный", 6=>"Западный", 7=>"Северо-западный");
		$cloudiness = array(0=>"Ясно", 1=>"Малооблачно", 2=>"Облачно", 3=>"Пасмурно");
		$precipitation = array(4=>"дождь", 5=>"ливень", 6=>"снег", 7=>"снег", 8=>"гроза", 9=>"нет данных", 10=>"без осадков");

		foreach ($data as $item=>$value){
			$temperature = $value->getElementsByTagName('HEAT')->item(0);
			$phenomena = $value->getElementsByTagName('PHENOMENA')->item(0);
			if ($tod[$value->getAttribute('tod')] == $tod[$day]){
				$temp = $temperature->getAttribute('max');
				$cloud = $cloudiness[$phenomena->getAttribute('cloudiness')];
				$prec = $precipitation[$phenomena->getAttribute('precipitation')];
				$wind = $direction[$value->getElementsByTagName('WIND')->item(0)->getAttribute('direction')];
				$pressure = $value->getElementsByTagName('PRESSURE')->item(0)->getAttribute('max');
				if ($temp < 0){
					$temp = $temperature->getAttribute('min');
				}				
			}
			if ($tod[$value->getAttribute('tod')] == "Ночь"){
				$night_max = $temperature->getAttribute('max');
				if ($night_max < 0){
					$night_max = $temperature->getAttribute('min');
				}
			}	
		}
		if ($temp > 0) {$temp = "<span>+</span>".$temp;} else if ($temp < 0) {$temp = preg_replace ('/\-/', '',$temp); $temp = "&ndash; ".$temp;}
		if ($night_max > 0) {$night_max = '<em class="plus">+</em>'.$night_max;} else if ($night_max < 0) {$night_max = preg_replace ('/\-/', '',$night_max); $night_max = "&ndash; ".$night_max;}
		if ($temp == "-0"){$temp = "0";} if ($night_max == "-0"){$night_max = "0";}
		
		if ($cloud == "Ясно"){$icon = 0;}
		else if ($cloud == "Малооблачно"){$icon = 1;}
		else if ($cloud == "Облачно"){$icon = 2;}
		else if ($cloud == "Пасмурно"){$icon = 2;}
		
		if ($prec == "дождь" || $prec == "ливень"){$icon = 3;}
		else if ($prec == "гроза"){$icon = 4;}
		else if ($prec == "снег"){$icon = 5;}
		if ($cloud == "Малооблачно" && $prec == "снег"){$icon = 6;}
		
		if (strlen($city) > 12 && strlen($city) < 16){$name = "Погода ".$city;}
		else if (strlen($city) > 15){$name = $city;}
		else {$name = "Погода в ".$city;}

		$pogoda = '<h3>'.$name.'</h3><div class="container"><div class="pogoda_show"><div class="temp_now">'.$temp.'<em>°C</em></div><div class="p-icon icon'.$icon.'"></div><div class="cloudiness">'.$cloud.'<br>'.$prec.'</div><div class="temp_night">'.$night_max.'<em>°C</em><span>ночью</span></div><div class="wind">'.$pressure.' мм р.с.<br>'.$wind.'</div></div></div>';

		if ($temp !="" && $night_max !=""){
			print $pogoda;
		}
	}
	
	function parse_string($string)
	{
		$pa['inetnum'] = '#<inetnum>(.*)</inetnum>#is';
		$pa['country'] = '#<country>(.*)</country>#is';
		$pa['city'] = '#<city>(.*)</city>#is';
		$pa['region'] = '#<region>(.*)</region>#is';
		$pa['district'] = '#<district>(.*)</district>#is';
		$pa['lat'] = '#<lat>(.*)</lat>#is';
		$pa['lng'] = '#<lng>(.*)</lng>#is';
		$data = array();
		foreach($pa as $key => $pattern)
		{
			preg_match($pattern, $string, $out);
			if(isset($out[1]) && $out[1])
			$data[$key] = trim($out[1]);
		}
		return $data;
	}	

	function get_ip()
	{
		if (isset($_SERVER['HTTP_X_FORWARDED_FOR']))
			$ip = trim(strtok($_SERVER['HTTP_X_FORWARDED_FOR'], ','));
		
		if (isset($_SERVER['HTTP_CLIENT_IP']))
			$ip = $_SERVER['HTTP_CLIENT_IP'];       
		
		if (isset($_SERVER['REMOTE_ADDR']))
			$ip = $_SERVER['REMOTE_ADDR'];
		
		if (isset($_SERVER['HTTP_X_REAL_IP']))
			$ip = $_SERVER['HTTP_X_REAL_IP'];
		
		return $ip;            
	}

?>