# C������� �����������

sub build_Auth
{
	my $login = shift;

	my $auth .='
				<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/validate_default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
				<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" />
				<div style="display:none;">
					<img src="/js/validate/i/baloon-body.gif" alt="">
					<img src="/js/validate/i/baloon-footer.gif" alt="">
					<img src="/js/validate/i/baloon-header.gif" alt="">
					<img src="/js/validate/i/baloon-header-flip.gif" alt="">
				</div>
				<div class="title">
					<h1>�����������</h1>
				</div>
				<div class="content-holder">
					<form method="post" action="/private/">
						<input type="hidden" value="private" name="alias">
						<input type="hidden" value="enter" name="action">
						<table class="form">
							<tr>
								<td class="name">��� E-mail (�����)</td>
								<td><input type="text" value="'.$login.'" name="user_login" format="email" notice="������� ��� �����" autocomplete="off"></td>
							</tr>
							<tr>
								<td class="name">������</td>
								<td><input type="password" value="" name="user_pass" format=".+" notice="������� ��� ������" autocomplete="off"></td>
							</tr>
							<tr>
								<td></td>
								<td><a href="/remember/" class="remember">��������� ������?</a></td>
							</tr>
							<tr>
								<td colspan="2"><input type="submit" value="�����" class="button right"></td>
							</tr>
						</table>
					</form>
				</div>';

	return $auth;
}


# C������� �����������

sub build_Register
{
	my $register="";
	my $db = new Core::DB();
	if ($action eq "register" && $user_name ne "" && $user_login ne ""){
		my $mail="";
		my $res = $db->query("SELECT * FROM users WHERE email = '".$user_login."' LIMIT 1");
		foreach my $line(@$res){
			$mail = $line->{email};
		}
		if ($mail ne ""){
			$register .= build_FormRegister().'
			<div id="message_block" class="up"><p>����� E-mail ��� ������������, �������� ����������� ����� ��� <a href="/remember/">������������ ������</a>.</p></div>';
		}
		else {
			if ($reg_pass){
				$register .='<div class="title"><h1>�����������</h1></div>
			<div id="message_block"><p>�� ������� ������ �����������, ��������� �������������� �� ��� E-mail, ������ <a href="/auth/">����� � ���� �������</a>.</p></div>';
			}
			else {
				$register .='<div class="title"><h1>�����������</h1></div>
			<div id="message_block"><p>�� ������� ������ �����������, ��������� ������� ���������� ��� �� E-mail.</p></div>';
			}
			
			use Digest::MD5 qw(md5_hex);

			my $pass = random_n(1,10).random_n(10,50).random_n(50,100).random_n(100,1000)*3;
			
			if ($reg_pass){$pass = $reg_pass;}
			
			use Core::DB::Users;
			my $user = new Core::DB::Users();
			
			my %params = (
				'date_create' => "NOW()",
				'name' => $user_name,
				'email' => $user_login,
				'pass' => $pass,
				'person' => 1,
				'sendmail' => 1
			);
			$user->addUser(\%params);

			my $url_site = $ENV{"HTTP_HOST"};
			$url_site =~ s/^\.//g;
			open (MZ,"|/usr/sbin/sendmail -t");
			print MZ "To: $user_login\n";
			print MZ "From: robot\@$url_site\n";
			print MZ "Subject: ����� ���������� �� $url_site, �� ������� ������������������\n";
			print MZ "MIME-Version: 1.0\n";
			print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
			print MZ "Content-Transfer-Encoding: 8bit\n\n";
			print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
			print MZ "������ ����!<br><br>��������� ������� � ��� ������ �������.<br><br><br>";
			print MZ "�����: <b>$user_login</b><br><br>";
			print MZ "������: <b>$pass</b><br><br>";
			print MZ "</div>";
			close (MZ);
		}
	}
	else {
		$register = build_FormRegister();
	}

	sub build_FormRegister
	{
		my $form ='
				<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/validate_default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
				<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" />
				<div style="display:none;">
					<img src="/js/validate/i/baloon-body.gif" alt="">
					<img src="/js/validate/i/baloon-footer.gif" alt="">
					<img src="/js/validate/i/baloon-header.gif" alt="">
					<img src="/js/validate/i/baloon-header-flip.gif" alt="">
				</div>
				<div class="title">
					<h1>�����������</h1>
				</div>

				<div class="content-holder">
					<form method="post" action="/register/">
						<input type="hidden" value="register" name="alias">
						<input type="hidden" value="register" name="action">
						<table class="form">
							<tr>
								<td class="name">���� ���</td>
								<td><input type="text" value="" name="user_name" format=".+" notice="������� ���� ���" autocomplete="off"></td>
							</tr>
							<tr>
								<td class="name">��� E-mail</td>
								<td><input type="text" value="" name="user_login" format="email" notice="������� ��� e-mail" autocomplete="off"></td>
							</tr>
							<tr>
								<td colspan="2"><input type="submit" value="�����������" class="button right"></td>
							</tr>
						</table>
					</form>
				</div>';

		return $form;
	}

	return $register;
}


