my $db = new Core::DB();


# Публикации в кратком содержании

sub build_Articles
{
	my $limit_public = shift;
	my $sort_public = shift;
	my $public = "";
	$result = $db->query("SELECT *, DATE_FORMAT(date, \"%d-%m-%Y\") as date_normal FROM news WHERE parent = '0' ORDER BY ".$sort_public." LIMIT ".$limit_public."");
	foreach my $line(@$result){
		if ($result){
			if ($line->{'show'} ne "0"){
				($day, $mouth, $year) = split(/\-/, $line->{date_normal});
				if ($mouth eq "01") {$mouth = "января";}
				if ($mouth eq "02") {$mouth = "февраля";}
				if ($mouth eq "03") {$mouth = "марта";}
				if ($mouth eq "04") {$mouth = "апреля";}
				if ($mouth eq "05") {$mouth = "мая";}
				if ($mouth eq "06") {$mouth = "июня";}
				if ($mouth eq "07") {$mouth = "июля";}
				if ($mouth eq "08") {$mouth = "августа";}
				if ($mouth eq "09") {$mouth = "сентября";}
				if ($mouth eq "10") {$mouth = "октября";}
				if ($mouth eq "11") {$mouth = "ноября";}
				if ($mouth eq "12") {$mouth = "декабря";}		
		
				$public .= "<div class='public'>\n
								<div class='container'>\n";
				if ($line->{'show_head'} ne "0"){
					$public .= "<div class='name'><a href='/public/".$line->{'alias'}."'>".$line->{'name'}."</a></div>\n";
				}	$public .= "".$line->{'html_sm'}."\n
								<div class='date'><em>".$day."</em> ".$mouth." ".$year."<span>|</span><a href='/public/".$line->{'alias'}."'>Подробнее</a></div>\n
							</div>
						</div><div class='clear'></div>";

			} else {$public .="";}
		}
	}
	
	if ($public ne ""){$public="<h2>Публикации</h2><div id='public'>".$public."</div>";}
	
	return $public;
}


# Страница публикаций

