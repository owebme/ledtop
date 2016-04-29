use Core::DB::Work;

$period=param('period');

if (!$period){$period = "now";}

my $db = new Core::DB();

$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=new"><span>Новые заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders"><span>Выполненные заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders"><span>Корзина заказов</span></a></li>
<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersStat"><span>Прибыль</span></a></li>~;

$content_html=qq~$content_html<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs">
				<ul>
					$new_pages
				</ul>
			</div>
			
			
		   <div id="buttons">
				<a style="text-indent:25px" href="http://msk.rusavtobus.ru/" id="cstmz" class="mapbox">Проложить маршрут</a>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content" style="min-height:535px; overflow:visible">
			<div id="ordersStat">
			<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />
			<script type="text/javascript" src="/admin/js/googleChartApi.js"></script>
			<script type="text/javascript" src="/admin/lib/ordersStat.js"></script>~;

my $sql = "DATE_FORMAT(order_date, '%Y%m%d') = DATE_FORMAT(NOW(), '%Y%m%d')";
if ($period eq "yesterday"){
	$sql = "DATE_FORMAT(order_date, '%Y%m%d') = DATE_FORMAT(DATE_ADD(NOW(), interval -1 day), '%Y%m%d')";
}
elsif ($period eq "week"){
	$sql = "order_date > NOW() - INTERVAL 7 DAY";
}
elsif ($period eq "month"){
	$sql = "order_date > NOW() - INTERVAL 30 DAY";
}
			
			
my $count_orders = 0; my $coming = 0; my $profit = 0; my $cost="";
my $result = $db->query("SELECT cat_orders.id, cat_orders.total FROM cat_orders WHERE ".$sql." AND status != '2' AND total > 0");
if ($result){
	$count_orders = @$result;
	foreach my $order(@$result){
		$coming += $order->{total};
		my $res = $db->query("SELECT * FROM cat_orders_product WHERE order_id='".$order->{id}."'");
		foreach my $item(@$res){
			my $product = $db->query("SELECT cat_product.p_price_cost FROM cat_product WHERE p_id='".$item->{p_id}."'");
			my $price = $product->[0]->{p_price_cost};
			$cost += $product->[0]->{p_price_cost};
			$profit += ($item->{p_price}-$price)*$item->{p_count};
		}
	}
}	

my $expense = 0;
my $ua = LWP::UserAgent->new;
$ua->timeout(10);
my $response = $ua->get('http://'.$ENV{"HTTP_HOST"}.'/admin/scripts/stat/yadirect.php?getExpense=true&period='.$period);
if ($response->is_success && $response->content > 0){$expense = $response->content;}

$profit = $profit-$expense;

my $roi = 0;
if ($expense > 0){
	$roi = sprintf("%.0f",((($coming-$cost)/$expense)*100));
}
$roi = '<p>ROI: <strong style="color:#76A7FA">'.$roi.'%</strong></p>';	
			
$content_html .="
			<script type='text/javascript'>
				google.load('visualization', '1', {packages:['corechart']});
				google.setOnLoadCallback(drawChart);
				function drawChart() {
				var data = google.visualization.arrayToDataTable([";
				
if ($period eq "now" or $period eq "yesterday"){
$content_html .="
				  ['Element', 'Рублей', { role: 'style' }],
				  ['Приход', ".$coming.", 'stroke-color: #EC6700; stroke-opacity: 0.6; stroke-width: 2; fill-color: #EC6700; fill-opacity: 0.35'],
				  ['Прибыль', ".$profit.", 'stroke-color: #769B1A; stroke-opacity: 0.6; stroke-width: 2; fill-color: #769B1A; fill-opacity: 0.35'],
				  ['Реклама', ".$expense.", 'stroke-color: #BE4B42; stroke-opacity: 0.6; stroke-width: 2; fill-color: #BE4B42; fill-opacity: 0.35']
				]);
				var options = {
					legend: { position: 'none' }
				};
					var chart = new google.visualization.ColumnChart(document.getElementById('graph-wrapper'));
					chart.draw(data, options);
				}";
}
else {

	my $field=""; my $coming = 0;
	my $result = $db->query("SELECT cat_orders.id, cat_orders.total, cat_orders.order_date, DATE_FORMAT(order_date, \"%Y-%m-%d\") as order_date_normal FROM cat_orders WHERE ".$sql." AND status != '2' AND total > 0 ORDER BY order_date ASC");
	if ($result){
		my $date=""; my $i=""; my $count = @$result;
		foreach my $order(@$result){
			$i++;
			if ($date ne $order->{order_date_normal} && $i ne "1" or $i eq $count){
				if ($i eq $count){$date = $order->{order_date_normal};}
				$field .= "['".$date."', ".($coming+$order->{total}).", 'stroke-color: #EC6700; stroke-opacity: 0.6; stroke-width: 2; fill-color: #EC6700; fill-opacity: 0.35'],\n";
				$coming = 0;
			}
			$coming += $order->{total};
			$date = $order->{order_date_normal};
		}
	}

$content_html .="
				  ['Element', 'Приход', { role: 'style' }],
				  ".$field."
				]);	
				var options = {
					legend: { position: 'in' },
					curveType: 'function',
					colors: ['#EC6700']
				};";
				
