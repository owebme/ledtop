<?php

require_once 'config.php';

header("Content-type: text/html; charset=windows-1251");

$domen = $_SERVER['HTTP_HOST'];

require_once 'db.php';
require_once 'Mobile_Detect.php';
$detect = new Mobile_Detect;	
		
	$res_sql = mysql_query("SELECT id FROM cat_orders ORDER BY id DESC".($_GET['lastOrder'] == "true"?" LIMIT 1":"")."");
	while ($row = @mysql_fetch_array($res_sql)){
	
		print "<h3>".$row["id"]."</h3>";
		
		$userAgent=""; $start_title=""; $source=""; $keyword=""; $referrer="";
		$res_goals = mysql_query("SELECT start_url, referrer, user_agent FROM goals WHERE order_id = '".$row["id"]."'");
		while ($goal = @mysql_fetch_array($res_goals)){
			$userAgent = $goal["user_agent"];
			$start_url = $goal["start_url"];
			$referrer = $goal["referrer"];
		}
		$detect->setUserAgent($userAgent);
		
		$deviceType = ($detect->isMobile() ? ($detect->isTablet() ? '2' : '1') : '3');	
		
		$start_title = '<a target="_blank" href="'.$start_url.'">'.getStartSection($start_url).'</a>';
		
		$source = getSource($referrer);
		
		$keyword = getKeyword($referrer);

		print $start_title." // ".$source." // <strong>".$keyword."</strong><br>";				
		
		mysql_query("UPDATE cat_orders SET start_title = '".$start_title."', trafic_source = '".$source."'".($keyword?" , keyword = '".$keyword."'":"")." , type_device = '".$deviceType."' WHERE id = ".$row["id"]."");
	}

function getStartSection($url){
	$section="";
	if (preg_match("/catalog\/search/i", $url)){
		$section = "Поиск на сайте";
	}
	else if (preg_match("/catalog\/filter/i", $url)){
		$section = "Поиск по параметрам на сайте";
	}
	else if (preg_match("/catalog/i", $url)){
		preg_match_all('%catalog/(.+)$%', $url, $result);
		$link = trim($result[1][0]);
		$link = preg_replace('/\?(.+)$/', '', $link); 
		$res = mysql_query("SELECT c_name FROM cat_category WHERE c_alias = '".$link."'");
		while ($row = @mysql_fetch_array($res)){
			$section = $row["c_name"];
		}
	}
	else if (preg_match("/products/i", $url)){
		preg_match_all('%products/(\d+)/%', $url, $result);
		$link = trim($result[1][0]);
		$res = mysql_query("SELECT p_name FROM cat_product WHERE p_art = '".$link."'");
		while ($row = @mysql_fetch_array($res)){
			$section = $row["p_name"];
		}		
	}
	else if (preg_match("/pages/i", $url)){
		preg_match_all('%pages/(.+)$%', $url, $result);
		$link = trim($result[1][0]);
		$res = mysql_query("SELECT name FROM strukture WHERE alias = '".$link."'");
		while ($row = @mysql_fetch_array($res)){
			$section = $row["name"];
		}		
	}
	else if (preg_match("/news/i", $url)){
		preg_match_all('%news/(.+)$%', $url, $result);
		$link = trim($result[1][0]);
		$res = mysql_query("SELECT name FROM news WHERE alias = '".$link."'");
		while ($row = @mysql_fetch_array($res)){
			$section = $row["name"];
		}	
		if (!$section){
			$section = 'Раздел новостей';
		}
	}
	else if (preg_match("/poleznoe/i", $url)){
		$section = 'Раздел полезное';	
	}	
	else {
		$section = 'Главная страница';
	}
	
	return $section;
}
	
function getSource($referrer){
	$source="";
	if (preg_match("/yandex.ru\/clck/i", $referrer) or preg_match("/clck.yandex.ru/i", $referrer)){
		$source = "Яндекс, результаты поиска";
	}
	else if (preg_match("/yandex.ru\/yandsearch/i", $referrer) or preg_match("/yandex.ru\/touchsearch/i", $referrer) or preg_match("/yandex.ru\/msearch/i", $referrer)){
		$source = "Яндекс.Директ, переход по рекламе";
	}
	else if (preg_match("/google.ru\/search/i", $referrer)){
		$source = "Google, результаты поиска";
	}
	else if (preg_match("/google.com\/uds/i", $referrer) or preg_match("/google.ru\/aclk/i", $referrer)){
		$source = "Google.Adwords, переход по рекламе";
	}	
	else if (preg_match("/go.mail.ru/i", $referrer)){
		$source = "Mail.ru, результаты поиска";
	}
	else if (preg_match("/rambler.ru/i", $referrer)){
		$source = "Rambler.ru, результаты поиска";
	}
	else if (preg_match("/bing/i", $referrer)){
		$source = "Bing.com, результаты поиска";
	}
	else if (preg_match("/yandex./i", $referrer)){
		$source = "Яндекс, результаты поиска";
	}
	else if (preg_match("/google./i", $referrer)){
		$source = "Google, результаты поиска";
	}	
	if (!$source && preg_match("%ledtop-shop.ru%i", $referrer)){
		$source = "Прямой заход на сайт";
	}
	if (!$source){
		preg_match_all('%http://(.+)(/)?$%', $referrer, $result);
		$link = trim($result[1][0]);		
		$source = 'Переход с сайта <a target="_blank" href="'.$referrer.'">'.$link.'</a>';
	}	
	if ($source){
		return $source;
	}
}	

function getKeyword($referrer){
	$keyword="";
	if (preg_match("/yandex/i", $referrer)){
		preg_match("/text=(.+)/", $referrer, $maches);
		$keyword = $maches[1];
	}
	else if (preg_match("/google/i", $referrer) && !preg_match("/q=&/i", $referrer)){
		preg_match("/q=(.+?)/Uis", $referrer, $maches);
		$keyword = $maches[1];
	}
	else if (preg_match("/go.mail.ru/i", $referrer)){
		preg_match("/q=(.+?)/Uis", $referrer, $maches);
		$keyword = $maches[1];
	}
	else if (preg_match("/rambler.ru/i", $referrer)){
		preg_match("/query=(.+?)/Uis", $referrer, $maches);
		$keyword = $maches[1];
	}	
	if (!$keyword){
		if (preg_match("/utm_term=/i", $referrer)){
			preg_match("/utm_term=(.+?)/Uis", $referrer, $maches);
			$keyword = $maches[1];
		}
		if (preg_match("/keyword=/i", $referrer)){
			preg_match("/keyword=(.+?)/Uis", $referrer, $maches);
			$keyword = $maches[1];
		}
	}	
	if ($keyword){
		$keyword = preg_replace('/&(.+)/', '', $keyword);
		$keyword = iconv("UTF-8","WINDOWS-1251",urldecode($keyword));	
		return $keyword;
	}
}

?>