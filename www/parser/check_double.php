<?php

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	$result = mysql_query("SELECT * FROM cat_product_rel");
	while ($row = @mysql_fetch_array($result)){
		$res = mysql_query("SELECT p_id FROM cat_product WHERE p_id = '".$row["cat_p_id"]."' LIMIT 1");
		if (!mysql_num_rows($res)){
			print "Лишняя запись cat_product_rel, не существующий товар: ".$row["cat_p_id"]." - category ".$row["cat_id"];
			mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$row["cat_p_id"]."' AND cat_id = '".$row["cat_id"]."'");
			print ' - <span style="color:red">запись удалена</span><br>';		
		}
		$res = mysql_query("SELECT c_id FROM cat_category WHERE c_id = '".$row["cat_id"]."' LIMIT 1");
		if (!mysql_num_rows($res)){
			print "Лишняя запись cat_product_rel, не существующая категория: ".$row["cat_id"];
			mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$row["cat_p_id"]."' AND cat_id = '".$row["cat_id"]."'");
			print ' - <span style="color:red">запись удалена</span><br>';
		}
	}
	
	$array = array();
	$result = mysql_query("SELECT p_id, p_art FROM cat_product");
	while ($row = @mysql_fetch_array($result)){
		if (!$array[$row["p_art"]]){
			$array[$row["p_art"]] = $row["p_id"];
		}
		else {
			print "Дубль cat_product: ".$row["p_id"]." - Артикуль: ".$row["p_art"]."<br>";
			//mysql_query("DELETE FROM cat_product WHERE p_id = '".$row["p_id"]."' LIMIT 1"); // Раскоментить для удаления
		}
	}	

	$array = array();
	$result = mysql_query("SELECT * FROM cat_product_rel");
	while ($row = @mysql_fetch_array($result)){
		if (!$array[$row["cat_p_id"].$row["cat_id"].$row["cat_main"]]){
			$array[$row["cat_p_id"].$row["cat_id"].$row["cat_main"]] = $row["p_pos"];
		}
		else {
			print "Дубль cat_product_rel: ".$row["cat_p_id"]." - ".$row["cat_id"]." - ".$row["cat_main"]." - ".$row["p_pos"];
			print ' - <span style="color:red">запись удалена</span><br>';
			mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$row["cat_p_id"]."' AND cat_id = '".$row["cat_id"]."' AND cat_main = '".$row["cat_main"]."' AND p_pos = '".$row["p_pos"]."' LIMIT 1");
		}
	}
	
	$array = array();
	$result = mysql_query("SELECT * FROM cat_product_fields");
	while ($row = @mysql_fetch_array($result)){
		if (!$array[$row["p_id"].$row["field"].$row["unic"]]){
			$array[$row["p_id"].$row["field"].$row["unic"]] = $row["value"];
		}
		else {
			print "Дубль cat_product_fields: ".$row["p_id"]." - ".$row["field"]." - ".$row["unic"]." - ".$row["value"]."<br>";
			//mysql_query("DELETE FROM cat_product_fields WHERE p_id = '".$row["p_id"]."' AND field = '".$row["field"]."' AND unic = '".$row["unic"]."' AND value = '".$row["value"]."' LIMIT 1"); // Раскоментить для удаления
		}
	}

?>