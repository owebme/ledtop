
if ($cache_mode eq "1"){
	opendir(DIR,"cache"); @files_cache=grep(/$_/, readdir(DIR)); closedir(DIR);
	foreach (@files_cache){
		my $delta = cachetime("cache/".$_, "720");
		if ($delta < 0){unlink("cache/$_");}
	}

	if ($cache_url ne "" && $show ne "0" && $show ne "off" && $error ne "404"){
		my $content = $tpl->fetch("MAIN"); 
		open OUT, (">cache/".$cache_url);
			print OUT $$content; 
		close(OUT);
	}

	sub cachetime {
		my $file = shift;
		my $limit = shift;
		my ($sec1, $min1, $hour1, $mday1, $mon1, $year1) = localtime((stat $file)[9]);
		$mon1++; $year1=1900+$year1;
		
		my $time = POSIX::difftime(POSIX::mktime($sec,$min,$hour,$mday,$mon-1,$year-1900), POSIX::mktime($sec1,$min1,$hour1,$mday1,$mon1-1,$year1-1900)) / 86400;
		$time = ($time*24)*60;
		my $delta = $limit-$time;
		
		return $delta;
	}
}

1;