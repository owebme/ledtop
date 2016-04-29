
my $f_date=""; my $f_time=""; my $s_time="";
my $p_time = $time;
$p_time =~s/://g;
$s_time = $time;
$s_time =~s/:/-/g;

if ($dirs_img eq "../../../uploads"){$dirs_main = "..";} else {$dirs_main = "../$dirs_site";}

opendir (DBDIR, "$dirs_main/pogoda/"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $exec) = split(/\./, $line_wall);
			if ($name_file eq "pogoda") {
				($name_file, $date) = split(/\./, $line_wall);
				while ($date =~ m/(\d+)-(\d+)-(\d+)_(\d+)-(\d+)/g) {
					$f_time = $4."".$5;
					$f_date = $1."-".$2."-".$3;
				}
			}
		}
	}
	
if ($today != $f_date or $p_time > 230 && $f_time < 230 or $p_time > 830 && $f_time < 830 or $p_time > 1430 && $f_time < 1430 or $p_time > 2030 && $f_time < 2030) {
	$pogoda = build_Pogoda();
}
else {
	open OUT, ("$dirs_main/pogoda/pogoda.$date"); @pogoda = <OUT>;
	foreach my $res(@pogoda) {$pogoda=qq~$pogoda$res~;}
}
	
sub build_Pogoda
{
	my $result="";
	use LWP::UserAgent;					
	my $ua_stocks = LWP::UserAgent->new;
	$ua_stocks->timeout(0);							
	my $response = $ua_stocks->get('http://www'.$url_site.'/pogoda/get.pogoda.php');
	if ($response->is_success) {$result = $response->content;}
	
	if ($result eq ""){
		rename("$dirs_main/pogoda/pogoda.$date", "$dirs_main/pogoda/pogoda.$today\_$s_time");
		open OUT, ("$dirs_main/pogoda/pogoda.$today\_$s_time"); @pogoda = <OUT>;
		foreach my $res(@pogoda) {$result=qq~$result$res~;}
	}
	else {
		unlink ("$dirs_main/pogoda/pogoda.$date");
		open OUT, (">$dirs_main/pogoda/pogoda.$today\_$s_time");
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

