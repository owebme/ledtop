<?php

header("Content-type: text/html; charset=utf-8");

require_once 'db.php';
require_once 'config.php';
require_once 'transport.php';

$api = new Transport();

if ($_GET['order_id'] > 0 && $_GET['sendNumSender'] != "" && $_GET['sendPhone'] != ""){

	$orderID = iconv("UTF-8","WINDOWS-1251", $_GET['order_id']);
	$phone = iconv("UTF-8","WINDOWS-1251", $_GET['sendPhone']);
	$number = iconv("UTF-8","WINDOWS-1251", $_GET['sendNumSender']);	
	if ($_GET['delivered'] == "true"){
		$text = "Ваш заказ на почте! Отправление №".$number." // LEDTOP-SHOP.ru";
	}
	else {
		$text = "Ваш номер отправления ".$number." // Интернет-магазин LEDTOP-SHOP.ru";
	}
	
	$params = array(
		//"source" => "LEDTop-Shop",
		"text" => $text,
		"onlydelivery" => 1 // Платить только за доставленные
		//"use_alfasource" => 1 // СМС приходит с указанием своего source, 80 коп.
	);
	$phones = array($phone);
	$send = $api->send($params,$phones);
	#print_r($send);
	$code=""; $descr=""; $smsid=""; $colSendAbonent=""; $price="";
	foreach ($send as $key => $value){
		if ($key == "code"){$code = $value;}
		if ($key == "descr"){$descr = $value;}
		if ($key == "smsid"){$smsid = $value;}
		if ($key == "colSendAbonent"){$colSendAbonent = $value;}
		if ($key == "price"){$price = $value;}
	}
	$desc = $descr;
	$descr = iconv("UTF-8","WINDOWS-1251", $descr);
	mysql_query("INSERT INTO `cat_orders_sender` (`order_id`, `phone`, `num`, `code`, `descr`, `smsid`, `sms`, `price`, `delivered`, `date_send`) VALUES('".$orderID."', '".$phone."', '".$number."', '".$code."', '".$descr."', '".$smsid."', '".$text."', '".$price."', '".$colSendAbonent."', NOW())");
	
	print $code."|".$desc;
}

if ($_GET['senderDebtors'] == "1"){

	$res_sql = mysql_query("SELECT cat_orders.id, cat_orders.phone, cat_orders.num_dispatch FROM cat_orders WHERE status = '0' AND dispatch = '2' ORDER BY id ASC");
	while ($row = @mysql_fetch_array($res_sql)){
	
		$orderID = $row["id"];
		$phone = $row["phone"];
		$number = $row["num_dispatch"];
		$phone = preg_replace('/\_/si', '', $phone);
		$phone = preg_replace('/\s/si', '', $phone);
		$phone = preg_replace('/\-/si', '', $phone);
		$phone = preg_replace('/\+7/si', '8', $phone);
		$phone = preg_replace('/^7(\d+)/si', '8$1', $phone);
		$phone = preg_replace('/(.+)\,(.+)/si', '$1', $phone);
		
		if ($number != ""){
			$text = "Заберите посылку на почте! Отправление №".$number." // LEDTOP-SHOP.ru";
		}
		else {
			$text = "Уважаемый, пожалуйста заберите посылку на почте! // LEDTOP-SHOP.ru";
		}
		$params = array(
			//"source" => "LEDTop-Shop",
			"text" => $text,
			"onlydelivery" => 1
		);
		$phones = array($phone);
		$send = $api->send($params,$phones);
		#print_r($send);	
		$code=""; $descr=""; $smsid=""; $colSendAbonent=""; $price="";
		foreach ($send as $key => $value){
			if ($key == "code"){$code = $value;}
			if ($key == "descr"){$descr = $value;}
			if ($key == "smsid"){$smsid = $value;}
			if ($key == "colSendAbonent"){$colSendAbonent = $value;}
			if ($key == "price"){$price = $value;}
		}	
		$desc = $descr;
		$descr = iconv("UTF-8","WINDOWS-1251", $descr);
		
		print "<h3>".$orderID." - ".$phone." // ".$desc."</h3>";
		
		mysql_query("INSERT INTO `cat_orders_sender` (`order_id`, `phone`, `num`, `code`, `descr`, `smsid`, `sms`, `price`, `delivered`, `date_send`) VALUES('".$orderID."', '".$phone."', '".$number."', '".$code."', '".$descr."', '".$smsid."', '".$text."', '".$price."', '".$colSendAbonent."', NOW())");
	}
}

?>
