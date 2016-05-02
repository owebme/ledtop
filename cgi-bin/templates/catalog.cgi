my $db = new Core::DB();


# Категории каталога (только верхний уровень)

sub build_CatalogMenu
{
	my $sort = shift;
	my $category = "";
	my $cat_id="";
	if ($adm_act eq "product"){
		my $res = $db->query("SELECT pl.cat_id, c.c_pid FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_p_id = '".$num_edit."' AND p.p_show != '0' AND pl.cat_main = '1' LIMIT 1;");
		foreach my $item(@$res){
			$cat_id = $item->{cat_id};
		}
	}	
	$category .= '<ul class="catalog_menu">';	
	$result = $db->query("SELECT c_id, c_pid, c_name, c_alias FROM cat_category WHERE c_pid = '0' ORDER BY $sort");
	foreach my $line(@$result){
		if ($line->{'c_show_menu'} ne "0"){
			my $active="";
			if ($adm_act eq "catalog" && $num_edit==$line->{c_id} or $adm_act eq "product" && $cat_id==$line->{c_id}){
				$active = " class='active'";
			}
			$category .= "<li><a".$active." href='/catalog/".$line->{'c_alias'}."'>".$line->{'c_name'}."</a></li>\n";
			
		} else {$category .="";}
	}
	$category .= '</ul>';		
    return $category;
}


# Категории каталога (только верхний уровень)

my $limit_cat = 5; # кол-во отображаемых

sub build_CatalogMenuLimit
{
	my $sort = shift;
	my $category = ""; my $count="";
	my $cat_id="";
	if ($adm_act eq "product"){
		my $res = $db->query("SELECT pl.cat_id, c.c_pid FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_p_id = '".$num_edit."' AND p.p_show != '0' AND pl.cat_main = '1' LIMIT 1;");
		foreach my $item(@$res){
			$cat_id = $item->{cat_id};
		}
	}
	$category .= '<ul class="catalog_menu_limit">';	
	my $result = $db->query("SELECT c_id, c_pid, c_name, c_alias FROM cat_category WHERE c_pid = '0' ORDER BY $sort");
	foreach my $line(@$result){
		if ($line->{'c_show_menu'} ne "0"){
			$count++;
			if ($count <= $limit_cat){
				my $active="";
				if ($adm_act eq "catalog" && $num_edit==$line->{c_id} or $adm_act eq "product" && $cat_id==$line->{c_id}){
					$active = " class='active'";
				}
				$category .= "<li><a".$active." href='/catalog/".$line->{'c_alias'}."'>".$line->{'c_name'}."</a></li>\n";
			}
		} else {$category .="";}
	}
	$category .= '</ul>';	
    return $category;
}

sub build_Brands
{
	my $brands = "";
	$brands .= '<div id="brands">';	
	my $result = $db->query("SELECT * FROM cat_product_type ORDER BY t_pos ASC");
	foreach my $line(@$result){
		if ($line->{'t_show'} ne "0"){
			$brands .= '<a href="/catalog/brands/'.$line->{'t_alias'}.'"><img src="'.$dirs_catalog_www.'/icons/'.$line->{'t_alias'}.'.png" alt="'.$line->{'t_name'}.'"></a>';
		} else {$brands .="";}
	}
	$brands .= '</div>';		
    return $brands;
}

sub build_SelectBrands
{
	my $select = ""; my $option = "";
	if ($brand_alias ne ""){$select .= '<div class="select_brands"><a href="#!" class="open">'.$brand_alias.'<em></em></a><ul>';}
	else {$select .= '<div class="select_brands"><a href="#!" class="open">Выберите бренд<em></em></a><ul>';}
	my $result = $db->query("SELECT * FROM cat_product_type ORDER BY t_pos ASC");
	foreach my $line(@$result){
		if ($line->{'t_show'} ne "0"){
			$option .= '<li><a href="/catalog/'.($page_alias ne ""?''.$page_alias.'/':'').'brands/'.$line->{'t_alias'}.'">'.$line->{'t_name'}.'</a></li>';
		} else {$option .="";}
	}
	$select .= $option.'</ul></div>';		
    return $select;
}


# Вывод подразделов катагории

