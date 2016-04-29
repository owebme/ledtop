<?php

	$date = new DateTime();
	$hour = $date->format('H')*1;
	
	require_once 'db.php';
	
	if ($hour == 0 or $hour < 7){
		mysql_query("UPDATE cat_product_sale SET sale = NULL, date = NOW()");
		print "clear";
	}	
	else if ($hour > 7 && $hour < 23){
		$sales = array();
		$res_sql = mysql_query("SELECT * FROM cat_product_sale ORDER BY RAND() LIMIT 8");
		while ($row = @mysql_fetch_array($res_sql)){
			$rand = random($sales, $row["sale"]);
			$sale = $row["sale"] + $rand;
			array_push($sales, $sale);
			mysql_query("UPDATE cat_product_sale SET sale = '".$sale."', date = NOW() WHERE id = ".$row["id"]."");
			print $sale." - ".$row["id"]."<br>";
		}
	}

	function random($sales, $num){
		$rand = rand(1,12);
		if ($rand == 10 or in_array(($rand+$num), $sales)){
			$rand = random($sales, $num);
		}
		return $rand;
	}
	
?>