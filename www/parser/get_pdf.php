<?php

ini_set('max_execution_time', 600);

require_once 'db.php';

header("Content-type: text/html; charset=windows-1251");

	$result = mysql_query("SELECT p.p_name, p.p_art, f.value FROM cat_product AS p JOIN cat_product_fields AS f ON(f.p_id=p.p_id) WHERE f.field = '—сылка на PDF' AND f.value !='' ORDER BY p.p_id ASC");
	while ($row = @mysql_fetch_array($result)){
		$pdf = $row["value"];
		if ($pdf && !file_exists("../files/catalog/pdf/".$row["p_art"].".pdf")){
			print $row["p_art"]." - ".$row["p_name"]."<br>";
			$file = file_get_contents($pdf);
			if ($file){
				$fp = fopen("../files/catalog/pdf/".$row["p_art"].".pdf", 'w');
				fwrite($fp, $file);
				fclose($fp);
			}
		}
	}
	

?>