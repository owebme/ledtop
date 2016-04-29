
# Контактная информация

sub build_Contacts
{
	open(BO, "admin/layouts/set_phone"); my @phone = <BO>; close(BO);
	foreach my $line(@phone)
		{
	chomp($line);
	my ($phone_code1_, $phone_num1_, $phone_code2_, $phone_num2_) = split(/\|/, $line);
	$phone_code1=qq~$phone_code1_~;
	$phone_num1=qq~$phone_num1_~;
	$phone_code2=qq~$phone_code2_~;
	$phone_num2=qq~$phone_num2_~;
		}
		
	$phone = '<div id="fph1"><p><span>'.$phone_code1.'</span> '.$phone_num1.'</p></div>';
	
	if ($phone_code2 ne "" && $phone_num2 ne ""){
		$phone .= '<div id="fph2"><p><span>'.$phone_code2.'</span> '.$phone_num2.'</p></div>';
	}
	
	if ($hide_address_set ne "1"){
		open OUT, ("admin/layouts/set_address"); @address = <OUT>;
		foreach my $text(@address) {$address=qq~$address$text~;}
	}
	if ($hide_timemode_set ne "1"){
		open OUT, ("admin/layouts/set_timemode"); @timemode = <OUT>;
		foreach my $text(@timemode) {$timemode=qq~$timemode$text~;}
	}
	if ($hide_copyright_set ne "1"){
		open OUT, ("admin/layouts/set_copyright"); @copyright = <OUT>;
		foreach my $text(@copyright) {$copyright=qq~$copyright$text~;}
	}

	return ($phone, $address, $timemode, $copyright);
}	
	
1;