# C������� �������������� ������

sub build_Remember
{
	my $remember="";
	my $db = new Core::DB();
	if ($action eq "remember" && $user_login ne ""){
		my $mail="";
		my $res = $db->query("SELECT * FROM users WHERE email = '".$user_login."' LIMIT 1");
		foreach my $line(@$res){
			$mail = $line->{email};
		}
		if ($mail ne ""){
			$remember .='<div class="title">
							<h1>�������������� ������</h1>
						</div>
			<div id="message_block"><p>�� ��� E-mail ���� ���������� ����� ��������� �������.</p></div>';

			my $pass = random_n(1,10).random_n(10,50).random_n(50,100).random_n(100,1000)*3;

			my $url_site = $ENV{"HTTP_HOST"};
			$url_site =~ s/^\.//g;
			open (MZ,"|/usr/sbin/sendmail -t");
			print MZ "To: $user_login\n";
			print MZ "From: robot\@$url_site\n";
			print MZ "Subject: �������������� ������ � ������ ������� �� $url_site\n";
			print MZ "MIME-Version: 1.0\n";
			print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
			print MZ "Content-Transfer-Encoding: 8bit\n\n";
			print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
			print MZ "������ ����!<br><br>�� ��������� ����� ������ � ��� ������ �������.<br><br><br>";
			print MZ "����� ������: <b>$pass</b><br><br>";
			print MZ "�����: <a href='http://".$ENV{"HTTP_HOST"}."/private/'>http://".$ENV{"HTTP_HOST"}."/private/</a><br><br>";
			print MZ "</div>";
			close (MZ);
			
			use Digest::MD5 qw(md5_hex);
			$db->update("UPDATE users SET `pass`='".md5_hex($pass)."' WHERE email='".$user_login."'");
			
		}
		else {
			$remember .= build_FormRemember().'
			<div id="message_block" class="up"><p>������������ � ����� E-mail �� ���������������, �������� <a href="/register/">�����������</a>.</p></div>';
		}
	}
	else {
		$remember = build_FormRemember();
	}

	sub build_FormRemember
	{
		my $form ='
				<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/validate_default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
				<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" />
				<div style="display:none;">
					<img src="/js/validate/i/baloon-body.gif" alt="">
					<img src="/js/validate/i/baloon-footer.gif" alt="">
					<img src="/js/validate/i/baloon-header.gif" alt="">
					<img src="/js/validate/i/baloon-header-flip.gif" alt="">
				</div>
				<div class="title">
					<h1>�������������� ������</h1>
				</div>
				<div class="content-holder">
					<form method="post" action="/remember/">
						<input type="hidden" value="remember" name="alias">
						<input type="hidden" value="remember" name="action">
						<table class="form">
							<tr>
								<td class="name">��� E-mail</td>
								<td><input type="text" value="" name="user_login" format="email" notice="������� ��� e-mail" autocomplete="off"></td>
							</tr>
							<tr>
								<td colspan="2"><input type="submit" value="������������" class="button right"></td>
							</tr>
						</table>
					</form>
				</div>';
		return $form;
	}

	return $remember;
}


