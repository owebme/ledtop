#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use Core::Config;
use Core::DB;
use CGI::Cookie;
use URI::Escape;

my $db = new Core::DB();

$name=param('name');
$phone=param('phone');
$buy_quick=param('buy_quick');

require "admin/engine/lib/parametr.cgi";

if ($name ne "" && $phone ne "" && $buy_quick ne "") {

use Encode "from_to";
from_to($name, "utf-8", "cp1251");
from_to($phone, "utf-8", "cp1251");

my $id = $buy_quick;
my $result = $db->query("SELECT p.*, c.c_alias, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_id ='".$id."' AND pl.cat_main ='1' LIMIT 1");
$page_alias = $result->[0]->{c_alias};
$p_name = $result->[0]->{p_name};
$p_art = $result->[0]->{p_art};
$alias = $result->[0]->{p_alias};
$price = $result->[0]->{p_price};

$p_name =~ s/'//g;
$p_name =~ s/"//g;
$price =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;

$url_site =~ s/^\.//g;

open (MZ,"|/usr/sbin/sendmail -t");
print MZ "To: $email_orders\n";
print MZ "From: robot\@$url_site\n";
print MZ "Subject: Быстрый заказ с сайта $url_site\n";
print MZ "MIME-Version: 1.0\n";
print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
print MZ "Content-Transfer-Encoding: 8bit\n\n";
print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
print MZ "Добрый день!<br><br>Поступил быстрый заказ с сайта.<br><br>";
print MZ "Имя: <b>".$name."</b><br><br>";
print MZ "Телефон: <b>".$phone."</b><br><br>";
if ($p_art ne ""){print MZ "Артикул: <b>".$p_art."</b><br><br>";}
print MZ "Товар: <a target='_blank' href='http://".$url_site."/products/".$page_alias."/".$p_art."'>".$p_name."</a><br><br>";
print MZ "Цена: <b>".$price." руб.</b><br><br>";
if (cookie("come_city")){
	print MZ "Город: <b>".uri_unescape(cookie("come_city"))."</b><br><br>";
}
print MZ "</div>";
close (MZ);

print header( -charset=>'windows-1251');

print "Ваш заказ успешно отправлен,<br>ожидайте звонка";

}
