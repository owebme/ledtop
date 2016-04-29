#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;
use Core::DB::Users;
use Encode "from_to";

require "../engine/lib/parametr.cgi";

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();

my $user = new Core::DB::Users();

if (param('client_id') && param('change_group') ne "") {

	my $client_id=param('client_id');
	my $change_group=param('change_group');

	if ($change_group eq "0"){
		$db->update("UPDATE users SET `group` = NULL WHERE id = '".$client_id."'");
	}
	else {
		$db->update("UPDATE users SET `group` = '".$change_group."' WHERE id = '".$client_id."'");
	}
	
	print "true";
}
elsif (param('getClientData')){

	my $id = param('getClientData');
	
	my $name=""; my $name_=""; my $group_id=""; my $group=""; my $phone=""; my $email=""; my $person="";
	my $result = $db->query("SELECT * FROM users WHERE id = '".$id."'");
	foreach my $client(@$result){	
		$name = ($client->{'name_f'}?$client->{'name_f'}.' ':'').$client->{'name'}.($client->{'name_m'}?' '.$client->{'name_m'}:'');
		$phone = $client->{'phone'};
		$email = $client->{'email'};
		$person = $client->{'person'};
		$group_id = $client->{'group'};
	}
	if ($group_id > 0){
		my $result = $db->query("SELECT g_name FROM users_group WHERE g_id = '".$group_id."'");
		$group = $result->[0]->{"g_name"};
	}
	my %data = ();
	my $result = $db->query("SELECT * FROM users_data WHERE user_id = '".$id."'");
	if ($result){
		$name_ = $name;
		foreach my $item(@$result){
			$name = $item->{'company'};
			%data = (
				'company' => $item->{company},
				'ogrn' => $item->{ogrn},
				'inn' => $item->{inn},
				'kpp' => $item->{kpp},
				'okpo' => $item->{okpo},
				'raschet' => $item->{raschet},
				'korchet' => $item->{korchet},
				'bik' => $item->{bik}
			);
		}
	}
	
	$name =~s/'/"/; 
	
	my $result ='<div data-id="'.$id.'" class="white-popup-block" style="min-height:480px">
		<h1>'.$name.'</h1>
		'.($name_?'<h3>Представитель: '.$name_.'</h3>':'').'
		'.($group?'<h3>Группа: <strong>'.$group.'</strong></h3>':'<h3>Группа: <strong>Розничный покупатель</strong></h3>').'
		'.($phone?'<h3>Телефон: '.$phone.'</h3>':'').'
		<h3>E-mail: <a href="mailto:'.$email.'">'.$email.'</a></h3>
		<p>
			<label><span class="radiobox__box"><input type="radio" name="user_person" value="1"'.($person ne "2"?' checked':'').'></span>Физ. лицо</label>
			&nbsp; &nbsp; 
			<label><span class="radiobox__box"><input type="radio" name="user_person" value="2"'.($person eq "2"?' checked':'').'></span>Юр. лицо</label>
		</p>
		<div class="table-form">
			<table class="form'.($person ne "2"?' hide':'').'">
				<tr>
					<td class="name">Название компании</td>
					<td><input type="text" class="u_company" placeholder="Название компании" value=\''.$name.'\'></td>
				</tr>
				<tr>
					<td class="name">ОГРН</td>
					<td><input type="text" class="u_ogrn" placeholder="ОГРН" value="'.$data{"ogrn"}.'"></td>
				</tr>
				<tr>
					<td class="name">ИНН</td>
					<td><input type="text" class="u_inn" placeholder="ИНН" value="'.$data{"inn"}.'"></td>
				</tr>
				<tr>
					<td class="name">КПП</td>
					<td><input type="text" class="u_kpp" placeholder="КПП" value="'.$data{"kpp"}.'"></td>
				</tr>
				<tr>
					<td class="name">ОКПО</td>
					<td><input type="text" class="u_okpo" placeholder="ОКПО" value="'.$data{"okpo"}.'"></td>
				</tr>
				<tr>
					<td class="name">Расчетный счет</td>
					<td><input type="text" class="u_raschet" placeholder="Расчетный счет" value="'.$data{"raschet"}.'"></td>
				</tr>
				<tr>
					<td class="name">Кор. счет</td>
					<td><input type="text" class="u_korchet" placeholder="Кор. счет" value="'.$data{"korchet"}.'"></td>
				</tr>
				<tr>
					<td class="name">БИК</td>
					<td><input type="text" class="u_bik" placeholder="БИК" value="'.$data{"bik"}.'"></td>
				</tr>
				<tr>
					<td colspan="2">
						<div class="button-submit right">
							<button class="submit">Сохранить</button>
						</div>
					</td>
				</tr>
			</table>
		</div>
	</div>';

	print $result;
}
elsif (param('saveClientData')){

	my $id = param('user_id');
	my $company = param('u_company');
	my $ogrn = param('u_ogrn');
	my $inn = param('u_inn');
	my $kpp = param('u_kpp');
	my $okpo = param('u_okpo');
	my $raschet = param('u_raschet');
	my $korchet = param('u_korchet');
	my $bik = param('u_bik');
	from_to($company, "utf-8", "cp1251");
	from_to($ogrn, "utf-8", "cp1251");
	from_to($inn, "utf-8", "cp1251");
	from_to($kpp, "utf-8", "cp1251");
	from_to($okpo, "utf-8", "cp1251");
	from_to($raschet, "utf-8", "cp1251");
	from_to($korchet, "utf-8", "cp1251");
	from_to($bik, "utf-8", "cp1251");	

	my %params = (
		'person' => param('user_person')
	);
	$user->editUser($id, \%params);
	
	if (param('user_person') eq "2" && param('u_company')){
		
		my %params = (
			'user_id' => $id,
			'company' => $company,
			'ogrn' => $ogrn,
			'inn' => $inn,
			'kpp' => $kpp,
			'okpo' => $okpo,
			'raschet' => $raschet,
			'korchet' => $korchet,
			'bik' => $bik
		);
		$user->addUserData($id, \%params);
	}
	
	print "true";
}