# ������ �������

sub build_Private
{
	my $private="";	my $logined="";
	my $error = build_Auth($user_login).'
		<div id="message_block" class="up"><p>�� ������� �������� ����� �/��� ������</p></div>';
	my $user_login = cookie("private_login");
	if ($user_login) {
		my $user_id=""; my $u_name=""; my $u_name_f=""; my $u_name_o=""; my $u_phone=""; my $u_login=""; my $u_person=""; my $u_sendmail="";
		my $db = new Core::DB();
		my $res = $db->query("SELECT * FROM users WHERE email = '".$user_login."' LIMIT 1");
		foreach my $line(@$res){
			if (cookie("private_pass") eq $line->{pass}){
				$user_id = $line->{id};
				$u_name = $line->{name};
				$u_name_f = $line->{name_f};
				$u_name_o = $line->{name_m};
				$u_phone = $line->{phone};
				$u_login = $line->{email};
				$u_person = $line->{person};
				$u_sendmail = $line->{sendmail};
				$logined = "enter";
			}
		}
		if ($logined ne "enter"){
			$private = $error;
		}
		elsif ($logined eq "enter") {

			$user_status = '<div id="user-status">
					<h3>��� ������</h3>
					<span>'.(!$user_status?'��������� ����������':$user_status).'</span>
				</div>';

			$private .='<div id="private">';

			if ($section eq "data"){
				$private .='<div class="title">
								<a href="/private/" class="back">������ �������</a>
								<h1 class="name">������ ������</h1>
							</div>';
							
				my %data = ();			
				my $res = $db->query("SELECT * FROM users_data WHERE user_id = '".$user_id."' LIMIT 1");
				foreach my $line(@$res){
					%data = (
						'company' => $line->{company},
						'ogrn' => $line->{ogrn},
						'inn' => $line->{inn},
						'kpp' => $line->{kpp},
						'okpo' => $line->{okpo},
						'raschet' => $line->{raschet},
						'korchet' => $line->{korchet},
						'bik' => $line->{bik}
					);
				}
				$private .= build_FormPrivate($user_id, $u_name, $u_name_f, $u_name_o, $u_phone, $u_login, $u_pass, $u_person, $u_sendmail, \%data);
			}
			elsif ($section eq "history"){

				$private .='<div class="title">
								<a href="/private/" class="back">������ �������</a>
								<h1 class="name">������� �������</h1>
							</div>';

				my $orders="";
				my $result = $db->query("SELECT *, DATE_FORMAT(order_date, \"%d-%m-%Y\") as date, DATE_FORMAT(order_date, \"%H:%i\") as time FROM cat_orders WHERE user_id ='".$user_id."' ORDER BY order_date DESC");
				foreach my $order(@$result){
					if ($order->{pay} ne ""){
						my $pay=""; my $products="";
						if ($order->{pay} eq "1"){$pay = "<span>�������</span>";}
						else {$pay = "������� ������";}
						my $res = $db->query("SELECT * FROM cat_orders_product WHERE order_id ='".$order->{id}."'");
						foreach my $line(@$res){
							my $pack = $db->query("SELECT p_unit FROM cat_product WHERE p_art ='".$line->{p_art}."'");
							$products .= '
									<tr>
										<td class="name"><strong>'.$line->{p_art}.'</strong> <a target="_blank" href="/products/'.$line->{p_art}.'">'.$line->{p_name}.'</a></td>
										<td class="count"><span class="col"><b>'.$line->{p_count}.'</b> '.($pack->[0]->{"p_unit"}?$pack->[0]->{"p_unit"}.'.':'��.').'</span> <em>&times;</em> <b class="price">'.$line->{p_price}.' ���.</b></span></td>
									</tr>';
						}
							$orders .='
								<div class="order-item">
									<h3><strong>����� #'.$order->{id}.'</strong><span> &ndash; '.$order->{date}.' � '.$order->{time}.'</span></h3>
									<div class="list">
										<table>
											'.$products.'
										</table>
									</div>
									<div class="total"><strong>�����:</strong> <span>'.$order->{total}.' ���.</div>
								</div>';
					}
				}
				$private .= ($orders eq ""?'<div id="message_block"><p>�� ��� �� ��������� �������</p></div>':'<div class="content-holder"><div class="order-history">'.$orders.'</div></div>');
			}
			elsif ($section eq "order"){

				use Core::DB::Catalog;
				my $catalog = new Core::DB::Catalog();

				$private .='<div class="title">
								<a href="/private/" class="back">������ �������</a>
								<h1 class="name">������� �����</h1>
							</div>';

				my $cat_id = cookie("private_sel_category");
				
				my $catalog_category="";
				if (!$cat_id){
					my $res = $db->query("SELECT cat_id FROM cat_product_rel WHERE cat_main ='1' LIMIT 1");
					if ($res){
						$cat_id = $res->[0]->{"cat_id"};
					}
				}	

				if ($cat_id) {
					$catalog_category = $catalog->getPrivateCategories($cat_id);
				}

				$private .= $catalog->getPrivateBasket();

				$private .='<div id="private-panel-top">';
				
				if ($catalog_category){
					$private .='
						<select class="category" data-id="'.$cat_id.'" name="sel_category">
							'.$catalog_category.'
						</select>';
				}
				$private .='<p>���� ������� � ���������� ������ � ������ ��� 18% � ���������� �� ���� ������� ��������� (��, � � �.�.), ��������� � ������� � ������� ��.</p></div>
				<div id="products-table">
					<table id="datatable-buttons" class="dataTable">
						<thead>
							<th>�������</th>
							<th></th>
							<th id="th-name">������������</th>
							<th></th>
							<th>����</th>
							<th>�����</th>
							<th>��.</th>
							<th>�����</th>
							<th id="th-desc">��������</th>
						</thead>
						<tbody>
						</tbody>
					</table>
				</div>';

			}
			else {

				use CGI::Session;
				my $session = CGI::Session->load( ) or die CGI::Session->errstr();
				$ids = $session->param('ids');

				my %idTS; my $counts = 0;
				if ($ids){
					while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
						if (!$idTS{$1}{'count'}){
							$counts++;
							$idTS{$1}{'count'} = 1;
						}
					}
				}

				$private .='<div class="private-sections">
					<div class="item">
						<a href="/private/data">
							<i class="fa fa-user"></i>
							<span>������ ������</span>
						</a>
					</div>
					<div class="item">
						<a href="/private/order">
							<i class="fa fa-shopping-cart">'.($counts > 0?'<ins>'.$counts.'</ins>':'').'</i>
							<span>������� �����</span>
						</a>
					</div>
					<div class="item">
						<a href="/private/history">
							<i class="fa fa-history"></i>
							<span>������� �������</span>
						</a>
					</div>
					<div class="item">
						<a href="mailto:orders@ledtop-shop.ru">
							<i class="fa fa-send-o"></i>
							<span>���������<br> ���������</span>
						</a>
					</div>
					<div class="clearfix"></div>
				</div>';

			}

			$private .='</div>';
	    }
	}
	else {
		if (param("user_login")){
			$private = $error;
		}
		else {
			$private = build_Auth();
		}
	}

	sub build_FormPrivate
	{
		my $user_id = shift;
		my $u_name = shift;
		my $u_name_f = shift;
		my $u_name_o = shift;
		my $u_phone = shift;
		my $u_login = shift;
		my $u_pass = shift;
		my $u_person = shift;
		my $u_sendmail = shift;
		my $data = shift;
		my %data = %{$data};
		
		my $form ='
				<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/validate_default.js" language="JavaScript" type="text/javascript"></script>
				<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
				<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" />
				<div style="display:none;">
					<img src="/js/validate/i/baloon-body.gif" alt="">
					<img src="/js/validate/i/baloon-footer.gif" alt="">
					<img src="/js/validate/i/baloon-header.gif" alt="">
					<img src="/js/validate/i/baloon-header-flip.gif" alt="">
				</div>
				<form method="post" action="/private/">
					<input type="hidden" value="private" name="alias">
					<input type="hidden" value="'.$user_id.'" name="user_id">
					<input type="hidden" value="save" name="action">
					<div class="content-holder">
						<div class="table-form f-left">
							<table class="form">
								<tr>
									<td class="name">���� �������</td>
									<td><input type="text" value="'.$u_name_f.'" name="user_name_f"></td>
								</tr>
								<tr>
									<td class="name">���� ���</td>
									<td><input type="text" value="'.$u_name.'" name="user_name" format=".+" notice="������� ���� ���"></td>
								</tr>
								<tr>
									<td class="name">���� ��������</td>
									<td><input type="text" value="'.$u_name_o.'" name="user_name_o"></td>
								</tr>
								<tr>
									<td class="name">��� �������</td>
									<td><input type="text" value="'.$u_phone.'" name="user_phone"></td>
								</tr>
								<tr>
									<td class="name">��� E-mail (�����)</td>
									<td><input type="text" value="'.$u_login.'" name="user_login" format="email" notice="������� ��� e-mail" readonly="readonly"></td>
								</tr>
								<tr>
									<td class="name">�������� ������</td>
									<td><input type="password" value="" name="user_pass" placeholder="�� ���������� ��� ����, ���� �� ������� ������"></td>
								</tr>
								<tr>
									<td class="name"><label><span class="radiobox__box"><input type="radio" name="user_person"'.($u_person ne "2"?' checked':'').' value="1"></span>���. ����</label></td>
									<td><label><span class="radiobox__box"><input type="radio" name="user_person"'.($u_person eq "2"?' checked':'').' value="2"></span>��. ����</label></td>
								</tr>
								<tr>
									<td class="name" colspan="2"><label><span class="checkbox__box"><input type="checkbox" name="user_sendmail"'.($u_sendmail eq "1"?' checked':'').'><i></i></span>�������� �������� � ����� ���������</label></td>
								</tr>
								<tr>
									<td colspan="2"><input type="submit" value="�������� ������" class="button right"></td>
								</tr>
							</table>
						</div>
						<div id="table-details" class="table-form f-right'.($u_person ne "2"?' hide':'').'">
							<table class="form">
								<tr>
									<td><div class="title"><h1>���� ���������</h1></div></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'company'}:'').'" name="u_company" placeholder="�������� ��������"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'ogrn'}:'').'" name="u_ogrn" placeholder="����"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'inn'}:'').'" name="u_inn" placeholder="���"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'kpp'}:'').'" name="u_kpp" placeholder="���"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'okpo'}:'').'" name="u_okpo" placeholder="����"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'raschet'}:'').'" name="u_raschet" placeholder="��������� ����"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'korchet'}:'').'" name="u_korchet" placeholder="���. ����"></td>
								</tr>
								<tr>
									<td><input type="text" value="'.($u_person eq "2"?$data{'bik'}:'').'" name="u_bik" placeholder="���"></td>
								</tr>
							</table>
						</div>
					</div>
				</form>';

		return $form;
	}

	return $private;
}

sub random_n($$){
	my($min, $max) = @_;
	return $min if $min == $max;
	($min, $max) = ($max, $min) if $min > $max;
	return $min + int rand(1 + $max - $min);
}

1;