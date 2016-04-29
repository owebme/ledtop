
if ($dirs_img eq "../../../uploads"){$dirs_main = "..";} else {$dirs_main = "../$dirs_site";}

opendir (DBDIR, "$dirs_main/valuta/"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $exec) = split(/\./, $line_wall);
			if ($name_file eq "valuta") {
				($name_file, $date) = split(/\./, $line_wall);
			}
		}
	}
	
if ($date eq "" or $date ne $today) {
	$valuta = build_Valuta();
}
else {
	open OUT, ("$dirs_main/valuta/valuta.$today"); @valuta = <OUT>;
	foreach my $res(@valuta) {$valuta=qq~$valuta$res~;}
}
	
sub build_Valuta
{
	my $result="";
	use LWP::UserAgent;					
	my $ua_stocks = LWP::UserAgent->new;
	$ua_stocks->timeout(0);							
	my $response = $ua_stocks->get('http://www'.$url_site.'/valuta/get.valuta.php');
	if ($response->is_success) {$result = $response->content;}
	
	if ($result eq ""){
		rename("$dirs_main/valuta/valuta.$date", "$dirs_main/valuta/valuta.$today");
		open OUT, ("$dirs_main/valuta/valuta.$today"); @valuta = <OUT>;
		foreach my $res(@valuta) {$result=qq~$result$res~;}
	}
	else {	
		unlink ("$dirs_main/valuta/valuta.$date");
		open OUT, (">$dirs_main/valuta/valuta.$today");
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

