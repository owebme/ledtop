<?php

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	$counts = 0;
	$result = mysql_query("SELECT p.p_art, f.* FROM cat_product AS p JOIN cat_product_fields AS f ON(f.p_id=p.p_id) WHERE p.p_supplier = '2'");
	while ($row = @mysql_fetch_array($result)){
		if ($row["field"] == "Класс пыле-влагозащиты") {
			$value = $row["value"];
			#$value = preg_replace("%\s%", "", $value);
			print $row["p_art"]." &ndash; ".$value."<br>";
			//mysql_query("UPDATE cat_product_fields SET `value` = '".$value."' WHERE field = 'Класс пыле-влагозащиты' AND p_id = '".$row["p_id"]."'");
		}
		
	}
	
	print $counts;

?>