sub build_CatalogSubMenu
{
	my $id = shift;
	my $parent = shift;
	my $sort = shift;
	my $catalog_submenu=""; my $subs="";
	if ($adm_act eq "catalog" or $adm_act eq "product"){
		my $result="";
		if ($adm_act eq "product"){
			my $res = $db->query("SELECT pl.cat_id, c.c_pid FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) JOIN cat_category AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_p_id = '".$num_edit."' AND p.p_show != '0' AND pl.cat_main = '1' LIMIT 1;");
			$id = $res->[0]->{cat_id};
			$parent = $res->[0]->{c_pid};
		}
		if ($parent > 0){
			$result = $db->query("SELECT cat_category.c_id, cat_category.c_name, cat_category.c_alias FROM cat_category WHERE c_pid = '".$id."'".($sort?" ORDER BY $sort":" ORDER BY c_pos ASC").";");
			if ($result){$subs = 1;}
		}
		if (!$result){
			$result = $db->query("SELECT cat_category.c_id, cat_category.c_name, cat_category.c_alias FROM cat_category WHERE c_pid = '".($parent eq "0"?"".$id."":"".$parent."")."'".($sort?" ORDER BY $sort":" ORDER BY c_pos ASC").";");
		}
		if ($result){
			foreach my $item(@$result){
				if ($item->{'c_id'} eq $id){
					$catalog_submenu .='<li><span>'.$item->{'c_name'}.'</span></li>';
				}
				else {
					$catalog_submenu .='<li><a href="/catalog/'.$item->{'c_alias'}.'">'.$item->{'c_name'}.'</a></li>';
				}
			}
		}
	}
	# else {
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lenty/lenta-klassa-lyuks">Ленты класса ЛЮКС</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lenty/lenta-na-diodah-3528">Ленты на диодах 3528</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lenty/lenta-na-diodah-5060-5050">Ленты на диодах 5060 (5050)</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/g4-220v">Лампы с цоколем G4 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/g9-220v">Лампы с цоколем G9 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/e27-220v">Лампы E27 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/e14-220v">Лампы E14 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-svetilniki/ultratonkie-svetilniki">Ультратонкие светильники</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/gu10-220v">Лампы GU10 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/mr16-gu53-220v">Лампы GU5.3 220V</a></li>';	
	# }
	if ($catalog_submenu){
	
		my $name = 'Категории';
		if ($parent ne "0" && !$subs && ($adm_act eq "catalog" or $adm_act eq "product")){$name = 'Категории';}
		elsif ($parent eq "0" or $subs && ($adm_act eq "catalog" or $adm_act eq "product")){$name = 'В этом разделе';}
		elsif ($parent ne "0" && $adm_act ne "catalog" && $adm_act ne "product"){$name = 'Популярные';}
		
		$catalog_submenu ='
			<div class="section">
				<h2>'.$name.'</h2>
				<ul>
					'.$catalog_submenu.'
				</ul>
			</div>';
	}
	
	return $catalog_submenu;
}


# Фильтрация товаров

