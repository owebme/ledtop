<?php

require_once 'db.php';

	function clearProducts(){
	
		$result = mysql_query("SELECT p_art, p_name, p_id, p_alias FROM cat_product WHERE DAY(p_date_up) != DAY(NOW()) AND p_supplier = '1' ORDER BY p_id ASC");
		while ($row = @mysql_fetch_array($result)){
			arhiveProduct($row["p_id"]);
			print "<b>".utf8($row["p_art"]).":</b> ".utf8($row["p_name"])." - <span style='color:red'>в архив</span><br>";
		}	
		
		$result = mysql_query("SELECT c_name, c_id FROM cat_category WHERE DAY(c_date_up) != DAY(NOW()) AND c_supplier = '1' AND c_pid < 10 ORDER BY c_pos ASC");
		while ($row = @mysql_fetch_array($result)){
			print "<b>".utf8($row["c_name"])."</b> - <span style='color:red'>удалена</span><br>";
			delCategory($row["c_id"]);
			recSubCategory($row["c_id"]);
		}
	}	
	
	function recSubCategory($id){
		$res = mysql_query("SELECT c_name, c_id FROM cat_category WHERE DAY(c_date_up) != DAY(NOW()) AND c_supplier = '1' AND c_pid = '".$id."' ORDER BY c_pos ASC");
		if (mysql_num_rows($res)){
			while ($row = @mysql_fetch_array($res)){
				print "&nbsp; &mdash; ".utf8($row["c_name"])."<br>";
				if (!recSubCategory($row["c_id"])){
					break;
				}
			}
		}		
		else {
			return 0;
		}
	}
	
	function arhiveProduct($id){
		mysql_query("UPDATE cat_product SET `p_show` = '0' WHERE p_id='".$id."' LIMIT 1");
	}
	
	function delProduct($id, $alias){
		mysql_query("DELETE FROM cat_product WHERE p_id = '".$id."'");
		mysql_query("DELETE FROM cat_product_rel WHERE cat_p_id = '".$id."'");
		mysql_query("DELETE FROM cat_product_fields WHERE p_id = '".$id."'");	
		if (file_exists("../files/catalog/pdf/".$alias.".pdf")){
			unlink('../files/catalog/pdf/".$alias.".pdf');
		}
	}
	
	function delCategory($id){
		file_get_contents(getDomen().'/cgi-bin/admin/modules/functions.cgi?category_del='.$id);	
	}
	

?>