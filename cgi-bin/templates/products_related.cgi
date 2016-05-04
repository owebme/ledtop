my $db = new Core::DB();

# Соседние и сопутствующие товары в категории

sub build_ProductRelated
{
	my $sort = shift;
	my $article = shift;
	my $related = shift;
	
	my $catalog=""; my %category=();
	if ($logined eq "enter" && $user_group > 0){
		use Core::DB::Catalog;
		$catalog = new Core::DB::Catalog();	
	}
	my $navigation=""; my $neighboring="";
	if ($related){
		$related =~ s/\s/, /g;
		$related =~ s/,\s$//g;
		$related =~ s/,,/,/g;
		my $res_related = $db->query("SELECT p.*, r.cat_id FROM cat_product AS p JOIN cat_product_rel AS r ON(r.cat_p_id=p.p_id) WHERE p_art IN (".$related.")");
		if ($res_related){
			foreach my $line(@$res_related){
				my $price = $line->{'p_price'};
				if ($logined eq "enter" && $user_group > 0){
					my ($price_, $category_) = $catalog->getDiscountPrice($line->{'cat_id'}, $line->{'p_price'}, $line->{'p_price_opt'}, $line->{'p_price_opt_large'}, \%user_group_ids, \%category);
					$price = $price_;
					%category = %{$category_};
				}			
				$neighboring .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, $c_alias, $price, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, 0, 0, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "related", $line->{'p_img_url'}, $c_name);
			}
		}
	}
	elsif (!$related){
		my $res_c_alias = $db->query("SELECT p.*, c.c_id, c.c_name, c.c_alias, pl.cat_id, pl.cat_main, pl.p_pos FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_art ='".$article."' AND pl.cat_main ='1' LIMIT 1");
		my $c_name = $res_c_alias->[0]->{c_name};
		my $c_alias = $res_c_alias->[0]->{c_alias};
		my $c_id = $res_c_alias->[0]->{c_id};
		my $p_pos = $res_c_alias->[0]->{p_pos};
		my $p_date = $res_c_alias->[0]->{p_date_add};
		my $p_price = $res_c_alias->[0]->{p_price};	
		
		if (!$related){
			if (cookie("sort_products")){$sort = cookie("sort_products");}
			my $sort2="";
			my $sort_ = $sort;
			my $trend = $sort;
			$sort_=~ s/\sASC$//g;
			$sort_=~ s/\sDESC$//g;
			$trend=~ s/(.+?)\s//g;
			if ($sort_ eq "p_pos"){$sort_ = "pl.".$sort_; $sort2 = $p_pos;}
			else {
				if ($sort_ eq "p_date_add"){$sort2 = $p_date;}
				elsif ($sort_ eq "p_price"){$sort2 = $p_price;}
				$sort_ = "p.".$sort_;
			}
			if ($trend eq "ASC") {$sort_prev = $sort_." DESC"; $sort_next = $sort_." ASC";}
			elsif ($trend eq "DESC") {$sort_prev = $sort_." DESC"; $sort_next = $sort_." ASC";}
			
			my $i=""; my $p_id_prev=""; my $p_name_prev=""; my $p_alias_prev="";
			my $res_prev = $db->query("SELECT p.*, c.c_id, pl.cat_id, pl.cat_main, ".$sort_." FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE ".$sort_." < '".$sort2."' AND pl.cat_id = '".$c_id."' AND pl.cat_main ='1' AND p.p_show = '1' ORDER BY ".$sort_prev." LIMIT 4");
			if ($res_prev){
				foreach my $line(@$res_prev){	
					my $price = $line->{'p_price'};
					if ($logined eq "enter" && $user_group > 0){
						my ($price_, $category_) = $catalog->getDiscountPrice($line->{'cat_id'}, $line->{'p_price'}, $line->{'p_price_opt'}, $line->{'p_price_opt_large'}, \%user_group_ids, \%category);
						$price = $price_;
						%category = %{$category_};
					}			
					$neighboring .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, $c_alias, $price, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, 0, 0, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "related", $line->{'p_img_url'}, $c_name);
				}
			}
			
			my $i=""; my $p_id_next=""; my $p_name_next=""; my $p_alias_next="";
			my $res_next = $db->query("SELECT p.*, c.c_id, pl.cat_id, pl.cat_main, ".$sort_." FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE ".$sort_." > '".$sort2."' AND pl.cat_id = '".$c_id."' AND pl.cat_main ='1' AND p.p_show = '1' ORDER BY ".$sort_next." LIMIT 4");
			if ($res_next){
				foreach my $line(@$res_next){
					my $price = $line->{'p_price'};
					if ($logined eq "enter" && $user_group > 0){
						my ($price_, $category_) = $catalog->getDiscountPrice($line->{'cat_id'}, $line->{'p_price'}, $line->{'p_price_opt'}, $line->{'p_price_opt_large'}, \%user_group_ids, \%category);
						$price = $price_;
						%category = %{$category_};
					}				
					$neighboring .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, $c_alias, $price, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, 0, 0, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "related", $line->{'p_img_url'}, $c_name);		
				}
			}
		}
	}
	
	if ($neighboring ne ""){
		$neighboring='
		<div class="products-holder">
			<div class="title">
				<h2>'.($related?'C этим товаром покупают':'Рекомендуем посмотреть').':</h2>
			</div>
			<div class="scroller related">
				<div class="products-list owl-carousel">	
				
				'.$neighboring.'
				
				</div>
			</div>
		</div><br><br>';
	}
	
	# Соседние товары

	if ($p_alias_prev ne ""){$navigation .='<div class="prev_prod"><a href="/products/'.$c_alias.'/'.$p_alias_prev.'" class="page_btn">« Предыдущий товар</a><div class="img"><a href="/products/'.$c_alias.'/'.$p_alias_prev.'"><img src="/files/catalog/'.$p_id_prev.'_small.jpg" alt="'.$p_name_prev.'"></a></div></div>';}			
	if ($p_alias_next ne ""){$navigation .='<div class="next_prod"><a href="/products/'.$c_alias.'/'.$p_alias_next.'" class="page_btn">Следующий товар »</a><div class="img"><a href="/products/'.$c_alias.'/'.$p_alias_next.'"><img src="/files/catalog/'.$p_id_next.'_small.jpg" alt="'.$p_name_next.'"></a></div></div>';}			
	if ($p_alias_prev ne "" or $p_alias_next ne ""){
		$navigation = '<div class="page_navigation clearfix">'.$navigation.'</div>';
	}

	return ($navigation, $neighboring);
}

1;