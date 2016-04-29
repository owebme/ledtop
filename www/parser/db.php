<?php

$up_file = fopen("../admin/backup/access", "r");
while (!feof ($up_file)) {                       
 $buffer = fgets($up_file, 4096);
 list($r_host, $r_user, $r_password, $r_name_db) = preg_split("%\|%",$buffer);
 $host = $r_host;
 $user = $r_user;
 $password = $r_password;
 $database = $r_name_db;
}
fclose($up_file);

mysql_connect($host,$user,$password) or die ("Не возможно соединиться с MySQL");
mysql_query("SET NAMES 'cp1251'");
mysql_select_db($database) or die ("Не возможно соединиться с базой данных");

?>