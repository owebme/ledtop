
sub ClearCache {
	my $path = shift;
	my $surely = shift;
	if ($path ne "" && $cache_mode eq "1" or $path ne "" && $surely eq "1"){
		opendir(DIR,$path."/cache"); @files_cache=grep(/$_/, readdir(DIR)); closedir(DIR);
		foreach (@files_cache){
			unlink($path."/cache/".$_);
		}
	}
}

1;