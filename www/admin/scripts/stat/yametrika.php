<?php

require_once 'config.php';

header("Content-type: text/html; charset=windows-1251");

$date = new DateTime();
$date_from = $date->format('Ymd');
$date_to = $date->format('Ymd');	
$period = $_GET['period'];

if ($period == "yesterday"){
	$date = new DateTime();
	$date->modify('-1 day');
	$date_from = $date->format('Ymd');
	$date_to = $date->format('Ymd');
}
else if ($period == "week"){
	$date = new DateTime();
	$date_from = $date->format('Ymd');
	$date->modify('-6 day');
	$date_to = $date->format('Ymd');
}
else if ($period == "month"){
	$date = new DateTime();
	$date_from = $date->format('Ymd');
	$date->modify('-30 day');
	$date_to = $date->format('Ymd');
}	

if ($_GET['method'] == "traffic_summary"){

	// Общая статистика на сегодня
	$response = file_get_contents($metrika_url.'stat/traffic/summary?id='.$client_id.'&date2='.$date_from.'&date1='.$date_to.'&pretty=1&oauth_token='.$token);	

		$xml = new DOMDocument();
		$xml->loadXML($response);
		$data = $xml->getElementsByTagName("totals");	
		foreach ($data as $element){
			foreach ($element->childNodes as $item){
				if ($item->nodeName == "visitors"){
					$visitors = $item->nodeValue;
				}
				if ($item->nodeName == "new_visitors"){
					$new_visitors = $item->nodeValue;
				}			
				if ($item->nodeName == "page_views"){
					$page_views = $item->nodeValue;
				}
			}
		}

	$result .= '<p>Посетителей: <strong style="color:#EC6700">'.(!$visitors?'0':''.$visitors.'').'</strong></p>';
	$result .= '<p>Новых посетителей: <strong style="color:#769B1A">'.($new_visitors > 0?'+<span style="padding-left:2px;">'.$new_visitors.'</span>':'0').'</strong> <span style="color:#666">('.round($new_visitors/$visitors*100).'%)</span></p>';
	$result .= '<p>Просмотров: <strong style="color:#bd3b31">'.(!$page_views?'0':''.$page_views.'').'</strong></p>';
	
	print $result;
}

if ($_GET['method'] == "ecommerce"){

	$date = new DateTime();
	$date_from = $date->format('Ymd');
	$date->modify('-2 day');
	$date_to = $date->format('Ymd');

	// Параметры интернет-магазинов
	$response = file_get_contents($metrika_url.'stat/content/ecommerce?id='.$client_id.'&date2='.$date_from.'&date1='.$date_to.'&goal_id=ORDER&pretty=1&oauth_token='.$token);

	$xml = new DOMDocument();
	$xml->loadXML($response);
	$data = $xml->getElementsByTagName("row");	
	$orders = array();
	foreach ($data as $element){
		$items = array(); $orderID=""; $trafic_source=""; $engine_name="";
		foreach ($element->childNodes as $item){
			if ($item->nodeName == "trafic_source_id"){
				array_push($items, $item->nodeValue);
			}
			else if ($item->nodeName == "engine_id"){
				array_push($items, $item->nodeValue);
			}		
			else if ($item->nodeName == "order_id"){
				$orderID = $item->nodeValue;
			}
			else if ($item->nodeName == "trafic_source_name"){
				$trafic_source = iconv("UTF-8","WINDOWS-1251",$item->nodeValue);
				array_push($items, $trafic_source);
			}
			else if ($item->nodeName == "engine_name"){
				$engine_name = iconv("UTF-8","WINDOWS-1251",$item->nodeValue);
				array_push($items, $engine_name);
			}
		}
		if (!in_array($orderID, $orders)) {
			array_push($orders, $orderID);
			array_push($orders, $items);
		}
	}
	
	require_once 'db.php';
	require_once 'Mobile_Detect.php';
	$detect = new Mobile_Detect;	
		
	$res_sql = mysql_query("SELECT cat_orders.id FROM cat_orders");
	while ($row = @mysql_fetch_array($res_sql)){
		for($i=0; $i < count($orders); $i++){
			if ($row["id"] == $orders[$i]){
				print "<h3>".$row["id"]."</h3>";
				$trafic_id=""; $trafic_source=""; $engine_id=""; $engine_name="";
				for($q=0; $q < count($orders[$i+1]); $q++){
					if ($q == 0){$trafic_id = $orders[$i+1][$q];}
					if ($q == 1){$engine_id = $orders[$i+1][$q];}
					if ($q == 2){$trafic_source = $orders[$i+1][$q];}
					if ($q == 3){$engine_name = $orders[$i+1][$q];}
				}
				
				$userAgent=""; $keyword=""; $referrer="";
				$res_goals = mysql_query("SELECT goals.referrer, goals.user_agent FROM goals WHERE order_id = '".$row["id"]."'");
				while ($goal = @mysql_fetch_array($res_goals)){
					$userAgent = $goal["user_agent"];
					$referrer = $goal["referrer"];
				}
				$detect->setUserAgent($userAgent);
				
				$deviceType = ($detect->isMobile() ? ($detect->isTablet() ? '2' : '1') : '3');	

				$keyword = get_keyword($referrer);

				print $trafic_source." ".$engine_name." ".$keyword."<br>";				
				
				mysql_query("UPDATE cat_orders SET trafic_id = '".$trafic_id."', trafic_source = '".$trafic_source."', engine_id = '".$engine_id."', engine_name = '".$engine_name."', keyword = '".$keyword."', type_device = '".$deviceType."' WHERE id = ".$row["id"]."");
			}
		}
	}	
}

function get_keyword($referrer){
	$keyword="";
	if (preg_match("/yandex/i", $referrer)){
		preg_match("/text=(.+?)(&?)(.*?)/Uis", $referrer, $maches);
		$keyword = $maches[1];
		$keyword = preg_replace('/&(.+)/', '', $keyword); 
		$keyword = iconv("UTF-8","WINDOWS-1251",urldecode($keyword));
	}
	else if (preg_match("/google/i", $referrer) && !preg_match("/q=&/i", $referrer)){
		preg_match("/q=(.+?)/Uis", $referrer, $maches);
		$keyword = $maches[1];	
		$keyword = preg_replace('/&(.+)/', '', $keyword);
		$keyword = iconv("UTF-8","WINDOWS-1251",urldecode($keyword));
	}
	else if (preg_match("/go.mail.ru/i", $referrer)){
		preg_match("/q=(.+?)/Uis", $referrer, $maches);
		$keyword = $maches[1];	
		$keyword = preg_replace('/&(.+)/', '', $keyword);
		$keyword = iconv("UTF-8","WINDOWS-1251",urldecode($keyword));
	}	
	if ($keyword){
		return $keyword;
	}
}

?>