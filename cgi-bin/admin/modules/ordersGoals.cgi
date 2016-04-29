use Core::DB::Work;
use URI::Escape;
use Encode "from_to";

$period=param('period');
$method=param('method');

if (!$period){$period = "today";}

my $db = new Core::DB();

$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=new"><span>Новые заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=1"><span>Выполненные заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=2"><span>Корзина заказов</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=3"><span>Перезвонить</span></a></li>
<li class="goalsvisor activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals"><span>GoalsVisor</span></a></li>~;

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
		<div id="content" style="min-height:535px; overflow:visible">
			<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />
			<div id="goalsVisor">~;
			
			my $params="";
			if ($method eq "direct"){$params ="&method=direct";}
			elsif ($method eq "bodyclick"){$params ="&method=bodyclick";}
			elsif ($method eq "visitweb"){$params ="&method=visitweb";}
			
			$content_html .='
				<div class="btn-group left">
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals" class="btn'.(!$method?' active':'').'">Цели</a>
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&method=direct" class="btn'.($method eq "direct"?' active':'').'">Яндекс.директ</a>
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&method=bodyclick" class="btn'.($method eq "bodyclick"?' active':'').'">BodyClick</a>
					<a href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&method=visitweb" class="btn'.($method eq "visitweb"?' active':'').'">VisitWeb</a>
				</div>
				<div class="btn-group period">
					<a class="btn'.($period eq "today"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals'.$params.'">Сегодня</a>
					<a class="btn'.($period eq "yesterday"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&period=yesterday'.$params.'">Вчера</a>
					<a class="btn'.($period eq "week"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&period=week'.$params.'">Неделя</a>
					<a class="btn'.($period eq "2week"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&period=2week'.$params.'">2 недели</a>
					<a class="btn'.($period eq "month"?' active':'').'" href="/cgi-bin/admin/engine/index.cgi?adm_act=ordersGoals&period=month'.$params.'">Месяц</a>
				</div>';
				
	my $sql = "DATE_FORMAT(date_goal, '%Y%m%d') = DATE_FORMAT(NOW(), '%Y%m%d')";

	if ($period eq "yesterday"){
		$sql = "DATE_FORMAT(date_goal, '%Y%m%d') = DATE_FORMAT(DATE_ADD(NOW(), interval -1 day), '%Y%m%d')";
	}
	elsif ($period eq "week"){
		$sql = "date_goal > NOW() - INTERVAL 7 DAY";
	}
	elsif ($period eq "2week"){
		$sql = "date_goal > NOW() - INTERVAL 14 DAY";
	}	
	elsif ($period eq "month"){
		$sql = "date_goal > NOW() - INTERVAL 30 DAY";
	}				

