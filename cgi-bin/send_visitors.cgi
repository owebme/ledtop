#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Cookie;
use CGI::Carp qw (fatalsToBrowser);
use Core::DB::Visits;

my $visit = new Core::DB::Visits();

require "admin/engine/lib/parametr.cgi";

print header( -charset=>'windows-1251');

if (param('visit')){

	my $referrer=""; my $user_agent="";
	if (cookie("set_referrer")){
		$referrer = cookie("set_referrer");
	}
	if ($ENV{'HTTP_USER_AGENT'}){
		$user_agent = $ENV{'HTTP_USER_AGENT'};
	}
	my %params = (
		'referrer' => $referrer,
		'start_url' => param('visit'),
		'user_agent' => $user_agent,
		'ip' => getIP()
	);
	$visit->add(\%params);
}

sub getIP {
	my $ip = $ENV{'REMOTE_ADDR'};
	if (!$ip && $ENV{'HTTP_X_FORWARDED_FOR'}){
		$ip = $ENV{'HTTP_X_FORWARDED_FOR'}; 
	}
	return $ip;
}