if ($period eq "week"){
$content_html .="				
					var chart = new google.visualization.ColumnChart(document.getElementById('graph-wrapper'));";
}
elsif ($period eq "month"){
$content_html .="				
					var chart = new google.visualization.LineChart(document.getElementById('graph-wrapper'));";
}	
$content_html .="			
					chart.draw(data, options);
				}";
}
$content_html .="				
			</script>";

if ($coming > 999){
	$coming =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
}
if ($profit > 999){
	$profit =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
}
if ($expense > 999){
	$expense =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
}

my $ids="";
my $result = $db->query("SELECT p.* FROM cat_orders_product AS p JOIN cat_orders AS r ON(r.id=p.order_id) WHERE r.status != '2' AND r.total > 0");
if ($result){
	foreach my $item(@$result){
		$ids .= "|".$item->{p_id}.'='.$item->{p_name}.'='.$item->{p_count};
	}
}
	
my %sales; my $counts="";
while($ids =~ m/\|(\d+)=(.+?)=(\d+)/g){
	$sales{$1}{'id'} = $1;
	$sales{$1}{'name'} = $2;
	if ($sales{$1}{'count'}) {
		$sales{$1}{'count'} = $sales{$1}{'count'}+$3;
		$counts += $3; 
	}
	else {$sales{$1}{'count'} = 1; $counts += 1;}
}

my $products=""; my %hash = (); my $all = keys %sales;
while (($key, $value) = each(%sales)){
	my $proc = sprintf("%.1f",($value->{'count'}/$counts*100));
	%hash = (%hash, $value->{'name'} => {proc => $proc, count => $value->{'count'}},);
}
my $num="";
foreach my $key (sort {$hash{$b}->{proc} <=> $hash{$a}->{proc}} keys %hash) {
	$num++;
	$products .='<li>'.$key.' &mdash; <span>'.$hash{$key}->{proc}.'%</span> <em>('.$hash{$key}->{count}.' шт.)</em></li>';
	if ($num eq "10"){
		$products .='</ul><a href="#" class="opener">Показать все</a><ul style="display:none">';
	}
}
if ($products){
	$products ='<ul>'.$products.'</ul>';
}		
		
$content_html .='
			<div class="stat-period">
				<div class="btn-group">
					<a class="btn'.($period eq "now"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersStat&period=now">Сегодня</a>
					<a class="btn'.($period eq "yesterday"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersStat&period=yesterday">Вчера</a>
					<a class="btn'.($period eq "week"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersStat&period=week">Неделя</a>
					<a class="btn'.($period eq "month"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersStat&period=month">Месяц</a>
				</div>
			</div>
			<div class="stat-graph">
				<div class="graph-container">
					<div id="graph-wrapper">					
					</div>
				</div>
				<div class="stat-products">
					<h3>Заказали за все время</h3>
					<div class="stat-products-counts">Всего: <strong>'.$counts.' шт.</strong></div>
					'.$products.'
				</div>
			</div>
			<div class="stat-tabRight">
				<div class="stat-traffic">
					'.$roi.'
				</div>	
				<div class="stat-direct">
				</div>
			</div>
			<div class="clear"></div>
			<div class="stat-blocks">
				<div class="item one">
					<span>'.$count_orders.'</span>
					<em>Заказов</em>
				</div>
				<div class="item two">
					<span>'.$profit.'</span>
					<i>руб.</i>
					<em class="abs">Прибыль</em>
				</div>
				<div class="item three">
					<span>'.$expense.'</span>
					<i>руб.</i>
					<em class="abs">Реклама</em>
				</div>
			</div>';
		
		
$content_html.= qq~
			</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;

-1;