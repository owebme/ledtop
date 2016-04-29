my $db = new Core::DB();

# Новинки товаров на главной странице

my $limit_hit = 8; # кол-во отображаемых

sub build_ProductHit
{
	my $type = shift;
	
	my $product_hit = ""; my $query=""; my $head="";
	if ($type eq "hit"){$query = "p.p_hit"; $head='<div class="title"><h2>Хиты продаж</h2></div>';}
	elsif ($type eq "new"){$query = "p.p_news"; $head='<div class="title"><h2>Новые поступления</h2></div>';}
	elsif ($type eq "spec"){$query = "p.p_spec"; $head='<div class="title"><h2>Спецпредложение</h2></div>';}
	
	my $result=""; my $cat_id=""; my $name=""; $num="";
	if ($type eq "spec"){
		$result = $db->query("SELECT p.*, pl.cat_id FROM cat_product AS p JOIN cat_product_hits AS h ON(h.p_ids=p.p_id) JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE h.hit_id = '1' AND pl.cat_main = '1' AND p.p_show = '1' ORDER BY h.p_pos ASC");
	}
	elsif ($type eq "new"){
		$result = $db->query("SELECT p.*, pl.cat_id FROM cat_product AS p JOIN cat_product_hits AS h ON(h.p_ids=p.p_id) JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE h.hit_id = '2' AND pl.cat_main = '1' AND p.p_show = '1' ORDER BY h.p_pos ASC");
	}
	elsif ($type eq "hit"){
		$result = $db->query("SELECT p.*, pl.cat_id FROM cat_product AS p JOIN cat_product_hits AS h ON(h.p_ids=p.p_id) JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE h.hit_id = '3' AND pl.cat_main = '1' AND p.p_show = '1' ORDER BY h.p_pos ASC");
	}
	if ($result){
		foreach my $line(@$result){
			$num++;
			my $label = 0;
			if ($num == 3) {$label = "reflect"; $num="";}			
			$product_hit .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, "", $line->{'p_price'}, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, $label, 0, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "hits", $line->{'p_img_url'});
			$cat_id = $line->{'cat_id'}; $name = $line->{'p_name'};
		}
	}
	
	if( ref($result) eq 'ARRAY' ){
		$product_hit = '<div class="products-holder">'.$head.''.build_ProductTags(1,0,"hits").''.$product_hit.''.build_ProductTags(0,1,"hits").'</div>';
	} else {$product_hit="";}
	
	return $product_hit;
}

1;