if (!$method){
				
	my %hash=();
	my $result = $db->query("SELECT goals.ip, goals.date_goal, DATE_FORMAT(date_goal, \"%Y%m%d%H%i%s\") as pos, DATE_FORMAT(date_goal, \"%Y%m%d\") as date FROM goals ".($period ne "all"?'WHERE '.$sql.'':'')." ORDER BY `ip` DESC");
	if ($result){
		foreach my $item(@$result){
			#if ($item->{ip} eq "5.228.34.93"){next;}
			if ($hash{$item->{ip}}->{date} ne $item->{date}){
				%hash = (%hash, $item->{ip} => {date => $item->{date}, pos => $item->{pos}});
			}
		}
	}

	my $goals=""; my $domen = $ENV{'HTTP_HOST'}; $domen =~ s/2//g;
	foreach my $key (sort {$hash{$b}->{pos} <=> $hash{$a}->{pos}} keys %hash) {
		my $num=""; my $from=""; my $goal="";
		my $result = $db->query("SELECT *, DATE_FORMAT(date_goal, \"%H:%i\") as time, DATE_FORMAT(date_goal, \"%d-%m-%Y\") as date FROM goals WHERE ip = '".$key."' AND DATE_FORMAT(date_goal, '%Y%m%d') = '".$hash{$key}->{date}."' ORDER BY date_goal ASC");
		my $counts = @$result;
		foreach my $item(@$result){
			$num++; 
			if ($num eq "1"){
				my $city = $item->{city};
				my $referrer = $item->{referrer};
				my $keyword = getComeKeyword($referrer, $url);
				if (!$keyword){
					if (!$referrer or $item->{referrer} =~ $domen or $item->{referrer} eq "start_url"){$keyword = "<em>Прямой заход</em>";}
					else {
						$keyword = $item->{referrer}."/1";
						while ($keyword =~ m/http:\/\/(.*?)\/(.*)/g) {
							$keyword = '<strong style="font-style:normal">'.$1.'</strong>';
						}
					}
				}
				else {$keyword =~ s/\+/ /g;
					$keyword = '«<strong>'.$keyword.'</strong>»';
				}	
				if (length($keyword) > 120){$keyword="";}
				my $c = $city;
				from_to($city, "utf-8", "cp1251");			
				if ($city =~/\?/){$city = $c;}
				my ($title, $engine) = getComeEngine($referrer);
				my $url = getStartUrl($item->{start_url});
				if ($keyword =~/Прямой заход/){
					$engine="";
				}
				$keyword =~ s/\/1$//g;
				$keyword =~ s/\/$//g;
				$keyword =~ s/^https?:\/\///g;
				$from = '
					<div class="goalsEngine '.$engine.'">
						<i title="'.$title.'"></i>
						<span>'.$keyword.'<em>'.$city.'</em></span>
					</div>';
				if ($url){
					$from .= '<a target="blank" class="link" href="'.$url.'">'.($url eq "/"?'Главная':''.$url.'').'</a>';
				}
			}
			my $date="";
			if ($period eq "week" or $period eq "2week" or $period eq "month"){
				my ($day, $mouth, $year) = split(/\-/, $item->{date});
				if ($mouth eq "01") {$mouth = "янв";}
				if ($mouth eq "02") {$mouth = "фев";}
				if ($mouth eq "03") {$mouth = "мар";}
				if ($mouth eq "04") {$mouth = "апр";}
				if ($mouth eq "05") {$mouth = "мая";}
				if ($mouth eq "06") {$mouth = "июн";}
				if ($mouth eq "07") {$mouth = "июл";}
				if ($mouth eq "08") {$mouth = "авг";}
				if ($mouth eq "09") {$mouth = "сен";}
				if ($mouth eq "10") {$mouth = "окт";}
				if ($mouth eq "11") {$mouth = "ноя";}
				if ($mouth eq "12") {$mouth = "дек";}
				$date = $day.' '.$mouth.' в ';			
			}
			$goal .='<ins></ins>
				<div class="goalItem '.$item->{goal}.'">
					<i></i>
					<span>'.($item->{goal} eq "ORDER"?'Заказ №'.$item->{order_id}.'':''.getNameGoal($item->{goal}).'').'</span>
					<em>'.$date.''.$item->{time}.'</em>
				</div>';
		}
		if ($goal){
			$goals .= '<li>'.$from.'<div class="goalsContainer">'.$goal.'</div></li>';
		}
	}

	if ($goals){
		$goals ='<ul class="goalsWay">'.$goals.'</ul>';
	}

	$content_html .= $goals;
}
elsif ($method eq "direct"){

	my $table .='<table class="table table-bordered">';
	$table .='<thead>';
	$table .='<th class="th1">Компании</th>';
	$table .='<th class="th2">Поиск/клик</th>';
	$table .='<th class="th3">РСЯ/клик</th>';
	$table .='<th class="th4">Целей</th>';
	$table .='<th class="th5">Телефон</th>';
	$table .='<th class="th6">В корзину</th>';
	$table .='<th class="th7">Заказов</th>';
	$table .='<th class="th8">Прибыль</th>';
	$table .='</thead>';
	$table .='</tbody>';
	my $result=""; my $profit_all=""; my $expense_all=""; my $click_all="";
	my $res = $db->query("SELECT * FROM stat_campaigns WHERE period = '".$period."' ORDER BY active DESC");
	if (@$res > 0){
		foreach my $item(@$res){
			$result .='<tr'.(!$item->{active}?' class="hide"':'').'>';
			$result .='<td class="name">'.$item->{name}.'</td>';
			$result .='<td>'.($item->{price_search} > 0?'<span>-'.$item->{price_search}.' руб.</span> / <strong>'.$item->{click_search}.'</strong>':'').'</td>';
			$result .='<td>'.($item->{price_context} > 0?'<span>-'.$item->{price_context}.' руб.</span> / <strong>'.$item->{click_context}.'</strong>':'').'</td>';
			$result .='<td>'.($item->{goals} > 0?'<strong class="num goals">'.$item->{goals}.'</strong>':'').'</td>';
			$result .=''.($item->{phone} > 0?'<td class="orange"><strong class="num orange">'.$item->{phone}.'</strong>':'<td>').'</td>';
			$result .=''.($item->{basket} > 0?'<td class="green"><strong class="num green">'.$item->{basket}.'</strong>':'<td>').'</td>';
			$result .='<td>'.($item->{orders} > 0?'<strong class="num orders">'.$item->{orders}.'</strong>':'').'</td>';
			$click_all = $click_all+$item->{click_search}+$item->{click_context};
			my $profit = $item->{profit}-$item->{price_search}-$item->{price_context};
			$profit_all = $profit_all+$profit;
			$profit =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
			if ($profit < 0){
				$profit = '<strong class="profit red">'.$profit.' руб.</strong>';
			}
			elsif ($profit > 0){
				$profit = '<strong class="profit green">+'.$profit.' руб.</strong>';
			}		
			$result .='<td>'.($profit?''.$profit.'':'').'</td>';
			$result .='</tr>';
			$expense_all = $expense_all-$item->{price_search}-$item->{price_context};
		}
		$expense_all =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
		$profit_all =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
		if ($profit_all < 0){
			$profit_all = '<strong class="profit red">'.$profit_all.' руб.</strong>';
		}
		elsif ($profit_all > 0){
			$profit_all = '<strong class="profit green">+'.$profit_all.' руб.</strong>';
		}			
		$table .='<tr><td></td><td><span>'.$expense_all.' руб.</span> / <strong>'.$click_all.'</strong></td><td></td><td></td><td></td><td></td><td></td><td>'.$profit_all.'</td></tr>';
		$table .= $result;
	}
	else {
		$table .='<tr><td colspan="8" class="center">Нет данных за выбранный период</td></tr>';
	}
	$table .='</tbody>';
	$table .='</table>';
	
	$content_html .= $table;	
}
elsif ($method eq "bodyclick"){
				
	my %hash=();
	my $result = $db->query("SELECT goals.ip, goals.date_goal, DATE_FORMAT(date_goal, \"%Y%m%d%H%i%s\") as pos, DATE_FORMAT(date_goal, \"%Y%m%d\") as date FROM goals ".($period ne "all"?'WHERE '.$sql.' AND start_url LIKE "%tclick%"':'WHERE start_url LIKE "%tclick%"')." ORDER BY `ip` DESC");
	if ($result){
		foreach my $item(@$result){
			if ($hash{$item->{ip}}->{date} ne $item->{date}){
				%hash = (%hash, $item->{ip} => {date => $item->{date}, pos => $item->{pos}});
			}
		}
	}

	my $goals=""; my $domen = $ENV{'HTTP_HOST'}; $domen =~ s/2//g;
	foreach my $key (sort {$hash{$b}->{pos} <=> $hash{$a}->{pos}} keys %hash){
		my $num=""; my $from=""; my $goal="";
		my $result = $db->query("SELECT *, DATE_FORMAT(date_goal, \"%H:%i\") as time, DATE_FORMAT(date_goal, \"%d-%m-%Y\") as date FROM goals WHERE ip = '".$key."' AND DATE_FORMAT(date_goal, '%Y%m%d') = '".$hash{$key}->{date}."' ORDER BY date_goal ASC");
		my $counts = @$result;
		foreach my $item(@$result){
			$num++; 
			if ($num eq "1"){
				my $city = $item->{city};
				my $referrer = $item->{referrer};
				my $keyword = getComeKeyword($referrer, $url);
				if (!$keyword){
					$keyword = $item->{referrer}."/1";
					while ($keyword =~ m/http:\/\/(.*?)\/(.*)/g) {
						$keyword = '<strong style="font-style:normal">'.$1.'</strong>';
					}
				}
				else {$keyword =~ s/\+/ /g;
					$keyword = '«<strong>'.$keyword.'</strong>»';
				}
				if (length($keyword) > 120){$keyword="";}
				my $c = $city;
				from_to($city, "utf-8", "cp1251");			
				if ($city =~/\?/){$city = $c;}
				my ($title, $engine) = getComeEngine($referrer);
				my $url = getStartUrl($item->{start_url});
				my $place = getTizerPlace($item->{start_url});
				$from = '
					<div class="goalsEngine '.$engine.'">
						<i></i>
						<span>'.$keyword.'<em>'.$city.''.($place?' &mdash; '.$place.'':'').'</em></span>
					</div>';
				if ($url){
					$from .= '<a target="blank" class="link" href="'.$url.'">'.($url eq "/"?'Главная':''.$url.'').'</a>';
				}
			}
			my $date="";
			if ($period eq "week" or $period eq "2week" or $period eq "month"){
				my ($day, $mouth, $year) = split(/\-/, $item->{date});
				if ($mouth eq "01") {$mouth = "янв";}
				if ($mouth eq "02") {$mouth = "фев";}
				if ($mouth eq "03") {$mouth = "мар";}
				if ($mouth eq "04") {$mouth = "апр";}
				if ($mouth eq "05") {$mouth = "мая";}
				if ($mouth eq "06") {$mouth = "июн";}
				if ($mouth eq "07") {$mouth = "июл";}
				if ($mouth eq "08") {$mouth = "авг";}
				if ($mouth eq "09") {$mouth = "сен";}
				if ($mouth eq "10") {$mouth = "окт";}
				if ($mouth eq "11") {$mouth = "ноя";}
				if ($mouth eq "12") {$mouth = "дек";}
				$date = $day.' '.$mouth.' в ';			
			}
			$goal .='<ins></ins>
				<div class="goalItem '.$item->{goal}.'">
					<i></i>
					<span>'.($item->{goal} eq "ORDER"?'Заказ №'.$item->{order_id}.'':''.getNameGoal($item->{goal}).'').'</span>
					<em>'.$date.''.$item->{time}.'</em>
				</div>';
		}
		if ($goal){
			$goals .= '<li>'.$from.'<div class="goalsContainer">'.$goal.'</div></li>';
		}
	}

	if ($goals){
		$goals ='<ul class="goalsWay">'.$goals.'</ul>';
	}

	$content_html .= $goals;
}
elsif ($method eq "visitweb"){
				
	my %hash=();
	my $result = $db->query("SELECT goals.ip, goals.date_goal, DATE_FORMAT(date_goal, \"%Y%m%d%H%i%s\") as pos, DATE_FORMAT(date_goal, \"%Y%m%d\") as date FROM goals ".($period ne "all"?'WHERE '.$sql.' AND start_url LIKE "%vclick%"':'WHERE start_url LIKE "%vclick%"')." ORDER BY `ip` DESC");
	if ($result){
		foreach my $item(@$result){
			if ($hash{$item->{ip}}->{date} ne $item->{date}){
				%hash = (%hash, $item->{ip} => {date => $item->{date}, pos => $item->{pos}});
			}
		}
	}

	my $goals=""; my $domen = $ENV{'HTTP_HOST'}; $domen =~ s/2//g;
	foreach my $key (sort {$hash{$b}->{pos} <=> $hash{$a}->{pos}} keys %hash){
		my $num=""; my $from=""; my $goal="";
		my $result = $db->query("SELECT *, DATE_FORMAT(date_goal, \"%H:%i\") as time, DATE_FORMAT(date_goal, \"%d-%m-%Y\") as date FROM goals WHERE ip = '".$key."' AND DATE_FORMAT(date_goal, '%Y%m%d') = '".$hash{$key}->{date}."' ORDER BY date_goal ASC");
		my $counts = @$result;
		foreach my $item(@$result){
			$num++; 
			if ($num eq "1"){
				my $city = $item->{city};
				my $referrer = $item->{referrer};
				my $keyword = getComeKeyword($referrer, $url);
				if (!$keyword){
					$keyword = $item->{referrer}."/1";
					while ($keyword =~ m/http:\/\/(.*?)\/(.*)/g) {
						$keyword = '<strong style="font-style:normal">'.$1.'</strong>';
					}
				}
				else {$keyword =~ s/\+/ /g;
					$keyword = '«<strong>'.$keyword.'</strong>»';
				}
				if (length($keyword) > 120){$keyword="";}
				my $c = $city;
				from_to($city, "utf-8", "cp1251");			
				if ($city =~/\?/){$city = $c;}
				my ($title, $engine) = getComeEngine($referrer);
				my $url = getStartUrl($item->{start_url});
				my ($place, $id) = getTizerPlace($item->{start_url});
				$from = '
					<div class="goalsEngine '.$engine.'">
						<i></i>
						<span><strong>ID '.$id.'</strong><em>'.$city.''.($place?' &mdash; '.$place.'':'').'</em></span>
					</div>';
				if ($url){
					$from .= '<a target="blank" class="link" href="'.$url.'">'.($url eq "/"?'Главная':''.$url.'').'</a>';
				}
			}
			my $date="";
			if ($period eq "week" or $period eq "2week" or $period eq "month"){
				my ($day, $mouth, $year) = split(/\-/, $item->{date});
				if ($mouth eq "01") {$mouth = "янв";}
				if ($mouth eq "02") {$mouth = "фев";}
				if ($mouth eq "03") {$mouth = "мар";}
				if ($mouth eq "04") {$mouth = "апр";}
				if ($mouth eq "05") {$mouth = "мая";}
				if ($mouth eq "06") {$mouth = "июн";}
				if ($mouth eq "07") {$mouth = "июл";}
				if ($mouth eq "08") {$mouth = "авг";}
				if ($mouth eq "09") {$mouth = "сен";}
				if ($mouth eq "10") {$mouth = "окт";}
				if ($mouth eq "11") {$mouth = "ноя";}
				if ($mouth eq "12") {$mouth = "дек";}
				$date = $day.' '.$mouth.' в ';			
			}
			$goal .='<ins></ins>
				<div class="goalItem '.$item->{goal}.'">
					<i></i>
					<span>'.($item->{goal} eq "ORDER"?'Заказ №'.$item->{order_id}.'':''.getNameGoal($item->{goal}).'').'</span>
					<em>'.$date.''.$item->{time}.'</em>
				</div>';
		}
		if ($goal){
			$goals .= '<li>'.$from.'<div class="goalsContainer">'.$goal.'</div></li>';
		}
	}

	if ($goals){
		$goals ='<ul class="goalsWay">'.$goals.'</ul>';
	}

	$content_html .= $goals;
}
		
