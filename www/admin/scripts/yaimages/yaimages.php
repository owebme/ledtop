<?php

if(!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) == 'xmlhttprequest'){

	if (isset($_GET['clear_upload']) && $_GET['clear_upload'] == "clear"){

		if ($objs = glob("../../../files/catalog/multi/upload/*")) {
			foreach($objs as $obj) {
				unlink($obj);
			}
		}
	}
}

?>