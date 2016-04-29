<?php

$cook = $_COOKIE['uplecms'];

if ($cook){
	list($_login, $_pass) = preg_split("%\|%",$cook);
	list($_var, $login) = preg_split("%\:%",$_login);
	list($_var, $pass) = preg_split("%\:%",$_pass);
	
	$path="";
	$path1 = $_SERVER['DOCUMENT_ROOT'].'/cgi-bin/';
	$path2 = $_SERVER['DOCUMENT_ROOT'].'/../cgi-bin/';
	
	if (file_exists($path1)) {
		$path = $path1;
	}
	else if (file_exists($path2)) {
		$path = $path2;
	}
	if ($path){
		$file = $path."admin/engine/password-settings/".$login;
		if ($pass && $login && file_exists($file) && $pass == file_get_contents($file) && file_get_contents($file) != "") {
		}
		else {
			header('HTTP/1.1 301 Moved Permanently');
			header('Location: /admin/');
			exit();
		}
	}
}
else {
	header('HTTP/1.1 301 Moved Permanently');
	header('Location: /admin/');
	exit();
}

	$backup = $_GET['backup']; 
	$restore = $_GET['restore']; 
	$delete = $_GET['delete'];	

	function listFiles($message) {	
		$current_dir = 'backup_files';
		$dir = opendir($current_dir);
	echo '<html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=windows-1251" />
		<title></title>
		<link rel="stylesheet" type="text/css" href="/admin/css/main_style.css" />
		<script type="text/javascript" src="/admin/js/jquery-1.4.2.min.js"></script>
		<script type="text/javascript" src="/admin/lib/backup.js"></script>
		</head>
		<body style="background:none;">
		<div id="content" style="width:473px; min-height:600px;">
		<h2 style="font:normal 18px Arial; color:#666; margin-top:8px;">Восстановление картинок</h2>
		<div style="position:relative;"><a class="add_backup" href="backup_files.php?backup">Создать бэкап</a></div>
		<div id="backup_files">';
	
		echo $message;
		echo '<div class="files">';

		while ($file = readdir($dir))
		{
		if(substr($file,0,1) == '.') continue;
		echo '<div class="file"><a title="Восстановить" class="name" href="backup_files.php?restore='.$file.'">'.$file.'</a><a title="Удалить" class="del" href="backup_files.php?delete='.$file.'"></a></div><div class="clear"></div>';
		}
		echo '</div>';
		closedir($dir);	
		

	echo '</div>
		  </div>
		  </body>
		  <html>';
	
	}

	require_once "../pclzip/pclzip.lib.php";


	if (isset($_GET['backup'])){
		$backupFiles = backupFiles();
		echo $backupFiles;
		return listFiles('<div class="save">Резервная копия создана</div>');
	}	
	if (isset($_GET['restore'])){
		$restoreFiles = restoreFiles($restore);
		echo $restoreFiles;
		return listFiles('<div class="restore">Картинки восстановлены из резервной копии</div>');	
	}
	if (isset($_GET['delete'])){
		$deleteFiles = deleteFiles($delete);
		echo $deleteFiles;
		return listFiles('<div class="delete">Резервная копия удалена</div>');
	}

	function deleteFiles($file) {

		$filename = 'backup_files/'.$file;

		unlink($filename);

	}	

	function backupFiles() {

		$files = "../../files/";
		$backup = "backup_files/";	
		$today = date("20y-m-d_H-i-s");

		$archive = new PclZip($backup."$today.zip");

		$openDIR = opendir($files);
		while (readdir($openDIR))
		{
		$list = $archive->add($files, PCLZIP_OPT_REMOVE_PATH, '/');
		}

	}
	
	function restoreFiles($file) {

		$upload_dir = dirname( __FILE__ );
		$filename = 'backup_files/'.$file; 

		$zip_dir = '../../files'; 
		function removeDirRec($dir)
		{
			if ($objs = glob($dir."/*")) {
				foreach($objs as $obj) {
					is_dir($obj) ? removeDirRec($obj) : unlink($obj);
				}
			}
		}
		removeDirRec($zip_dir);

		$archive = new PclZip($filename); 

		$archive->extract(PCLZIP_OPT_PATH, $upload_dir.'/'.$zip_dir);

	}
	
	return listFiles('');

?>