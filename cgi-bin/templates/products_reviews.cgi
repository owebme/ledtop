my $db = new Core::DB();

# Отзывы покупателей

sub build_ProductReviews
{
	my $id = shift;
	my $name = shift;
	my $products=""; my $count=""; my $reviews="";
	my $result = $db->query("SELECT *, DATE_FORMAT(v_date, \"%Y.%m.%d\") as date FROM cat_product_reviews WHERE p_id ='".$id."' AND v_public = '1' ORDER BY v_date DESC");
	foreach my $item(@$result){
		if ($result){
			 $reviews .='<div class="item">
				<div class="name">
					<span>'.$item->{'v_name'}.'</span>
					<div class="raiting_star">
						<div class="raiting_blank"></div>
						<div class="raiting_votes" style="width:'.($item->{'v_raiting'}*29).'px;"></div>
					</div>
				</div>
				<div class="comments">
					'.$item->{'v_text'}.'
				</div>
			</div>';
			$count++;
		}
	}
	if (!$reviews){
		$reviews ='<div id="products_reviews_container"><p class="note">Пока нет отзывов, оставляйте свои отзывы.</p></div>';
	}
	else {
		$reviews ='<div id="products_reviews_container">'.$reviews.'</div>';
	}
	$products ='<div id="products_reviews_wrap"'.($id eq "68"?' class="godgi"':'').'>
		<h3>Отзывы покупателей <span>«'.$name.'»</span></h3>
		'.$reviews.'
		<div class="clear"></div>
		<a href="#" class="add_show_reviews'.(!$count?' up':'').'">Добавить свой отзыв</a>
		<div class="clear"></div>
		<div id="products_reviews_send" >
			<div class="raiting"><span>Оцените товар</span>
				<div title="Поставить оценку" class="raiting_star" data-id="'.$id.'" data-raiting="">
					<div class="raiting_blank"></div>
					<div class="raiting_hover"></div>
					<div class="raiting_votes"></div>
				</div>
			</div>
			<div class="head">Написать комментарий</div>
			<textarea></textarea>
			<div class="send">
				<label>Имя</label>
				<input type="text" name="name" class="normal" value="">
				<input type="button" value="Добавить" class="button">
			</div>
		</div>
	</div>';
	
	return $products;
}

1;