sub filterProducts {
	
	my $c_id = shift;
	my $g_id = shift;
	my $query = shift;
	%query = %{$query};
	
	my $group_id="";
	if ($g_id){$group_id = $g_id;}
	else {$group_id = findFilterCat($c_id, $parent_id);}
	
	my $result=""; my $filter="";
	if ($group_id > 0){
		my $res = $db->query("SELECT * FROM cat_product_filters WHERE gid = '".$group_id."' AND f_pid ='0' ORDER BY f_pos ASC;");
		if ($res){
			my $num="";
			foreach my $item(@$res){
				$num++;
				my $alias = $item->{'f_alias'};				
				if ($query && $query{$alias} or $num eq "1"){
					$filter .='<li data-alias="'.$alias.'" class="expanded">';
				}
				elsif ($alias eq "proizvoditel" && (param('proizvoditel_1') eq "on" or param('proizvoditel_2') eq "on")){
					$filter .='<li data-alias="'.$alias.'" class="expanded">';
				}		
				else {
					$filter .='<li data-alias="'.$alias.'">';
				}
				$filter .='<a class="opener" href="#">'.$item->{'name'}.'</a>';
				my $fields = $db->query("SELECT * FROM cat_product_filters WHERE f_pid = '".$item->{'filter_id'}."' ORDER BY name ASC;");
				if ($fields){
					if ($alias eq "color"){
						$filter .='<div class="filter-color">';
					}
					else {
						$filter .='<ul class="filter-drop">';
					}
					my $ids=""; my $colors=""; my $three=""; my $rgb=""; my $pro="";
					if ($query && $query{$alias}){$ids = $query{$alias}.",";}
					foreach my $line(@$fields){
						my $id = $line->{'filter_id'}; my $checked="";
						if ($ids && $ids =~/$id,/){$checked = "true";}
						if ($alias eq "color"){
							if (param('color') eq $line->{'field'}){$checked = "true";}
							my $count=""; my $c1=""; my $c2=""; my $c3="";
							my $color = $line->{'field'}."|";
							while ($color =~ m/(.+?)\|/g) {
								$count++;
								if ($count eq "1"){$c1 = $1;}
								elsif ($count eq "2"){$c2 = $1;}
								elsif ($count eq "3"){$c3 = $1;}
							}
							if ($count eq "1"){
								$filter .='<label data-name="'.$line->{'field'}.'" class="color one'.($checked?' active':'').'"><ins class="'.$c1.'">&nbsp;</ins></label>';
							}
							elsif ($count eq "2"){
								$colors .='<label data-name="'.$line->{'field'}.'" class="color two'.($checked?' active':'').'"><ins class="'.$c1.'">&nbsp;</ins><ins class="'.$c2.'">&nbsp;</ins></label>';
							}		
							elsif ($count eq "3"){
								if ($c1 eq "red" && $c2 eq "green" && $c3 eq "blue"){
									$rgb .='<label data-name="'.$line->{'field'}.'" class="color three'.($checked?' active':'').'"><ins class="'.$c1.'">&nbsp;</ins><ins class="'.$c2.'">&nbsp;</ins><ins class="'.$c3.'">&nbsp;</ins></label>';
								}
								else {
									$three .='<label data-name="'.$line->{'field'}.'" class="color three'.($checked?' active':'').'"><ins class="'.$c1.'">&nbsp;</ins><ins class="'.$c2.'">&nbsp;</ins><ins class="'.$c3.'">&nbsp;</ins></label>';
								}
							}
						}
						elsif ($alias eq "proizvoditel"){
							$pro++;
							my $checked;
							if (param('proizvoditel_1') eq "on" && $pro eq "1" or param('proizvoditel_2') eq "on" && $pro eq "2"){
								$checked = "true";
							}
							$filter .='<li data-id="'.$id.'">
									<input class="checkbox"'.($checked?' checked':'').' type="checkbox" name="'.$alias.'_'.$pro.'" id="ch'.$id.'" />
									<label for="ch'.$id.'">'.$line->{'name'}.'</label>
								</li>';	
						}
						else {
							$filter .='<li data-id="'.$id.'">
									<input class="checkbox"'.($checked?' checked':'').' type="checkbox" name="f_'.$alias.'['.$id.']" id="ch'.$id.'" />
									<label for="ch'.$id.'">'.$line->{'name'}.'</label>
								</li>';
						}
					}
					if ($alias eq "color"){
						$filter .= $colors;
						$filter .= $rgb;
						$filter .= $three;
						
						$filter .='</div>';
					}
					else {					
						$filter .='</ul>';
					}
				}
				$filter .='</li>';
			}
		}
	}
	if ($filter){
			my $price_from=""; my $price_to="";
			my $res = $db->query("SELECT c_ids FROM cat_product_filters_group WHERE g_id = '".$group_id."'");
			my $ids = $res->[0]->{'c_ids'};
			if ($group_id eq "3" or $group_id eq "5"){
				$price_from="45"; $price_to="16000";
			}
			else {
				$price_from="5"; $price_to="5000";
			}
			if (!$price_from && !$price_to){
				my $from = $db->query("SELECT p.p_price FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE pl.cat_id IN (".$ids.") AND p.p_price > 0 ORDER BY p.p_price ASC LIMIT 1");
				my $to = $db->query("SELECT p.p_price FROM cat_product AS p JOIN cat_product_rel AS pl ON(pl.cat_p_id=p.p_id) WHERE pl.cat_id IN (".$ids.") AND p.p_price > 0 ORDER BY p.p_price DESC LIMIT 1");
				
				$price_from = $from->[0]->{'p_price'};
				$price_to = $to->[0]->{'p_price'};
				
				$price_from = sprintf("%.0f",$price_from);
				$price_to = sprintf("%.0f",$price_to);	
			}
	
			$result ='<div class="filter-title">Воспользуйтесь <span>фильтром это удобно</span></div>
					<form class="filter-box" action="/catalog/filter/">
					<input type="hidden" name="cid" value="'.$c_id.'">
					<input type="hidden" name="ids" value="'.$ids.'">
					<input type="hidden" name="gid" value="'.$group_id.'">
					<input type="hidden" name="color" value="'.param('color').'">
					<fieldset>
						<div class="choice-prices">
							<strong>Цена</strong>
							<div class="labels">
								<em>от</em>
								<input class="text" type="text" id="minCost" name="price_from" value="'.(param('price_from')?''.param('price_from').'':''.$price_from.'').'"/>
								<em>до</em>
								<input class="text" type="text" id="maxCost" name="price_to" value="'.(param('price_to')?''.param('price_to').'':''.$price_to.'').'"/>
							</div>
							<div class="slider-price">
								<span class="price" id="price_from">'.$price_from.'</span>
								<span class="price price2" id="price_to">'.$price_to.'</span>
							</div>
							<div class="slider-wrap">
								<div id="slider"></div>
							</div>
						</div>
						<div class="filter-holder">
							<ul class="filter-list">
								'.$filter;
				if ($c_id ne $parent_id && $c_id ne $parent_cid){				
					$result .='<li class="option">
									<label><input type="checkbox" name="find_parent"'.($find_parent?' checked':'').'><span>Искать во всем разделе</span></label>
								</li>';
				}
				else {
					$result .='<input type="hidden" name="find_parent" value="on">';
				}
					$result .='
							</ul>
							<input type="submit" class="submit" value="Подобрать" />
						</div>
					</fieldset>
				</form>';
	}
				
	return $result;
}

