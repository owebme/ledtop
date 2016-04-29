
my $cook=cookie("uplecms");

if ($cook) {
	my($user_login, $user_pass) = split(/\|/, $cook);
	my($xxx, $user_pass) = split(/:/, $user_pass);
	my($xxx, $user_login) = split(/:/, $user_login);
	my $dbg="../engine/password-settings/$user_login";
	open (BO, "$dbg");
	@b = <BO>;
	close (BO);
	my $zapros_password=$b[0];
	if ($zapros_password && $zapros_password eq $user_pass) {
	}
	else {
		my $URL = "http://".$ENV{"HTTP_HOST"}."/admin/";
		print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
		exit;
	}
}
else {
	my $URL = "http://".$ENV{"HTTP_HOST"}."/admin/";
	print "Status: 301 Moved Permanantly\nLocation: $URL\n\n";
	exit;
}

1;
