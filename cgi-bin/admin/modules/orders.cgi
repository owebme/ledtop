
$status=param('status');
$region=param('region');
$period=param('period');

use Digest::MD5 qw(md5_hex);

my $default_city = "������-��-����";

my $cookie_status = cookie("orders_status");
my $cookie_region = cookie("orders_region");
my $cookie_period = cookie("orders_period");

if ($cookie_status ne "" && !$status){
	$status = $cookie_status;
}
if (!$status){$status = 0;}
if ($status eq "new"){$status = 0;}

if ($cookie_region ne ""){
	$region = $cookie_region;
}
else {
	if (!$region){
		$region = "all";
	}
}

if ($cookie_period ne ""){
	$period = $cookie_period;
}
else {
	if (!$period){
		$period = "all";
	}
}

$private_enter = cookie("private_enter");

if ($private_enter eq "true"){
	$new_pages .='<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients"><span>���� �������</span></a></li>';
}
$new_pages .='<li class="'.(!$private_enter?'first':'').''.(!$status?' activetab':'').'"><a data-value="0" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=new"><span>����� ������</span></a></li>
<li'.($status eq "1"?' class="activetab"':'').'><a data-value="1" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=1"><span>����������� ������</span></a></li>
<li'.($status eq "2"?' class="activetab"':'').'><a data-value="2" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=2"><span>������� �������</span></a></li>
<li'.($status eq "3"?' class="activetab"':'').'><a data-value="3" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=3"><span>�����������</span></a></li>';

if (!$private_enter){
	$new_pages .='<li class="goalsvisor"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals"><span>GoalsVisor</span></a></li>';
}

if (-e "../modules/sendmail.cgi"){
	$new_pages .=qq~<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=sendmail"><span>��������</span></a></li>~;
}


$content_html=qq~$content_html<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
			<div id="tabs" style="width:960px;">
				<ul>
					$new_pages
				</ul>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content" style="position:relative;">
		<div id="orders">
<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />
<script type="text/javascript" src="/admin/lib/orders.js?5645654764733"></script>
<script type="text/javascript" src="/admin/js/fancybox/jquery.fancybox-1.3.3.pack.js"></script>
<link rel="stylesheet" type="text/css" href="/admin/js/fancybox/jquery.fancybox-1.3.3.css" />~;

$content_html .='<div class="btn-group region">
					<a data-value="all" class="btn'.($region eq "all"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders">���</a>
					<a data-value="1" class="btn'.($region eq "1"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&region=1">'.$default_city.'</a>
					<a data-value="2" class="btn'.($region eq "2"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&region=2">�� ������</a>';
					
				if ($region eq "2"){
					$content_html .='
						<button id="dispatch1" class="btn" href="#">���������</button>
						<button id="dispatch2" class="btn" href="#">���������</button>';
				}
				
$content_html .='	
				</div>
				<div class="btn-group period">
					<a data-value="now" class="btn'.($period eq "now"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&period=now">�������</a>
					<a data-value="yesterday" class="btn'.($period eq "yesterday"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&period=yesterday">�����</a>
					<a data-value="month" class="btn'.($period eq "month"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&period=month">�����</a>
					<a data-value="all" class="btn'.($period eq "all"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=orders">���</a>
				</div>				
				<div class="clear"></div>';

	my $db = new Core::DB();
	
