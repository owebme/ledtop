my $db = new Core::DB();

# Просмотренные товары

my $limit_viewed = 4; # кол-во отображаемых

sub build_ProductViewed
{
	my $products=""; my $count="";
	if (cookie("viewed_products") ne ""){
		my $viewed_products = cookie("viewed_products");
		while($viewed_products =~ m/(\d+)\|/g){
			my $alias = $1; $count++;
			if ($count <= $limit_viewed){
				my $result = $db->query("SELECT * FROM cat_product WHERE p_alias = '".$alias."'");
				foreach my $line(@$result){				
					my $num_foto = 1000+$line->{'p_id'};
					my $image=""; $rand_num=rand(1);
					if (-e "$dirs_catalog_www2/$num_foto\_small.jpg"){
						$image = '<img src="/files/catalog/'.$num_foto.'_small.jpg?'.$rand_num.'" title="'.$line->{p_desc_sm}.'" alt="'.$line->{p_name}.'">';
					}
					else {$image = '<img src="/admin/site/img/no_photo.png" alt="">';}
					
					my $res = $db->query("SELECT p.*, c.c_alias, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE p.p_alias ='".$line->{'p_alias'}."' AND pl.cat_main ='1' LIMIT 1");
					my $c_alias = $res->[0]->{c_alias};	
					
					$products .='<div class="related_item">
										<div class="img"><a href="/products/'.$c_alias.'/'.$line->{p_alias}.'">'.$image.'</a></div>
										<a href="/products/'.$c_alias.'/'.$line->{p_alias}.'" class="name">'.$line->{p_name}.'</a>
										<div class="price">'.price_trans($line->{'p_price'}).'&nbsp;'.($line->{'p_price_old'} ne ""?'<span class="old_price">'.price_old_trans($line->{'price_old'}).'</span>':'').'</div>
									</div>';
				}
			}
		}
	}
	
	if ($products ne ""){
		$products = '
		<div style="clear: both;" class="related_issues viewed">
			<div id="tabs">
				<ul class="tab_btns">
					<li><a class="active" href="#tabs-1">Просмотренные товары</a></li>
				</ul>
				<div class="tab_content clearfix" id="tabs-1">
				'.$products.'
				</div>
			</div>
		</div>';
	}
	
	return $products;
}

1;