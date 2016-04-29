<?php

set_time_limit(600);

require_once 'config.php';

header("Content-type: text/html; charset=windows-1251");

$period = $_GET['period'];
if (!$period){$period = "today";}

$date = new DateTime();
$date_from = $date->format('Y-m-d');
$date_to = $date->format('Y-m-d');
if ($period == "yesterday"){
	$date = new DateTime();
	$date->modify('-1 day');
	$date_from = $date->format('Y-m-d');
	$date_to = $date->format('Y-m-d');
}
else if ($period == "week"){
	$date = new DateTime();
	$date_from = $date->format('Y-m-d');
	$date->modify('-6 day');
	$date_to = $date->format('Y-m-d');
}
else if ($period == "2week"){
	$date = new DateTime();
	$date_from = $date->format('Y-m-d');
	$date->modify('-14 day');
	$date_to = $date->format('Y-m-d');
}
else if ($period == "month"){
	$date = new DateTime();
	$date_from = $date->format('Y-m-d');
	$date->modify('-30 day');
	$date_to = $date->format('Y-m-d');
}

if (isset($_GET['getExpense']) && $_GET['getExpense'] != ""){
	
	print GetExpense($direct_url, $direct_login, $token, $date_from, $date_to);
}

if (isset($_GET['getCampaignsStat']) && $_GET['getCampaignsStat'] != ""){
	
	print GetCampaignsStat($direct_url, $direct_login, $token, $date_from, $date_to, $period);
}

if (isset($_GET['getCampaignsList']) && $_GET['getCampaignsList'] != ""){

	$data = GetCampaignsList($direct_url, $direct_login, $token);
	$json = json_decode($data);	
	$count = sizeof($json->{'data'});
	$result="";
	for($i=0; $i<$count; $i++){
		$result .='<p'.(iconv("UTF-8","WINDOWS-1251", $json->{'data'}[$i]->{'Status'}) != 'Идут показы'?' class="hide"':'').'><span>'.iconv("UTF-8","WINDOWS-1251", $json->{'data'}[$i]->{'Name'}).'</span> &mdash; <strong>'.$json->{'data'}[$i]->{'Rest'}.' у.е.</strong></p>';
	}
	print $result;
}

function GetCampaignsList($direct_url, $direct_login, $token){

	$request = array(
		"method" => "GetCampaignsList",
		"param" => array(
		  $direct_login
		),
		"locale" => "ru",
		"token" => $token
	);
	$request = json_encode($request);
	$additionalHeaders = array('Content-Length: ' . strlen($request), 'Content-Type: application/json; charset=utf-8');
	$response = GetData($direct_url, $request, $additionalHeaders);
	
	return $response;	
}

function GetBanners($ids, $direct_url, $token){

	$request = array(
		"method" => "GetBanners",
		"param" => array(
		  "CampaignIDS" => $ids
		),
		"locale" => "ru",
		"token" => $token 
	);
	$request = json_encode($request);
	$additionalHeaders = array('Content-Length: ' . strlen($request), 'Content-Type: application/json; charset=utf-8');
	$response = GetData($direct_url, $request, $additionalHeaders);
	
	return $response;	
}

function GetSummaryStat($ids, $date_from, $date_to, $direct_url, $token){

	$request = array(
		"method" => "GetSummaryStat",
		"param" => array(
		  "CampaignIDS" => $ids,
		  "StartDate" => $date_to,
		  "EndDate" => $date_from
		),
		"locale" => "ru",
		"token" => $token 
	);
	$request = json_encode($request);
	$additionalHeaders = array('Content-Length: ' . strlen($request), 'Content-Type: application/json; charset=utf-8');
	$response = GetData($direct_url, $request, $additionalHeaders);
	
	return $response;	
}

function GetExpense($direct_url, $direct_login, $token, $date_from, $date_to){

	$data = GetCampaignsList($direct_url, $direct_login, $token);
	$json = json_decode($data);	
	$count = sizeof($json->{'data'});
	$ids = array();
	for($i=0; $i<$count; $i++){
		array_push($ids, $json->{'data'}[$i]->{'CampaignID'});
	}
	
	$data = GetSummaryStat($ids, $date_from, $date_to, $direct_url, $token);
	$json = json_decode($data);	
	$count = sizeof($json->{'data'});
	$expense="";
	for($i=0; $i<$count; $i++){
		$expense += $json->{'data'}[$i]->{'SumSearch'}; // Стоимость кликов с поиска
		$expense += $json->{'data'}[$i]->{'SumContext'}; // Стоимость кликов с РСЯ
	}
	
	if ($expense > 0){
		$expense = $expense*30;
		$expense = round($expense, 0);
		return $expense;
	}
}

