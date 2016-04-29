
sub prodTitle {

	$title = shift;
	
	if ($title =~/Day White/){
		$title =~ s/Day White/����� ������� Day White/g;
	}
	elsif ($title =~/S-Warm/){
		$title =~ s/S-Warm/����� ������ S-Warm/g;
	}
	elsif ($title =~/Warm/){
		$title =~ s/Warm/����� ������ Warm/g;
	}	
	elsif ($title =~/White/){
		$title =~ s/White/����� White/g;
	}
	elsif ($title =~/Cool/){
		$title =~ s/Cool/����� �������� Cool/g;
	}
	elsif ($title =~/Blue/){
		$title =~ s/Blue/����� Blue/g;
	}
	elsif ($title =~/Green/){
		$title =~ s/Green/������� Green/g;
	}
	elsif ($title =~/IR880/){
		$title =~ s/IR880/����������� IR880/g;
	}
	elsif ($title =~/UV400/){
		$title =~ s/UV400/���������� UV400/g;
	}	
	elsif ($title =~/Orange/){
		$title =~ s/Orange/��������� Orange/g;
	}
	elsif ($title =~/Pink/){
		$title =~ s/Pink/������� Pink/g;
	}
	elsif ($title =~/Red/){
		$title =~ s/Red/������� Red/g;
	}	
	elsif ($title =~/Yellow/){
		$title =~ s/Yellow/������ Yellow/g;
	}	
	elsif ($title =~/RGB/){
		$title =~ s/RGB/������������� RGB/g;
	}		
	
	return $title;
}

sub prodDesc {

	my $desc = shift;
	
	if ($desc =~/�����/){
		$desc =~ s/�����/�����/g;
	}
	return $desc;
}

sub buildTitle {

	my $id = shift;	
	my $params = shift;
	
	my $db = new Core::DB();
	
	my $title=""; my $subTitle="";
	if ($params eq "category"){
	
		my $result = $db->query("SELECT c_name, c_pid FROM cat_category WHERE c_id = '".$id."';");
		foreach my $item(@$result){
			$title .= Core::DB::Work::upperString($item->{'c_name'}).' ';
			if ($subTitle = buildSubTitle($item->{'c_pid'}, Core::DB::Work::lowerString($item->{'c_name'}))){
				$title .= $subTitle.' ';
			}
		}
	}
	$title =~ s/\/\s\// \//g;
	$title =~ s/\s+/ /g;
	$title =~ s/\s$//g;
	
	return $title;
	
	sub buildSubTitle {
	
		my $id = shift;
		my $name = shift;
		my $title="";
		
		my $result = $db->query("SELECT c_name, c_pid FROM cat_category WHERE c_id = '".$id."';");
		foreach my $item(@$result){
			if ($result){
				if ($item->{'c_pid'} eq "0"){
					$title .= '/ '.$item->{'c_name'};
				}
				else {
					my $name_ = Core::DB::Work::lowerString($item->{'c_name'});
					if ($name){
						$name =~ s/\[//g;
						$name =~ s/\]//g;
						$name =~ s/\(//g;
						$name =~ s/\)//g;
						$name =~ s/\+//g;
						my @words = split / /, $name;
						foreach my $item(@words){
							$name_ =~ s/$item//gi;
						}
					}
					$title .= $name_.' ';
				}
				if ($subTitle = buildSubTitle($item->{'c_pid'})){
					$title .= $subTitle.' ';
				}
				return $title;
			}
			else {
				return 0;
			}
		}
	}
}

