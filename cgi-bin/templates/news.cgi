my $db = new Core::DB();


# ������� � ������� ����������

sub build_News
{
	my $limit_news = shift;
	my $sort_news = shift;
	my $theme = shift;	
	my $news = "";
	$result = $db->query("SELECT *, DATE_FORMAT(date, \"%d-%m-%Y\") as date_normal FROM news WHERE parent = '0' ORDER BY ".$sort_news." LIMIT ".$limit_news."");
	my $num=""; $counts = scalar @$result;
	foreach my $line(@$result){
		if ($result){
			if ($line->{'show'} ne "0"){
				$num++;
				($day, $mouth, $year) = split(/\-/, $line->{date_normal});
				if ($mouth eq "01") {$mouth = "������";}
				if ($mouth eq "02") {$mouth = "�������";}
				if ($mouth eq "03") {$mouth = "�����";}
				if ($mouth eq "04") {$mouth = "������";}
				if ($mouth eq "05") {$mouth = "���";}
				if ($mouth eq "06") {$mouth = "����";}
				if ($mouth eq "07") {$mouth = "����";}
				if ($mouth eq "08") {$mouth = "�������";}
				if ($mouth eq "09") {$mouth = "��������";}
				if ($mouth eq "10") {$mouth = "�������";}
				if ($mouth eq "11") {$mouth = "������";}
				if ($mouth eq "12") {$mouth = "�������";}	

				$news .='<li>
							<span class="date">'.$day.' '.$mouth.' '.$year.'</span>
							<a href="/news/'.$line->{'alias'}.'"'.($num eq "1" && $counts > 2?' class="new"':'').''.($num eq "2" && $counts > 2?' class="new"':'').'>'.$line->{'html_sm'}.'</a>
						</li>';

			} else {$news .="";}
		}
	}
	
	if ($news){$news ='<div class="news-holder">
						<div class="title">
							<h3>�������</h3>
							<a href="/news/">��� �������</a>
						</div>
						<ul class="news-list">
							'.$news.'
						</ul>
					</div>';}
	
	return $news;
}


# �������� ��������

sub build_New_main
{
	my $sort_news = shift;
	my $theme = shift;
	$name = '<div class="title"><h1>�������</h1></div>';

	my $content="";
	my $result = $db->query("SELECT *, DATE_FORMAT(date, \"%d-%m-%Y\") as date_normal FROM news WHERE parent = '0' ORDER BY ".$sort_news."");
	foreach my $line(@$result){
		if ($result){
			if ($line->{'show'} ne "0"){
				($day, $mouth, $year) = split(/\-/, $line->{date_normal});
				if ($mouth eq "01") {$mouth = "������";}
				if ($mouth eq "02") {$mouth = "�������";}
				if ($mouth eq "03") {$mouth = "�����";}
				if ($mouth eq "04") {$mouth = "������";}
				if ($mouth eq "05") {$mouth = "���";}
				if ($mouth eq "06") {$mouth = "����";}
				if ($mouth eq "07") {$mouth = "����";}
				if ($mouth eq "08") {$mouth = "�������";}
				if ($mouth eq "09") {$mouth = "��������";}
				if ($mouth eq "10") {$mouth = "�������";}
				if ($mouth eq "11") {$mouth = "������";}
				if ($mouth eq "12") {$mouth = "�������";}		
				
				my $image=""; my $rand_num=rand(1);
				if ($hide_news_photo ne "1"){
					my $img_num = $line->{id}+1000;
					if (-e "$dirs_news_www2/$img_num.jpg"){
						$image =qq~<img src="$dirs_news_www/$img_num.jpg?$rand_num" alt="">~;
					}
					else {
						$image =qq~<img src="/admin/site/img/no_photo.png" alt="">~;
					}
				}
				$content .= '<li>';
				if ($image ne ""){
					$content .= '<div class="foto"><a href="/news/'.$line->{'alias'}.'">'.$image.'</a></div>';
				}
				$content .= '<span class="date">'.$day.' '.$mouth.' '.$year.'</span>
							 <a href="/news/'.$line->{'alias'}.'">'.$line->{'name'}.'</a>
							 <p>'.$line->{'html_sm'}.'</p>';
				$content .= '</li>';

			} else {$content .="";}
		}
	}
	if ($content ne ""){$content='<div class="content-holder news-arhive"><ul class="news-list">'.$content.'</ul></div>';}
	
	return $content;
}


# �������� �������

sub build_New
{
	my $id = shift;
	my $content = shift;
	my $theme = shift;
	my $result="";
	my $res = $db->query("SELECT *, DATE_FORMAT(date, \"%d-%m-%Y\") as date_normal FROM news WHERE id = '".$id."' LIMIT 1");
	foreach my $line(@$res){
		if($line->{'show'} ne "0"){
			($day, $mouth, $year) = split(/\-/, $line->{date_normal});
			if ($mouth eq "01") {$mouth = "������";}
			if ($mouth eq "02") {$mouth = "�������";}
			if ($mouth eq "03") {$mouth = "�����";}
			if ($mouth eq "04") {$mouth = "������";}
			if ($mouth eq "05") {$mouth = "���";}
			if ($mouth eq "06") {$mouth = "����";}
			if ($mouth eq "07") {$mouth = "����";}
			if ($mouth eq "08") {$mouth = "�������";}
			if ($mouth eq "09") {$mouth = "��������";}
			if ($mouth eq "10") {$mouth = "�������";}
			if ($mouth eq "11") {$mouth = "������";}
			if ($mouth eq "12") {$mouth = "�������";}	
			
			my $referer = $ENV{"HTTP_REFERER"};
			if ($referer =~/\/news\//) {$referer = "��������� � ��������";}
			else {
				$referer = "��� �������";
			}
			
			$result = '<div class="content-holder content-text content-news">'.$content.'<div class="date"><em>'.$day.' '.$mouth.' '.$year.'<span>|</span></em><a href="/news/">'.$referer.'</a></div></div>'.shareLinks();
		}
	}	
	return $result;
}

1;