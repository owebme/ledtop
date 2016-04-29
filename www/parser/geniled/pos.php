<?php

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	$category = array();
	$pos = 0; $c_id=""; $i="";
	$result = mysql_query("SELECT p.*, pl.p_pos, pl.cat_main, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_supplier = '2' ORDER BY pl.cat_id ASC");
	while ($row = @mysql_fetch_array($result)){
		$i++;
		if ($c_id != $row["cat_id"] && $c_id > 0 or $i == "1") {
			if ($c_id > 0){
				if (!$category[$c_id]){
					$category[$c_id] = $pos;
				}
			}
			$pos = 0;
		}
		$pos++;
		mysql_query("UPDATE cat_product_rel SET `p_pos` = '".$pos."' WHERE cat_p_id = '".$row["p_id"]."' AND cat_id = '".$row["cat_id"]."' AND cat_main = '".$row["cat_main"]."' LIMIT 1");
		print "Перемещен на вверх <strong>".$row["p_name"]." - CategoryID: ".$row["cat_id"]."</strong> позиция ".$row["p_pos"]." => ".$pos."<br>";		
		$c_id = $row["cat_id"];
	}
	if (!$category[$c_id]){
		$category[$c_id] = $pos;
	}
	
	foreach ($category as $cat_id => $p_pos){
		$pos = $p_pos;
		$result = mysql_query("SELECT p.*, pl.p_pos, pl.cat_main, pl.cat_id FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_supplier != '2' AND pl.cat_id = '".$cat_id."' ORDER BY pl.p_pos ASC");
		while ($row = @mysql_fetch_array($result)){
			$pos++;
			mysql_query("UPDATE cat_product_rel SET `p_pos` = '".$pos."' WHERE cat_p_id = '".$row["p_id"]."' AND cat_id = '".$row["cat_id"]."' AND cat_main = '".$row["cat_main"]."' LIMIT 1");
			print "<strong>".$row["p_name"]." - CategoryID: ".$row["cat_id"]."</strong> позиция ".$row["p_pos"]." => ".$pos."<br>";
		}
	}

?>