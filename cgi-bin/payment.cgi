#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Digest::MD5 qw(md5_hex);
use Core::Config;
use Core::DB;
use Core::DB::Work;
use Core::DB::Catalog;
use Encode "from_to";

my $db = new Core::DB();

my $action = param("action");
my $orderSumAmount = param("orderSumAmount");
my $orderSumCurrencyPaycash = param("orderSumCurrencyPaycash");
my $orderSumBankPaycash = param("orderSumBankPaycash");
my $shopId = param("shopId");
my $invoiceId = param("invoiceId");
my $shopPassword = "shop1235741";

my $orderSession = param("orderSession");
my $paymentType = param("paymentType");
my $customerNumber = param("customerNumber");
my $user_id = param('user_id');
my $totalcena = param('custTotalcena');
my $delivery = param('custDelivery');
my $custName = param('custName');
my $custNameF = param('custNameF');
my $email = param('custEMail');
my $city = param('custCity');
my $index = param('custIndex');
my $address = param('custAddr');
my $text = param('orderDetails');

from_to($totalcena, "utf-8", "cp1251");
from_to($delivery, "utf-8", "cp1251");
from_to($custName, "utf-8", "cp1251");
from_to($custNameF, "utf-8", "cp1251");
from_to($email, "utf-8", "cp1251");
from_to($city, "utf-8", "cp1251");
from_to($index, "utf-8", "cp1251");
from_to($address, "utf-8", "cp1251");
from_to($text, "utf-8", "cp1251");

my $code = 1;
my $md5 = Core::DB::Work::upperString(md5_hex($action.';'.$orderSumAmount.';'.$orderSumCurrencyPaycash.';'.$orderSumBankPaycash.';'.$shopId.';'.$invoiceId.';'.$customerNumber.';'.$shopPassword));

if ($md5 eq param("md5")){$code = 0;}

#open OUT, (">>payment.txt");
#my @params = param();
#foreach my $item(@params){
#	print OUT $item." => ".param($item)."\n";
#}
#print OUT "md5_ => ".$md5."\n";
#close(OUT);