sub findFilterCat {

	my $id = shift;
	my $parent_id = shift;
	if (!$parent_id){
		$parent_id = findParentCat($id);
	}
	my $result="";
	my $res = $db->query("SELECT * FROM cat_product_filters_group");
	if ($res){
		foreach my $item(@$res){
			my $ids = $item->{'c_ids'}.",";
			while ($ids =~ m/(\d+)\,/g) {
				if ($id eq $1 or $parent_id eq $1){
					$result = $item->{'g_id'}; last;
				}
			}
			if ($result){
				return $result; last;
			}
		}
	}
	if (!$result){
		return 0;
	}
}


# Стилизация товара

sub build_ProductLabel {

	my $id = shift;
	my $parent_id = shift;

	my $label1=""; my $label2=""; my $label3=""; my $label4="";
	my $color1=""; my $color2=""; my $color3=""; my $pack=""; my $packnorm=""; my $unit="";
	my $result = $db->query("SELECT field, value FROM cat_product_fields WHERE p_id ='".$id."'");
	if ($parent_id){
		foreach my $line(@$result){
			if ($line->{'field'} eq "Цвет 1" && $line->{'value'}){
				$color1 = $line->{'value'};
			}
			if ($line->{'field'} eq "Цвет 2" && $line->{'value'}){
				$color2 = $line->{'value'};
			}
			if ($line->{'field'} eq "Цвет 3" && $line->{'value'}){
				$color3 = $line->{'value'};
			}
			elsif ($parent_id eq "10"){
				if ($line->{'field'} eq "Прямой потребляемый ток, A"){
					my $value = modSpec($line->{'value'});
					$label2 ='<label title="Прямой потребляемый ток">'.$value.'</label>';
				}		
				elsif ($line->{'field'} eq "Рассеиваемая мощность, W"){
					my $value = modSpec($line->{'value'});
					$label3 ='<label title="Рассеиваемая мощность">'.$value.'</label>';
				}
			}
			elsif ($line->{'field'} eq "Цоколь"){
				$label2 ='<label title="Цоколь">'.$line->{'value'}.'</label>';
			}			
			elsif ($line->{'field'} eq "Напряжение питания, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="Напряжение питания">'.$value.'</label>';
			}
			elsif (($parent_id eq "6" or $parent_id eq "8") && $line->{'field'} eq "Входное напряжение, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="Входное напряжение">'.$value.'</label>';
			}				
			elsif ($parent_id eq "1" && ($line->{'field'} eq "Падение напряжения, V" or $line->{'field'} eq "Прямой потребляемый ток, A")){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="Падение напряжения">'.$value.'</label>';
			}
			if (($parent_id eq "2" or $parent_id eq "5") && $line->{'field'} eq "Потребляемая мощность, W"){
				$label3 ='<label title="Потребляемая мощность">'.$line->{'value'}.'</label>';
			}	
			if (($parent_id eq "7" or $parent_id eq "8") && $line->{'field'} eq "Выходная мощность, W"){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="Выходная мощность">'.$value.'</label>';
			}
			if ($parent_id eq "1" && $line->{'field'} eq "Рассеиваемая мощность, W"){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="Рассеиваемая мощность">'.$value.'</label>';
			}
			if (($parent_id eq "1" or $parent_id eq "3" or $parent_id eq "4" or $parent_id eq "6" or $parent_id eq "10") && $line->{'field'} eq "Потребляемая мощность, W"){
				my $value = $line->{'value'};
				$value =~ s/,/./g;
				$label3 ='<label>'.$value.'</label>';
			}
			if (($parent_id eq "9") && $line->{'field'} eq "Размеры, мм"){
				my $value = $line->{'value'};
				$value =~ s/,/./g;
				$label4 ='<label>'.$value.'</label>';
			}
			elsif ($line->{'field'} eq "Плотность светодиодов, шт/м" && $line->{'value'}){
				my $v = $line->{'value'};
				$v =~ s/\/м$//g;
				$label4 ='<label title="Плотность светодиодов, шт/м">'.$v.'</label>';
			}				
			if ($line->{'field'} eq "Вид упаковки"){$pack = $line->{'value'};}
			if ($line->{'field'} eq "Норма упаковки"){$packnorm = $line->{'value'};}
			if ($line->{'field'} eq "Единица измерения"){$unit = $line->{'value'};}		
		}
	}
	else {
		foreach my $line(@$result){
			if ($line->{'field'} eq "Цвет 1" && $line->{'value'}){
				$color1 = $line->{'value'};
			}
			if ($line->{'field'} eq "Цвет 2" && $line->{'value'}){
				$color2 = $line->{'value'};
			}
			if ($line->{'field'} eq "Цвет 3" && $line->{'value'}){
				$color3 = $line->{'value'};
			}
			if ($line->{'field'} eq "Цоколь"){
				$label2 ='<label title="Цоколь">'.$line->{'value'}.'</label>';
			}			
			elsif ($line->{'field'} eq "Напряжение питания, V" && $line->{'value'}){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="Напряжение питания">'.$value.'</label>';
			}
			elsif ($line->{'field'} eq "Входное напряжение, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="Входное напряжение">'.$value.'</label>';
			}			
			elsif ($line->{'field'} eq "Падение напряжения, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="Падение напряжения">'.$value.'</label>';
			}
			if ($line->{'field'} eq "Потребляемая мощность, W" && $line->{'value'}){
				$label3 ='<label title="Потребляемая мощность">'.$line->{'value'}.'</label>';
			}	
			elsif ($line->{'field'} eq "Выходная мощность, W" && $line->{'value'}){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="Выходная мощность">'.$value.'</label>';
			}			
			elsif ($line->{'field'} eq "Рассеиваемая мощность, W" && $line->{'value'}){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="Рассеиваемая мощность">'.$value.'</label>';
			}
			if ($line->{'field'} eq "Плотность светодиодов, шт/м" && $line->{'value'}){
				my $v = $line->{'value'};
				$v =~ s/\/м$//g;
				$label4 ='<label title="Плотность светодиодов, шт/м">'.$v.'</label>';
			}			
			if ($line->{'field'} eq "Вид упаковки"){$pack = $line->{'value'};}
			if ($line->{'field'} eq "Норма упаковки"){$packnorm = $line->{'value'};}
			if ($line->{'field'} eq "Единица измерения"){$unit = $line->{'value'};}			
		}
	}
	
	if ($color1 && !$color2 && !$color3){
		$label1 ='<label class="color one" title="'.getColorRus($color1).'"><ins class="'.$color1.'">&nbsp;</ins></label>';
	}
	elsif ($color1 && $color2 && !$color3){
		$label1 ='<label class="color two" title="MIX"><ins class="'.$color1.'">&nbsp;</ins><ins class="'.$color2.'">&nbsp;</ins></label>';
	}
	elsif ($color1 && $color2 && $color3){
		$label1 ='<label class="color three"'.($color1 eq "red" && $color2 eq "green" && $color3 eq "blue"?' title="Мультицветный RGB"':' title="MIX"').'><ins class="'.$color1.'">&nbsp;</ins><ins class="'.$color2.'">&nbsp;</ins><ins class="'.$color3.'">&nbsp;</ins></label>';
	}	
	
	return ($label1, $label2, $label3, $label4, $pack, $packnorm, $unit);
}

