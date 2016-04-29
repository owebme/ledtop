
		require "admin/engine/lib/parametr.cgi";
		require "templates/news.cgi";
		require "templates/articles.cgi";
		require "templates/name.cgi";
		require "templates/auth.cgi";
		require "templates/private.cgi";
		require "templates/pages.cgi";
		require "templates/catalog.cgi";
		require "templates/products.cgi";		
		require "templates/products_hit.cgi";
		
		require "templates/feedback.cgi";
		require "templates/sitemap.cgi";
		require "templates/fadepage.cgi";
		
		require "templates/contacts.cgi";
		my ($phone, $address, $timemode, $copyright) = build_Contacts();
		
		
		
		require "templates/callback.cgi";
		
		
		
		open(BO, "admin/$dirs/sort_strukture"); $sort_pages = <BO>; close(BO);
		open(BO, "admin/$dirs/sort_catalog"); @select_sort = <BO>; close(BO);
		foreach my $line(@select_sort){chomp($line);
		my ($select_sort_cat_, $select_sort_product_) = split(/\|/, $line);
		$sort_category=qq~$select_sort_cat_~;
		$sort_product=qq~$select_sort_product_~;}
		open(BO, "admin/$dirs/sort_news"); $sort_news = <BO>; close(BO);
		open(BO, "admin/$dirs/set_news"); @set_news = <BO>; close(BO);
		foreach my $line(@set_news){chomp($line);
		my ($limit_news_, $type_news_) = split(/\|/, $line);
		$limit_news=qq~$limit_news_~; $type_news=qq~$type_news_~;}
		open(BO, "admin/$dirs/sort_articles"); $sort_articles = <BO>; close(BO);
		open(BO, "admin/$dirs/set_articles"); @set_articles = <BO>; close(BO);
		foreach my $line(@set_articles){chomp($line);
		my ($limit_articles_, $ajax_save_) = split(/\|/, $line);
		$limit_articles=qq~$limit_articles_~;}
		open OUT, ("admin/engine/lib/counter"); @counter = <OUT>;
		foreach my $text(@counter) {$counter=qq~$counter$text~;}
		$random_n = rand(1);
		1;