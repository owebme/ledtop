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
		"��������" => 4,
		"�������" => 9,
		"�����" => 34,
		"�������" => 35,
		"����" => 58,
		"���������" => 2,
		"������" => 6,
		"������" => 2,
		"�����" => 215,
		"������" => 1,
		"������" => 37,
		"����" => 115,
		"��������" => 127,
		"����������" => 101,
		"�����" => 59,
		"����" => 121,
		"�����-���������" => 69,
		"���������" => 199,
		"����������" => 147,
		"������" => 125,
		"���������" => 21,
		"�����������" => 4,
		"�������" => 132,
		"�����������" => 99,
		"������" => 104,
		"������" => 185,
		"�����" => 107,
		"��������" => 112,
		"�����" => 102,
		"������" => 156,
		"�������" => 149,
		"��������" => 167,
		"����" => 116,
		"������" => 65,
		"���������" => 90,
		"�����" => 169,
		"���������" => 92,
		"�������" => 129,
		"��������" => 86,
		"������������" => 178,
		"����������" => 146,
		"������������" => 60,
		"���������" => 10,
		"������������" => 154,
		"���������" => 32,
		"�������" => 191,
		"���������" => 5,
		"������" => 130,
		"�����������" => 105,
		"�������" => 100,
		"�������" => 85,
		"�����������-��-�����" => 27,
		"����-���" => 109,
		"���������" => 11,
		"�����������" => 98,
		"�������" => 144,
		"�������" => 196,
		"����" => 177,
		"������������" => 122,
		"�������" => 160,
		"�������" => 168,
		"�������" => 163,
		"������ ��������" => 120,
		"������" => 141,
		"������� �����" => 71,
		"������" => 164,
		"���������" => 162,
		"���������" => 201,
		"����������" => 180,
		"������" => 182,
		"����" => 128,
		"������������" => 137,
		"���" => 140,
		"�������" => 166,
		"������" => 133,
		"����������" => 75,
		"��������" => 113,
		"���������" => 198,
		"�������" => 148,
		"������-��-����" => 135,
		"�����" => 159,
		"����-���������" => 94,
		"������ �����" => 74,
		"������" => 173,
		"������" => 47,
		"�����" => 175,
		"�������" => 190,
		"�����" => 87,
		"��������" => 176,
		"��������" => 123,
		"������������" => 8,
		"������-���" => 142,
		"��������" => 134,
		"������" => 158,
		"���������" => 126,
		"�����������" => 3,
		"������������" => 54,
		"�����" => 24,
		"������" => 486,
		"��������" => 172,
		"�������" => 30,
		"��������" => 7,
		"�������" => 170,
		"�������" => 70,
		"���������������" => 96,
		"�����������" => 165,
		"��������" => 62,
		"������" => 114,
		"������������" => 106,
		"������� ��������" => 151,
		"������" => 110,
		"��������" => 117,
		"������" => 88,
		"���������" => 84,
		"��������" => 189,
		"�������" => 48,
		"������" => 194,
		"��������������" => 53,
		"�����" => 197,
		"���������" => 171,
		"�������" => 186,
		"��������" => 72,
		"�����" => 73,
		"�����" => 179,
		"�������������-����������" => 111,
		"�������" => 20,
		"�������" => 49,
		"������������" => 15,
		"�����������" => 138,
		"��������" => 136,
		"�����������" => 124,
		"�������������" => 145,
		"������" => 202,
		"��������" => 118,
		"�������" => 16,
		"�����" => 150,
		"�������-���������" => 19,
		"������������" => 174,
		"���������� �����" => 12,
		"������ �����" => 108,
		"������" => 91,
		"��������" => 51,
		"����" => 89,
		"�������" => 184,
		"�������" => 67,
		"��������" => 103,
		"�����������" => 187,
		"�������-�����" => 57,
		"�������-���������" => 195,
		"������-�������" => 221,
		"����������" => 228,
		"�����������" => 222,
		"�����" => 181,
		"�������" => 18,
		"�����" => 29,
		"����������" => 183,
		"��������" => 219,
		"�����" => 224,
		"�������������" => 223,
		"�����������" => 200,
		"���������" => 227,
		"���������" => 229,
		"��������" => 217,
		"��������" => 157,
		"�����������" => 63,
		"����������" => 155,
		"���������" => 139,
		"������������" => 152,
		"����" => 143,
		"����������" => 192,
		"�������" => 161,
		"���������" => 153,
		"�������" => 188,
		"������� ����" => 193,
		"�������" => 119,
		"��������" => 23,
		"����" => 93,
		"�����������" => 56,
		"���������" => 26,
		"��������" => 36,
		"�����������" => 50,
		"��������������" => 52,
		"��������" => 61,
		"������" => 64,
		"����������" => 216,
		"������" => 218,
		"���������" => 220,
		"������� ������" => 225,
		"������" => 226,
		"����������" => 436,
		"�������" => 437,
		"�������" => 5,
		"��������������" => 13,
		"������" => 14,
		"�������" => 22,
		"����" => 25,
		"������ ���" => 28,
		"�����" => 31,
		"���������" => 33,
		"������" => 55,
		"���������" => 95,
		"�������" => 97,
		"�����������" => 434
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
		
		if (!$id_city){$id_city = 37; $city = "������";}
		
		$xml_file="http://xml.meteoservice.ru/export/gismeteo/point/".$id_city.".xml"; 

		$xml = file_get_contents($xml_file);
		$dom = new DOMDocument();
		$dom->loadXML($xml);
		$dom->validateOnParse = true;
		$data = $dom->getElementsByTagName('FORECAST');
		$tod = array(0=>"����", 1=>"����", 2=>"����", 3=>"�����");
		$direction = array(0=>"��������", 1=>"������-���������", 2=>"���������", 3=>"���-���������", 4=>"�����", 5=>"���-��������", 6=>"��������", 7=>"������-��������");
		$cloudiness = array(0=>"����", 1=>"�����������", 2=>"�������", 3=>"��������");
		$precipitation = array(4=>"�����", 5=>"������", 6=>"����", 7=>"����", 8=>"�����", 9=>"��� ������", 10=>"��� �������");

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
			if ($tod[$value->getAttribute('tod')] == "����"){
				$night_max = $temperature->getAttribute('max');
				if ($night_max < 0){
					$night_max = $temperature->getAttribute('min');
				}
			}	
		}
		if ($temp > 0) {$temp = "<span>+</span>".$temp;} else if ($temp < 0) {$temp = preg_replace ('/\-/', '',$temp); $temp = "&ndash; ".$temp;}
		if ($night_max > 0) {$night_max = '<em class="plus">+</em>'.$night_max;} else if ($night_max < 0) {$night_max = preg_replace ('/\-/', '',$night_max); $night_max = "&ndash; ".$night_max;}
		if ($temp == "-0"){$temp = "0";} if ($night_max == "-0"){$night_max = "0";}
		
		if ($cloud == "����"){$icon = 0;}
		else if ($cloud == "�����������"){$icon = 1;}
		else if ($cloud == "�������"){$icon = 2;}
		else if ($cloud == "��������"){$icon = 2;}
		
		if ($prec == "�����" || $prec == "������"){$icon = 3;}
		else if ($prec == "�����"){$icon = 4;}
		else if ($prec == "����"){$icon = 5;}
		if ($cloud == "�����������" && $prec == "����"){$icon = 6;}
		
		if (strlen($city) > 12 && strlen($city) < 16){$name = "������ ".$city;}
		else if (strlen($city) > 15){$name = $city;}
		else {$name = "������ � ".$city;}

		$pogoda = '<h3>'.$name.'</h3><div class="container"><div class="pogoda_show"><div class="temp_now">'.$temp.'<em>�C</em></div><div class="p-icon icon'.$icon.'"></div><div class="cloudiness">'.$cloud.'<br>'.$prec.'</div><div class="temp_night">'.$night_max.'<em>�C</em><span>�����</span></div><div class="wind">'.$pressure.' �� �.�.<br>'.$wind.'</div></div></div>';

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