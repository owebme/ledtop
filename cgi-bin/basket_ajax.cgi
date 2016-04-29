#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 
use Fcntl;

use CGI qw/:standard/;
use CGI::Cookie;
use URI::Escape;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Goals;
use Core::DB::Work;
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;

$load=param('load');
$addtobasket=param('addtobasket');
$addtobasketall=param('addtobasketall');
$delproduct=param('delproduct');
$newcount=param('newcount');
$newcount_id=param('newcount_id');
$cena=param('cena');
$col=param('col');
$goals=param('goals');


require "admin/engine/lib/parametr.cgi";
require "templates/basket_ajax.cgi";

	use CGI::Session;
	$session = CGI::Session->load( ) or die CGI::Session->errstr();
	if ( $session->is_empty ) {
       		$session = $session->new() or die $session->errstr;
			$c = new CGI::Cookie(
					 -name    =>  $session->name,
					 -value   =>  $session->id, 
                     -domain  =>  $url_site,
                     -path    =>  "/",
                     -secure  =>  0
			);
	}
	
$ids = $session->param('ids');

print header( -cookie=>$c, -charset=>'windows-1251');

if ($delproduct ne ""){
	$ids = $session->param('ids');
	$ids =~ s/\|($delproduct)[=](\d+[.]\d+)//g;
	if($ids eq "") {$session->param('ids',"");}
	else {$session->param('ids',$ids);}
	$session->flush();
}
	
if ($addtobasket ne ""){
	$cena =~ s/\s//g; 	
	my $price = $cena;
	while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
		if ($addtobasket eq $1){
			$price = $2; last;
		}
	}	
	if ($col ne "1" && $col ne "") {
		my $i=1;
		my $add="";
		my $ids = $session->param('ids');
		if (!is_int($col)){$col += 0.5;}
		while ($i <= $col) {
			$add .= "|$addtobasket=$price";
			$i++;
		}		
		$session->param('ids', "$ids$add");		
	}
	else {
		$session->param('ids', "$ids|$addtobasket=$price");
	}
	
	if ($goals ne "false"){
		my $db = new Core::DB();
		my $goal = new Core::DB::Goals();
		
		my $res = $db->query("SELECT p_name FROM cat_product WHERE p_art ='".$addtobasket."' LIMIT 1");
		my $p_name = $res->[0]->{p_name};

		my %params = (
			'goal' => 'BASKET',
			'referrer' => cookie("set_referrer"),
			'start_url' => cookie("set_start_url"),
			'user_agent' => $ENV{HTTP_USER_AGENT},
			'ip' => $ENV{'REMOTE_ADDR'},
			'p_id' => $addtobasket,
			'p_name' => $p_name,
			'p_count' => $col,
			'p_price' => $price
		);	
		if (cookie("come_city")){
			%params = (%params,
				'city' => uri_unescape(cookie("come_city"))
			);
		}	
		$goal->add(\%params);
	}
}

if ($addtobasketall ne ""){
	$cena =~ s/\s//g; 	
	my $price = $cena;
	while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
		if ($addtobasketall eq $1){
			$price = $2; last;
		}
	}
	$ids =~ s/\|($addtobasketall)[=](\d+[.]\d+)//g;
	$session->param('ids', $ids);
	$session->flush();
	if ($col ne "1" && $col ne "") {
		my $i=1;
		my $add="";
		my $ids = $session->param('ids');
		if (!is_int($col)){$col += 0.5;}
		while ($i <= $col) {
			$add .= "|$addtobasketall=$price";
			$i++;
		}		
		$session->param('ids', "$ids$add");	
	}
	else {
		$session->param('ids', "$ids|$addtobasketall=$price");
	}
}

if ($newcount_id ne ""){	
	$ids = $session->param('ids');
	$ids =~ s/\|($newcount_id)[=](\d+[.]\d+)//g;
	if($ids eq "") {$session->param('ids',"");}
	else {$session->param('ids',$ids);}
	$session->flush();
	if($newcount > 0) {
		my $i=1;
		my $add="";
		while ($i <= $newcount) {
			$add .= "|$newcount_id=$cena";
			$i++;
		}
		
		$session->param('ids', "$ids$add");	
	}
}

my %idTS; my $counts = 0;
while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
	$idTS{$1}{'cena'} = $2;
	if ($idTS{$1}{'count'}){
		$idTS{$1}{'count'}++;
		$idTS{$1}{'cena'} = $2*$idTS{$1}{'count'};
	}
	else {
		$counts++;
		$idTS{$1}{'count'} = 1;
	}
}	

$totalcount = 0;
$totalcena = 0;
while (($key, $value) = each(%idTS)){
     $totalcount += $value->{'count'};
     $totalcena += $value->{'cena'};
}

if ($delproduct ne "") {
	$totalcena = sprintf("%.2f",$totalcena);
	$totalcena =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
	print "$totalcena";
}
elsif (param('getSession') eq "true") {
	my %idTS;
	while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
		$idTS{$1}{'cena'} = $2;
		if (!$idTS{$1}{'price'}){$idTS{$1}{'price'} = $2;}
		if($idTS{$1}{'count'}) {$idTS{$1}{'count'}++;}
		else {$idTS{$1}{'count'} = 1;}
	}
	my $result="";
	while (($key, $value) = each(%idTS)){
		$result .= $key.':'.$value->{'count'}.'='.$value->{'price'}.'|';
	}
	print $result;
}
elsif ($load eq "") {
	my $basket = build_BasketAjax($counts, $totalcena);
	print $basket;
}

sub is_int {
	my $i = shift;
	return 1 if($i=~/^\d+$/);
	return undef;
}
