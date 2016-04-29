#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use Fcntl;                                   # O_EXCL, O_CREAT � O_WRONLY
use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);          # ����� ������ � browser-� 
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;

$name=param('name');
$tema=param('tema');
$mail=param('mail');
$phone=param('phone');
$text=param('note');
$asc_product=param('asc_product');
$captcha=param('captcha');
$captcha_num1=param('captcha_num1');
$captcha_num2=param('captcha_num2');
$captcha_num3=param('captcha_num3');

require "admin/engine/lib/parametr.cgi";

if ($name ne "" && $tema ne "" && $mail ne "" && $text ne "" && $captcha ne ""){

	if ($captcha eq ($captcha_num1+$captcha_num2-$captcha_num3)){

		$text =~ s/</&lt;/g;
		$text =~ s/>/&gt;/g;
		$text =~ s/\n/\<br>/g;

		open (MZ,"|/usr/sbin/sendmail -t");
		print MZ "To: $email_feedback\n";
		print MZ "From: $mail\n";
		print MZ "Subject: ����� ��������� � ����� www$url_site\n";
		print MZ "MIME-Version: 1.0\n";
		print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
		print MZ "Content-Transfer-Encoding: 8bit\n\n";
		print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
		print MZ "������ ����!<br><br>��������� ����� ���������.<br><br><br>";
		print MZ "��: <b>$name</b><br><br>";
		print MZ "����: <b>$tema</b><br><br>";
		print MZ "E-mail: <a href='mailto:$mail'>$mail</a><br><br>";
		if ($phone ne "") {
		print MZ "�������: <b>$phone</b><br><br>";
		} else {print MZ "�������: <b style='color:#ccc;'>�� ������</b><br><br>";}
		print MZ "<b>���������:</b> $text";
		print MZ "</div>";
		close (MZ);
	}
}

if ($asc_product ne "" && $name ne "" && $mail ne "" && $text ne "") {

use Encode "from_to";
from_to($asc_product, "utf-8", "cp1251");
from_to($name, "utf-8", "cp1251");
from_to($text, "utf-8", "cp1251");

$text =~ s/</&lt;/g;
$text =~ s/>/&gt;/g;
$text =~ s/\n/\<br>/g;

open (MZ,"|/usr/sbin/sendmail -t");
print MZ "To: $email_feedback\n";
print MZ "From: $mail\n";
print MZ "Subject: ������ �� ������ �$asc_product�\n";
print MZ "MIME-Version: 1.0\n";
print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
print MZ "Content-Transfer-Encoding: 8bit\n\n";
print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
print MZ "������ ����!<br><br>�������� ����� ������.<br><br><br>";
print MZ "��: <b>$name</b><br><br>";
print MZ "E-mail: <a href='mailto:$mail'>$mail</a><br><br>";
print MZ "<b>������:</b> $text";
print MZ "</div>";
close (MZ);

print header( -charset=>'windows-1251');

print "��� ������ ������� ���������,<br>�������� ������";

}
