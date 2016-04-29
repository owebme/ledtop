<?php

	$date = new DateTime();
	$hour = $date->format('H');
	
	if ($hour > 9 && $hour < 23){
	
		$up_file = fopen("orders_last.txt", "r");
		while (!feof ($up_file)) {
			$last = fgets($up_file, 4096);
		}
		fclose($up_file);	
	
		$up_file = fopen("orders.txt", "r");
		while (!feof ($up_file)) {
			$num = fgets($up_file, 4096);
			$rand = random($last);
			$num = $num+$rand;
		}
		fclose($up_file);
		
		$fp = fopen("orders.txt", 'w');
		fwrite($fp, "$num");
		fclose($fp);
		
		$fp = fopen("orders_last.txt", 'w');
		fwrite($fp, "$rand");
		fclose($fp);		
		
		print $num;
	}

	function random($num){
		$rand = rand(3,6);
		if ($rand == $num){
			$rand = random($num);
		}
		return $rand;
	}
	
?>