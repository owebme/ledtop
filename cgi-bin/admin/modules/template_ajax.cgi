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

$file_edit=param('file_edit');
$template_edit=param('template_edit');
$template_del=param('template_del');
$template_create=param('template_create');
$maket_screen=param('maket_screen');

print header(-charset => 'windows-1251'); 


if ($template_edit ne "" && $file_edit ne "") {

	print "ok";

	use Encode "from_to";
	from_to($template_edit, "utf-8", "cp1251");
	$template_edit =~ s/    /	/g;

	open OUT, (">../../templates/$file_edit.cgi");	   
			print OUT "$template_edit"; 	   
	close(OUT);

	ClearCache("../..");
}

if ($template_create ne "") {

	use Core::DB::Work;
	
	use Encode "from_to";
	from_to($template_create, "utf-8", "cp1251");
	$template_create=Core::DB::Work::translit($template_create);
	
	open OUT, (">../../templates/$template_create.cgi");
	close(OUT);	
	
	print $template_create; 	
}

if ($template_del ne "") {
	
	my $id = $template_del;
	
	unlink("../../templates/$template_del.cgi");
	
	print "ok";
}

if ($maket_screen ne "") {
	
	if ($maket_screen eq "1" or $maket_screen eq "0"){
		open OUT, (">../$dirs/set_screen");	   
				print OUT "$maket_screen"; 	   
		close(OUT);
	}
}

