my $db = new Core::DB();


# Заголовок страниц

sub build_NamePage
{
	my $name = shift;
	
	my $result = '<div class="title">
					<h1>'.$name.'</h1>
				</div>';
				
	return $result;
}

# Заголовок категории каталога

sub build_NameCategory
{
	my $name = shift;
	my $c_pid = shift;
	my $count = shift;
	
	my $section=""; my $c_alias="";
	if ($c_pid ne "0"){
		my $res = $db->query("SELECT c_name, c_name_short, c_pid, c_alias FROM cat_category WHERE c_id='".$c_pid."';");
		$section = $res->[0]->{c_name};
		$c_alias = $res->[0]->{c_alias};
	}	
	my $result = '<div class="title">';
	
	if ($section){
		$result .='<a class="back" href="/catalog/'.$c_alias.'">'.$section.'</a>
				<h1 class="name">'.$name.'</h1>';
	}
	else {
		$result .='<h1>'.$name.'</h1>';
	}
	if ($count > 0){
		$result .='
			<div class="filter-views">
				<ul>
					<li class="list'.(cookie("view_products") ne "table"?' active':'').'"><a href="#">list</a></li>
					<li class="table'.(cookie("view_products") eq "table"?' active':'').'"><a href="#">table</a></li>
				</ul>
				<span>Товаров: <strong>'.$count.'</strong></span>
				<span class="filter-price"><em'.(cookie("filter_price") eq "ASC"?' class="active"':'').' data-filter="ASC">Подешевле</em><ins>|</ins><em'.(cookie("filter_price") eq "DESC"?' class="active"':'').' data-filter="DESC">Подороже</em></span>
			</div>';
	}	
	$result .='
			</div>';

	return $result;
}

# Заголовок товара

sub build_NameProduct
{
	my $id = shift;
	my $name = shift;
	my $cid = "";
	
	my $result_cid = $db->query("SELECT cat_id FROM cat_product_rel WHERE cat_p_id = '".$id."' AND cat_main = '1' LIMIT 1;");
	foreach my $line(@$result_cid){
		$cid = $line->{'cat_id'};	
	}	
	my $res = $db->query("SELECT cat_category.c_pid, cat_category.c_name, cat_category.c_alias FROM cat_category WHERE c_id = '".$cid."';");
	my $section = $res->[0]->{c_name};
	my $c_alias = $res->[0]->{c_alias};	
	
	my $path="";
	while ($res->[0]->{c_pid} != 0){
		$res = $db->query("SELECT cat_category.c_name, cat_category.c_alias FROM cat_category WHERE c_id='".$res->[0]->{c_pid}."';");
		$path .= '<li><a href="/catalog/'.$res->[0]->{c_alias}.'">'.$res->[0]->{c_name}.'</a></li>';
	}	
	
	my $referer="";
	my $ref = $ENV{"HTTP_REFERER"};
	if ($ref =~/catalog/) {$referer = $ENV{"HTTP_REFERER"};}
	if ($ref =~/catalog\/search/ or $ref =~/catalog\/filter/) {
		$path="";
		$section = "Вернуться к результатам поиска";
	}
	
	my $result ='<div class="title-holder">
					<h1>'.$name.'</h1>
					<ul class="breadcrumbs">
						<li><a href="/">Главная</a></li>
						'.$path.'
						<li><a href="'.($referer?''.$referer.'':'/catalog/'.$c_alias.'').'">'.$section.'</a></li>
					</ul>
				</div>';
				
	return $result;
}

# Заголовок новости

sub build_NameNews
{
	my $name = shift;
	
	my $result = '<div class="title">
				<a class="back" href="/news/">Новости</a>
				<h1 class="name">'.$name.'</h1>
			  </div>';
			  
	return $result; 
}

1;