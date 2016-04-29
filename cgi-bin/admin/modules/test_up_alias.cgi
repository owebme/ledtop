#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB::Catalog;
use Core::DB::Work;
use Core::DB;

require "../engine/lib/parametr.cgi";

print header(-charset=>'windows-1251');

my $catalog = new Core::DB::Catalog();
my $db = new Core::DB();

my $result = $db->query("SELECT c_id, c_name FROM cat_category WHERE c_pid != '0';");
foreach my $item(@$result){
	my $id = $item->{'c_id'};
	$db->update("UPDATE cat_category SET `c_supplier` = '1' WHERE c_id = '".$id."'");
	print $item->{'c_name'}."<br>";
}

sub upperFirstLetter {
	my $text = shift;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^�/�/g;
	$text =~ s/^a/A/g;
	$text =~ s/^b/B/g;
	$text =~ s/^c/C/g;
	$text =~ s/^d/D/g;
	$text =~ s/^e/E/g;
	$text =~ s/^f/F/g;
	$text =~ s/^g/G/g;
	$text =~ s/^h/H/g;
	$text =~ s/^i/I/g;
	$text =~ s/^g/G/g;
	$text =~ s/^k/K/g;
	$text =~ s/^l/L/g;
	$text =~ s/^m/M/g;
	$text =~ s/^n/N/g;
	$text =~ s/^o/O/g;
	$text =~ s/^p/P/g;
	$text =~ s/^q/Q/g;
	$text =~ s/^r/R/g;
	$text =~ s/^s/S/g;
	$text =~ s/^t/T/g;
	$text =~ s/^u/U/g;
	$text =~ s/^v/V/g;
	$text =~ s/^w/W/g;
	$text =~ s/^x/X/g;
	$text =~ s/^y/Y/g;
	$text =~ s/^z/Z/g;
	return $text;
}