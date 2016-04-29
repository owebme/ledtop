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

$c_pid=param('id');

if ($c_pid > 0){

	my $result = $db->query("SELECT c_alias FROM cat_category WHERE c_id = '".$c_pid."';");
	my $c1_alias = $result->[0]->{c_alias};

	my $result = $db->query("SELECT c_id, c_name, c_name_org FROM cat_category WHERE c_pid = '".$c_pid."';");
	foreach my $item(@$result){
		my $id = $item->{'c_id'};
		my $name_ = $item->{'c_name_org'};
		if (!$name_){$name_ = $item->{'c_name'};}
		$name_ = filter($name_);
		my $name = filter($item->{'c_name'});
		$c2_alias = $c1_alias."/".Core::DB::Work::translit($name_);
		$db->update("UPDATE cat_category SET `c_name` = '".$name."', `c_alias` = '".$c2_alias."' WHERE c_id = '".$id."'");
		print $name."<br>";
		my $res = $db->query("SELECT c_id, c_name, c_name_org FROM cat_category WHERE c_pid = '".$id."';");
		foreach my $line(@$res){
			my $id = $line->{'c_id'};
			my $name_ = $line->{'c_name_org'};
			if (!$name_){$name_ = $line->{'c_name'};}
			$name_ = filter($name_);
			$name = filter(upperFirstLetter($line->{'c_name'}));
			my $c3_alias = $c2_alias."/".Core::DB::Work::translit($name_);
			$db->update("UPDATE cat_category SET`c_name` = '".$name."', `c_alias` = '".$c3_alias."' WHERE c_id = '".$id."'");
			print $name."<br>";
			my $res = $db->query("SELECT c_id, c_name, c_name_org FROM cat_category WHERE c_pid = '".$id."';");
			if ($res){
				foreach my $line(@$res){
					my $id = $line->{'c_id'};
					my $name_ = $line->{'c_name_org'};
					if (!$name_){$name_ = $line->{'c_name'};}
					$name_ = filter($name_);
					$name = filter(upperFirstLetter($line->{'c_name'}));
					my $alias = $c3_alias."/".Core::DB::Work::translit($name_);
					$db->update("UPDATE cat_category SET`c_name` = '".$name."', `c_alias` = '".$alias."' WHERE c_id = '".$id."'");
					print $name."<br>";
				}
			}
		}
	}
}

if (param('category_del') ne "") {

	my $id = param('category_del');
	$catalog->delCat($id);
}

sub filter {
	$name = shift;
	if ($name =~/AC\/DC источники напряжения/){
		$name =~s/AC\/DC источники напряжения/Блоки питания/g; 
	}
	elsif ($name =~/AC\/DC/){
		$name =~s/AC\/DC/Блоки питания/g; 
	}
	if ($name =~/Источники тока/){
		$name =~s/Источники тока/Драйверы/g; 
	}
	elsif ($name =~/источники тока/){
		$name =~s/источники тока/драйверы/g; 
	}	
	if ($name =~/ток\s/){
		$name =~s/ток\s//g; 
	}
	if ($name =~/Флэш-модули/){
		$name =~s/Флэш-модули/Пиксели/g; 
	}
	if ($name =~/флэш-модули/){
		$name =~s/флэш-модули/пиксели/g; 
	}	
	return $name;
}

sub upperFirstLetter {
	my $text = shift;
	$text =~ s/^а/А/g;
	$text =~ s/^б/Б/g;
	$text =~ s/^в/В/g;
	$text =~ s/^г/Г/g;
	$text =~ s/^д/Д/g;
	$text =~ s/^е/Е/g;
	$text =~ s/^ё/Ё/g;
	$text =~ s/^ж/Ж/g;
	$text =~ s/^з/З/g;
	$text =~ s/^и/И/g;
	$text =~ s/^й/Й/g;
	$text =~ s/^к/К/g;
	$text =~ s/^л/Л/g;
	$text =~ s/^м/М/g;
	$text =~ s/^н/Н/g;
	$text =~ s/^о/О/g;
	$text =~ s/^п/П/g;
	$text =~ s/^р/Р/g;
	$text =~ s/^с/С/g;
	$text =~ s/^т/Т/g;
	$text =~ s/^у/У/g;
	$text =~ s/^ф/Ф/g;
	$text =~ s/^х/Х/g;
	$text =~ s/^ц/Ц/g;
	$text =~ s/^ч/Ч/g;
	$text =~ s/^ш/Ш/g;
	$text =~ s/^щ/Щ/g;
	$text =~ s/^ъ/Ъ/g;
	$text =~ s/^ы/Ы/g;
	$text =~ s/^ь/Ь/g;
	$text =~ s/^э/Э/g;
	$text =~ s/^ю/Ю/g;
	$text =~ s/^я/Я/g;
	$text =~ s/^a/A/g;
	$text =~ s/^b/B/g;
	$text =~ s/^c/C/g;
	$text =~ s/^d/D/g;
	$text =~ s/^e/E/g;
	$text =~ s/^f/F/g;
	$text =~ s/^g/G/g;
	$text =~ s/^h/H/g;
	$text =~ s/^i/I/g;
	$text =~ s/^j/J/g;
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