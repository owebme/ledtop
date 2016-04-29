#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use MIME::Base64;

$name=param('name');
$mail=param('mail');
$phone=param('phone');
$type=param('type');
$length=param('length');
$width=param('width');
$height=param('height');
$address=param('address');
$text=param('note');
$mail_file=param('mail_file');

require "admin/engine/lib/parametr.cgi";

print header( -charset=>'windows-1251');

if ($type eq "1"){$type="Баня";}
elsif ($type eq "2"){$type="Сауна";}
elsif ($type eq "3"){$type="Хаммам";}
elsif ($type eq "4"){$type="Бассейн";}
elsif ($type eq "5"){$type="Spa зона";}

my $imagefile = $mail_file;
$imagefile =~ m#([^\\/:]+)$#;
use Encode "from_to";
from_to($imagefile, "cp1251", "utf-8");

mkdir ("$dirs_catalog_www2/../../uploads/mail", 0755);

if ($mail_file) {
	   open OUT, (">$dirs_catalog_www2/../../uploads/mail/$imagefile");
	    binmode (OUT);
	    while (<$mail_file>) { print OUT "$_"; } 
	   close(OUT);
}
	
	$bound="1234";
	use LWP::Simple;
	my $file = get("http://".$ENV{"HTTP_HOST"}."/uploads/mail/".$imagefile);

if ($name ne "" && $phone ne "" && $type ne ""){
	
	open (MZ,"|/usr/sbin/sendmail -t");
	print MZ "To: $email_orders\n";
	print MZ "From: $mail\n";
	print MZ "Subject: Новое сообщение с сайта www$url_site\n";
	print MZ "MIME-Version: 1.0\n";
	print MZ "Content-Type: multipart/mixed; boundary=$bound\n";
	print MZ "--$bound\n";
	print MZ "Content-type: text/html; charset=\"windows-1251\"\n";
	print MZ "Content-Transfer-Encoding: quoted-printable\n\n";	
	print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
	print MZ "Добрый день!<br><br>Поступило новое сообщение.<br><br><br>";
	print MZ "От: <b>$name</b><br><br>";
	print MZ "E-mail: <a href='mailto:$mail'>$mail</a><br><br>";
	if ($phone ne "") {
	print MZ "Телефон: <b>$phone</b><br><br>";
	} else {print MZ "Телефон: <b style='color:#ccc;'>не указан</b><br><br>";}
	print MZ "Тип строительства: <b>$type</b><br><br>";
	print MZ "Адрес строительства: <b>$address</b><br><br>";
	print MZ "Длина: <b>$length</b><br><br>";
	print MZ "Ширина: <b>$width</b><br><br>";
	print MZ "Высота: <b>$height</b><br><br>";	
	print MZ "<b>Подробности:</b> $text";
	print MZ "</div>";
	print MZ "\n\n--$bound\n";
	print MZ "Content-Type: application/octet-stream; ";
	print MZ "name=".$imagefile."\n";
	print MZ "Content-Transfer-Encoding:base64\n";
	print MZ "Content-Disposition:attachment\n\n";
	print MZ encode_base64($file)."\n";
	print MZ "$bound--\n\n";	
	close (MZ);

	#unlink("$dirs_catalog_www2/../../uploads/mail/$imagefile");	
}	
	