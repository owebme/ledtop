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

if ($type eq "1"){$type="����";}
elsif ($type eq "2"){$type="�����";}
elsif ($type eq "3"){$type="������";}
elsif ($type eq "4"){$type="�������";}
elsif ($type eq "5"){$type="Spa ����";}

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
	print MZ "Subject: ����� ��������� � ����� www$url_site\n";
	print MZ "MIME-Version: 1.0\n";
	print MZ "Content-Type: multipart/mixed; boundary=$bound\n";
	print MZ "--$bound\n";
	print MZ "Content-type: text/html; charset=\"windows-1251\"\n";
	print MZ "Content-Transfer-Encoding: quoted-printable\n\n";	
	print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
	print MZ "������ ����!<br><br>��������� ����� ���������.<br><br><br>";
	print MZ "��: <b>$name</b><br><br>";
	print MZ "E-mail: <a href='mailto:$mail'>$mail</a><br><br>";
	if ($phone ne "") {
	print MZ "�������: <b>$phone</b><br><br>";
	} else {print MZ "�������: <b style='color:#ccc;'>�� ������</b><br><br>";}
	print MZ "��� �������������: <b>$type</b><br><br>";
	print MZ "����� �������������: <b>$address</b><br><br>";
	print MZ "�����: <b>$length</b><br><br>";
	print MZ "������: <b>$width</b><br><br>";
	print MZ "������: <b>$height</b><br><br>";	
	print MZ "<b>�����������:</b> $text";
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
	