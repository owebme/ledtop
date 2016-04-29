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
			header('HTTP/1.1 301 Moved Permanently');
			header('Location: /admin/');
			exit();
		}
	}
}
else {
	header('HTTP/1.1 301 Moved Permanently');
	header('Location: /admin/');
	exit();
}
	
	require_once 'db.php';
	
	if (isset($_GET['type']) && $_GET['type'] != ""){

		$titles = array("id", "Категория[id]", "Артикул", "Название", "Цена", "Цена от 3 до 10", "Цена от 10", "Цена закупки", "Количество", "Краткое описание", "Показывать", "Удалить");
		
		$type = $_GET['type'];
		$data = array(); $c_alias="";
		$res_sql = mysql_query("SELECT p.*, c.c_name, c.c_alias, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_main = '1' ".($type > 0?"AND pl.cat_id = '".$type."'":"")." ORDER BY c.c_pos ASC, pl.p_pos ASC");
		while ($row = @mysql_fetch_array($res_sql)){
			$desc_sm = $row["p_desc_sm"];
			$desc_sm = preg_replace("%&amp;%si", "&", $desc_sm);
			$desc_sm = preg_replace("%&quot;%si", "\"", $desc_sm);
			$desc_sm = preg_replace("%&nbsp;%si", " ", $desc_sm);
			$desc_sm = preg_replace("%&gt;%si", ">", $desc_sm);
			$desc_sm = preg_replace("%&lt;%si", "<", $desc_sm);
			$line = array($row["p_id"], trim($row["c_name"])."[".$row["cat_id"]."]", trim($row["p_art"]), trim($row["p_name"]), $row["p_price"], $row["p_price_from3"], $row["p_price_from10"], $row["p_price_cost"], $row["p_count"], trim($desc_sm), $row["p_show"]);
			array_push($data, $line);
			if ($type > 0){$c_alias = $row["c_alias"];}
		}
			
		$date = new DateTime();	
		download_send_headers($_SERVER['HTTP_HOST'].'_'.($c_alias?''.$c_alias.'_':'').''.$date->format('Y-m-d').'.csv');
		echo arrayCSV($data, $titles);
		die();
	}

function download_send_headers($filename) {
	// disable caching
	$now = gmdate("D, d M Y H:i:s");
	header("Expires: Sun, 20 Apr 2014 06:00:00 GMT");
	header("Cache-Control: max-age=0, no-cache, must-revalidate, proxy-revalidate");
	header("Last-Modified: {$now} GMT");

	// force download
	header("Content-Type: application/force-download");
	header("Content-Type: application/octet-stream");
	header("Content-Type: application/download");

	// disposition / encoding on response body
	header("Content-Disposition: attachment;filename={$filename}");
	header("Content-Transfer-Encoding: binary");
}

function arrayCSV(array &$array, $titles) {
	if (count($array) == 0) {
		return null;
	}
	ob_start();
	$df = fopen("php://output", 'w');
	fputcsv($df, $titles, ';');
	foreach ($array as $row) {
		fputcsv($df, $row, ';');
	}
	fclose($df);
	return ob_get_clean();
}

?>