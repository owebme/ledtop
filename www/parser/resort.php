<?php

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	cat_resort(1);
	cat_resort(2);
	cat_resort(3);
	cat_resort(4);
	cat_resort(5);
	cat_resort(6);
	
	function cat_resort($id){
		$category = array();
		$result = mysql_query("SELECT c_id, c_name FROM cat_category WHERE c_pid = '".$id."' ORDER BY c_pos ASC");
		while ($row = @mysql_fetch_array($result)){
			print "<h2>".$row["c_name"]."</h2>";
			resort($row["c_id"], $id);
			$res = mysql_query("SELECT c_name, c_id FROM cat_category WHERE c_pid = '".$row["c_id"]."' ORDER BY c_pos ASC");
			if (mysql_num_rows($res)){
				while ($row2 = @mysql_fetch_array($res)){		
					print "<h3>".$row2["c_name"]."</h3>";
					resort($row2["c_id"], $id);
				}
			}
		}
	}
	
	function resort($cat_id, $parent_id){
		$products = array(); $last = array();
		$result = mysql_query("SELECT p.p_id, p.p_art, p.p_name, p.p_price, pl.cat_id, pl.p_pos, pl.cat_main, f.* FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) JOIN cat_product_fields AS f ON(f.p_id = p.p_id) WHERE pl.cat_id = '".$cat_id."' AND f.field = '÷вет 1' ORDER BY f.value ASC, p.p_price ASC");
		while ($row = @mysql_fetch_array($result)){
			if (!$products[$row["p_id"]]){
				if ($row["value"] && $parent_id > 0 && $parent_id < 7){
					//$products[$row["p_id"]] = "<strong>".$row["p_art"]."</strong> ".$row["p_name"]." = ".$row["p_price"]." руб.";
					$products[$row["p_id"]] = $row["p_id"];
				}
				else {
					//$last[$row["p_id"]] = "<strong>".$row["p_art"]."</strong> ".$row["p_name"]." = ".$row["p_price"]." руб.";
					$last[$row["p_id"]] = $row["p_id"];
				}
			}
		}
		$array = array_merge($products, $last);
		$pos = 0;
		foreach ($array as $item){
			$pos++;
			print $pos." - ".$item." - ".$cat_id."<br>";
			mysql_query("UPDATE cat_product_rel SET `p_pos` = '".$pos."' WHERE cat_p_id = '".$item."' AND cat_id = '".$cat_id."' LIMIT 1");
		}		
		//print_r($array);
	}

?>