#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Cookie;
use URI::Escape;
use CGI::Carp qw (fatalsToBrowser);
use Core::DB::Goals;

my $goal = new Core::DB::Goals();

require "admin/engine/lib/parametr.cgi";

print header( -charset=>'windows-1251');

if (param('goal')){

	my $referrer=""; my $start_url=""; my $user_agent="";
	if (cookie("set_referrer")){
		$referrer = cookie("set_referrer");
	}
	if (cookie("set_start_url")){
		$start_url = cookie("set_start_url");
	}
	if ($ENV{'HTTP_USER_AGENT'}){
		$user_agent = $ENV{'HTTP_USER_AGENT'};
	}
	my %params = (
		'goal' => param('goal'),
		'referrer' => $referrer,
		'start_url' => $start_url,
		'user_agent' => $user_agent,
		'ip' => getIP()
	);	
	if (cookie("come_city")){
		%params = (%params,
			'city' => uri_unescape(cookie("come_city"))
		);
	}
	$goal->add(\%params);
}

sub getIP {
	my $ip = $ENV{'REMOTE_ADDR'};
	if (!$ip && $ENV{'HTTP_X_FORWARDED_FOR'}){
		$ip = $ENV{'HTTP_X_FORWARDED_FOR'}; 
	}
	return $ip;
}