function GetCampaignsStat($direct_url, $direct_login, $token, $date_from, $date_to, $period){

	$data = GetCampaignsList($direct_url, $direct_login, $token);
	$json = json_decode($data);	
	$count = sizeof($json->{'data'});
	$campaigns = array(); $ids = array();
	for($i=0; $i<$count; $i++){
		$id = $json->{'data'}[$i]->{'CampaignID'};
		$name = $json->{'data'}[$i]->{'Name'};
		$status = 0;
		if (iconv("UTF-8","WINDOWS-1251", $json->{'data'}[$i]->{'Status'}) == 'Идут показы'){
			$status = 1;
		}
		$result = GetBanners(array($id), $direct_url, $token);
		$json_result = json_decode($result);	
		$counts = sizeof($json_result->{'data'});
		for($j=0; $j<$counts; $j++){
			$href = $json_result->{'data'}[$j]->{'Href'};
			if (preg_match("/utm_campaign/i", $href)){
				$href = preg_replace("'.*utm_campaign=(.*?)'si", "$1", $href);
				$href = preg_replace("'(.*?)\&.*'si", "$1", $href);
				if ($href){
					$campaigns[$id] = array($status, $name, $href);
					break;
				}
			}
		}
		array_push($ids, $id);
	}
	
	$expense="";
	$data = GetSummaryStat($ids, $date_from, $date_to, $direct_url, $token);
	$json = json_decode($data);	
	$count = sizeof($json->{'data'});
	$SumSearch=""; $ClicksSearch=""; $SumContext=""; $ClicksContext="";
	for($i=0; $i<$count; $i++){
		if ($json->{'data'}[$i]->{'CampaignID'} != $id && $i > 0 && $campaigns[$id]){
			array_push($campaigns[$id], round($SumSearch*30, 0));
			array_push($campaigns[$id], $ClicksSearch);
			array_push($campaigns[$id], round($SumContext*30, 0));
			array_push($campaigns[$id], $ClicksContext);
			$SumSearch=""; $ClicksSearch=""; $SumContext=""; $ClicksContext="";
		}
		$id = $json->{'data'}[$i]->{'CampaignID'};
		$SumSearch += $json->{'data'}[$i]->{'SumSearch'};
		$SumContext += $json->{'data'}[$i]->{'SumContext'};
		$ClicksSearch += $json->{'data'}[$i]->{'ClicksSearch'};
		$ClicksContext += $json->{'data'}[$i]->{'ClicksContext'};
		if ($SumSearch > 0 or $SumContext > 0){
			$expense = 1;
		}
	}	
	
	require_once 'db.php';
	
	if (sizeof($campaigns) > 0 && $expense && $period){
	
		$sql = "DATE_FORMAT(date_goal, '%Y%m%d') = DATE_FORMAT(NOW(), '%Y%m%d')";
		if ($period == "today"){
			mysql_query("DELETE FROM stat_campaigns WHERE period = '".$period."'");
		}
		if ($period == "yesterday"){
			mysql_query("DELETE FROM stat_campaigns WHERE period = '".$period."'");
			$sql = "DATE_FORMAT(date_goal, '%Y%m%d') = DATE_FORMAT(DATE_ADD(NOW(), interval -1 day), '%Y%m%d')";
		}
		if ($period == "week"){
			mysql_query("DELETE FROM stat_campaigns WHERE period = '".$period."'");
			$sql = "date_goal > NOW() - INTERVAL 6 DAY";
		}
		if ($period == "2week"){
			mysql_query("DELETE FROM stat_campaigns WHERE period = '".$period."'");
			$sql = "date_goal > NOW() - INTERVAL 13 DAY";
		}
		if ($period == "month"){
			mysql_query("DELETE FROM stat_campaigns WHERE period = '".$period."'");
			$sql = "date_goal > NOW() - INTERVAL 30 DAY";
		}		
		$result=""; $arr_goals = array();
		$res_sql = mysql_query("SELECT goals.id, goals.start_url FROM goals WHERE ".$sql);
		while ($row = @mysql_fetch_array($res_sql)){
			$href = $row["start_url"];
			if (preg_match("/utm_campaign/i", $href)){
				$href = preg_replace("'.*utm_campaign=(.*?)'si", "$1", $href);
				$href = preg_replace("'(.*?)\&.*'si", "$1", $href);
				if ($arr_goals[$href]){
					array_push($arr_goals[$href], $row["id"]);
				}
				else {
					$arr_goals[$href] = array($row["id"]);
				}
			}
		}
		foreach ($campaigns as $key => $value){
			$goals=""; $phone=""; $basket=""; $orders=""; $coming=""; $profit="";
			$active = cp1251($value[0]);
			$name = cp1251($value[1]);
			$utm = cp1251($value[2]);
			$price_search = cp1251($value[3]);
			$click_search = cp1251($value[4]);
			$price_context = cp1251($value[5]);
			$click_context = cp1251($value[6]);
			if ($arr_goals[$utm] && ($click_search or $click_context)){
				$ids=""; $num="";
				$goals += sizeof($arr_goals[$utm]);
				foreach ($arr_goals[$utm] as $id){
					$num++; $ids .= $id;
					if ($num != $goals){$ids .=',';}
				}
				$res_sql = mysql_query("SELECT goals.goal, goals.order_id FROM goals WHERE id IN (".$ids.")");
				while ($row = @mysql_fetch_array($res_sql)){
					if ($row["goal"] == "PHONE"){$phone++;}
					if ($row["goal"] == "BASKET"){$basket++;}
					if ($row["goal"] == "ORDER"){
						$orders++;
						$res_order = mysql_query("SELECT cat_orders.total FROM cat_orders WHERE id = '".$row["order_id"]."' LIMIT 1");
						while ($order = @mysql_fetch_array($res_order)){
							$coming += $order["total"];
						}
						$res_product_order = mysql_query("SELECT * FROM cat_orders_product WHERE order_id = '".$row["order_id"]."'");
						while ($product = @mysql_fetch_array($res_product_order)){
							$price_cost="";
							$res_price_cost = mysql_query("SELECT cat_product.p_price_cost FROM cat_product WHERE p_id = '".$product["p_id"]."'");
							while ($cost = @mysql_fetch_array($res_price_cost)){
								$price_cost = $cost["p_price_cost"];
							}
							$profit += ($product["p_price"]-$price_cost)*$product["p_count"];
						}						
					}
				}
			}		
			
			mysql_query("INSERT INTO `stat_campaigns` (`id`, `name`, `utm`, `price_search`, `click_search`, `price_context`, `click_context`, `goals`, `phone`, `basket`, `orders`, `coming`, `profit`, `active`, `period`, `date_update`) VALUES('".$key."', '".$name."', '".$utm."', '".$price_search."', '".$click_search."', '".$price_context."', '".$click_context."', '".$goals."', '".$phone."', '".$basket."', '".$orders."', '".$coming."', '".$profit."', '".$active."', '".$period."', NOW())");
			
			if (!$goals){$goals = 0;}
			if (!$phone){$phone = 0;}
			if (!$basket){$basket = 0;}
			if (!$orders){$orders = 0;}
			if (!$coming){$coming = 0;}
			if (!$price_search){$price_search = 0;}			
			$result .= $name.' - '.$goals.' | '.$phone.' | '.$basket.' | '.$orders.' - '.$coming.' руб. | '.$price_search.' руб.<br>';
		}
		return $result;
	}
}

function GetData($url, $request, $additionalHeaders){

	$headers = array(
		'Host: api.direct.yandex.ru'
	);
	$headers = array_merge($headers, $additionalHeaders);
	$curl = curl_init();
	curl_setopt($curl, CURLOPT_URL, $url);
	curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
	curl_setopt($curl, CURLOPT_POSTFIELDS, $request);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
	$response = curl_exec($curl);
	curl_close($curl);
	
	return $response;
}

function cp1251($data){
	if ($data){
		$data = iconv("UTF-8","WINDOWS-1251", $data);
	}
	return $data;
}

?>