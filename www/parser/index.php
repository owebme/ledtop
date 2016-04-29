<?php

ini_set('max_execution_time', 600);

function getDomen(){
	return 'http://ledtop-shop.ru';
}

$pars_xml = 0;
$pars_catalog = 1;
$backup_to = 1;
$backup_from = 1;
$clear = 1;

require_once 'db.php';
require_once 'function.php';

header("Content-type: text/html; charset=utf-8");

print '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />';
print '<style>html {width:988px; margin:25px auto 0; font-family: Arial, Helvetica;} body {margin:0;} h2, h3 {margin:0 0 10px;} h2 {font-size:1.7em; margin-bottom:12px;}</style>';

if ($backup_to){
	file_get_contents(getDomen().'/parser/backup.php?action=security&time=to');
}

require_once 'get_xml.php';

if ($pars_xml){
	getFile('ledribbon');
	getFile('supply');
	getFile('lightcontrol');
	getFile('profile');
	getFile('ledlamps');
	getFile('ledbulbs');
	getFile('ledmodules');
	getFile('ledprojectors');
	getFile('leds');
}

require_once 'modules/leds.php';
require_once 'modules/lenta.php';
require_once 'modules/lamp.php';
require_once 'modules/svet.php';
require_once 'modules/moduli.php';
require_once 'modules/projectors.php';
require_once 'modules/control.php';
require_once 'modules/power.php';
require_once 'modules/profile.php';
require_once 'clear.php';

if ($pars_catalog){
	parserLeds();
	parserLenta();
	parserLamp();
	parserSvet();
	parserModuli();
	parserProjectors();
	parserControl();
	parserPower();
	parserProfile();
}

if ($clear){
	clearProducts();
}

if ($backup_from){
	file_get_contents(getDomen().'/parser/backup.php?action=security&time=from');
}

?>