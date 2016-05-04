#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use Core::Config;
use Core::DB;

my $db = new Core::DB();

$sort=param('sort');
$cat_alias=param('cat_alias');
$brand_alias=param('brand_alias');
$current_page=param('page_cat');
$raiting=param('raiting');
$raiting_id=param('raiting_id');
$ask_product_id=param('ask_product_id');
$filter_price=param('filter_price');
$filter_price_pointer=param('filter_price_pointer');
$autocomplete=param('autocomplete');
$get_autocomplete_alias=param('get_autocomplete_alias');
$buy_quick=param('buy_quick');
$reviews_raiting=param('reviews_raiting');
$reviews_raiting_id=param('reviews_raiting_id');
$reviews_raiting_name=param('reviews_raiting_name');
$reviews_raiting_text=param('reviews_raiting_text');
$products_ids=param('products_ids');
$products_limit=param('products_limit');
$products_cat_name=param('products_cat_name');

require "admin/engine/lib/parametr.cgi";
require "templates/catalog.cgi";
require "templates/products.cgi";
if (cookie("private_login")){
	require "templates/auth.cgi";
}

print header(-type => 'text/html', -charset => 'windows-1251');

if ($cat_alias ne ""){

	$cat_alias =~ s/#//g;
	$cat_alias =~ s/#!//g;
	$cat_alias =~ s/\/page_(.*)$//g;
	
	open(BO, "$dirs_catalog_www2/page_settings.txt"); my @pages_count = <BO>; close(BO);
	foreach my $line(@pages_count)
		{
	chomp($line);
	my ($pages_admin, $pages_site) = split(/\|/, $line);
	$count_pages=qq~$pages_site~;
		}	
	my $products="";
	if ($filter_price ne "" && $filter_price_pointer ne "" or cookie("filter_price") ne "" && cookie("filter_price_pointer") ne ""){
		my $filter_price = cookie("filter_price");
		my $filter_price_pointer = cookie("filter_price_pointer");
		$products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id, c.c_name FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE c.c_alias ='".$cat_alias."'".($filter_price_pointer eq "to"?" AND p.p_price <= '".$filter_price."'":" AND p.p_price > '".$filter_price."'")." AND p.p_show != '0' AND p.p_price != '0'");				
	}	
	else {
		$products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id, c.c_name FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE c.c_alias ='".$cat_alias."' AND p.p_show != '0'");	
	}
	my $pages_amount="";
	foreach my $product(@{$products}){
		$pages_amount++;
		$num_edit = $product->{'cat_id'};
		$cat_name = $product->{'c_name'};
	}	
	my $pagess="";
	if ($pages_amount ne ""){
		$pagess = $pages_amount/$count_pages;
		$pagess = $pagess+0.49;
		$pagess = sprintf("%.0f",$pagess);
	}
	
	if ($sort eq "" && !cookie("sort_products")){
		open(BO, "admin/$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
		foreach my $line(@select_sort){chomp($line);
		my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
		$sort=qq~$select_sort_product_~;}	
	}

	$product_cat = build_ProductCat($num_edit, $current_page, $count_pages, $cat_name, $cat_alias, $pagess, $sort, "ajax", $brand_alias);
	
	print $product_cat;
}

if ($raiting ne "" && $raiting_id ne ""){

	my $raiting_all = $raiting; my $count=1;
	my $result = $db->query("SELECT cat_product_raiting.r_raiting FROM cat_product_raiting WHERE p_id ='".$raiting_id."'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'r_raiting'};
		$count++;
	}
	my $result = $db->query("SELECT cat_product_reviews.v_raiting FROM cat_product_reviews WHERE p_id ='".$raiting_id."' AND v_public = '1'");
	foreach my $line(@$result){
		$raiting_all = $raiting_all+$line->{'v_raiting'};
		$count++;
	}
	$raiting_all = $raiting_all/$count;
	$raiting_all = sprintf("%.1f",$raiting_all);
	
	print '<div p_raiting="'.$raiting_all.'" p_id="'.$raiting_id.'" class="raiting" id="no_active">
				<div class="raiting_blank"></div>
				<div class="raiting_hover"></div>
				<div class="raiting_votes"></div>
			</div>';
	
	$db->update("UPDATE cat_product SET `p_raiting`='".$raiting_all."' WHERE p_id='".$raiting_id."'");
	$db->update("UPDATE cat_product SET `p_raiting_count`='".$count."' WHERE p_id='".$raiting_id."'");

	require "templates/auth.cgi";
	$db->insert("INSERT INTO `cat_product_raiting` (`p_id`, `r_raiting`, `r_user_id`, `r_user_ip`, `r_date`) VALUES('".$raiting_id."', '".$raiting."', '".($user_id ne ""?"".$user_id."":"")."', '".$ENV{'REMOTE_ADDR'}."', '".$today_sql."')");
	
}

if ($ask_product_id ne ""){
	my $id = $ask_product_id;
	my $form="";
	
	my $p_name="";
	my $result = $db->query("SELECT cat_product.p_id, cat_product.p_name FROM cat_product WHERE p_id ='".$id."' LIMIT 1");
	foreach my $line(@$result){
		$p_name = $line->{'p_name'};
	}
	
	$form .='<div class="ask_about-container" style="display:none;">
		<h3>Задать вопрос</h3>
		<form action="#">
			<fieldset>
				<input type="hidden" name="P_NAME" value="'.$p_name.'">
				<label>Ваше Имя <span>*</span></label>
				<div class="text-wrap">
					<input type="text" name="NAME" value="Введите" class="text requried">
				</div>
				<label>Ваш контактный e-mail <span>*</span></label>
				<div class="text-wrap">
					<input type="text" name="MAIL" value="Введите" class="text requried">
				</div>
				<label>Ваш вопрос <span>*</span></label>
				<div class="textarea-wrap">
					<textarea name="NOTE" value="" class="text requried"></textarea>
				</div>				
				<span class="note">Специалисты нашей компании, готовы проконсультировать по любым вопросам.</span>
				<input type="submit" value="Отправить вопрос" class="submit ask_product">
				<a id="jSbox-close" href="#">Отменить</a>
			</fieldset>
		</form>
	</div>
	<script type="text/javascript">
	$(function(){
		$("div#jSbox-container input[type=submit].ask_product").live("click", function(e){

			var hBox = $("div#jSbox-wrap").height();
			var p_name = $("div#jSbox-container input[name=P_NAME]").attr("value");
			var name = $("div#jSbox-container input[name=NAME]").attr("value");
			var mail = $("div#jSbox-container input[name=MAIL]").attr("value");
			var text = $("div#jSbox-container textarea").val();
			
			if (!checkMail(mail)){
				$("#jSbox-container input[name=MAIL]").attr("value", "Введите корректный e-mail");
				return false;
			}				
			if (p_name!="" && name != "" && name != "Введите" && checkMail(mail) && text != ""){			
				var params = new Object();
				params.name = name;
				params.mail = mail;
				params.note = text;
				params.asc_product = p_name;
				$.get("/cgi-bin/send_mail_page.cgi", params, function(data){
					if (data != ""){
						$("div#jSbox-wrap").css("height", hBox+"px");
						$("div#jSbox-wrap").append(\'<div id="jSbox-message-send">\'+data+\'</div>\');
						$("div#jSbox-wrap div#jSbox-container").fadeOut(400, function(){
							$("div#jSbox-wrap div#jSbox-message-send").fadeIn(600, function(){
								window.setTimeout(function(){
									$().jSboxClose();
								}, 2500);
							});
						});
					}
				});			
			}
			else {
				return false;
			}
			e.preventDefault();
		});
	});
	function checkMail(email){
		var filter = /^\w+@\w+\.\w{2,4}$/i;
		var result = filter.test(email.toLowerCase());
		return result;
	}	
	</script>';

	print $form;
}

if ($buy_quick ne ""){
	my $id = $buy_quick;
	my $form="";
	
	my $p_name=""; my $price="";
	my $result = $db->query("SELECT cat_product.p_id, cat_product.p_name FROM cat_product WHERE p_id ='".$id."' LIMIT 1");
	foreach my $line(@$result){
		$p_name = $line->{'p_name'};
	}
	$p_name =~ s/'/&quot;/g;
	$p_name =~ s/"/&quot;/g;
	
	$form .='
	<div class="buy-quick-container" style="display:none;">
		<h3>Быстрая покупка</h3>
		<form action="#">
			<fieldset>
				<label>Ваше Имя <span>*</span></label>
				<div class="text-wrap">
					<input type="text" name="NAME" value="Введите" class="text requried">
				</div>
				<label>Ваш контактный номер <span>*</span></label>
				<div class="text-wrap">
					<input type="text" name="PHONE" value="Введите" class="text requried">
				</div>
				<label>Выбранный товар</label>
				<div class="text-wrap">
					<input type="text" name="ID" p_id="'.$id.'" value="'.$p_name.'" class="text" readonly="readonly">
				</div>					
				<span class="note">Пожалуйста, заполните краткую контактную информацию. Наши сотрудники свяжутся с вами в удобное для вас время.</span>
				<input type="submit" value="Отправить заказ" class="submit buy-quick-send">
				<a id="jSbox-close" href="#">Отменить</a>
			</fieldset>
		</form>
	</div>';

	print $form;
}

if ($autocomplete eq "load"){
	
	my $result='{';

	my $catalog=""; my %category=();
	if ($logined eq "enter" && $user_group > 0){
		use Core::DB::Catalog;
		$catalog = new Core::DB::Catalog();	
	}	
	my $res = $db->query("SELECT p.p_art, p.p_name, p.p_price, p.p_price_opt, p.p_price_opt_large, r.cat_id FROM cat_product AS p JOIN cat_product_rel AS r ON(r.cat_p_id=p.p_id)");
	foreach my $line(@$res){
		my $name = $line->{'p_name'};
		$name =~ s/'//g;
		$name =~ s/"//g;
		my $price = $line->{'p_price'};
		if ($logined eq "enter" && $user_group > 0){
			my ($price_, $category_) = $catalog->getDiscountPrice($line->{'cat_id'}, $line->{'p_price'}, $line->{'p_price_opt'}, $line->{'p_price_opt_large'}, \%user_group_ids, \%category);
			$price = $price_;
			%category = %{$category_};
		}		
		$result .= '"'.$line->{'p_art'}.'['.($price > 0?''.$price.'':'0').']": "'.$line->{'p_art'}.' '.$name.'",';
	}
	$result =~ s/,$//g;
	$result .='}';
	
	print $result;
}

if ($get_autocomplete_alias ne ""){

	my $article = $get_autocomplete_alias;
	
	my $result="";
	my $res = $db->query("SELECT p_alias FROM cat_product WHERE p_art ='".$article."'");
	
	print $res->[0]->{p_alias};
}

if ($reviews_raiting ne "" && $reviews_raiting_id ne ""){

	my $p_id = $reviews_raiting_id;
	my $name = $reviews_raiting_name;
	my $text = $reviews_raiting_text;
	
	use Encode "from_to";
	from_to($name, "utf-8", "cp1251");
	from_to($text, "utf-8", "cp1251");
	$text =~ s/</&lt;/g;
	$text =~ s/>/&gt;/g;
	$text =~ s/\n/\<br>/g;
	$text =~ s/\'/\\'/g;
	
	require "templates/auth.cgi";
	$db->insert("INSERT INTO `cat_product_reviews` (`p_id`, `v_raiting`, `v_name`, `v_text`, `v_user_id`, `v_user_ip`, `v_public`, `v_date`) VALUES('".$p_id."', '".$reviews_raiting."', '".$name."', '".$text."', '".($user_id ne ""?"".$user_id."":"")."', '".$ENV{'REMOTE_ADDR'}."', '0', '".$today_sql."')");
	
	my $result = $db->query("SELECT p.* FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_id ='".$p_id."' AND pl.cat_main ='1' LIMIT 1");
	my $p_name = $result->[0]->{p_name};

	$p_name =~ s/'//g;
	$p_name =~ s/"//g;	
	
	open (MZ,"|/usr/sbin/sendmail -t");
	print MZ "To: $email_orders\n";
	print MZ "From: robot\@$url_site\n";
	print MZ "Subject: Оставлен отзыв по товару заказ с сайта $url_site\n";
	print MZ "MIME-Version: 1.0\n";
	print MZ "Content-Type: text/html\; charset=\"windows-1251\"\n";
	print MZ "Content-Transfer-Encoding: 8bit\n\n";
	print MZ "<div style='position:relative; border:1px dotted #999; width:600px; padding:20px 20px 92px 30px; font:normal 14px Tahoma; background: url(http://uplecms.ru/img/logo_mail.png) bottom right no-repeat #eaeaea;'>";
	print MZ "Добрый день!<br><br>Поступил новый отзыв, требующий вашей модерации.<br><br>";
	print MZ "Товар: <a target='_blank' href='http://".$url_site."/cgi-bin/admin/engine/index.cgi?adm_act=products&num_edit=".$p_id."'>".$p_name."</a><br><br>";
	print MZ "От: <b>".$name."</b><br><br>";
	print MZ "Содержание: ".$text."<br><br>";
	print MZ "</div>";
	close (MZ);

	print "ok";		
}

if ($products_ids && $products_cat_name){

	open(BO, "$dirs_catalog_www2/page_settings.txt"); my @pages_count = <BO>; close(BO);
	foreach my $line(@pages_count){chomp($line);
	my ($pages_admin, $pages_site) = split(/\|/, $line);
	$limit_count=qq~$pages_site~;}

	my $p_ids = $products_ids;
	my $cat_name="Результаты поиска";
	
	if ($ENV{"HTTP_REFERER"} =~/catalog\/filter/){
		$cat_name = $products_cat_name;
		use Encode "from_to";
		from_to($cat_name, "utf-8", "cp1251");	
	}
	
	my $catalog=""; my %category=();
	if ($logined eq "enter" && $user_group > 0){
		use Core::DB::Catalog;
		$catalog = new Core::DB::Catalog();	
	}
	my $products="";
	my $result = $db->query("SELECT p.*, r.cat_id FROM cat_product AS p JOIN cat_product_rel AS r ON(r.cat_p_id=p.p_id) WHERE p_id IN (".$p_ids.")");
	foreach my $line(@$result){
		$count++; $i++; my $mark="";
		if ($line->{'p_news'} eq "1"){$mark="new";}
		if ($line->{'p_hit'} eq "1"){$mark="hit";}
		if ($line->{'p_spec'} eq "1"){$mark="spec";}
		my $label = 0;
		if ($count == 3) {$label = "reflect"; $count="";}		
		my $price = $line->{'p_price'};
		if ($logined eq "enter" && $user_group > 0){
			my ($price_, $category_) = $catalog->getDiscountPrice($line->{'cat_id'}, $line->{'p_price'}, $line->{'p_price_opt'}, $line->{'p_price_opt_large'}, \%user_group_ids, \%category);
			$price = $price_;
			%category = %{$category_};
		}			
		$products .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, "", $price, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, $label, $mark, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "catalog", $line->{'p_img_url'}, $cat_name, "", "", "", $line->{'p_color_rel'});
		if ($i eq ($limit_count*2)){last;}
	}
	if ($products){
		print $products;
	}
}