my $sql_period="";
if ($period eq "now"){
	$sql_period = "DATE_FORMAT(order_date, '%Y%m%d') = DATE_FORMAT(NOW(), '%Y%m%d') AND";
}
elsif ($period eq "yesterday"){
	$sql_period = "DATE_FORMAT(order_date, '%Y%m%d') = DATE_FORMAT(DATE_ADD(NOW(), interval -1 day), '%Y%m%d') AND";
}
elsif ($period eq "month"){
	$sql_period = "order_date > NOW() - INTERVAL 30 DAY AND";
}
elsif ($period eq "all"){
	$sql_period="";
}
		
	my $result = $db->query("SELECT *, DATE_FORMAT(order_date, \"%d-%m-%Y\") as orderDate, DATE_FORMAT(order_date, \"%H:%i\") as orderTime FROM cat_orders WHERE ".$sql_period." ".($region ne "all"?"ch_region ='".$region."' AND":"")." status ='".$status."' ORDER BY order_date DESC");
	if ($result){
		my $count = @$result;
		foreach my $order(@$result){
			$num++;
			$order_id = $order->{id};
				$result = $db->query("SELECT * FROM cat_orders_product WHERE order_id ='".$order->{id}."'");
				foreach my $line(@$result){
					$product_order .= '
					<div class="product" data-art="'.$line->{"p_art"}.'" data-count="'.$line->{"p_count"}.'">
						<div class="count">'.$line->{"p_count"}.' ��. <em>x</em> '.$line->{"p_price"}.' ���.</div>
						<div class="name"><a data-price="'.$line->{"p_price"}.'" data-art="'.$line->{"p_art"}.'" target="_blank" href="/products/'.$line->{"p_art"}.'">'.$line->{"p_name"}.'</a><span class="art">���: <strong>'.$line->{"p_art"}.'</strong></span></div>
						'.($order->{pay} ne "1"?'<div class="change"><span title="�������� �������">+ <em>��������</em></span><a href="#" class="edit">�������� �������</a><a class="link" target="_blank" href="/products/'.$line->{"p_art"}.'">�� ����� <em>&rarr;</em></a><ins title="������� �������"></ins></div>':'').'
					</div>';
				}
			
			my $totalcena = $order->{total};
			if (!$totalcena){$totalcena = 0;}
			else {$totalcena = price_trans($totalcena);}
			
			my $delivery_price = 0;
			my $totalcena_pay = $order->{total};
			if ($order->{delivery} eq "1"){$delivery_price = 0;}
			elsif ($order->{delivery} eq "2"){$delivery_price = 0;}
			elsif ($order->{delivery} eq "3"){$delivery_price = 300;}

			$totalcena_pay = $totalcena_pay + $delivery_price;
			$totalcena_pay = price_trans($totalcena_pay);
				
			my $name=""; my $phone=""; my $email=""; my $city=""; my $address=""; my $index=""; my $metro=""; 
			if ($order->{name} eq "") {$name="<span class='edit none'>��� �� �������</span>"} else {$name = '<span class="edit">'.$order->{name}.'</span>';}
			if ($order->{phone} eq "") {$phone="<span class='edit none'>������� �� ������</span>"} else {$phone = '<span class="edit">'.$order->{phone}.'</span>';}			
			if ($order->{email} eq "") {$email="<span class='edit none'>�� ������</span>"} else {$email = '<span class="edit">'.$order->{email}.'</span>';}	

			if ($order->{city} eq "") {$city="<span class='edit none'>����� �� ������</span>"} else {$city = '<span class="edit">'.$order->{city}.'</span>';}
			if ($order->{address} eq "") {$address="<span class='edit none'>����� �� ������</span>"} else {$address = '<span class="edit">'.$order->{address}.'</span>';}
			if ($order->{index} eq "") {$index="<span class='edit none'>������ �� ������</span>"} else {$index = '<span class="edit">'.$order->{index}.'</span>';}
			#if ($order->{metro} eq "") {$metro="<span class='edit none'>����� �� �������</span>"} else {$metro = '<span class="edit">'.$order->{metro}.'</span>';}
			if ($order->{comments} eq "") {$comments="<span class='none'>����������� �� ������</span>"} else {$comments = $order->{comments};}
			if ($order->{pay} ne "0") {$pay='class="pay" title="�������" id_pay="'.$order->{id}.'"'} else {$pay='class="pay pay_off" href="#" title="�� �������" id_pay="'.$order->{id}.'"';}
			if($order->{manager} eq "") {$manager='<div class="manager" atr="manager"><a href="#" class="add_comment">����������� ���������</a></div>'}
			else {$manager='<div class="manager active" atr="manager"><span class="edit">'.$order->{manager}.'</span></div>'} 
			$new_orders_list .= '
			<div class="container" '.($num == $count?'id="end"':'').' id_order="'.$order->{id}.'">
				<div class="order_info">
					<div class="num_order"><a href="#" '.$pay.'>����� �'.$order->{id}.'</a></div>';
			if ($region eq "all"){
				$new_orders_list .= '
					<div class="btn-group ch-region">
						<button data-value="1" class="btn'.($order->{ch_region} eq "1"?' active':'').'">'.$default_city.'</button>
						<button data-value="2" class="btn'.($order->{ch_region} eq "2"?' active':'').'">�� ������</button>
					</div>';
			}
			my $numSender = $order->{num_dispatch};
			my $num_dispatch ='<!--<div class="metro'.($order->{ch_region} eq "1"?' hide':'').'" atr="num_dispatch">����� ����: '.(!$numSender?'<span class="edit none">�������</span>':'<span class="edit">'.$numSender.'</span>').'</div>-->';
			
			$new_orders_list .= '
					<div class="date">����: <span>'.$order->{orderDate}.' � '.$order->{orderTime}.'</span></div>
					<div class="name" atr="name">���: '.($order->{user_id} > 0?'<i class="fa fa-user"></i> ':'').''.$name.'</div>
					<div class="phone" atr="phone">�������: '.$phone.'</div>
					<div class="email" atr="email">E-mail: '.$email.'</div>
					<div class="address" atr="city">�����: '.$city.'</div>
					<div class="address" atr="address">�����: '.$address.''.($order->{address} ne ""?'&nbsp;<a class="map" title="���������� ����� �� �����" target="_blank" href="http://maps.yandex.ru/?text='.$order->{address}.'"></a>':'').'</div>
					<div class="address'.($order->{ch_region} eq "1"?' hide':'').'" atr="index">������: '.$index.'</div>
					'.$num_dispatch.'
					<!--<div class="metro" atr="metro">�����: '.$metro.'</div>-->
					<div class="btn-group ch-dispatch">
						<button data-value="1" class="btn'.($order->{dispatch} eq "1"?' active':'').'">���������</button>
						<button data-value="2" class="btn'.($order->{dispatch} eq "2"?' active':'').'">���������</button>
					</div>				
					<div class="comments">�����������: '.$comments.'</div>
					'.$manager.'
				</div>
				<div class="order_product">
				'.$product_order.'
				'.($order->{pay} ne "1"?'<div class="total_price">����� � ������ &mdash; <span><em id="totalcena">'.$totalcena.'</em> + <em id="delivery_price">'.$delivery_price.'</em> = <em id="totalcena_pay">'.$totalcena_pay.'</em> ���.</span><a target="_blank" href="/payment/?pay='.md5_hex($order->{id}.$order->{phone}).'&order='.$order->{id}.'" class="getLink"><i></i>���� �� ������</a></div>':'<div class="total_price">������� �� ����� &mdash; <span><em id="totalcena">'.price_trans($order->{totalPayment}).'</em> ���.</span></div>').'
				<div class="btn-group ch-delivery">
					<button data-value="1" class="btn'.($order->{delivery} eq "1"?' active':'').'">�� ������</button>
					<button data-value="2" class="btn'.($order->{delivery} eq "2"?' active':'').'">�� �������</button>
					<button data-value="3" class="btn'.($order->{delivery} eq "3"?' active':'').'">������</button>
				</div>';
				
				if ($order->{trafic_source} ne ""){
					my $source="";
					if ($order->{trafic_source} =~ /������\.������/){
						$source = '<i class="b-engine b-coin"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /Google\.Adwords/){
						$source = '<i class="b-engine b-coin"></i>&nbsp;';
					}					
					elsif ($order->{trafic_source} =~ /������/){
						$source = '<i class="b-engine b-engine1"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /Google/){
						$source = '<i class="b-engine b-engine2"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /Mail/){
						$source = '<i class="b-engine b-engine6"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /Rambler/){
						$source = '<i class="b-engine b-engine10"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /Bing/){
						$source = '<i class="b-engine b-engine85"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /������ �����/){
						$source = '<i class="b-source b-source1"></i>&nbsp;';
					}
					elsif ($order->{trafic_source} =~ /������� � �����/){
						$source = '<i class="b-source b-source2"></i>&nbsp;';
					}					
					$new_orders_list .= '
						<div class="came_from">
							'.$source.$order->{trafic_source}.''.($order->{keyword} ne ""?' �<strong>'.$order->{keyword}.'</strong>�':'').'
						</div>';
				}
				$new_orders_list .= '
					<div class="came_device">
						<div class="came_device_wrapper">';
				if ($order->{type_device} eq "1"){
					$new_orders_list .= '<span>'.$order->{start_title}.'</span><div class="i-device"><i title="���������" class="i-mobile"></i></div>';
				}
				elsif ($order->{type_device} eq "2"){
					$new_orders_list .= '<span>'.$order->{start_title}.'</span><div class="i-device"><i title="�������" class="i-tablet"></i></div>';
				}
				elsif ($order->{type_device} eq "3"){
					$new_orders_list .= '<span>'.$order->{start_title}.'</span><div class="i-device"><i title="PC" class="i-pc"></i></div>';
				}
				$new_orders_list .= '		
						</div>
					</div>';				

				$new_orders_list .= '
				<div class="clear"></div>
				</div>';
			
			if ($status eq "0"){
				$new_orders_list .= '<div class="arrow" id_order="'.$order->{id}.'"><a href="#" class="ready">� �����������</a><a href="#" class="del">� �������</a><a href="#" class="call">�����������</a><a href="#" class="del_rel">�������</a></div>';
			}
			elsif ($status eq "1"){
				$new_orders_list .= '<div class="arrow" id_order="'.$order->{id}.'"><a href="#" class="del">� �������</a><a href="#" class="del_rel">�������</a></div>';
			}			
			elsif ($status eq "2"){
				$new_orders_list .= '<div class="arrow" id_order="'.$order->{id}.'"><a href="#" class="new">� ����� ������</a><a href="#" class="call">�����������</a><a href="#" class="del_rel">�������</a></div>';
			}
			elsif ($status eq "3"){
				$new_orders_list .= '<div class="arrow" id_order="'.$order->{id}.'"><a href="#" class="new">� ����� ������</a><a href="#" class="del">� �������</a><a href="#" class="del_rel">�������</a></div>';
			}			
				
			$new_orders_list .= '	
			</div>
			<div class="clear"></div>';
			$product_order="";
		}
	}
		
	if ($order_id eq "") {$content_html .= '<div class="orders"><div class="save_page orders">��� ������� �� ��������� ������</div></div>';}
	else {$content_html .= '<div class="orders">'.$new_orders_list.'</div>';}
		
		
$content_html.= qq~
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;


sub price_trans {
	my $price = shift;
	my $fraction = shift;
	if ($price > 0){
		if ($fraction){
			$price = sprintf("%.2f",$price);
		}
		else {
			$price = sprintf("%.0f",$price);
		}
		$price =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
	}
	else {
		$price = 0;
	}
	return $price;
}


-1;