sub modSpec {

	my $value = shift;
	
	$value =~ s/(\n+)/ /g;
	$value =~ s/(\w+):\s//g;
	$value =~ s/;//g;
	$value =~ s/,/./g;
	$value =~ s/\s(\w\s)(\d+)/-$2/g;
	$value =~ s/(\d+)\s(\w)/$1$2/g;
	$value =~ s/-(\d+)-/.../g;
	
	return $value;
}
	
# Дерево категорий каталога

sub build_CatalogTree
{
	my $sort = shift;
	my $section = shift;
	my $point="";
	my $count="";
	my $flag="";
	if ($adm_act eq "pages" && $num_edit eq "1"){
		$flag = 1;
	}	
	if (!$flag){
		$limit_catalog_tree = 8;
	}
	my $adm_act = $adm_act;
	my $num_edit = $num_edit;
	if ($adm_act eq "product"){
		$parent_cid = $parent_id;
	}
	if ($adm_act eq "catalog" && param('cid') > 0){
		$num_edit = param('cid');
	}
	my $tree = "";
	my $result = $db->query("SELECT * FROM cat_category WHERE c_pid = '0' AND c_show_menu = '1' ORDER BY $sort;");
	foreach my $item(@$result){
		my $class=""; my $c_pid=""; $count++;
		if ($adm_act eq "catalog" && $num_edit==$item->{c_id}){$class = ' class="active" data-active="true"';}
		if ($adm_act eq "catalog" && $parent_cid==$item->{c_id}){$class = ' class="active" data-active="true"';}
		
		if (!$class && $parent_cid ne "0" && ($adm_act eq "catalog" or $adm_act eq "product")){
			if ($parent_id eq $item->{c_id}){
				$class = ' class="active" data-active="true"';
			}
		}
		
		if ($section > 0){
			if ($section == $item->{c_id}){
				my $subs ="";
				if (my $sub = recMenuCatalog($item->{c_id}, 0, $section)){
					$subs = $sub;
				}		
				$tree = $subs;
			}
		}
		else {	
			my $subs ="";
			if (my $sub = recMenuCatalog($item->{c_id}, 0)){
				$subs = $sub;
			}
			if ($subs){
				if ($item->{c_id} eq "1"){
					$subs ='
					<div class="submenu br-none custom width-854">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}
				elsif ($item->{c_id} eq "2"){
					$subs ='
					<div class="submenu inline custom width-674">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}	
				elsif ($item->{c_id} eq "3"){
					$subs ='
					<div class="submenu">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}
				elsif ($item->{c_id} eq "4"){
					$subs ='
					<div class="submenu br-none custom width-724">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}				
				elsif ($item->{c_id} eq "5" or $item->{c_id} eq "6"){
					$subs ='
					<div class="submenu custom width-654">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}
				elsif ($item->{c_id} eq "7"){
					$subs ='
					<div class="submenu br-none custom width-854">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}	
				elsif ($item->{c_id} eq "8"){
					$subs ='
					<div class="submenu br-none custom width-784">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}				
				else {
					$subs ='
					<div class="submenu br-none custom width-694">
						<div class="column-holder">
							'.$subs.'
						</div>
					</div>';
				}		
			}
			if ($limit_catalog_tree > 0 && $count <= $limit_catalog_tree or $limit_catalog_tree eq ""){
				my $num = $count;
				if (!$flag){$num += 1;}
				$tree .= '<li class="list'.($num < 10?'0'.$num.'':''.$num.'').'">';
				if ($flag){
					$tree .= '<a'.$class.' href="/catalog/'.$item->{c_alias}.'">'.$item->{c_name}.'</a>';
					$tree .= $subs;
					$tree .= '</li>';
				}
				else {
					$tree .= '<div class="holder">';
					$tree .= '<a'.$class.' href="/catalog/'.$item->{c_alias}.'">'.$item->{c_name_short}.'</a>';
					$tree .= $subs;
					$tree .= '</div>';
					$tree .= '</li>';
				}
			}
		}
	}
	
	sub recMenuCatalog {

		my $id = shift;
		my $level = shift;
		my $section = shift;
			
		my $text="";		
		my $result = $db->query("SELECT c_id, c_pid, c_name, c_desc_sm, c_alias FROM cat_category WHERE c_pid='".$id."' AND c_show_menu = '1' ORDER BY $sort");
		if ($result){
			foreach my $item(@$result){
				my $subs ="";
				if (my $sub = recMenuCatalog($item->{c_id}, $level+1)){
					$subs = $sub;
				}		
				if ($subs){
					my $clear="";
					if ($section){$clear = ' clearfix';}
					$subs = '<ul'.($level eq "0"?' class="bullet-list'.$clear.'"':'').'>'.$subs.'</ul>';
				}				
				if ($level eq "0"){
				
					my $image=""; my $class="";
					if ($section eq "2" or $section eq "3" or $section eq "4"){
						$class = " image";
						if ($section eq "2" or $section eq "3"){
							$class .= " desc";
						}
						$image = '<div class="foto"><img src="/files/catalog/category/'.($item->{c_id}+1000).'.png" alt=""/></div>';
					}
					else {
						if ($item->{c_desc_sm}){
							$class .= " desc-box";
						}
					}
					$text .= '<div class="column'.$class.'">';
					
					if ($section){
						$text .= '<a class="parent" href="/catalog/'.$item->{c_alias}.'">'.$image.'<span>'.$item->{c_name}.'</span>'.($item->{c_desc_sm}?'<p>'.$item->{c_desc_sm}.'</p>':'').'</a>';
					}
					else {
						$text .= '<a class="parent'.($item->{c_pid} eq "2"?' p2':'').'" href="/catalog/'.$item->{c_alias}.'">'.$item->{c_name}.''.($item->{c_pid} ne "2"?'<span class="br"></span>':'').'</a>';
					}
					$text .= $subs;
					
					$text .= '</div>';
				}
				else {
					$text .= '<li>';
					$text .= '<a'.($item->{c_id} eq "178"?' class="ws"':'').' href="/catalog/'.$item->{c_alias}.'">'.$item->{c_name}.'</a>';
					$text .= $subs;
					$text .= '</li>';
				}
			}
		}
		else {
			return 0;
		}
		return $text;
	};
	if ($tree && $flag){
		$tree = '<ul>'.$tree.'</ul>';
	}
	return $tree;
}


