#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use CGI::Cookie;
use URI::Escape;
use CGI::Session;
use Core::Config;
use Core::DB;
use Core::DB::Catalog;
use Core::DB::Work;

my $db = new Core::DB();
my $orders = new Core::DB::Catalog();

	$session = CGI::Session->load( ) or die CGI::Session->errstr();
	if ( $session->is_empty ) {
       		$session = $session->new() or die $session->errstr;
			$c = new CGI::Cookie(
					 -name    =>  $session->name,
					 -value   =>  $session->id, 
                     -domain  =>  $url_site,
                     -path    =>  "/",
                     -secure  =>  0);
	}
	
$ids = $session->param('ids');

$name=param('NAME');
$phone=param('PHONE');
$email=param('EMAIL');
$address=param('ADDRESS');
$metro=param('METRO');
$text=param('NOTE');

$city=param('CITY');
$index=param('INDEX');
$delivery=param('delivery');

require "admin/engine/lib/parametr.cgi";
if ($hide_private ne "1"){
	require "templates/auth.cgi";
	if ($logined eq "enter"){
		$user_id=param('user_id');
	}
}

my %idTS;
while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
	$idTS{$1}{'cena'} = $2;
	if (!$idTS{$1}{'price'}){$idTS{$1}{'price'} = $2;}
	if($idTS{$1}{'count'}) {$idTS{$1}{'count'}++;
	$idTS{$1}{'cena'} = $2*$idTS{$1}{'count'};}
	else {$idTS{$1}{'count'} = 1;}
}

$totalcena = 0;
while (($key, $value) = each(%idTS)){
	$totalcena += $value->{'cena'};
}

$totalcena = sprintf("%.2f",$totalcena);

#if ($totalcena eq "0"){exit;}

if ($name eq ""){$name = "Аноним";}
	
if ($name ne "" && $phone ne "") {

	if ($text !=""){
		$text =~ s/</&lt;/g;
		$text =~ s/>/&gt;/g;
		$text =~ s/\n/\<br>/g;
	}
	
	my $order_id="";
	my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'cat_orders';");
	foreach my $item(@$result){	
		$order_id = $item->{Auto_increment};
	}
	
	#open OUT, (">>orders.txt");
	#	print OUT $order_id.$ids."|".$ENV{HTTP_USER_AGENT}."\n";
	#close(OUT);	
	
	my $ch_region=""; my $delivery_price="";
	if ($delivery eq "1" or $delivery eq "2"){
		$ch_region = "1";
	}	
	elsif ($delivery eq "3"){
		$metro="";
		$delivery_price = "от 300";
		$ch_region = "2";
	}

	my %params = (
			'order_date' => "$today_sql",
			'user_id' => "$user_id",
			'name' => "$name",
			'phone' => "$phone",
			'ch_region' => "$ch_region",
			'city' => "$city",
			'index' => "$index",			
			'address' => "$address",
			'metro' => "$metro",				
			'email' => "$email",
			'comments' => "$text",
			'delivery' => "$delivery",
			'manager' => "",			
			'status' => "0",
			'pay' => "0",
			'payment' => "",
			'total' => "$totalcena"			
		);
			
	$orders->addOrder(\%params);
	
	my $send_goal="";
	$send_goal ='var yaParams = {
		order_id: "'.$order_id.'",
		order_price: "'.$totalcena.'", 
		currency: "RUR",
		exchange_rate: 1,
		goods: 
			[';
	
	while (($key, $value) = each(%idTS)){

		my $result = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$key."'");
		if ($result){
			foreach my $line(@$result){
			
				my %params_product = (
					'order_id' => "$order_id",
					'p_art' => "$key",
					'p_name' => "$line->{'p_name'}",
					'p_price' => "$value->{'price'}",
					'p_price_value' => "$value->{'price'}",
					'p_count' => "$value->{'count'}"
				);
				
				$send_goal .='
				{
				  id: "'.$key.'", 
				  name: "'.$line->{'p_name'}.'", 
				  price: '.$value->{'cena'}.',
				  quantity: '.$value->{'count'}.'
				},';
						
				$orders->addOrderProduct(\%params_product);			   
			}
		}
	}	
	
	$send_goal .=']};';
	
if ($email_orders ne "") {
open (MZ,"|/usr/sbin/sendmail -t");
print MZ "To: $email_orders\n";
print MZ "From: $email\n";
print MZ "Subject: Новый заказ с сайта www$url_site\n";
print MZ "MIME-Version: 1.0\n";
print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
print MZ "Content-Transfer-Encoding: 8bit\n\n";
print MZ "<table style='width:800px; border-collapse:collapse;'><tr><td style='border:1px dotted #999; width:400px; padding:20px 20px 60px 20px; font:normal 14px Tahoma, Helvetica; vertical-align:top; background-color:#eaeaea;'>";
print MZ "<b><u style='font-size:18px;'>Заказ №$order_id</u></b><br><br>";
print MZ "От: <b>$name</b><br><br>\n";
print MZ "Телефон: <b>$phone</b><br><br>\n";
print MZ "E-mail: <a href=\"mailto:$email\">$email</a><br><br>\n";
print MZ "Город: <b>$city</b><br><br>\n";
if ($index ne "") {
print MZ "Индекс: <b>$index</b><br><br>\n";
}
print MZ "Адрес доставки: <a target='_blank' href='http://maps.yandex.ru/?text=$address'>$address</a><br><br>\n";
if ($text eq "") {
print MZ "<b>Коментарий:</b> <b style='color:#ccc;'>не указан</b>\n";
}else {
print MZ "<b>Коментарий:</b> $text\n";
}
print MZ "</td>
<td style='border:1px dotted #999; width:400px; padding:20px 20px 60px 30px; font:normal 14px Tahoma, Helvetica; vertical-align:top; background: url(http://uplecms.ru/img/logo_order.png) bottom right no-repeat;'>\n";
print MZ "<table style='width:400px; font-size:13px; border-collapse:collapse;'><tr><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Товар</b></td><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Цена</b></td><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Кол-во</b></td></tr>";

while (($key, $value) = each(%idTS)){

	my $result = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$key."'");
	foreach my $line(@$result){	
		print MZ "
		   <tr>\n
			  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\"><b>".$key."</b> ".$line->{'p_name'}."</td>\n
			  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$value->{'price'}."</td>\n
			  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$value->{'count'}."</td>\n
		   </tr>\n";
	}
}

print MZ "</table><br>\n";
if ($delivery_price){
	print MZ "<b>Итого к оплате:</b> <b style='color:#A60000;'>$totalcena руб. + $delivery_price руб. доставка почтой</b>\n";
}
else {
	print MZ "<b>Итого к оплате:</b> <b style='color:#A60000;'>$totalcena руб.</b>\n";
}
print MZ "</td></tr></table>\n";
close (MZ);
}


