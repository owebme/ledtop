# Обратная связь на странице

sub build_feedbackPage
{
	my $content = shift;
	my $class="";
	if ($content eq ""){$class=' class="no_head"';}
	
	my $num1 = random_num(1,20);
	my $num2 = random_num(1,20);
	my $num3 = random_num(1,10);
	
my $feedback="";

	$feedback=qq~
	<script src="/js/validate/js/default.js" language="JavaScript" type="text/javascript"></script>
	<script src="/js/validate/js/validate_page.js" language="JavaScript" type="text/javascript"></script>
	<script src="/js/validate/js/baloon.js" language="JavaScript" type="text/javascript"></script>
	<link href="/js/validate/css/baloon.css" rel="stylesheet" type="text/css" /> 
	<div style="display:none;">
		<img src="/js/validate/i/baloon-body.gif" alt="">
		<img src="/js/validate/i/baloon-footer.gif" alt="">
		<img src="/js/validate/i/baloon-header.gif" alt="">
		<img src="/js/validate/i/baloon-header-flip.gif" alt="">		
	</div>
	
	<div style="clear:both"></div>
	<div id="feedback_info">Сообщение отправлено...<br> Мы обязательно ответим на него в ближайшее время.</div>
	<div id="feedback_page"$class>
	<div id="feedback_container" class="simple">
	<form method="post" action="/cgi-bin/send_mail_page.cgi" target="send">
	<input type="hidden" name="captcha_num1" value="$num1">
	<input type="hidden" name="captcha_num2" value="$num2">
	<input type="hidden" name="captcha_num3" value="$num3">
	<table class="form" cellpadding="0" cellspacing="0">
		<tr>
			<td colspan="2" class="head"><h1>Обратная связь</h1></td>
		</tr>
		<tr>
			<td class="name"><span style="color:red;">*</span>Как к Вам обратиться?</td>
			<td><input class="name" name="name" value="" format=".+" notice="Введите Ваше имя" type="text"></td>
		</tr>
		<tr>
			<td class="name"><span style="color:red;">*</span>Тема письма:</td>
			<td><input class="name" name="tema" value="" format=".+" notice="Введите тему письма" type="text"></td>
		</tr>		
		<tr>
			<td class="name"><span style="color:red;">*</span>Электронная почта:</td>
			<td><input class="name" name="mail" value="" format="email" notice="Введите Ваш e-mail" type="text"></td>
		</tr>
		<tr>
			<td class="name">Мобильный телефон:</td>
			<td><input class="name" name="phone" value="" type="text"></td>
		</tr>
		<tr>
			<td class="name comment"><span style="color:red;">*</span>Сообщение:</td>
			<td><textarea name="note" format=".+" notice="Введите сообщение"></textarea></td>
		</tr>
		<tr>
			<td class="name captcha"><span class="num1">$num1</span> + <span class="num2">$num2</span> - <span class="num3">$num3</span> = <em>?</em></td>
			<td><input class="name" name="captcha" value="" placeholder="Введите число" type="text"></td>
		</tr>
		<tr>
			<td colspan="2"><input name="send" class="button right" type="submit" value="Отправить сообщение" /></td>
		</tr>
	</table>

	<iframe style="display:none; width:1px; height:1px;" name="send"></iframe>
	</form>
	</div>
	</div>~;

return $feedback;

}

sub random_num ($$) {
    my($min, $max) = @_;
    return $min if $min == $max;
    ($min, $max) = ($max, $min) if $min > $max;
    return $min + int rand(1 + $max - $min);
}

1;