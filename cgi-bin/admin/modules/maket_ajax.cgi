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
require "../engine/lib/Cache/ClearCache.cgi";

$id_maket=param('id_maket');
$maket_edit=param('maket_edit');
$maket_del=param('maket_del');
$maket_create=param('maket_create');
$maket_screen=param('maket_screen');
$css_edit=param('css_edit');

print header(-charset => 'windows-1251'); 


if ($maket_edit ne "" && $id_maket ne "") {

	print "ok";

	use Encode "from_to";
	from_to($maket_edit, "utf-8", "cp1251");
	$maket_edit =~ s/    /	/g;

	open IN, ("../$dirs/maket_html.$id_maket");
	@maket_old = <IN>; close(IN);
	foreach my $text(@maket_old) {$maket_old=qq~$maket_old$text~;}

	mkdir "../$dirs/backup", 0755;  
	open IN2, (">../$dirs/backup/maket_html.$id_maket.$today_time");
	print IN2 "$maket_old"; close(IN2);

	my $num ="";
	opendir (DBDIR, "../$dirs/backup"); @list_dir = readdir(DBDIR); close DBDIR;
	@list_dir=reverse sort(@list_dir);
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $date) = split(/\.$id_maket\./, $line_wall);
			if ($name_file eq "maket_html"){
				$num++;
				if ($num > 5){
					unlink("../$dirs/backup/maket_html.$id_maket.$date");
				}
			}
		}
	}

	open OUT, (">../$dirs/maket_html.$id_maket");	   
			print OUT "$maket_edit"; 	   
	close(OUT);
	
	ClearCache("../..");
}

if ($maket_create ne "") {
	my $id_maket=""; $count="";
	opendir (DBDIR, "../$dirs"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $num) = split(/\./, $line_wall);
			if ($name_file eq "maket" && $num > 0 && $num ne "404") { 
				$count++;
			}
		}
	}
	$id_maket = $count+1;
	
	use Encode "from_to";
	from_to($maket_create, "utf-8", "cp1251");
	
	open OUT, (">../$dirs/maket.$id_maket");	   
			print OUT "$maket_create|$today"; 	   
	close(OUT);
	open OUT, (">../$dirs/maket_html.$id_maket");   
	close(OUT);		
	
	print $id_maket; 	
}

if ($maket_del ne "") {
	
	my $id = $maket_del;
	
	unlink("../$dirs/maket.$id"); 
	unlink("../$dirs/maket_html.$id"); 
	
	print "ok";
}

if ($css_edit ne "") {

print "ok";

use Encode "from_to";
from_to($css_edit, "utf-8", "cp1251");

open OUT, (">$dirs_css");	   
		print OUT "$css_edit"; 	   
close(OUT); 

my $css_tinymce="";
if ($dirs_fonts ne ""){
	$dirs_fonts =~ s/^\///g;
	$css_tinymce .="\@import url('/".$dirs_fonts."');\n";
}
while ($css_edit =~ m/#content (.+?){(.+?)}/g) {
	if ($1 eq "a "){
		my $link = $2;
		$link =~ s/;$/ \!important;/g;
		$css_tinymce .= "a {".$link."}\n";
	}
	else {$css_tinymce .= $1."{".$2."}\n";}
}
while ($css_edit =~ m/#content (.+?){\s+(.*)/g) {
	$css_tinymce .= $1."{".$2."}\n";
}

$dirs_css =~ s/\/(\w+).css$/\/style_tinymce.css/g;

open OUT, (">$dirs_css");	   
		print OUT "$css_tinymce"; 	   
close(OUT); 

ClearCache("../..");
}

if ($maket_screen ne "") {
	
	if ($maket_screen eq "1" or $maket_screen eq "0"){
		open OUT, (">../$dirs/set_screen");	   
				print OUT "$maket_screen"; 	   
		close(OUT);
	}
}

