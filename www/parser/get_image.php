<?php

ini_set('max_execution_time', 600);

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	$result = mysql_query("SELECT p_name, p_art, p_img_url FROM cat_product WHERE p_img_url !='' ORDER BY p_id ASC");
	while ($row = @mysql_fetch_array($result)){
		$image = $row["p_img_url"];
		if ($image && !file_exists("../files/catalog/".$row["p_art"].".jpg")){
			print $row["p_art"]." - ".$row["p_name"]."<br>";
			$file = file_get_contents($image);
			if ($file){
				$fp = fopen("../files/catalog/".$row["p_art"].".jpg", 'w');
				fwrite($fp, $file);
				fclose($fp);
			}
		}
	}
	

?>