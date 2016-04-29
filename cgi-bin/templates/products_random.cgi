my $db = new Core::DB();

# Вывод случайных товаров

sub build_ProductRandom
{
	my $random=""; my $products=""; my $count=""; my $ids="";
	my $limit_random = 20;
	my $res_max = $db->query("SELECT cat_product.p_id FROM cat_product ORDER BY p_id DESC LIMIT 1");
	my $max_id = $res_max->[0]->{p_id};
	for ($id=1; $id <= $limit_random+10; $id++) {
		$ids .= rand_product(1, $max_id).", ";
	}
	$ids=~ s/,\s$//g;
	my $result = $db->query("SELECT * FROM cat_product WHERE p_show != '0' AND p_id IN (".$ids.") ORDER BY RAND() LIMIT ".$limit_random."");
	foreach my $line(@$result){
		$products .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, "", $line->{'p_price'}, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, 0, 0, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "hits");
	}
	
	if ($products ne ""){
		$random.='
			<script type="text/javascript" src="/js/windy/modernizr.custom.js"></script>
			<script type="text/javascript" src="/js/windy/jquery.windy.js"></script>
			<script type="text/javascript" src="/js/windy/jquery.windy-settings.js"></script>			
			<div class="products_random">
				<div class="head">20 случайных товаров</div>
				<div class="container" id="random-items">
				'.$products.'
				</div>
				<div class="nav">
					<span id="nav-prev">Предыдущий</span>
					<span id="nav-next">Следующий</span>
				</div>
			</div>';
	}

	return $random;
}

sub rand_product ($$) {
    my($min, $max) = @_;
    return $min if $min == $max;
    ($min, $max) = ($max, $min) if $min > $max;
    return $min + int rand(1 + $max - $min);
}

1;