$content_html .= qq~
			</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;

sub getNameGoal {
	my $goal = shift;

	if ($goal eq "CALL_BACK"){
		return "Заказали звонок";
	}
	elsif ($goal eq "BASKET"){
		return "Добавлен в корзину";
	}
	elsif ($goal eq "NEXT_BUY"){
		return "Продолжить покупки";
	}
	elsif ($goal eq "GO_BASKET"){
		return "Переход в корзину";
	}
	elsif ($goal eq "BUY_QUICK"){
		return "<strong>Быстрая покупка</strong>";
	}	
	elsif ($goal eq "ORDER"){
		return "Отправлен заказ";
	}
	elsif ($goal eq "FAVORITE"){
		return "Добавить в закладки";
	}	
}

sub getStartUrl {
	my $url = shift;
	my $link="";
	my $domen = $ENV{'HTTP_HOST'};
	$domen =~ s/2//g;
	while ($url =~ m/http:\/\/(.*?)\/(.*)/g) {
		$link = $2;
	}
	if ($link =~/\?/){
		($link, $temp) = split(/\?/, $link);
	}
	if (!$link && $url =~ $domen){
		return "/";
	}
	if ($link){
		return "/".$link;
	}
}

sub getTizerPlace {
	my $url = shift;
	if ($url =~ /tclick/){
		my $bodyclick="";
		while ($url =~ m/tclick=(.*?)&/g){
			$bodyclick = $1;
		}
		if ($bodyclick){
			if ($bodyclick eq "context"){$bodyclick ="Контекст";}
			elsif ($bodyclick eq "tizer"){$bodyclick ="Тизер";}
			elsif ($bodyclick =~ /banner/){
				while ($url =~ m/tsize=(.*?)&(.*)/g){
					$bodyclick ="Баннер ".$1;
				}
			}
			elsif ($bodyclick eq "clickunder"){$bodyclick ="Кликандер";}
			elsif ($bodyclick eq "messenger"){$bodyclick ="Мессенджер";}
			return $bodyclick;
		}
	}
	elsif ($url =~ /vclick/){
		my $visitweb=""; my $id="";
		while ($url =~ m/vclick=(.*?)&vclick_id=(.*)/g){
			$visitweb = $1;
			$id = $2;
		}
		if ($visitweb && $id){
			return ($visitweb, $id);
		}
	}	
}

