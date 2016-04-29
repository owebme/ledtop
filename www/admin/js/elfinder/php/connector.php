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

error_reporting(0); // Set E_ALL for debuging

include_once dirname(__FILE__).DIRECTORY_SEPARATOR.'elFinderConnector.class.php';
include_once dirname(__FILE__).DIRECTORY_SEPARATOR.'elFinder.class.php';
include_once dirname(__FILE__).DIRECTORY_SEPARATOR.'elFinderVolumeDriver.class.php';
include_once dirname(__FILE__).DIRECTORY_SEPARATOR.'elFinderVolumeLocalFileSystem.class.php';
// Required for MySQL storage connector
// include_once dirname(__FILE__).DIRECTORY_SEPARATOR.'elFinderVolumeMySQL.class.php';
// Required for FTP connector support
// include_once dirname(__FILE__).DIRECTORY_SEPARATOR.'elFinderVolumeFTP.class.php';


/**
 * Simple function to demonstrate how to control file access using "accessControl" callback.
 * This method will disable accessing files/folders starting from  '.' (dot)
 *
 * @param  string  $attr  attribute name (read|write|locked|hidden)
 * @param  string  $path  file path relative to volume root directory started with directory separator
 * @return bool|null
 **/
function access($attr, $path, $data, $volume) {
	return strpos(basename($path), '.') === 1       // if file/folder begins with '.' (dot)
		? !($attr == 'read' || $attr == 'write')    // set read+write to false, other (locked+hidden) set to true
		:  null;                                    // else elFinder decide it itself
}

$opts = array(
	// 'debug' => true,
	'roots' => array(
		array(
			'driver'        => 'LocalFileSystem',   // driver for accessing file system (REQUIRED)
			'path'          => '../../../..',         // path to files (REQUIRED)
			'URL'           => '/', // URL to files (REQUIRED)
			'accessControl' => 'access'             // disable and hide dot starting files (OPTIONAL)
		)
	)
);

// run elFinder
$connector = new elFinderConnector(new elFinder($opts));
$connector->run();

