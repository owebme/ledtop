#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);

print header(-charset=>'windows-1251');

opendir(DIR, "cache"); @files_cache=grep(/$_/, readdir(DIR)); closedir(DIR);
foreach (@files_cache){
	if ($_ ne "." && $_ ne ".."){
		unlink("cache/".$_);
	}
}