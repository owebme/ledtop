#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');} 
use Fcntl;                                   # O_EXCL, O_CREAT и O_WRONLY

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);          # вывод ошибок к browser-у 
use POSIX qw(locale_h);
$old_locale = setlocale(LC_CTYPE);
setlocale(LC_CTYPE, "ru_SU.KOI8-R");
use locale;

require "../engine/lib/auth.cgi";
require "../engine/lib/parametr.cgi";

$title_site=param('title_site');
$showtop=param('showtop');
$filesUpload=param('filesUpload');
$filesUploadName=param('filesUploadName');

print header(-type => 'text/html', -charset => 'windows-1251'); 

if ($title_site) {
	use Encode "from_to";
	from_to($title_site, "utf-8", "cp1251");
	$title_site =~ s/\'/\"/g;
	open OUT, (">../$dirs/meta_title");	   
			print OUT "$title_site"; 	   
	close(OUT);  
}


if ($showtop eq "active") {
	open IN, ("../$dirs/set_panel"); $set = <IN>;   
	open OUT, (">../$dirs/set_panel");	 

	if ($set eq "0") {$showtop = 1; print "0";} else {$showtop = 0; print "1";};
			print OUT "$showtop"; 	   
	close(OUT);
	close(IN); 
}

if ($filesUpload ne "" && $filesUploadName ne ""){

	my $name = $filesUploadName;
	use Encode "from_to";
	from_to($name, "utf-8", "cp1251");
	
	if ($name !~ /\.php$/ && $name !~ /\.cgi$/ && $name !~ /\.pl$/ && $name !~ /\.pm$/ && $name !~ /\.js$/){
		use LWP::Simple;
		my $file = get($filesUpload);
		open (FH, ">$dirs_img/$name"); binmode FH;
		print FH $file; close FH;
		print "upload";
	}
	else {
		print "error";
	}
	
}

