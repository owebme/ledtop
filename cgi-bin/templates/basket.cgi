use CGI::Cookie;
use CGI::Session;

# ���� �������
open OUT, ("admin/$dirs/meta_title"); $main_title = <OUT>; close(OUT);
$title =qq~������� ������� // $main_title~;

# ��������� �������
$name =qq~<div class="title"><h1>������� �������</h1></div>~;

	
	$session = CGI::Session->load( ) or die CGI::Session->errstr();
	if ( $session->is_empty ) {
			   $session = $session->new() or die $session->errstr;
			$c = new CGI::Cookie(
					 -name	=>  $session->name,
					 -value   =>  $session->id, 
					 -domain  =>  $ENV{"HTTP_HOST"},
					 -path	=>  "/",
					 -secure  =>  0);
	}
	
$ids = $session->param('ids');
	
my %idTS;
while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
	$idTS{$1}{'cena'} = $2;
	if (!$idTS{$1}{'price'}){$idTS{$1}{'price'} = $2;}
	if($idTS{$1}{'count'}) {$idTS{$1}{'count'}++;}
	else {$idTS{$1}{'count'} = 1;}
}	

my %idTS2;
while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
	$idTS2{$1}{'cena'} = $2;
	if($idTS2{$1}{'count'}) {$idTS2{$1}{'count'}++;
	$idTS2{$1}{'cena'} = $2*$idTS2{$1}{'count'};}
	else {$idTS2{$1}{'count'} = 1;}
}

$list_orders ="";

$totalcena = 0;
while (($key, $value) = each(%idTS2)){
	$totalcena += $value->{'cena'};
}

my $db = new Core::DB();

# ������� �������

my $product_orders="";
while (($key, $value) = each(%idTS)){
	my $result = $db->query("SELECT * FROM products_alright WHERE p_art ='".$key."'");
	if ($result){
		foreach my $line(@$result){
			my $packnorm = $line->{'p_packnorm'};
			if ($packnorm =~/(\d+)\.5/){
				$packnorm = $packnorm*2;
			}
			$product_orders .= build_TemplateProduct("", $line->{'p_art'}, $line->{'p_name'}, "", "", $value->{'price'}, "", $line->{'p_desc'}, $value->{'count'}, "", 0, "", "", "basket", "", "", "", $packnorm, $line->{'p_unit'});
		}
	}
	else {
		my $result = $db->query("SELECT * FROM cat_product WHERE p_art ='".$key."'");
		foreach my $line(@$result){
			$product_orders .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, "", $value->{'price'}, "", $line->{'p_desc_sm'}, $value->{'count'}, "", 0, "", "", "basket");
		}
	}
}

if ($product_orders ne ""){$product_orders = build_ProductTags(1,0,"basket").'<div class="line"></div>'.$product_orders.'<div class="clear"></div>'.build_ProductTags(0,1,"basket");}


# ���������� ������

