my $db = new Core::DB();

# Рекомендуемые товары (с этим товаром покупают)

sub build_ProductRecomend
{
	my $id = shift;
	my $products_rec="";
	my $result = $db->query("SELECT p.*, pl.r_pos, pl.p_ids FROM cat_product AS p JOIN cat_product_recomend AS pl ON(pl.rec_id=p.p_id) WHERE p.p_id ='".$id."' ORDER BY pl.r_pos ASC");
	if ($result){
		foreach my $line(@$result){
			my $p_id = $line->{p_ids};			
			my $res = $db->query("SELECT p.*, c.c_id, c.c_alias, pl.cat_id, pl.cat_main, pl.p_pos FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_id ='".$p_id."' AND pl.cat_main ='1' LIMIT 1");
			foreach my $line(@$res){
				my $c_alias = $line->{c_alias};			
				$products_rec .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, $c_alias, $line->{'p_price'}, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, 0, 0, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "related", $line->{'p_img_url'}, $c_name);
			}
		}
	}
	
	if ($products_rec ne ""){
		$products_rec='
		<div class="products-holder">
			<div class="title">
				<h2>Сопутствующие товары:</h2>
			</div>
			<div class="scroller related">
				<div class="products-list owl-carousel">	
				
				'.$products_rec.'
				
				</div>
			</div>
		</div><br><br>';
	}

	return ($products_rec);
}

1;