# Поиск родительской категории

sub findParentCat {
	my $c_pid = shift;
	my $res = $db->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$c_pid."'");
	foreach my $line(@$res){
		my $result = $line->{c_id}; 
		if ($line->{c_pid} eq "0"){
			return $result; last;
		}
		else {
			if (my $ids = findSubParentCat($line->{c_pid})){
				$result = $ids;
			}
			if ($result){
				return $result; last;
			}
		}
	}
	sub findSubParentCat {
		my $parent = shift;
		my $result="";
		my $res_parent = $db->query("SELECT cat_category.c_id, cat_category.c_pid FROM cat_category WHERE c_id='".$parent."'");
		if ($res_parent){
			foreach my $line(@$res_parent){
				my $result = $line->{c_id};
				if ($line->{c_pid} eq "0"){
					return $result; last;
				}
				else {
					if (my $ids = findSubParentCat($line->{c_pid})){
						$result = $ids;
					}
					if ($result){
						return $result; last;
					}
				}
			}
		}
	}
}


# Подсчет товаров в категории

sub getCountProducts {
	$id = shift;
	my $result = $db->query("SELECT cat_p_id FROM cat_product_rel WHERE cat_id = '".$id."' AND cat_main = '1';");
	return @$result;
}


# Цвета на русском