my ($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
if ($mday < 10 ) {$mday ="0".$mday;}
if ($hour < 10 ) {$hour ="0".$hour;}
if ($min < 10 ) {$min ="0".$min;}
if ($sec < 10 ) {$sec ="0".$sec;}
$mon++; if ($mon < 10) {$mon ="0".$mon;}
$year=1900+$year; 
my $today="$year-$mon-$mday\T$hour:$min:$sec";

if ($action eq "checkOrder"){
	print header(-type => 'xml', -charset => 'utf-8');
	print '<?xml version="1.0" encoding="UTF-8"?>
<checkOrderResponse performedDatetime="'.$today.'.000+04:00" code="'.$code.'" invoiceId="'.$invoiceId.'" shopId="'.$shopId.'"/>';
}
elsif ($action eq "paymentAviso"){

	print header(-type => 'xml', -charset => 'utf-8');
	print '<?xml version="1.0" encoding="UTF-8"?>
<paymentAvisoResponse performedDatetime="'.$today.'.000+04:00" code="'.$code.'" invoiceId="'.$invoiceId.'" shopId="'.$shopId.'"/>';
	
	if ($code eq "0"){	
	
		open OUT, (">>payment.txt");
			print OUT "$action $customerNumber $invoiceId $today\n";
		close(OUT);
	
		my $order_id="";
		my $result = $db->query("SELECT id FROM cat_orders WHERE ".(param('paymentOrder')?"id = '".param('paymentOrder')."'":"phone = '".$customerNumber."'")." AND pay != '1' ORDER BY id DESC LIMIT 1");
		if ($result){
			foreach my $order(@$result){
				$order_id = $order->{id};
				$db->update("UPDATE cat_orders SET `pay` = '1', payment = '".$paymentType."', invoiceId = '".$invoiceId."', totalPayment = '".$orderSumAmount."', datePayment = NOW() WHERE id='".$order_id."'");
			}		
		}
		else {

			my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'cat_orders';");
			foreach my $item(@$result){	
				$order_id = $item->{Auto_increment};
			}		
	
			use URI::Escape;
			
			my $ch_region="";
			if ($delivery eq "1" or $delivery eq "2"){
				$ch_region = "1";
			}	
			elsif ($delivery eq "3"){
				$ch_region = "2";
			}
			
			my $orders = new Core::DB::Catalog();
			my %params = (
				'order_date' => "NOW()",
				'user_id' => "$user_id",
				'name' => "$custName $custNameF",
				'phone' => "$customerNumber",
				'ch_region' => "$ch_region",
				'city' => "$city",
				'index' => "$index",			
				'address' => "$address",
				'metro' => "",				
				'email' => "$email",
				'comments' => "$text",
				'delivery' => "$delivery",
				'delivery_price' => "",
				'manager' => "",			
				'status' => "0",
				'pay' => "1",
				'payment' => "$paymentType",
				'datePayment' => "NOW()",
				'invoiceId' => "$invoiceId",
				'total' => "$totalcena",
				'totalPayment' => "$orderSumAmount"
			);
			$orders->addOrder(\%params);
			
			while ($orderSession =~ m/(\d+)[:](\d+)[=]*(\d+[.]\d+)*\|/g){
				my $article = $1;
				my $count = $2;
				my $price = $3;
				my $result = $db->query("SELECT p_name FROM products_alright WHERE p_art ='".$article."'");
				if (!$result){
					$result = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$article."'");
				}
				if ($result){
					foreach my $line(@$result){
						my %params_product = (
							'order_id' => "$order_id",
							'p_art' => "$article",
							'p_name' => "$line->{'p_name'}",
							'p_price' => "$price",
							'p_price_value' => "$price",
							'p_count' => "$count"
						);
						$orders->addOrderProduct(\%params_product);
					}
				}				
			}
			
			require "admin/engine/lib/parametr.cgi";
			
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
				print MZ "От: <b>$custName $custNameF</b><br><br>\n";
				print MZ "Телефон: <b>$customerNumber</b><br><br>\n";
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

				while ($orderSession =~ m/(\d+)[:](\d+)[=]*(\d+[.]\d+)*\|/g){
					my $article = $1;
					my $count = $2;
					my $price = $3;

					my $result = $db->query("SELECT p_name FROM products_alright WHERE p_art ='".$article."'");
					if (!$result){
						$result = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$article."'");
					}	
					foreach my $line(@$result){	
						print MZ "
						   <tr>\n
							  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\"><b>".$article."</b> ".$line->{'p_name'}."</td>\n
							  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$price."</td>\n
							  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$count."</td>\n
						   </tr>\n";
					}
				}

				print MZ "</table><br>\n";
				print MZ "<b>Заказ оплачен на сумму:</b> <b style='color:#A60000;'>$orderSumAmount руб.</b>\n";
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
			print MC "Здравствуйте, <b>$custName</b>.<br><br>";
			print MC "Ваш заказ <b><u>№$order_id</u></b>, принят.<br><br>";
			print MC "Спасибо, за Ваш заказ.<br> Наш менеджер, в ближайшее время свяжется с Вами.<br><br>";
			print MC "</td>
			<td style='border:1px dotted #999; width:400px; padding:20px 20px 60px 30px; font:normal 14px Tahoma, Helvetica; vertical-align:top; background: url(http://uplecms.ru/img/logo_order.png) bottom right no-repeat;'>\n";
			print MC "<table style='width:400px; font-size:13px; border-collapse:collapse;'><tr><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Товар</b></td><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Цена</b></td><td style='border:1px solid #ccc; padding:2px 5px 4px 5px;' align='center'><b>Кол-во</b></td></tr>";

			while ($orderSession =~ m/(\d+)[:](\d+)[=]*(\d+[.]\d+)*\|/g){
				my $article = $1;
				my $count = $2;
				my $price = $3;

				my $result = $db->query("SELECT p_name FROM products_alright WHERE p_art ='".$article."'");
				if (!$result){
					$result = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$article."'");
				}
				foreach my $line(@$result){	
					print MC "
					   <tr>\n
						  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\"><b>".$article."</b> ".$line->{'p_name'}."</td>\n
						  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$price."</td>\n
						  <td style=\"border:1px solid #ccc; padding:2px 5px 4px 5px;\" align=\"center\">".$count."</td>\n
					   </tr>\n";
				}
			}

			print MC "</table><br>\n";
			print MC "<b>Заказ оплачен на сумму:</b> <b style='color:#A60000;'>".$orderSumAmount." руб.</b>\n";
			print MC "</td></tr></table>\n";
			close (MC);				
			
			use Core::DB::Goals;
			my $goal = new Core::DB::Goals();

			my %params = (
				'goal' => 'ORDER',
				'referrer' => cookie("set_referrer"),
				'start_url' => cookie("set_start_url"),
				'user_agent' => $ENV{'HTTP_USER_AGENT'},
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
		}
	}
}
elsif (param("result") eq "success" && $code eq "0"){

	use CGI::Session;
	
	$session = CGI::Session->load();
	$session->param('ids',"");
	$session->flush();

	require "templates/connection/require.cgi";
	use CGI::FastTemplate;
	
	$tpl = new CGI::FastTemplate("admin/$dirs/"); 
		$tpl->define( index     => "maket_html.2",
	);

	require "templates/connection/variables.cgi";	

	print header(-charset => 'windows-1251');
	
	$title = 'Статус заказа / LEDTOP-SHOP.ru';
	$name = '<div class="title"><h1>Заказ оплачен</h1></div>';
	$content = '<div class="content-holder content-text">
		<p>Мы поздравляем, ваш заказ успешно оплачен!</p><br><p style="text-align:center">В ближайшее время мы свяжемся с вами для уточнения деталей заказа.</p>
	</div>';
	
	require "templates/connection/variables_assign.cgi";

	$tpl->parse(MAIN => "index");
	$tpl->print();	
}
elsif (param("pay") && param("order")){

	my $md5 = param("pay");
	my $order_id = param("order");
	
	my $result = $db->query("SELECT phone, pay, total, DATE_FORMAT(datePayment, \"%d-%m-%Y в %H:%i\") as date FROM cat_orders WHERE id = '".$order_id."'");
	my $date_payment = $result->[0]->{"date"};
	my $phone = $result->[0]->{"phone"};
	my $pay = $result->[0]->{"pay"};
	my $totalcena = $result->[0]->{"total"};
	my $totalcena_ = $totalcena;
	$totalcena_ =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;	

	if ($result && $md5 eq md5_hex($order_id.$phone)){

		require "templates/connection/require.cgi";
		use CGI::FastTemplate;
		
		$tpl = new CGI::FastTemplate("admin/$dirs/"); 
			$tpl->define( index     => "maket_html.4",
		);

		require "templates/connection/variables.cgi";	

		print header(-charset => 'windows-1251');
		
		$title = 'Счет на оплату / LEDTOP-SHOP.ru';
		$name = '<div class="title"><h1>Счет на оплату заказа #'.$order_id.'</h1></div>';
		$content = '<div class="content-holder">
			<div class="order-history">
				<div class="order-item">
					<div class="list">
						<table>
							<tbody>';
							
						my $products="";
						my $res = $db->query("SELECT * FROM cat_orders_product WHERE order_id ='".$order_id."'");
						foreach my $line(@$res){
							my $pack = $db->query("SELECT p_unit FROM products_alright WHERE p_art ='".$line->{p_art}."'");
							$products .= '
									<tr>
										<td class="name"><strong>'.$line->{p_art}.'</strong> <a target="_blank" href="/products/'.$line->{p_art}.'">'.$line->{p_name}.'</a></td>
										<td class="count"><span class="col"><b>'.$line->{p_count}.'</b> '.($pack->[0]->{"p_unit"}?$pack->[0]->{"p_unit"}.'.':'шт.').'</span> <em>&times;</em> <b class="price">'.$line->{p_price}.' руб.</b></span></td>
									</tr>';
						}
						$content .= $products.'
							</tbody>
						</table>
					</div>
					<div class="total"><strong>Итого на оплату:</strong> <span>'.$totalcena_.' руб.</span></div>
				</div>		
			</div>
			<div class="pay-wizard">';
			   
			   if ($pay eq "1"){
				   $content .= '<div class="payment-cart">
						<div class="cart-head">
							<div class="total-check">Дата оплаты: '.$date_payment.'</div>
							<div class="total-sum"><span id="total-price-invoice">'.$totalcena_.'</span><span class="curr">&nbsp;<span class="rur">р<span>уб.</span></span></span></div>
						</div>
						<div class="cart-footer"></div>
				   </div>
				   <div class="printCheck"></div>'			
			   }
			   else {
				   $content .= '<div class="payment-cart">
						<div class="cart-head">
							<div class="total-check">Сумма к оплате</div>
							<div class="total-sum"><span id="total-price-invoice">'.$totalcena_.'</span><span class="curr">&nbsp;<span class="rur">р<span>уб.</span></span></span></div>
						</div>
						<div class="cart-footer"></div>
				   </div>
				   <form id="paymentFormOrder" name="paymentFormOrder" action="https://money.yandex.ru/eshop.xml" method="post">
						<input name="shopId" value="114706" type="hidden"/>
						<input name="scid" value="44039" type="hidden"/>
						<input name="sum" value="'.$totalcena.'" type="hidden">
						<input name="customerNumber" value="'.$phone.'" type="hidden"/>
						<input name="paymentOrder" value="'.$order_id.'" type="hidden">
						<input id="form-paymentType" name="paymentType" value="PC" type="hidden"/>
						<input id="paymentButton" class="button" type="submit" value="Оплатить заказ" />
				   </form>';
			   }
			   
		$content .= '
			</div>	
			<div class="payment-block">
				<div class="payment-block-box">Поддерживаем основные виды оплат:</div>
				<div class="payment-block-items">
					<div class="item">
						<i class="icon icon1"></i>
						<span>Банковские карты</span>
						<em>Visa (включая Electron)</em>
						<em>MasterCard</em>
						<em>Maestro</em>
					</div>
					<div class="item">
						<i class="icon icon2"></i>
						<span>Электронные деньги</span>
						<em>Яндекс.Деньги</em>
						<em>WebMoney</em>
					</div>
					<div class="item">
						<i class="icon icon3"></i>
						<span>Наличные</span>
						<em>Более <a target="_blank" href="https://money.yandex.ru/pay/doc.xml?id=526209">170 тысяч пунктов</a> приема по России</em>
					</div>
					<div class="item">
						<i class="icon icon4"></i>
						<span>Баланс<br> телефона</span>
						<em>Билайн</em>
						<em>Мегафон</em>
						<em>МТС</em>
					</div>
					<div class="item">
						<i class="icon icon5"></i>
						<span>Интернет банкинг</span>
						<em>Сбербанк Онлайн</em>
						<em>Альфа.Клик</em>
					</div>					
				</div>
			</div>			
		</div>';
		
		require "templates/connection/variables_assign.cgi";

		$tpl->parse(MAIN => "index");
		$tpl->print();
	}
	else {
		print header( -status=> '404 Not found', -charset=>'windows-1251');
	}
}
else {
	print header( -status=> '404 Not found', -charset=>'windows-1251');
}

