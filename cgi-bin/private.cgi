#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 
use Fcntl;

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;
use CGI::FastTemplate; 
use Core::Config;
use Core::DB;

my $db = new Core::DB();

$page_alias=param('alias');
$action=param('action');
$user_id=param('user_id');
$user_name=param('user_name');
$user_name_f=param('user_name_f');
$user_name_o=param('user_name_o');
$user_phone=param('user_phone');
$user_login=param('user_login');
$user_pass=param('user_pass');
$reg_pass=param('reg_pass');
$user_person = param('user_person');
$user_sendmail=param('user_sendmail');
$section=param('section');
$adm_act = "private";

require "templates/connection/require.cgi";

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_private",
);

require "templates/connection/variables.cgi";

open OUT, ("admin/$dirs/meta_title"); $main_title = <OUT>; close(OUT);

if ($page_alias eq "auth"){
	$title = "Авторизация // ".$main_title;
	$content = "".build_Auth()."";
}
elsif ($page_alias eq "register"){
	$title = "Регистрация // ".$main_title;
	$content = "".build_Register()."";
}
elsif ($page_alias eq "remember"){
	$title = "Восстановление пароля // ".$main_title;
	$content = "".build_Remember()."";
}
elsif ($page_alias eq "private"){

	$title = "Личный кабинет // ".$main_title;
	$content ="";
	my $result="";
	if ($action eq "enter"){
	
		use Digest::MD5 qw(md5_hex);
		$user_pass = md5_hex($user_pass);
	
		my $res = $db->query("SELECT * FROM users WHERE email = '".$user_login."' LIMIT 1");
		foreach my $line(@$res){
			if ($user_pass eq $line->{pass}){
				$result = "enter";
			}
		}
		if ($result eq "enter"){
		
			my %cookie = (
				'private_login' => $user_login,
				'private_pass' => $user_pass
			);
		    createCookie(\%cookie, '/private/');
		}
	}
	elsif ($action eq "exit"){
	
		my %cookie = (
			'private_login' => "",
			'private_pass' => ""
		);
		deleteCookie(\%cookie, "/");
	}
	elsif ($action eq "save" && $logined eq "enter" && $user_id ne ""){
	
		my %params = ();
	
		if ($user_pass && length($user_pass) > 4){
		
			use Digest::MD5 qw(md5_hex);
			$user_pass = md5_hex($user_pass);			
			%params = ('pass' => $user_pass);
			
			my %cookie = (
				'private_login' => cookie("private_login"),
				'private_pass' => $user_pass
			);
			createCookie(\%cookie);
			
			$db->update("UPDATE users SET `pass`='".$user_pass."' WHERE id='".$user_id."'");
		}
		else {
			print header( -charset=>'windows-1251');
		}
		
		use Core::DB::Users;
		my $user = new Core::DB::Users();
		
		%params = (%params,
			'name' => $user_name,
			'name_f' => $user_name_f,
			'name_m' => $user_name_o,
			'phone' => $user_phone,
			'person' => $user_person,
			'sendmail' => ($user_sendmail?'1':'0')
		);
		$user->editUser($user_id, \%params);
		
		if ($user_person eq "2" && param('u_company')){
			my %params = (
				'user_id' => $user_id,
				'company' => param('u_company'),
				'ogrn' => param('u_ogrn'),
				'inn' => param('u_inn'),
				'kpp' => param('u_kpp'),
				'okpo' => param('u_okpo'),
				'raschet' => param('u_raschet'),
				'korchet' => param('u_korchet'),
				'bik' => param('u_bik')
			);
			$user->addUserData($user_id, \%params);
		}
		
		refresh("/private/data");
	}
	$content = build_Private();
}
if ($page_alias eq "auth" or $page_alias eq "remember" or $page_alias eq "register" or $page_alias eq "private") {
	print header( -charset=>'windows-1251');
}

sub createCookie {
	my $params = shift;
	my $redirect = shift;
	my $always = shift;
	my $hour = 8;
	if ($always eq "on"){$hour=26280;}
	if ($hour && $params){
		my $d = $hour*3600;
		my @weekdays=('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
		my @months=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
		my $t=time;
		$t+=$d;
		my ($SS,$MM,$HH,$DD,$MON,$YY,$WD)=gmtime($t);
		$YY = $YY+1900;
		my $exp_date="$weekdays[$WD], $DD-$months[$MON]-$YY $HH:$MM:$SS GMT";
		my $z = "0";
		$exp_date=~s/(\D)(\d{1})(\D)/$1$z$2$3/g;
		my $data = "Content-type: text/html[n][r]";
		while (my($key,$value) = each(%{$params})){
			$data .= "Set-Cookie: ".$key."=".$value."\; path=/\; expires=".$exp_date."\;[n][r]";
		}
		if ($redirect){
			$redirect = "http://".$ENV{"HTTP_HOST"}.$redirect;
			$data =~ s/\[n\]\[r\]$/\n\rStatus: 301 Moved Permanantly\nLocation: $redirect\r\n\n/g;
		}
		else {$data =~ s/\[n\]\[r\]$/\r\n\n/g;}
		$data =~ s/\[n\]/\n/g; $data =~ s/\[r\]/\r/g;
		print $data;
	}
}
sub deleteCookie {
	my $params = shift;
	my $redirect = shift;
	if ($params){
		my @weekdays=('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
		my @months=('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
		my $t=time;
		$t-=3600;
		my ($SS,$MM,$HH,$DD,$MON,$YY,$WD)=gmtime($t);
		$YY = $YY+1900;
		my $exp_date="$weekdays[$WD], $DD-$months[$MON]-$YY $HH:$MM:$SS GMT";
		my $z = "0";
		$exp_date=~s/(\D)(\d{1})(\D)/$1$z$2$3/g;
		my $data = "Content-type: text/html[n][r]";
		while (my($key,$value) = each(%{$params})){
			$data .= "Set-Cookie: ".$key."=\; path=/\; expires=".$exp_date."\;[n][r]";
		}	
		if ($redirect){
			$redirect = "http://".$ENV{"HTTP_HOST"}.$redirect;
			$data =~ s/\[n\]\[r\]$/\n\rStatus: 301 Moved Permanantly\nLocation: $redirect\r\n\n/g;
		}
		else {$data =~ s/\[n\]\[r\]$/\r\n\n/g;}
		$data =~ s/\[n\]/\n/g; $data =~ s/\[r\]/\r/g;
		print $data;
	}
}

sub refresh {

	my $url = shift;

	print '<script type="text/javascript">
			<!--
			location.replace("http://'.$ENV{"HTTP_HOST"}.$url.'");
			//-->
			</script>
			<noscript>
			<meta http-equiv="refresh" content="0; url=http://'.$ENV{"HTTP_HOST"}.$url.'">
			</noscript>';
}

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();
