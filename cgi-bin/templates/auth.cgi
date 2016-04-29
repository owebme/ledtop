my $db = new Core::DB();

# Проверка авторизации

$logined="";
my $user_login = cookie("private_login");
if ($user_login) {
	$user_id=""; $u_name =""; $u_name_f =""; $u_name_o =""; $u_email =""; $u_phone=""; $user_status=""; $user_group="";
	my $res = $db->query("SELECT * FROM users WHERE email = '".$user_login."' LIMIT 1");
	foreach my $line(@$res){
		if (cookie("private_pass") eq $line->{pass}){
			$user_id = $line->{id};
			$u_name = $line->{name};
			$u_name_f = $line->{name_f};
			$u_name_o = $line->{name_m};
			$u_email = $line->{email};
			$u_phone = $line->{phone};
			$user_group = $line->{group};
			$logined="enter";
			if ($user_group > 0){
				my $group = $db->query("SELECT g_name FROM users_group WHERE g_id = '".$user_group."' LIMIT 1");
				$user_status = $group->[0]->{g_name};
			}
		}
	}
	if ($logined eq "enter") {
		$private_panel='
			<ul>
				<li class="enter"><a href="/private/"><span>Личный кабинет</span></a></li>
				<li class="exit">
					<form method="post" action="/private/">
						<input type="hidden" value="private" name="alias">
						<input type="hidden" name="action" value="exit">
						<input class="exit" type="submit" value="Выйти из кабинета">
					</form>
				</li>
			</ul>';
	}
}
if ($logined eq "") {
$private_panel='
			<ul id="private-enter">
				<li class="input"><a id="enter" data-tag="login" href="#"><span>Вход в личный кабинет</span></a></li>
				<li class="registration"><a id="reg" data-tag="register" href="#"><span>Регистрация</span></a></li>
			</ul>';
}
	
	
1;