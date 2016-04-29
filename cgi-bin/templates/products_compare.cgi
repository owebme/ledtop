my $db = new Core::DB();

# Сравнение товаров

sub build_ProductCompare
{
	my $products=""; my $count="";
	if (cookie("compare_products") ne ""){
		my $compare_products = cookie("compare_products");
		while($compare_products =~ m/(\d+)\|/g){
			my $id = $1; $count++;
			my $result = $db->query("SELECT * FROM cat_product WHERE p_id = '".$id."'");
			foreach my $line(@$result){			
				my $num_foto = 1000+$line->{'p_id'};
				my $image=""; $rand_num=rand(1);
				if (-e "$dirs_catalog_www2/$num_foto\_small.jpg"){
					$image = '<img src="/files/catalog/'.$num_foto.'_small.jpg?'.$rand_num.'" alt="">';
				}
				else {$image = '<img src="/admin/site/img/no_photo.png" alt="">';}
				
				my $res = $db->query("SELECT p.*, c.c_alias, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_alias ='".$line->{'p_alias'}."' AND pl.cat_main ='1' LIMIT 1");
				my $page_alias = $res->[0]->{c_alias};	
				
				$products .= '<td p_id="'.$line->{'p_id'}.'">
								<div class="name"><a title="'.$line->{'p_name'}.'" href="/products/'.$page_alias.'/'.$line->{'p_alias'}.'">'.$line->{'p_name'}.'</a></div>
								<div class="foto"><a href="/products/'.$page_alias.'/'.$line->{'p_alias'}.'">'.$image.'</a></div>
								<div class="desc">'.$line->{'p_desc_top'}.'</div>
								<div class="price">'.$line->{'p_price'}.' руб.</div>
								<input type="button" class="del_compare" value="УБРАТЬ">
							  </td>';
			}
		}
	}

	if ($products ne ""){
		$products = '<table class="products_compare"><tr>'.$products.'</tr></table>';
	}
	
	return $products;
}

1;