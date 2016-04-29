#!/usr/bin/perl
BEGIN {push (@INC, '../engine/lib');}

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;
use Core::DB::Work;
use Core::DB::Users;
use Encode "from_to";

require "../engine/lib/parametr.cgi";

$group_id=param('group_id');
$group_name=param('group_name');
$add_group1=param('add_group1');
$add_group2=param('add_group2');

print header(-type => 'text/html', -charset => 'windows-1251'); 

$db = new Core::DB();

my $group = new Core::DB::Users();

if ($group_id && $group_name) {

	from_to($group_name, "utf-8", "cp1251");
	
	if ($group_id eq "new"){
	
		my $result = $db->query("SELECT g_id FROM users_group ORDER BY g_id DESC LIMIT 1");
		$group_id = $result->[0]->{"g_id"}+1;		
		
		my %params = (
			'g_name' => $group_name
		);
		$group->addUserGroup(\%params);
	}
	elsif ($group_id > 0) {
		$db->delete("DELETE FROM users_group_category WHERE group_id = '".$group_id."'");
		$db->update("UPDATE users_group SET `g_name`='".$group_name."' WHERE g_id='".$group_id."'");
	}
	
	if ($add_group1){
		while ($add_group1 =~ m/(.+?)\|/g) {
			my %params = (
				'group_id' => $group_id,
				'cat_id' => $1,
				'type' => "opt_small"
			);
			$group->addUserGroupCategory(\%params);
		}
	}
	if ($add_group2){
		while ($add_group2 =~ m/(.+?)\|/g) {
			my %params = (
				'group_id' => $group_id,
				'cat_id' => $1,
				'type' => "opt_large"
			);
			$group->addUserGroupCategory(\%params);
		}
	}
	
	print "true";
}
