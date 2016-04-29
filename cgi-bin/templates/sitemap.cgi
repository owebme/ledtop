my $db = new Core::DB();


# Карта сайта на странице


sub build_Sitemap
{

	# Вывод страниц

	my $res_col_pages = $db->query("SELECT * FROM strukture WHERE parent = '0'");
	my $col_page="";
	foreach my $item(@$res_col_pages){
		if ($item->{show} == 1) {$col_page++;}
	}
	$col_page = $col_page-2;
	my $tree_pages = "";
	$tree_pages .= '<ul id="primaryNav" class="col'.($col_page > 5?'5':''.$col_page.'').'">';	
	my $result = $db->query("SELECT * FROM strukture WHERE parent = '0' ORDER BY pos");
	foreach my $item(@$result){
		if ($item->{show} == 1) {
			my $subs ="";
			if( my $sub = recMenuPagesCat($item->{id}, 0) ){
			$subs = $sub;
			}
			if($item->{'id'} eq "1"){
			$tree_pages .= '<li id="home">';			
			$tree_pages .= '<a '.($subs ne "" && $item->{html} eq ""?'id="no_link" href="#"':'id="no_link" href="/"').'>&nbsp;'.$item->{name}.'&nbsp;</a>';
			$tree_pages .= $subs;
			$tree_pages .= '</li>';
			}
			elsif ($page_alias eq $item->{alias}){
			$tree_pages .= '';
			}
			else {
			$tree_pages .= '<li>';			
			$tree_pages .= '<a '.($subs ne "" && $item->{html} eq ""?'id="no_link" href="#"':'href="/pages/'.$item->{alias}.'"').'>&nbsp;'.$item->{name}.'&nbsp;</a>';
			$tree_pages .= $subs;
			$tree_pages .= '</li>';
			}
		}
		else {
			$tree_pages .= '';
		}
	}
	
	sub recMenuPagesCat{

		my $id = shift;
		my $level = shift;
		
		my $text = '<ul>';
		my $cat_level=$level+1;
		
		my $result = $db->query("SELECT * FROM strukture WHERE parent='".$id."' ORDER BY pos");
		if($result){
			foreach my $item(@$result){
				if ($item->{show} == 1) {				
						my $subs ="";
						if( my $sub = recMenuPagesCat($item->{id}, $level+1) ){
							$subs = $sub;
						}
						$text .= '<li>';
						$text .= '<a '.($subs ne "" && $item->{html} eq ""?'href="#"':'href="/pages/'.$item->{alias}.'"').'>&nbsp;'.$item->{name}.'&nbsp;</a>';
						$text .= $subs;
						$text .= '</li>';						
				}
				else {
					$text .= '';
				}				
			}

		} else {
			return 0;
		}
		$text .= '</ul>'; 
		return $text;
	};
	$tree_pages .= '</ul>';

	
	# Вывод новостей

	my $tree_news = "";
	$result = $db->query("SELECT * FROM news WHERE parent = '0' ORDER BY date DESC");
	my $col_news="";
	foreach my $line(@$result){
		if($line->{'show'} ne "0"){
			$col_news++;
			$item_news .= '<li><div><a href="/news/'.$line->{alias}.'"">'.$line->{name}.'<div class="date_tree_news">'.$line->{'date'}.'</div></a></div></li>';
		} else {$item_news .="";}
	}
	if(ref($result) eq 'ARRAY'){		
			$tree_news='<ul id="primaryNav" class="three_news col'.($col_news > 5?'5':''.$col_news.'').'"><li id="home"><a id="no_link" href="/news/">Новости</a></li>'.$item_news.'</ul>';
	} else {
			$tree_news="";
	}	

	
	# Вывод категорий каталога с товарами
	
	my $res_col_cat = $db->query("SELECT * FROM cat_category WHERE c_pid = '0'");
	my $col_cat="";
	foreach my $item(@$res_col_cat){
		if ($item->{c_show} == 1) {$col_cat++;}
	}
	my $tree_catalog = "";
	if ($col_cat ne "") {$tree_catalog .= '<ul id="primaryNav" class="col'.($col_cat > 5?'5':''.$col_cat.'').'"><li id="home"><a id="no_link" href="#">Каталог</a></li>';} else {$tree_catalog="";}
	my $result = $db->query("SELECT * FROM cat_category WHERE c_pid = '0' ORDER BY c_pos;");
	foreach my $item(@$result){
		if ($item->{c_show} == 1) {
			my $subs ="";
			if( my $sub = recMenuCatalogCat($item->{c_id}, 0) ){
			$subs = $sub;
			}
			my $have_product ="";
			my $res_have = $db->query("SELECT * FROM cat_product_rel WHERE cat_id='".$item->{c_id}."' and cat_main='1';");
			my $cat_products="";
			if (ref($res_have) eq 'ARRAY') {
				my $res_products ="";
				my $res_products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$item->{c_id}."' AND pl.cat_main = '1' ORDER BY pl.p_pos ASC");
				$cat_products .= '<ul class="category_products">';
				foreach my $item(@$res_products){
					$cat_products .= '<li><div><a href="/products/'.$item->{p_alias}.'"">&nbsp;'.$item->{p_name}.'&nbsp;</a></li>';
				}
				$cat_products .= "</ul>";
			$have_product ="ok";
			} else {$have_product ="";}	
		
			$tree_catalog .= '<li>';
			$tree_catalog .= '<a '.($subs ne "" && $have_product eq ""?'href="#"':'href="/catalog/'.$item->{c_alias}.'"').'>&nbsp;'.$item->{c_name}.'&nbsp;</a>';
			$tree_catalog .= $cat_products;
			$tree_catalog .= $subs;
			$tree_catalog .= '</li>';
		}
		else {
			$tree_catalog .= '';
		}
	}
	
	sub recMenuCatalogCat{

		my $id = shift;
		my $level = shift;
		
		$result_parent = $db->query("SELECT * FROM cat_category WHERE c_id='".$id."'");
			
		my $text = '<ul class="sub_category">';
		my $cat_level=$level+1;
		
		my $result = $db->query("SELECT * FROM cat_category WHERE c_pid='".$id."' ORDER BY c_pos");
		if($result){
			foreach my $item(@$result){
				if ($item->{c_show} == 1) {										
						my $subs ="";
						if( my $sub = recMenuCatalogCat($item->{c_id}, $level+1) ){
							$subs = $sub;
						}
						my $have_product ="";
						my $res_have = $db->query("SELECT * FROM cat_product_rel WHERE cat_id='".$item->{c_id}."' and cat_main='1';");
						my $cat_products="";
						if (ref($res_have) eq 'ARRAY') {
							my $res_products ="";
							my $res_products = $db->query("SELECT p.*, pl.p_pos, pl.cat_id, pl.cat_main FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$item->{c_id}."' AND pl.cat_main = '1' ORDER BY pl.p_pos ASC LIMIT 5");
							$cat_products .= '<ul class="category_products">';
							foreach my $item(@$res_products){
								$cat_products .= '<li><a href="/products/'.$item->{p_alias}.'"">&nbsp;'.$item->{p_name}.'&nbsp;</a></li>';
							}
							$cat_products .= "</ul>";
						$have_product ="ok";
						} else {$have_product ="";}						
						$text .= '<li>';
						$text .= '<a '.($subs ne "" && $have_product eq ""?'href="#"':'href="/catalog/'.$item->{c_alias}.'"').'>&nbsp;'.$item->{c_name}.'&nbsp;</a>';
						$text .= $cat_products;						
						$text .= $subs;
						$text .= '</li>';						
				}
				else {
					$text .= '';
				}				
			}
			
		} else {
			return 0;
		}
		$text .= '</ul>'; 
		return $text;
	};
	$tree_catalog .= '</ul>';
	

	my $sitemap="";
	$sitemap=qq~<link href="/admin/site/sitemap/style.css" rel="stylesheet" type="text/css" />
				<div>$tree_pages</div>
				<div>$tree_news</div>
				<div style="padding-top:20px;">$tree_catalog</div>~;


return $sitemap;

}

1;