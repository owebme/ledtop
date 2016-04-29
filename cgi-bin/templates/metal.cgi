
if ($dirs_img eq "../../../uploads"){$dirs_main = "..";} else {$dirs_main = "../$dirs_site";}

opendir (DBDIR, "$dirs_main/metal/"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $exec) = split(/\./, $line_wall);
			if ($name_file eq "metal") {
				($name_file, $date) = split(/\./, $line_wall);
			}
		}
	}
	
if ($date eq "" or $date ne $today) {
	$metal = build_Metal();
}
else {
	open OUT, ("$dirs_main/metal/metal.$today"); @metal = <OUT>;
	foreach my $res(@metal) {$metal=qq~$metal$res~;}
}
	
sub build_Metal
{
	my $result="";
	use LWP::UserAgent;					
	my $ua_stocks = LWP::UserAgent->new;
	$ua_stocks->timeout(0);							
	my $response = $ua_stocks->get('http://www'.$url_site.'/metal/get.metal.php');
	if ($response->is_success) {$result = $response->content;}
	
	if ($result eq ""){
		rename("$dirs_main/metal/metal.$date", "$dirs_main/metal/metal.$today");
		open OUT, ("$dirs_main/metal/metal.$today"); @metal = <OUT>;
		foreach my $res(@metal) {$result=qq~$result$res~;}
	}
	else {	
		unlink ("$dirs_main/metal/metal.$date");
		open OUT, (">$dirs_main/metal/metal.$today");
			print OUT "$result";   
		close(OUT);
		if ($cache_mode eq "1"){
			opendir(DIR,"cache"); @files_cache=grep(/$_/, readdir(DIR)); closedir(DIR);
			foreach (@files_cache){
				unlink("cache/".$_);
			}
		}
	}
		
	return $result;	
}	

1;

