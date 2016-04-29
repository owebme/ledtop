<?php

header("Content-type: text/html; charset=windows-1251");
setlocale(LC_ALL, "ru_RU.cp1251");

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

	$makets = fopen($path."admin/layouts/set_maket", "r");
	while (!feof($makets)) {                       
		$buffer = fgets($makets, 4096);
		list($maket_page, $maket_article, $maket_news, $maket_gallery, $maket_catalog, $maket_product, $maket_product_compare, $maket_basket, $maket_private) = preg_split("%\|%",$buffer);
		$maket = $maket_product;
	}
	fclose($makets);

	require_once 'db.php';

if(!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest'){
	if ($_FILES['file']['name']){

		$file_name = iconv("UTF-8","WINDOWS-1251",$_FILES['file']['name']);
		preg_match('/(.*)\.csv$/', $file_name, $matches); 
		if ($matches){
			$get_csv = getCSV($_FILES['file']['tmp_name']);
			$num="";
			foreach ($get_csv as $value) {				
				if ($value[0] == "id") {continue;}
				if ($value[1] != ""){
					$num += saveField(trim($value[0]), trim($value[1]), trim($value[2]), trim($value[3]), trim($value[4]), trim($value[5]), trim($value[6]), trim($value[7]), trim($value[8]), trim($value[9]), trim($value[10]), trim($value[11]), $maket);
				}
			}
			if (!$num){$num = 0;}
			
			print $num;
			
			if ($num > 0){
				if (is_dir($path."cache")){
					if ($files = glob($path."cache/*")) {
					   foreach($files as $file) {
							unlink($file);
					   }
					}				
				}
			}
		}
	}	
}

function saveField($id, $category, $art, $name, $price, $price_from3, $price_from10, $price_cost, $count, $desc_sm, $show, $delete, $maket){
	$cat_id="";
	preg_match('/(.*)\[(\d+)\]$/', $category, $matches); 
	$c_id = $matches[2];
	$res_category = mysql_query("SELECT cat_category.c_id FROM cat_category WHERE c_id = '".$c_id."' LIMIT 1");
	while ($row = @mysql_fetch_array($res_category)){
		$cat_id = $row["c_id"];
	}
	if ($cat_id > 0 && $name != ""){
		if ($delete != 1){
			$update="";
			if ($id > 0){
				$res_product = mysql_query("SELECT cat_product.p_id FROM cat_product WHERE p_id = '".$id."' LIMIT 1");
				while ($row = @mysql_fetch_array($res_product)){
					if ($row["p_id"] == $id){						
						// Обновление информации о товаре
						mysql_query("UPDATE cat_product SET `p_art`='".$art."', `p_name`='".$name."', `p_price`='".$price."', `p_price_from3`=".($price_from3 > 0?"'".$price_from3."'":"NULL").", `p_price_from10`=".($price_from10 > 0?"'".$price_from10."'":"NULL").", `p_price_cost`=".($price_cost > 0?"'".$price_cost."'":"NULL").", `p_count`=".($count > 0?"'".$count."'":"NULL").", `p_desc_sm`='".$desc_sm."', `p_show`='".($show == ""?"1":"".$show."")."' WHERE p_id='".$id."' LIMIT 1");
						$update = true;
					}
				}
			}
			if (!$update){
				// Добавление нового товара
				$id=""; $pos="";
				$res_id = mysql_query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1");
				while ($res = @mysql_fetch_array($res_id)){
					$id = $res["p_id"]+1;
				}
				if (!$id){$id = 1;}
				if (!$maket){$maket = 1;}
				mysql_query("INSERT INTO `cat_product` (`p_id`, `p_name`, `p_price`, `p_price_from3`, `p_price_from10`, `p_price_old`, `p_count`, `p_hit`, `p_spec`, `p_news`, `p_art`, `p_desc_sm`, `p_desc_top`, `p_desc_bottom`, `p_title`, `p_meta_desc`, `p_meta_key`, `p_date_add`, `p_date_up`, `p_show`, `p_show_head`, `p_alias`, `p_redirect`, `p_type_id`, `p_raiting`, `p_raiting_count`, `p_feature1`, `p_feature2`, `p_feature3`, `p_maket`) VALUES('".$id."', '".$name."', '".$price."', ".($price_from3 > 0?"'".$price_from3."'":"NULL").", ".($price_from10 > 0?"'".$price_from10."'":"NULL").", `p_price_cost`=".($price_cost > 0?"'".$price_cost."'":"NULL").", NULL, ".($count > 0?"".$count."":"NULL").", '0', '0', '0', '".$art."', '".$desc_sm."', '', '', NULL, '', '', NOW(), NOW(), '".($show == ""?"1":"".$show."")."', '1', '".($id+1000)."', NULL, NULL, '0', '0', NULL, NULL, NULL, '".$maket."')");
				
				$res_pos = mysql_query("SELECT cat_product_rel.p_pos FROM cat_product_rel WHERE cat_id = '".$cat_id."' AND cat_main = '1' ORDER BY p_pos DESC LIMIT 1");
				while ($res = @mysql_fetch_array($res_pos)){
					$pos = $res["p_pos"]+1;
				}
				if (!$pos){$pos = 1;}
				mysql_query("INSERT INTO `cat_product_rel` (`cat_p_id`, `cat_id`, `cat_main`, `p_pos`) VALUES('".$id."', '".$cat_id."', '1', '".$pos."')");
			}			
		}
		else if ($delete == 1 && $id > 0){
			// Удаление товара
			mysql_query("DELETE FROM cat_product WHERE p_id = '".$id."'");
			mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$id."'");

			$num = $id+1000;
			$dirs_catalog = "../../../files/catalog";
			
			unlink($dirs_catalog."/".$num."_small.jpg");
			unlink($dirs_catalog."/".$num."_normal.jpg");	
			unlink($dirs_catalog."/".$num."_big.jpg");	
			unlink($dirs_catalog."/".$num."_preview.jpg");

			for ($i=1; $i<13; $i++) {
				if(file_exists($dirs_catalog."/".$num."_".$i."_small.jpg")){
					unlink($dirs_catalog."/".$num."_".$i."_small.jpg");
				}
				if(file_exists($dirs_catalog."/".$num."_".$i."_normal.jpg")){
					unlink($dirs_catalog."/".$num."_".$i."_normal.jpg");
				}
				if(file_exists($dirs_catalog."/".$num."_".$i."_big.jpg")){
					unlink($dirs_catalog."/".$num."_".$i."_big.jpg");
				}
			}			
		}
		return 1;
	}
}

function getCSV($file) {
	$handle = fopen($file, "r");

	$array_line_full = array();
	while (($line = fgetcsv($handle, 0, ";")) !== FALSE) { 
		$array_line_full[] = $line;
	}
	fclose($handle);
	return $array_line_full;
}

?>