if ($product_orders ne "") {

my $totalcena_ = $totalcena;
$totalcena_ = sprintf("%.2f",$totalcena_);
$totalcena_ =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;

my ($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
if ($mday < 10 ) {$mday ="0".$mday;}
if ($hour < 10 ) {$hour ="0".$hour;}
if ($min < 10 ) {$min ="0".$min;}
if ($sec < 10 ) {$sec ="0".$sec;}
$mon++; if ($mon < 10) {$mon ="0".$mon;}
$year=1900+$year; 
my $today="$year-$mon-$mday\T$hour:$min:$sec";

use Digest::MD5 qw(md5_hex);

my $authLogin = "84e481b64f9955ff19d1dcd7a33b720c";
my $secure = md5_hex("$today&f6e83a2f6b273a1cbb168e1289ffd6a9");

$content='

<span id="send_info" style="display:none;"><p style="padding-left:10px">�� ���������� ��� �� ����������� ����� �� ����� �����.</p></span>

<div id="send_form">

	'.$product_orders.'
	
	<div class="order-sum">
		<div class="order-total">����� ��������� � <span id="total_price">'.$totalcena_.'</span><span> ���.</span></div>
	</div>
	
	<div class="order-delivery">
		<i></i>
		<strong>����������� ��������</strong>
		<form method="GET" id="formParamsDelivery" action="">
			<input name="senderCityId" value="44" autocomplate="off" type="hidden">
			<label><span>�����-����������:</span><input id="cityDelivery" class="input-text" type="text" value="" placeholder="������� ������� � �������� �� ������" autocomplate="off"><a id="sendParamsDelivery" href="#">����������</a></label>
			<input id="receiverCityId" name="receiverCityId" value="" autocomplate="off" type="hidden">
			<input name="version" value="1.0" hidden />
			<input name="dateExecute" value="'.$today.'" hidden />
			<input name="authLogin" value="'.$authLogin.'" hidden />
			<input name="secure" value="'.$secure.'" hidden />		
			<input name="tariffId" value="137" hidden />
			<div class="result-block">
				<label><span>��� �����, ��.</span><input class="input-text" name="goods[0].weight" type="text" data-value="3" value="3" autocomplate="off"></label>
				<label><span>����� �����, ��.</span><input class="input-text" name="goods[0].length" type="text" data-value="30" value="30" autocomplate="off"></label>
				<label><span>������ �����, ��.</span><input class="input-text" name="goods[0].width" type="text" data-value="30" value="30" autocomplate="off"></label>
				<label><span>������ �����, ��.</span><input class="input-text" name="goods[0].height" type="text" data-value="30" value="30" autocomplate="off"></label>
				<div class="order-delivery-result">
				</div>
			</div>
		</form>
	</div>
	<div class="clearfix"></div>	
	<div id="city-list">
		<h4>���� ������������� � ��������:</h4>
		<ul>
			<li><span class="red">������-��-����</span></li>
			<li><span>���������</span></li>
			<li><span>����������</span></li>
			<li><span>���������</span></li>
			<li><span>����</span></li>
			<li><span>����</span></li>
			<li><span>�������</span></li>
			<li><span>������</span></li>
			<li><span>���������</span></li>
			<li><span>������</span></li>
		</ul>
		<p>�������� �������������� �� ��� ������� ������ �� �����.<br \>��������� �������� � ����� ������� � 300 ���.</p>
	</div>';

if ($surely_register eq "1" && $logined ne "enter"){
	$content .='<p class="message"><br><br>��� ���������� ������ �������� <a href="/register/">�����������</a> ��� <a href="/auth/">���������������</a></p>';
}
else {	
	
	use URI::Escape;
	
	my $city = uri_unescape(cookie("come_city"));
	
	my $delivery = 2;
	if ($city eq "������-��-����"){$delivery = 1;}
	elsif ($city && $city ne "������-��-����"){$delivery = 3;}
	
	$content .='					
	<div class="form_order">
		<div class="title">
			<h1>���������� ������</h1>
		</div>
		<div class="content-holder basket">
			<form method="post" name="sendOrder" action="/cgi-bin/send_order.cgi" target="send">
				'.($logined eq "enter"?'<input type="hidden" value="'.$user_id.'" name="user_id">':'').'
				<table class="form">
					<tr>
						<td class="name delivery">��������:</td>
						<td>
							<div class="fake-select-wrap">
								<select name="delivery">
									<option value="3"'.($city eq "���������"?' selected':'').'>���������</option>
									<option value="3"'.($city eq "����������"?' selected':'').'>����������</option>
									<option value="3"'.($city eq "���������"?' selected':'').'>���������</option>
									<option value="3"'.($city eq "����"?' selected':'').'>����</option>
									<option value="3"'.($city eq "����"?' selected':'').'>����</option>
									<option value="3"'.($city eq "�������"?' selected':'').'>�������</option>
									<option value="3"'.($city eq "������"?' selected':'').'>������</option>
									<option value="3"'.($city eq "���������"?' selected':'').'>���������</option>
									<option value="3"'.($city eq "������"?' selected':'').'>������</option>
									<option value="1"'.($delivery eq "1"?' selected':'').'>������-��-����</option>
									<option value="2"'.($delivery eq "2"?' selected':'').'>���������� �������</option>
									<option value="3"'.($delivery eq "3"?' selected':'').'>�� ������</option>
								</select>
								<div class="fake-select wide">'.($city && $city ne "������-��-����"?'�� ������':'�� �������-��-����').'</div>
							</div>
						</td>
					</tr>				
					<tr>
						<td class="name"><span style="color:red;">*</span>���� ���:</td>
						<td class="required"><input class="name" name="NAME" value="'.($logined eq "enter"?''.$u_name.'':'').'" format=".+" notice="������� ���� ���" type="text" autocomplete="off"></td>
					</tr>
					<tr>
						<td class="name"><span style="color:red;">*</span>���� �������:</td>
						<td class="required"><input class="name" name="NAME_F" value="'.($logined eq "enter"?''.$u_name_f.'':'').'" format=".+" notice="������� ���� �������" type="text" autocomplete="off"></td>
					</tr>
					<tr>
						<td class="name"><span style="color:red;">*</span>���������� �������:</td>
						<td class="required"><input class="name" name="PHONE" value="'.($logined eq "enter"?''.$u_phone.'':'').'" format=".+" notice="������� ��� �������" type="text" autocomplete="off"></td>
					</tr>
					<tr>
						<td class="name"><span style="color:red;">*</span>E-mail:</td>
						<td class="required"><input class="name" name="EMAIL" value="'.($logined eq "enter"?''.$u_email.'':'').'" format="email" notice="������� ��� e-mail" type="text" autocomplete="off"></td>
					</tr>
					<tr class="field_city">
						<td class="name"><span style="color:red;">*</span>��� �����:</td>
						<td class="required"><input class="name" name="CITY" value="'.$city.'" type="text" format=".+" notice="������� ����� ��������" type="text" autocomplete="off"></td>
					</tr>	
					<tr class="field_index">
						<td class="name">������:</td>
						<td><input class="name" name="INDEX" value="" type="text" autocomplete="off" placeholder="���������, ���� �������� ������"></td>
					</tr>					
					<tr class="field_address">
						<td class="name"><span style="color:red;">*</span>����� ��������:</td>
						<td class="required"><textarea style="height:80px;" name="ADDRESS" format=".+" notice="������� ����� ��������" autocomplete="off"></textarea></td>
					</tr>
					<!--<tr>
						<td class="name">��������� �����:</td>
						<td><input class="name" name="METRO" value="" type="text" autocomplete="off"></td>
					</tr>-->
					<tr>
						<td class="name">�����������:</td>
						<td><textarea name="NOTE" autocomplete="off"></textarea></td>
					</tr>
					<tr>
						<td colspan="2" align="right"><input name="send" class="button right" type="submit" value="��������� ��� ������" /></td>
					</tr>
				</table>
			<iframe style="display:none; width:1px; height:1px;" name="send"></iframe>
			</form>
			<form class="form-payment" id="paymentForm" name="paymentForm" action="https://money.yandex.ru/eshop.xml" method="post">
				<input name="shopId" value="114706" type="hidden"/>
				<input name="scid" value="44039" type="hidden"/>
				<input id="form-sum" name="sum" value="'.$totalcena.'" type="hidden">
				'.($logined eq "enter"?'<input name="user_id" value="'.$user_id.'" type="hidden">':'').'
				<input id="form-totalcena" name="custTotalcena" value="'.$totalcena.'" type="hidden">
				<input id="form-delivery" name="custDelivery" value="'.$delivery.'" type="hidden">				
				<input id="form-name" name="custName" value="'.($logined eq "enter"?''.$u_name.'':'').'" type="hidden">
				<input id="form-name_f" name="custNameF" value="'.($logined eq "enter"?''.$u_name_f.'':'').'" type="hidden">
				<input id="form-phone" name="customerNumber" value="'.($logined eq "enter"?''.$u_phone.'':'').'" type="hidden"/>
				<input id="form-email" name="custEMail" value="'.($logined eq "enter"?''.$u_email.'':'').'" type="hidden">
				<input id="form-city" name="custCity" value="" type="hidden">
				<input id="form-index" name="custIndex" value="" type="hidden">
				<input id="form-address" name="custAddr" value="" type="hidden">				
				<input id="form-note" name="orderDetails" value="" type="hidden">
				<input id="form-session" name="orderSession" value="" type="hidden">
				<input id="form-paymentType" name="paymentType" value="PC" type="hidden"/>
				<input id="paymentButton" class="button green" type="submit" value="�������� �����" />	
			</form>
		</div>
	</div>
	<div class="clearfix"></div>
	'.($logined ne "enter"?'<div class="order-reg-block">��� ���������� ������ <a class="reg" id="reg" data-tag="register" href="/register/">�����������������</a> (����� ������)<br>��� <a class="auth" id="auth" data-tag="login" href="/auth/">���������������</a> ���� ������ ���� �������.</div>':'<br>').'
	<div class="payment-block">
		<div class="payment-block-box">������������ �������� ���� �����:</div>
		<div class="payment-block-items">
			<div class="item">
				<i class="icon icon1"></i>
				<span>���������� �����</span>
				<em>Visa (������� Electron)</em>
				<em>MasterCard</em>
				<em>Maestro</em>
			</div>
			<div class="item">
				<i class="icon icon2"></i>
				<span>����������� ������</span>
				<em>������.������</em>
				<em>WebMoney</em>
			</div>
			<div class="item">
				<i class="icon icon3"></i>
				<span>��������</span>
				<em>����� <a target="_blank" href="https://money.yandex.ru/pay/doc.xml?id=526209">170 ����� �������</a> ������ �� ������</em>
			</div>
			<div class="item">
				<i class="icon icon4"></i>
				<span>������<br> ��������</span>
				<em>������</em>
				<em>�������</em>
				<em>���</em>
			</div>
			<div class="item">
				<i class="icon icon5"></i>
				<span>�������� �������</span>
				<em>�������� ������</em>
				<em>�����.����</em>
			</div>					
		</div>
	</div>';
}
$content .='</div>';
} else {$content=qq~<div class="content-holder"><p style="font-size:18px">���� ������� �����</p></div>~;}