sub getColorRus {
	
	$color = shift;
	$param = shift;
	
	if ($color eq "day_white"){
		$color = "Day White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Белый дневной <strong>".$color."</strong>";}
		else {return "Белый дневной ".$color;}
	}
	elsif ($color eq "warm_white"){
		$color = "Warm White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Белый теплый <strong>".$color."</strong>";}
		else {return "Белый теплый ".$color;}
	}
	elsif ($color eq "white"){
		$color = "White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Белый <strong>".$color."</strong>";}
		else {return "Белый ".$color;}
	}
	elsif ($color eq "cool_white"){
		$color = "Cool White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Белый холодный <strong>".$color."</strong>";}
		else {return "Белый холодный ".$color;}
	}
	elsif ($color eq "blue"){
		$color = "Blue";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Синий <strong>".$color."</strong>";}
		else {return "Синий ".$color;}
	}
	elsif ($color eq "green"){
		$color = "Green";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Зеленый <strong>".$color."</strong>";}
		else {return "Зеленый ".$color;}
	}
	elsif ($color eq "ir880"){
		$color = "Aluminum";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Алюминиевый <strong>".$color."</strong>";}
		else {return "Алюминиевый ".$color;}
	}
	elsif ($color eq "uv400" or $color eq "violet"){
		$color = "Violet";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Фиолетовый <strong>".$color."</strong>";}
		else {return "Фиолетовый ".$color;}
	}
	elsif ($color eq "orange"){
		$color = "Orange";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Оранжевый <strong>".$color."</strong>";}
		else {return "Оранжевый ".$color;}
	}	
	elsif ($color eq "pink"){
		$color = "Pink";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Розовый <strong>".$color."</strong>";}
		else {return "Розовый ".$color;}
	}
	elsif ($color eq "red"){
		$color = "Red";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Красный <strong>".$color."</strong>";}
		else {return "Красный ".$color;}
	}
	elsif ($color eq "yellow"){
		$color = "Yellow";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Желтый <strong>".$color."</strong>";}
		else {return "Желтый ".$color;}
	}
	elsif ($color eq "green_yellow"){
		$color = "Green/Yellow";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Оливковый <strong>".$color."</strong>";}
		else {return "Оливковый ".$color;}
	}
	elsif ($color eq "rgb" or $color eq "red|green|blue"){
		$color = "RGB";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Мультицветный <strong>".$color."</strong>";}
		else {return "Мультицветный ".$color;}
	}
	else {
		$color = "MIX";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "Смешенный <strong>".$color."</strong>";}
		else {return "Смешенный ".$color;}		
	}
}


# Вывод категорий на главной

