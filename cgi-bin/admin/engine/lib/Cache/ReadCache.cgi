
if ($cache_mode eq "1"){
	use Digest::MD5 qw(md5_hex);
	$cache_url = md5_hex($ENV{REQUEST_URI});

	if ($ENV{REQUEST_URI} eq "/"){
		$cache_url = md5_hex("index");
	}
	my $file = "cache/".$cache_url;
	if(-e $file && $cache_url ne ""){
		my $page="";
		open FILE, $file;
		while (defined (my $file_line = <FILE>)) {
			$page .= $file_line;
		}
		close FILE;	
		if ($page ne ""){
			print header( -charset=>'windows-1251');
			print $page;
			$|=1;
			exit;
		}
	}
}

1;