sub getComeEngine {
	my $referrer = shift;
	my $title=""; my $engine="";
	if ($referrer =~/yandex.ru\/clck/ or $referrer =~/clck.yandex.ru/){
		$title="Яндекс, результаты поиска";
		$engine="yandex";
	}
	elsif ($referrer =~/yandex.ru\/yandsearch/ or $referrer =~/yandex.ru\/touchsearch/ or $referrer =~/yandex.ru\/msearch/){
		$title="Яндекс.Директ, переход по рекламе";
		$engine="yandex_direct";
	}
	elsif ($referrer =~/google.ru\/search/){
		$title="Google, результаты поиска";
		$engine="google";
	}
	elsif ($referrer =~/google.com\/uds/ or $referrer =~/google.ru\/aclk/){
		$title="Google.Adwords, переход по рекламе";
		$engine="google_adwords";
	}
	elsif ($referrer =~/go.mail.ru/){
		$title="Mail.ru, результаты поиска";
		$engine="mail";
	}
	elsif ($referrer =~/rambler.ru/){
		$title="Rambler.ru, результаты поиска";
		$engine="rambler";
	}	
	elsif ($referrer =~/bing/){
		$title="Bing.com, результаты поиска";
		$engine="bing";
	}	
	elsif ($referrer =~/yandex./){
		$title="Яндекс";
		$engine="yandex";
	}
	elsif ($referrer =~/google./){
		$title="Google";
		$engine="google";
	}
	else {
		$title="Заход с сторонних источников";
		$engine="site";
	}
	return ($title, $engine);
}

