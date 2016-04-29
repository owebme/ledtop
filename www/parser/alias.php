<?php

ini_set('max_execution_time', 600);

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	$result = mysql_query("SELECT p_id, p_art FROM cat_product");
	while ($row = @mysql_fetch_array($result)){
		print $row["p_art"]."<br>";
		mysql_query("UPDATE cat_product SET `p_alias`='".$row["p_art"]."' WHERE p_id='".$row["p_id"]."' LIMIT 1");
	}
	

?>