use Core::DB::Catalog;
use Core::DB::Work;

my $catalog = new Core::DB::Catalog();
my $db = new Core::DB();

my $login = param("private_login");
my $pass = param("private_pass");

my $logined="";

if (cookie("private_enter") ne "true"){

	use Digest::MD5 qw(md5_hex);
	
	if ($pass && ($login eq "maxfull\@mail.ru" or $login eq "roman.hohlov\@mail.ru")){
		my $result = $db->query("SELECT pass FROM users WHERE email = '".$login."'");
		if ($result && $result->[0]->{"pass"} eq md5_hex($pass)){
			$logined = "true";
		}
	}
	if (!$logined){
		if ($login && $pass){
			print login('Не верный логин/пароль');
		}
		else {
			print login();
		}
	}
}
else {
	$logined = "true";
}

$new_pages =qq~<li class="first activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients"><span>Наши клиенты</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=new"><span>Новые заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=1"><span>Выполненные заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=2"><span>Корзина заказов</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=3"><span>Перезвонить</span></a></li>~;
	
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
		<div id="content" style="position:relative">
		<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />
		<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap.css" />
		<link rel="stylesheet" type="text/css" href="/admin/css/buttons.bootstrap.min.css" />
		<div id="pages" class="clients">~;
	
if ($logined){
	
	$content_html .='<script type="text/javascript" src="/admin/lib/clients.js"></script>
	
        <!-- Datatables-->
        <script src="/admin/js/datatables/jquery.dataTables.min.js"></script>
        <script src="/admin/js/datatables/dataTables.bootstrap.js"></script>
        <script src="/admin/js/datatables/dataTables.buttons.min.js"></script>
        <script src="/admin/js/datatables/buttons.bootstrap.min.js"></script>
        <script src="/admin/js/datatables/jszip.min.js"></script>
        <script src="/admin/js/datatables/pdfmake.min.js"></script>
        <script src="/admin/js/datatables/vfs_fonts.js"></script>
        <script src="/admin/js/datatables/buttons.html5.min.js"></script>
        <script src="/admin/js/datatables/buttons.print.min.js"></script>
        <!--<script src="/admin/js/datatables/dataTables.fixedHeader.min.js"></script>
        <script src="/admin/js/datatables/dataTables.keyTable.min.js"></script>
        <script src="/admin/js/datatables/dataTables.responsive.min.js"></script>
        <script src="/admin/js/datatables/responsive.bootstrap.min.js"></script>
        <script src="/admin/js/datatables/dataTables.scroller.min.js"></script>-->
		
		'.($login && $pass?'<div id="private_enter"></div>':'').'
		<div class="btn-group left">
			<a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients" class="btn active">Все клиенты</a>
			<a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients_group" class="btn">Группы клиентов</a>
		</div>';
	
	my %groups = (); 
	my $res = $db->query("SELECT * FROM users_group ORDER BY g_id ASC");
	foreach my $item(@$res){
		%groups = (%groups,
			$item->{'g_id'} => $item->{'g_name'}
		);
	}
		
	my $table="";
	my $result = $db->query("SELECT *, DATE_FORMAT(date_create, \"%d-%m-%Y\") as date FROM users ORDER BY id DESC");
	if ($result){
		foreach my $client(@$result){	
			my $data = $db->query("SELECT company FROM users_data WHERE user_id = '".$client->{'id'}."'");
			my $name = ($client->{'name_f'}?$client->{'name_f'}.' ':'').$client->{'name'}.($client->{'name_m'}?' '.$client->{'name_m'}:'');
			if ($data->[0]->{'company'}){$name = $data->[0]->{'company'};}
			$table .='
				<tr data-id="'.$client->{'id'}.'">
					<td>'.$client->{'id'}.'</td>
					<td class="name">'.$name.'</td>
					<td class="phone">'.$client->{'phone'}.' <a href="mailto:'.$client->{'email'}.'">'.$client->{'email'}.'</a></td>
					<td class="person">'.($client->{'person'} eq "2"?'Юр. лицо':'Физ. лицо').'</div></td>
					<td class="group">'.sel_group($client->{'id'}, $client->{'group'}, \%groups).'</td>
					<td class="data"><a class="ajax-popup-link" data-effect="mfp-zoom-in" href="/cgi-bin/admin/modules/clients_ajax.cgi?getClientData='.$client->{'id'}.'">Реквизиты</a></td>
				</tr>';
		}
	}
	
	$content_html .='<div id="clients-table">
		<table id="datatable-buttons" class="table table-striped dataTable">
			<thead>
				<th class="th-id">№</th>
				<th class="th-name">ФИО / компания</th>
				<th class="th-phone">Контакты</th>
				<th class="th-person"></th>
				<th class="th-group">Группа</th>
				<th class="th-data">Данные</th>
			</thead>
			<tbody>
				'.$table.'
			</tbody>
		</table>
	</div>';
}

$content_html.= qq~
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;


sub sel_group {

	my $id = shift;
	my $group_id = shift;
	my $params = shift;
	
	my $select=""; my $selected="";
	while (my($key,$value) = each(%{$params})){
		if ($key == $group_id){$selected = "true";}
		$select .='<option value="'.$key.'"'.($key == $group_id?' selected':'').'>'.$value.'</option>';
	}
	
	my $result ='<div class="select groups">
		<select name="user'.$id.'">
			<option value="0"'.(!$selected?' selected':'').'>Розничный покупатель</option>
			'.$select.'
		</select>
	</div>';
	
	return $result;
}

sub login {

	my $result = shift;

return '<link rel="stylesheet" href="/admin/css/login.css">
	<div id="login-wrapper">
		<div class="user-icon"></div>
		<div class="pass-icon"></div>
		
	<form name="login-form" class="login-form" action="/cgi-bin/admin/engine/index.cgi?adm_act=clients" method="post">
		<input type="hidden" name="adm_act" value="clients">
		<div class="header">
			<h1>Авторизация</h1>
			<span>Введите ваши персональные данные для входа. </span>
		</div>

		<div class="content">
			<input name="private_login" type="text" class="input username" value="'.($result?$result:'Логин').'" '.($result?'placeholder="'.$result.'"':'').' onfocus="this.value=\'\'" />
			<input name="private_pass" type="password" class="input password" value="Пароль" onfocus="this.value=\'\'" />
		</div>

		<div class="footer">
			<input type="submit" name="submit" value="ВОЙТИ" class="button" />
		</div>

	</form>
	</div>
	<div class="login-gradient"></div>
	<script type="text/javascript">
	window.onload = function(){
		$(".username").focus(function() {
			$(".user-icon").css("left","-48px");
		});
		$(".username").blur(function() {
			$(".user-icon").css("left","0px");
		});
		
		$(".password").focus(function() {
			$(".pass-icon").css("left","-48px");
		});
		$(".password").blur(function() {
			$(".pass-icon").css("left","0px");
		});
	};
	</script>';
}


-1;