sub getComeKeyword {
	my $referrer = shift;
	my $url = shift;
	my $keyword="";
	if ($referrer =~/yandex/){
		while ($referrer =~ m/.*text=(.+)/g) {
			$keyword = $1;
		}
	}
	elsif ($referrer =~/google/ && $referrer !=~/q=&/){
		while ($referrer =~ m/.*q=(.+)/g) {
			$keyword = $1;
		}
	}
	elsif ($referrer =~/go.mail.ru/){
		while ($referrer =~ m/.*q=(.+)/g) {
			$keyword = $1;
		}
	}
	elsif ($referrer =~/rambler.ru/){
		while ($referrer =~ m/.*query=(.+)/g) {
			$keyword = $1;
		}
	}	
	if (!$keyword){
		if ($referrer =~/utm_term=/){
			while ($referrer =~ m/.*utm_term=(.+)/g) {
				$keyword = $1;
			}		
		}
		if ($url =~/keyword=/){
			while ($url =~ m/.*keyword=(.+)/g) {
				$keyword = $1;
			}		
		}
	}
	
	($keyword, $url_) = split(/&/, $keyword);	
	if ($keyword){
		$keyword = uri_unescape($keyword);
		from_to($keyword, "utf-8", "cp1251");	
		return $keyword;
	}
	
}

-1;