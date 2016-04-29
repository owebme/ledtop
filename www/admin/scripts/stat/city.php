<?php

require_once 'config.php';
require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");
		
$res_sql = mysql_query("SELECT goals.id, goals.ip, goals.city FROM goals");
while ($row = @mysql_fetch_array($res_sql)){
	if ($row["city"] == "" && $row["ip"]){
		$ip = trim(strtok($row["ip"], ','));
		$city = get_city($ip);
		if ($city){
			print $city."<br>";
			mysql_query("UPDATE goals SET city = '".$city."' WHERE id = ".$row["id"]."");
		}
	}
}

function get_city($ip){
	$link = 'http://ipgeobase.ru:7020/geo?ip='.$ip;
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
	if (!$city){
		$city = $data['country'];
	}
	if ($city){
		return $city;
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

?>