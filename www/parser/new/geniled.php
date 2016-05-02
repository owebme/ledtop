<?

ini_set('max_execution_time', 600);

require_once 'db.php';
require_once '../function.php';

header("Content-type: text/html; charset=utf-8");

$url = '../geniled.xml';
 
$yml = simplexml_load_file($url);

mysql_query("TRUNCATE TABLE `catalog_geniled`");
mysql_query("TRUNCATE TABLE `products_geniled`");

print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<style>html {width:988px; margin:25px auto 0; font-family: Arial, Helvetica;} body {margin:0;} h2, h3 {margin:0 0 10px;} h2 {font-size:1.7em; margin-bottom:12px;}</style>';

echo '<h2 style="color:brown">Категории</h2>';
 
foreach ($yml->shop->categories->category as $item) {
	// Добавляем категорию
	mysql_query("INSERT INTO `catalog_geniled` (`c_id`, `c_pid`, `c_name`) VALUES('".$item["id"]."', '".$item["parentId"]."', '".cp1251($item)."')");
	echo '<h3 style="color:green">'.$item.'</h3>';
}

echo '<br><h2 style="color:brown">Товары</h2>';

foreach ($yml->shop->offers->offer as $item) {
	// Добавляем товар
	foreach ($item as $key => $value) {
		if ($key == "price"){
			$price = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}	
		else if ($key == "categoryId"){
			$cat_id = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}		
		else if ($key == "picture"){
			$img = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}
		else if ($key == "name"){
			$name = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}
		else if ($key == "description"){
			$descript = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}	
		else if ($key == "param" && $value["name"] == "Артикул"){
			$article = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}	
		else if ($key == "param" && $value["name"] == "Остаток на складе"){
			$stock = $value;
			echo "<p style='color:green; font-weight:bold'>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}		
		else {
			echo "<p>".$key.": ".($value["name"] ? $value["name"]." - " : "").$value."</p>";
		}
	}
	mysql_query("INSERT INTO `products_geniled` (`p_art`, `cat_id`, `p_name`, `p_image`, `p_price`, `p_price_opt`, `p_price_opt_large`, `p_price_cost`, `p_desc`, `p_stock`, `p_waiting`, `p_possible`, `p_color`, `p_pack`, `p_packnorm`, `p_unit`, `p_related`) VALUES('".$article."', '".$cat_id."', '".cp1251($name)."', '".$img."', '".$price."', NULL, NULL, NULL, '".cp1251($descript)."', '".$stock."', NULL, NULL, NULL, NULL, NULL, NULL, '".($related ? $related : '')."')");	
	echo "<hr>";
}

?>