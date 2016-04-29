<?

ini_set('max_execution_time', 600);

require_once 'db.php';
require_once '../function.php';

header("Content-type: text/html; charset=utf-8");

$url = '../geniled.xml';
 
$yml = simplexml_load_file($url);
 
foreach ($yml->shop->categories->category as $item) {
	mysql_query("INSERT INTO `catalog_geniled` (`c_id`, `c_pid`, `c_name`) VALUES('".$item["id"]."', '".$item["parentId"]."', '".cp1251($item)."')");

	echo '<h3>'.$item.'</h3>';
}
?>