open (MC,"|/usr/sbin/sendmail -t");
print MC "To: $email\n";
print MC "From: $email_orders\n";
print MC "Subject: Ваш заказ №$order_id принят на сайте www$url_site\n";
print MC "MIME-Version: 1.0\n";
print MC "Content-Type: text/html\; charset=\"windows-1251\"\n";
print MC "Content-Transfer-Encoding: 8bit\n\n";
print MC "<table style='width:850px; border-collapse:collapse;'><tr><td style='border:1px dotted #999; width:450px; padding:20px 0px 60px 20px; font:normal 14px Tahoma, Helvetica; vertical-align:top; background-color:#eaeaea;'>";
print MC "Здравствуйте, <b>$name</b>.<br><br>";
print MC "Ваш заказ <b><u>№$order_id</u></b>, принят.<br><br>";
print MC "Спасибо, за Ваш заказ.<br> Наш менеджер, в ближайшее время свяжется с Вами.<br><br>";
print MC "</td>
<td style='border:1px dotted #999; width:400px; padding:20px 20px 60px 30px; font:normal 14px Tahoma, Helvetica; vertical-align:top; background: url(http://uplecms.ru/img/logo_order.png) bottom right no-repeat;'>\n";
print MC "<table style='width:400px; font-size:13px; border-collapse:collapse;'><tr><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Товар</b></td><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Цена</b></td><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Кол-во</b></td></tr>";

while (($key, $value) = each(%idTS)){

	my $result = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$key."'");
	foreach my $line(@$result){	
		print MC "
		   <tr>\n
			  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\"><b>".$key."</b> ".$line->{'p_name'}."</td>\n
			  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$value->{'price'}."</td>\n
			  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$value->{'count'}."</td>\n
		   </tr>\n";
	}
}

print MC "</table><br>\n";
if ($delivery_price){
	print MC "<b>Итого к оплате:</b> <b style='color:#A60000;'>".$totalcena." руб. + ".$delivery_price." руб. доставка почтой</b>\n";
}
else {
	print MC "<b>Итого к оплате:</b> <b style='color:#A60000;'>".$totalcena." руб.</b>\n";
}
print MC "</td></tr></table>\n";
close (MC);

$session->param('ids',"");
$session->flush();

open OUT, ("admin/engine/lib/counter"); @counter = <OUT>;
foreach my $text(@counter) {$counter=qq~$counter$text~;}

print header( -charset=>'windows-1251');

#print $counter.'<script type="text/javascript">'.$send_goal.' setTimeout(function(){yaCounter27711255.reachGoal("ORDER", yaParams); _gaq.push(["_trackEvent", "button", "ORDER", "ok"]);}, 500);</script>';
print $counter.'<script type="text/javascript">'.$send_goal.' setTimeout(function(){yaCounter27711255.reachGoal("ORDER", yaParams);}, 1000);</script>';

use Core::DB::Goals;
my $goal = new Core::DB::Goals();

	my %params = (
		'goal' => 'ORDER',
		'referrer' => cookie("set_referrer"),
		'start_url' => cookie("set_start_url"),
		'user_agent' => $ENV{HTTP_USER_AGENT},
		'ip' => $ENV{'REMOTE_ADDR'},
		'order_id' => $order_id
	);	
	if (cookie("come_city")){
		%params = (%params,
			'city' => uri_unescape(cookie("come_city"))
		);
	}	
	$goal->add(\%params);
	
	use LWP::UserAgent;
	my $ua = LWP::UserAgent->new;
	$ua->timeout(10);
	my $response = $ua->get('http://'.$ENV{"HTTP_HOST"}.'/admin/scripts/stat/sourceOrders.php?lastOrder=true');

} else {}