sub build_Category
{
	my $sort = shift;
	my $big = shift;
	my $category = "";
	my $result = $db->query("SELECT cat_category.c_id, cat_category.c_alias, cat_category.c_name FROM cat_category WHERE c_pid = '0' AND cat_category.c_show_menu = '1' ORDER BY $sort;");
	foreach my $item(@$result){
		$category .='<li>
						<a href="/catalog/'.$item->{c_alias}.'">
							<div class="image-box">
								<img src="'.$dirs_catalog_www.'/category/'.($item->{c_id}+1000).''.($big?'_big':'').'.png" alt="'.$item->{c_name}.'" />
							</div>
							<span class="name">'.$item->{c_name}.'</span>
						</a>
					</li>';
	}	
	if ($category){
		$category = '<ul class="catalog-list">'.$category.'</ul>';
	}

	return $category;
}

sub descCategory {

	my $section = shift;
	my $id = shift;
	
	my $result="";
	if ($section == "2"){
		if ($id == "89" or $id == "90" or $id == "91" or $id == "92" or $id == "93" or $id == "94" or $id == "95" or $id == "96"){
			$result ='<p>Доступные цвета: белый, холодный белый, теплый белый, синий, голубой, зеленый, оранжевый, розовый, красный, фиолетовый, желтый, RGB. С мощностью: от 5w до 60w. </p>';
		}
	}

	return $result;
}

sub categorySidebar {

	my $id = shift;
	
	my $result="";
	
	if ($id == "2"){	
		$result .='<h3 class="name"><span class="h3_1">Какие</span> <span class="h3_2">признаки</span> <span class="h3_3">некачественной</span> <span class="h3_4">ленты?</span></h3>
			<img src="/img/man1.jpg" class="man1">
			<ul class="checkbox">
				<li><span>Низкое качество</span><br>светодиодов</li>
				<li><span>Плохая</span> проводни-<br>ковая основа</li>
				<li><span>Низкое качество</span><br> герметиков и<br> клейкой основы</li>
				<li><span class="big">Низкая цена</span></li>
			</ul>
			<p class="desc">Особое внимание просим обратить наших клиентов, <strong>что 95% ленты поставляемой на российский рынок производится в Китае или Тайване.</strong> Заявления многих поставщиков, что их светодиодная лента "европейская" или "американская" являются ложью. Также, если Вы приобрели, как Вам кажется, дешевую, но "качественную" ленту Вы можете столкнуться с быстрым падением светового потока (до 50%), выгоранием отдельных светодиодов или вообще всей ленты, а также данные эксперименты могут закончится пожаром. Выбор остается за Вами!</p>';
	}

	return $result;
}

sub categoryFooter {

	my $parent_id = shift;
	
	my $result=""; my $gallery=""; my $name="";
	if ($parent_id eq "2" or $parent_id eq "3" or $parent_id eq "4"){
		my $folder=""; my $counts="";
		if ($parent_id eq "2"){$folder="lenta"; $counts = 27; $name = "Светодиодные ленты в интерьере";}
		elsif ($parent_id eq "3"){$folder="lampa"; $counts = 15; $name = "Светодиодные лампы в интерьере";}
		elsif ($parent_id eq "4"){$folder="svet"; $counts = 14; $name = "Светодиодные светильники в интерьере";}
		for (my $num=1001; $num < ($counts+1001); $num++) {
			$gallery .='<div class="item"><a href="/files/catalog/'.$folder.'/'.$num.'_big.jpg"><img src="/files/catalog/'.$folder.'/'.$num.'_small.jpg" alt=""/></a></div>';
		}
	}
	if ($gallery){
		$result .= '<div class="product-gallery-wrap">
			<h2>'.$name.'</h2>
			<div class="product-gallery scroller">
				<div class="product-gallery-list owl-carousel">
					'.$gallery.'
				</div>
			</div>
		</div>';
	}
	
	if ($parent_id eq "1"){$name = "светодиодов";}
	elsif ($parent_id eq "2"){$name = "светодиодных лент";}
	elsif ($parent_id eq "3"){$name = "светодиодных ламп";}
	elsif ($parent_id eq "4"){$name = "светильников";}
	elsif ($parent_id eq "5"){$name = "LED модулей";}
	elsif ($parent_id eq "6"){$name = "LED прожекторов";}
	elsif ($parent_id eq "7"){$name = "управления освещением";}
	elsif ($parent_id eq "8"){$name = "источников питания";}
	elsif ($parent_id eq "9"){$name = "профилей";}
	
	if ($parent_id > 10000){
		$result .= '<div class="content-billboard">
			<div class="container">
				<h4>Получить дилерский прайс<br> по закупке '.$name.'<br> оптом</h4>
				<button><span>оставить заявку</span></button>
			</div>
		</div>';
	}
	
	return $result;
}

1;