sub catTitle {

	my $section = shift;
	
	my %title = ();
	if ($section == "2"){
		%title = (
			'title' => 'C����������� ����� ������ ������� ��������, LED smd ����������� � RGB, 5050 (5060), 3528, 5630, 2835, ������� �����, �������, �������, 5v, 12v, 24v, 36v, 220 �����, ������ ����, ����������',
			'desc' => '������ ������������ ����� ������� �������� �� ��������� �����, ��� �����, rgb, 5050 (5060), 3528, 5630, 2835, ����� ������� � �������, ����������� �� 5v �� 220 �����, ������ ����, ����������',
			'keys' => '������������ �����, ������������ ����� rgb, led ������������ �����, ������������ ����� 12 �����, ������������ ����� 24 �����, ������������ ����� �����, ����� ������������ �����, ������������ ����������� �����'
		)
	}
	elsif ($section == "89"){
		%title = (
			'title' => 'C����������� ����� ������ ������ LUX (����), ������������ ����� ������� ������, �����: rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������������ ����� ������ LUX (����), ����� �������� ��������, ������� ������, rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'keys' => '������������ ����� lux, ������������ ����� ����, ����� ������������ �������, ������������ ����� ������� ������'
		)
	}
	elsif ($section == "90"){
		%title = (
			'title' => 'C����������� ����� 3528 ������ �� 12v/24v, 60/120/240 ��/�, rgb led 3528 smd �����, ip33, ip65, ip67, �����: �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������������ ����� � ���������� ����������� 3528 �������� ��������, ip33, ip65, ip67, rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'keys' => '������������ ����� 3528, ����� 3528 60, ������������ ����� led smd 3528, rgb ����� 3528, ������������ ����� 3528 ������ �����, ������������ ����� 3528 120 led'
		)
	}
	elsif ($section == "91"){
		%title = (
			'title' => 'C����������� ����� 5060(5050) ������ �� 12v/24v, 60/120/240 ��/�, rgb led 5050 smd �����, ip20, ip33, ip65, ip67, �����: �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������������ ����� � ���������� ����������� 5050 �������� ��������, ip20, ip33, ip65, ip67, rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'keys' => '������������ ����� 5050, led ����� 5050, rgb ����� 5050, ����� smd 5050, rgb led ����� 5050, ������������ ����� smd 5050 60, ������������ ����� 5050 120'
		)
	}
	elsif ($section == "92"){
		%title = (
			'title' => 'C����������� ����� 5630, 2835 ������ ����� �� 12v/24v, 60/120/240 ��/�, rgb led 5630 smd �����, ip20, ip33, ip65, ip67, �����: �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������������ ����� � ���������� ����������� 5630 � 2835 �������� ��������, ip20, ip33, ip65, ip67, rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'keys' => '����� 5630, ����� 2835, ������������ ����� 5630, ����� ������������ 2835, ����� smd 5630, led ����� 5630, ����� ������������ smd 5630, ������������ ����� 5630 60'
		)
	}
	elsif ($section == "93"){
		%title = (
			'title' => 'C����������� ����� 5��, ����� ����� �� 12v/24v, 60/120 ��/�, �����: �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ����� ������������ ����� 5��, ���� ������: �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'keys' => '����� 5��, ����� ������������ 5��, ������������ ����� ������� 5 ��, ����� ������������ �����'
		)
	}
	elsif ($section == "94"){
		%title = (
			'title' => 'C����������� ����� RGB (�������������) ������ �� 12v/24v, 60/120 ��/�, ����� rgb 5050 smd led �����, ip20, ip33, ip65, ip66, ip67',
			'desc' => '������ ������������ rgb �����, rgb led ����� �������� ��������',
			'keys' => 'rgb �����, ������������ ����� rgb, rgb ����� 5050, ����� rgb 60, ����� 5050 60 rgb, ����� smd 5050 rgb'
		)
	}
	elsif ($section == "95"){
		%title = (
			'title' => '������������ ����� ������� ����� ������ �� 12v/24v, 60 ��/�, ����� rgb ������� �����, ip20, ip33, ip65, ip66',
			'desc' => '������ ������������ ����� ������� �����, ����� �������� ��������',
			'keys' => '������� ����� �����, ������������ ����� ������� �����'
		)
	}
	elsif ($section == "96"){
		%title = (
			'title' => '������������ ����� �������, ������� ������ �� 12v/24v, 60/120 ��/�, ����� �������� �������� ip33, ip65, ip66, �����: �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������������ ����� �������� �������� �������� ��������',
			'keys' => '������� �����, ������������ ����� �������, ����� �������� ��������, ������������ ����� �������, ������������ ����� �������� ��������'
		)
	}
	elsif ($section == "97"){
		%title = (
			'title' => '������������ ������ ���� ������ �� 220v, 72 ��/�, ������ ����� ip67, �����: rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������ ���� �������� ��������',
			'keys' => '������ �����, ������������ ������ ����, �������� ������ ����, ������ ���� ��� ����'
		)
	}
	elsif ($section == "98"){
		%title = (
			'title' => '������������ ������������ WR-���� ������ �� 12v, 20 ��/�, ������������ �������� ip65, �����: rgb, �����, ��������, ������, �����, ������, �������, ���������, ����������������, �������',
			'desc' => '������ ������������ WR-���� �������� ��������',
			'keys' => '������������ ����, ������������ �������� ����, ������������ ���� ��� ����'
		)
	}
	elsif ($section == "99"){
		%title = (
			'title' => '���������� ��� ������������ ����� ������, ��������� ��� RGB �����',
			'desc' => '������ ���������� ��� ������������ ����� �������� ��������',
			'keys' => '��������� ��� �����, ��������� ��� ������������ �����, ��������� rgb �����, ��������� ��� ������������ ����� ������, ��������� ��� ����� 3528, ��������� ������� ��� ������������ �����, ��������� ��� rgb ������������ �����, ��������� ��� led �����, ��������� ��� ������� �����'
		)
	}	
	
	return %title;
}

1;