
		$pages_menu = build_PagesMenu($sort_pages);
		$pages_menu_limit = build_PagesMenuLimit($sort_pages);
		
		
		$catalog_menu = build_CatalogMenu($sort_category);
		
		if ($adm_act ne "private"){$catalog_tree = build_CatalogTree($sort_category);}
		if ($adm_act ne "private"){$catalog_category = build_Category($sort_category);}
		$news = build_News($limit_news, $sort_news, $type_news);
		
		
		
		
		if ($adm_act eq "pages" && $num_edit eq "1"){$products_hit = build_ProductHit("hit");}
		if ($adm_act eq "pages" && $num_edit eq "1"){$products_new = build_ProductHit("new");}
		if ($adm_act eq "pages" && $num_edit eq "1"){$products_spec = build_ProductHit("spec");}
		
		if ($adm_act eq "pages" && $num_edit eq "1"){
			if ($products_hit ne ""){$products_hit .= $script_product_hit;}
			elsif ($products_new ne ""){$products_new .= $script_product_hit;}
			elsif ($products_spec ne ""){$products_spec .= $script_product_hit;}
		}
		1;