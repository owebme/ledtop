my $db = new Core::DB();


# Вопросы и ответы

sub build_Questions
{

	open(BO, "admin/$dirs/set_question"); my @set_questions = <BO>; close(BO);
	foreach my $line(@set_questions)
		{
	chomp($line);
	my ($name_admin1, $message1, $email1, $check_email1, $check_auto_update1, $size_body1, $count_pages1, $clear_limit1) = split(/\|/, $line);
	$name_admin=qq~$name_admin1~;
	$message_top=qq~$message1~;
	$size_body=qq~$size_body1~;
	$count_pages=qq~$count_pages1~;		
		}		

	my $size_form="";
	if ($size_body =~ /%/) {
		$size_form = "width: ".$size_body;
		$size_body = "width: ".$size_body;		
	}
	else {
		$size_form = $size_body-18;
		$size_form = "width: ".$size_form."px";
		$size_body = "width: ".$size_body;
	}
	
	my $questions = $db->query("SELECT questions.q_id FROM questions WHERE q_status = '1' AND q_client_id = '0'");
	my $pages_amount="";
	foreach my $item(@{$questions}){
		$pages_amount++;
	}
				
	my $pagess = $pages_amount/$count_pages;
	$pagess = $pagess+0.49;
	$pagess = sprintf("%.0f",$pagess);	
	

	my $message="";
	my $result = $db->query("SELECT *, DATE_FORMAT(q_date, \"%d-%m-%Y\") as q_date_normal, DATE_FORMAT(q_date, \"%H:%i\") as q_time FROM questions WHERE q_status = '1' AND q_client_id = '0' ORDER BY q_date DESC LIMIT 0,".$count_pages."");
	foreach my $line(@$result){
		if ($line->{q_status} eq "1" && $line->{q_client_id} eq "0"){
		$message .='<div class="item que">
						<p class="author">'.$line->{q_name}.'</p>
						<p>'.$line->{q_html}.'</p>
						<div class="date">'.$line->{q_date_normal}.' в '.$line->{q_time}.'</div>
					</div>';
					
			my $res = $db->query("SELECT *, DATE_FORMAT(q_date, \"%d-%m-%Y\") as q_date_normal, DATE_FORMAT(q_date, \"%H:%i\") as q_time FROM questions WHERE q_client_id = '".$line->{q_id}."' ORDER BY q_date ASC");			
			foreach my $line(@$res){
			$message .='<div class="item answer">
							<img class="admin" src="/admin/site/img/avator.gif" alt="">
							<p class="author">'.$line->{q_name}.'</p>
							<p>'.$line->{q_html}.'</p>
							<div class="date">'.$line->{q_date_normal}.' в '.$line->{q_time}.'</div>
						</div>';
			}
			
		}
		else {$message .='';}
	}
	
	my $i=1;
	while ($i <= $pagess) {
		if ($i == $curent_page) {$page = '<a class="current" id="'.$count_pages.'" href="#">'.$curent_page.'</a>';}
		elsif ($curent_page == "") {$page = ''.($i == 1?'<a class="current" id="'.$count_pages.'" href="#">'.$i.'</a>':'<a href="#" id="'.$count_pages.'">'.$i.'</a>').'';}
		else {$page = ''.($i == 1?'<a href="#" id="'.$count_pages.'">'.$i.'</a>':'<a href="#" id="'.$count_pages.'">'.$i.'</a>').'';}
		$pages .= $page;
		$i++;
			}
	if ($i == "2") {$pages_show ="";} else {$pages_show = $pages;}	


	my $questions ="";
	$questions .= '<div class="questions" style="'.$size_body.'">
						<div class="container-que">
							<div class="main">
								<div class="page">'.$pages_show.'</div>
								<p class="author">'.$name_admin.'</p>
								<p>'.$message_top.'</p>
							</div>
							<div class="body-que">
								'.$message.'								
							</div>
						</div>
						<div class="send_form">
							<div class="container-send">
								<input type="text" style="'.$size_form.'" class="name" value="Представьтесь, пожалуйста...">
								<textarea style="'.$size_form.'" class="question">Ваш вопрос...</textarea>
								<button class="send_que">Отправить</button>
							</div>
						</div>
						<div class="clear"></div>
					</div>';

	return $questions;
}


1;