<?php

require_once 'config.php';

header("Content-type: text/html; charset=windows-1251");

// Подключение и инициализация класса
require_once 'Mobile_Detect.php';
$detect = new Mobile_Detect;

$filename='orders.txt'; 
$lines = array(); 
$file = fopen($filename, 'r');

$items = array(); 
while(!feof($file)) { 
    $lines = fgets($file, 4096); 
	$line = explode('|',$lines);
	$items[$line[0]] = $line[1];
}

require_once 'db.php';

$res_sql = mysql_query("SELECT cat_orders.id FROM cat_orders");
while ($row = @mysql_fetch_array($res_sql)){
	$userAgent="";
	$userAgent = $items[$row["id"]];
	if ($userAgent){
		$detect->setUserAgent($userAgent);
		
		$deviceType = ($detect->isMobile() ? ($detect->isTablet() ? '2' : '1') : '3');		

		print "<h3>".$row["id"]."</h3>";
		print $deviceType."<br>";				
		
		mysql_query("UPDATE cat_orders SET type_device = '".$deviceType."' WHERE id = ".$row["id"]."");
	}
}	

?>