sub build_Article_main
{
	my $current_page = shift;	
	my $count_pages = shift;
	my $pagess = shift;	
	my $sort_articles = shift;
	if ($current_page eq "all"){$current_page=""; $count_pages="10000";}

	my $content=""; my $color = 0;
	my $result = $db->query("SELECT *, DATE_FORMAT(date, \"%d-%m-%Y\") as date_normal FROM articles WHERE parent = '0' ORDER BY ".$sort_articles." ".($current_page!=""?"LIMIT ".($current_page-1)*$count_pages.",".$count_pages."":"LIMIT 0,".$count_pages."")."");
	foreach my $line(@$result){
		if ($result){
			if ($line->{'show'} ne "0"){
				($day, $mouth, $year) = split(/\-/, $line->{date_normal});
				if ($mouth eq "01") {$mouth = "января";}
				if ($mouth eq "02") {$mouth = "февраля";}
				if ($mouth eq "03") {$mouth = "марта";}
				if ($mouth eq "04") {$mouth = "апреля";}
				if ($mouth eq "05") {$mouth = "мая";}
				if ($mouth eq "06") {$mouth = "июня";}
				if ($mouth eq "07") {$mouth = "июля";}
				if ($mouth eq "08") {$mouth = "августа";}
				if ($mouth eq "09") {$mouth = "сентября";}
				if ($mouth eq "10") {$mouth = "октября";}
				if ($mouth eq "11") {$mouth = "ноября";}
				if ($mouth eq "12") {$mouth = "декабря";}

					my $html_sm = $line->{'html'};
					$html_sm =~ s/<script[^>]*?>.*?<\/script>//g;
					$html_sm =~ s/<[\/\!]*?[^<>]*?>//g;
					$html_sm =~ s/([\r\n])[\s]+//g;
					$html_sm =~ s/&(quot|#34);//g;
					$html_sm =~ s/&nbsp;/ /g;
					$html_sm =~ s/\s+/ /g;
					$html_sm =~ s/\'/\\'/g;
					my $string = length($html_sm);
					if ($string > 194){
						$html_sm=substr($html_sm,0,194); $html_sm=qq~$html_sm...~;
					}
				
				$color++;
				if ($color == 6){$color = 1;}
					
				$content .='<div class="art-article theme'.$color.'" onclick="document.location=\'/public/'.$line->{'alias'}.'\'">
					<div class="art-photo">
						<a href="/public/'.$line->{'alias'}.'"><img src="'.$dirs_public_www.'/'.($line->{'id'}+1000).'.jpg" alt="'.$line->{'name'}.'"></a>
						<div class="art-clear"></div>
					</div>
					<div class="art-text">
						<div class="art-head">
							<div class="art-date"><strong>'.$day.'</strong><span class="art-date-month">'.$mouth.'</span><span class="art-date-year">'.$year.'</span></div>
							<a href="/public/'.$line->{'alias'}.'" class="art-name">'.$line->{'name'}.'</a>
							<div class="art-clear"></div>
						</div>
						<p>'.$html_sm.'</p>
						<div class="art-more">
							<a class="art-more-link" href="/public/'.$line->{'alias'}.'">Подробнее »</a>
						</div>
					</div>
					<div class="art-clear"></div>
				</div>';

			} else {$content .="";}
		}
	}
	
	# Страницы публикаций //
	
	my $pages = $pagess;
	my $page = $current_page;
	my $i=1; my $p=""; my $pagess=""; my $path = "/public/";
	while ($i <= $pages) {
		if ($i > ($page-4) && $i < ($page-2)){
			$pagess .= '<li><a href="'.$path.($i > 1?'page_'.$i.'':'').'">&larr;</a></li>';
		}			
		elsif ($i > ($page-3) && $i < ($page+3) && $page > 2 or $page < 3 && $i < 6){
			if ($i == $page) {$p = '<li class="art-active"><a href="#">'.$page.'</a></li>';}
			elsif ($page == "") {$p = ''.($i == 1?'<li class="art-active"><a href="#">'.$i.'</a></li>':'<li><a href="'.$path.'page_'.$i.'">'.$i.'</a></li>').'';}
			else {$p = ''.($i == 1?'<li><a href="'.$path.'">'.$i.'</a></li>':'<li><a href="'.$path.'page_'.$i.'">'.$i.'</a></li>').'';}
			$pagess .= $p;
		}
		elsif ($i > ($page+2) && $i < ($page+4) && $page > 2 or $page < 3 && $i == 6){
			$pagess .= '<li><a href="'.$path.'page_'.$i.'">&rarr;</a></li>';
		}
		$i++;
	}
	if ($i == "2") {$pagess ="";} else {$pagess = '<ul class="art-pagination"><li class="art-first">Страница</li>'.$pagess.'</ul>';}	
	
	if ($content ne ""){
		$content ='<link href="/css/template3.css" rel="stylesheet">
			<div id="art-mainArticle">
				<div class="art-body">	
					<h1>Материалы о мире света<span> и светодиодов</span></h1>
					'.($pagess?'<div class="art-nav">'.$pagess.'</div>':'').'
					<div class="art-clear"></div>	
					<div id="art-blog" class="art-blog effect-2">
						'.$content.'
					</div>
					<div class="art-nav-bottom">
						'.$pagess.'
					</div>
					<div class="art-clear"></div>
				</div>
				<div class="art-video">
					<h2>Видео публикации</h2>
					<a class="link-to" href="/public/video/">Все видео</a>';
					
				$content .= build_VideoList(5, "main");

		$content .='		
				</div>
			</div>';
	}
	
	return $content;
}


# Страница публикации

sub build_Article
{
	my $id = shift;
	my $name = shift;
	my $content = shift;
	my $result="";
	my $res = $db->query("SELECT *, DATE_FORMAT(date, \"%d-%m-%Y\") as date_normal FROM articles WHERE id = '".$id."' LIMIT 1");
	foreach my $line(@$res){
		if ($line->{'show'} ne "0"){
			($day, $mouth, $year) = split(/\-/, $line->{date_normal});

			$result = '<div class="content-holder content-text content-news content-category">
						<img class="first" src="'.$dirs_public_www.'/'.($line->{'id'}+1000).'_big.jpg" alt="'.$line->{'name'}.'">
						'.$content.'
						<div class="date"><em>'.$day.'</em> '.$mouth.' '.$year.'<span>|</span><a href="/public/">Все публикации</a></div>
					</div>'.shareLinks();
		}
	}

	$name = '<div class="title">
		<a href="/public/" class="back" style="margin-bottom:8px;">Публикации</a>
		<h1 class="name">'.$name.'</h1>
	  </div>';
	
	return ($name, $result);
}

# Страница видео публикаций

sub build_VideoContent
{
	
	my $name = '<div class="title">
					<h1>Видео раздел: LED, свет, освещение</h1>
					<a class="name back" href="/public/">Вернуться к публикациям</a>
				</div>';
				
	$content = build_VideoList();

	if ($content){
		$content ='<link href="/css/template3.css" rel="stylesheet">
		<div id="art-mainArticle">
			<div id="art-video" class="art-video effect-2">
				'.$content.'
			</div>
		</div>'.shareLinks();
	}
	else {
		$content ='<div class="content-holder content-text">
			<p>В разделе еще нет видео материалов.</p>
		</div>';
	}
	
	return ($name, $content);
}

sub build_VideoList {

	my $limit = shift;
	my $section = shift;
	
	if (!$limit) {$limit = 1000;}

	my $content="";	my $color = 0; my $i = 0;
	open OUT, ("$dirs_video_www2/video.txt"); @list = <OUT>; 
	@list = reverse sort(@list);
	foreach my $line(@list){
		$i++; if ($limit == $i){last;}
		my ($num, $name, $url, $date) = split(/\|/, $line);
		my ($year, $mouth_, $day) = split(/\-/, $date);
		my $mouth = getMouth($mouth_);
		$color++;
		if ($color == 7){$color = 1;}
		if ($section eq "main"){$color = "6"}
		$content .='<div class="art-article theme'.$color.''.($section eq "main"?' first':'').'" data-video="'.$url.'">
					<div class="art-photo">
						<a href="/public/video/#'.$url.'">
							<img class="art-play" src="/img/play.svg" />
							<img class="art-play art-play-green" src="/img/play_green.svg" />
							<img class="image" src="'.$dirs_video_www.'/'.$num.'.jpg" alt="'.$name.'" />
							<i class="art-photo-shadow"></i>
						</a>
					</div>
					<div class="art-text">
						<div class="art-head">
							<div class="art-date"><strong>'.$day.'</strong><span class="art-date-month">'.$mouth.'</span><span class="art-date-year">'.$year.'</span></div>
							<a href="/public/video/#'.$url.'" class="art-name">'.$name.'</a>
							<div class="art-clear"></div>
						</div>
					</div>
				</div>';
	}	
	
	return $content;
}

sub getMouth {

	my $mouth = shift;

	if ($mouth eq "01") {$mouth = "января";}
	if ($mouth eq "02") {$mouth = "февраля";}
	if ($mouth eq "03") {$mouth = "марта";}
	if ($mouth eq "04") {$mouth = "апреля";}
	if ($mouth eq "05") {$mouth = "мая";}
	if ($mouth eq "06") {$mouth = "июня";}
	if ($mouth eq "07") {$mouth = "июля";}
	if ($mouth eq "08") {$mouth = "августа";}
	if ($mouth eq "09") {$mouth = "сентября";}
	if ($mouth eq "10") {$mouth = "октября";}
	if ($mouth eq "11") {$mouth = "ноября";}
	if ($mouth eq "12") {$mouth = "декабря";}
	
	return $mouth;
}

sub random_int ($$) {
    my($min, $max) = @_;
    return $min if $min == $max;
    ($min, $max) = ($max, $min) if $min > $max;
    return $min + int rand(1 + $max - $min);
}

1;