#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Cookie;
use URI::Escape;

$name=param('name');
$phone=param('phone');

require "admin/engine/lib/parametr.cgi";

if ($phone ne "") {

	use Encode "from_to";
	from_to($phone, "utf-8", "cp1251");
	from_to($name, "utf-8", "cp1251");

	$url_site =~ s/^\.//g;

	open (MZ,"|/usr/sbin/sendmail -t");
	print MZ "To: $email_feedback\n";
	print MZ "From: robot\@$url_site\n";
	print MZ "Subject: !!! ЖДУТ ЗВОНКА !!! $phone с сайта $url_site\n";
	print MZ "MIME-Version: 1.0\n";
	print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
	print MZ "Content-Transfer-Encoding: 8bit\n\n";
	print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
	print MZ "Добрый день!<br><br>Заказали обратный звонок.<br><br>";
	print MZ "Имя: <b>$name</b><br><br>";
	print MZ "Телефон: <b>$phone</b><br><br>";
	if (cookie("come_city")){
		print MZ "Город: <b>".uri_unescape(cookie("come_city"))."</b><br><br>";
	}
	print MZ "</div>";
	close (MZ);

	print header( -charset=>'windows-1251');

	print "Ваша заявка успешно отправлена,<br>ожидайте звонка";

}
