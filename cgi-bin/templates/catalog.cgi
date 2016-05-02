my $db = new Core::DB();


# ��������� �������� (������ ������� �������)

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


# ��������� �������� (������ ������� �������)

my $limit_cat = 5; # ���-�� ������������

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
	else {$select .= '<div class="select_brands"><a href="#!" class="open">�������� �����<em></em></a><ul>';}
	my $result = $db->query("SELECT * FROM cat_product_type ORDER BY t_pos ASC");
	foreach my $line(@$result){
		if ($line->{'t_show'} ne "0"){
			$option .= '<li><a href="/catalog/'.($page_alias ne ""?''.$page_alias.'/':'').'brands/'.$line->{'t_alias'}.'">'.$line->{'t_name'}.'</a></li>';
		} else {$option .="";}
	}
	$select .= $option.'</ul></div>';		
    return $select;
}


# ����� ����������� ���������

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
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lenty/lenta-klassa-lyuks">����� ������ ����</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lenty/lenta-na-diodah-3528">����� �� ������ 3528</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lenty/lenta-na-diodah-5060-5050">����� �� ������ 5060 (5050)</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/g4-220v">����� � ������� G4 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/g9-220v">����� � ������� G9 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/e27-220v">����� E27 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/e14-220v">����� E14 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-svetilniki/ultratonkie-svetilniki">������������ �����������</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/gu10-220v">����� GU10 220V</a></li>';
		# $catalog_submenu .='<li><a href="/catalog/svetodiodnye-lampy/mr16-gu53-220v">����� GU5.3 220V</a></li>';	
	# }
	if ($catalog_submenu){
	
		my $name = '���������';
		if ($parent ne "0" && !$subs && ($adm_act eq "catalog" or $adm_act eq "product")){$name = '���������';}
		elsif ($parent eq "0" or $subs && ($adm_act eq "catalog" or $adm_act eq "product")){$name = '� ���� �������';}
		elsif ($parent ne "0" && $adm_act ne "catalog" && $adm_act ne "product"){$name = '����������';}
		
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


# ���������� �������

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
	
			$result ='<div class="filter-title">�������������� <span>�������� ��� ������</span></div>
					<form class="filter-box" action="/catalog/filter/">
					<input type="hidden" name="cid" value="'.$c_id.'">
					<input type="hidden" name="ids" value="'.$ids.'">
					<input type="hidden" name="gid" value="'.$group_id.'">
					<input type="hidden" name="color" value="'.param('color').'">
					<fieldset>
						<div class="choice-prices">
							<strong>����</strong>
							<div class="labels">
								<em>��</em>
								<input class="text" type="text" id="minCost" name="price_from" value="'.(param('price_from')?''.param('price_from').'':''.$price_from.'').'"/>
								<em>��</em>
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
									<label><input type="checkbox" name="find_parent"'.($find_parent?' checked':'').'><span>������ �� ���� �������</span></label>
								</li>';
				}
				else {
					$result .='<input type="hidden" name="find_parent" value="on">';
				}
					$result .='
							</ul>
							<input type="submit" class="submit" value="���������" />
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


# ���������� ������

sub build_ProductLabel {

	my $id = shift;
	my $parent_id = shift;

	my $label1=""; my $label2=""; my $label3=""; my $label4="";
	my $color1=""; my $color2=""; my $color3=""; my $pack=""; my $packnorm=""; my $unit="";
	my $result = $db->query("SELECT field, value FROM cat_product_fields WHERE p_id ='".$id."'");
	if ($parent_id){
		foreach my $line(@$result){
			if ($line->{'field'} eq "���� 1" && $line->{'value'}){
				$color1 = $line->{'value'};
			}
			if ($line->{'field'} eq "���� 2" && $line->{'value'}){
				$color2 = $line->{'value'};
			}
			if ($line->{'field'} eq "���� 3" && $line->{'value'}){
				$color3 = $line->{'value'};
			}
			elsif ($parent_id eq "10"){
				if ($line->{'field'} eq "������ ������������ ���, A"){
					my $value = modSpec($line->{'value'});
					$label2 ='<label title="������ ������������ ���">'.$value.'</label>';
				}		
				elsif ($line->{'field'} eq "������������ ��������, W"){
					my $value = modSpec($line->{'value'});
					$label3 ='<label title="������������ ��������">'.$value.'</label>';
				}
			}
			elsif ($line->{'field'} eq "������"){
				$label2 ='<label title="������">'.$line->{'value'}.'</label>';
			}			
			elsif ($line->{'field'} eq "���������� �������, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="���������� �������">'.$value.'</label>';
			}
			elsif (($parent_id eq "6" or $parent_id eq "8") && $line->{'field'} eq "������� ����������, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="������� ����������">'.$value.'</label>';
			}				
			elsif ($parent_id eq "1" && ($line->{'field'} eq "������� ����������, V" or $line->{'field'} eq "������ ������������ ���, A")){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="������� ����������">'.$value.'</label>';
			}
			if (($parent_id eq "2" or $parent_id eq "5") && $line->{'field'} eq "������������ ��������, W"){
				$label3 ='<label title="������������ ��������">'.$line->{'value'}.'</label>';
			}	
			if (($parent_id eq "7" or $parent_id eq "8") && $line->{'field'} eq "�������� ��������, W"){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="�������� ��������">'.$value.'</label>';
			}
			if ($parent_id eq "1" && $line->{'field'} eq "������������ ��������, W"){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="������������ ��������">'.$value.'</label>';
			}
			if (($parent_id eq "1" or $parent_id eq "3" or $parent_id eq "4" or $parent_id eq "6" or $parent_id eq "10") && $line->{'field'} eq "������������ ��������, W"){
				my $value = $line->{'value'};
				$value =~ s/,/./g;
				$label3 ='<label>'.$value.'</label>';
			}
			if (($parent_id eq "9") && $line->{'field'} eq "�������, ��"){
				my $value = $line->{'value'};
				$value =~ s/,/./g;
				$label4 ='<label>'.$value.'</label>';
			}
			elsif ($line->{'field'} eq "��������� �����������, ��/�" && $line->{'value'}){
				my $v = $line->{'value'};
				$v =~ s/\/�$//g;
				$label4 ='<label title="��������� �����������, ��/�">'.$v.'</label>';
			}				
			if ($line->{'field'} eq "��� ��������"){$pack = $line->{'value'};}
			if ($line->{'field'} eq "����� ��������"){$packnorm = $line->{'value'};}
			if ($line->{'field'} eq "������� ���������"){$unit = $line->{'value'};}		
		}
	}
	else {
		foreach my $line(@$result){
			if ($line->{'field'} eq "���� 1" && $line->{'value'}){
				$color1 = $line->{'value'};
			}
			if ($line->{'field'} eq "���� 2" && $line->{'value'}){
				$color2 = $line->{'value'};
			}
			if ($line->{'field'} eq "���� 3" && $line->{'value'}){
				$color3 = $line->{'value'};
			}
			if ($line->{'field'} eq "������"){
				$label2 ='<label title="������">'.$line->{'value'}.'</label>';
			}			
			elsif ($line->{'field'} eq "���������� �������, V" && $line->{'value'}){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="���������� �������">'.$value.'</label>';
			}
			elsif ($line->{'field'} eq "������� ����������, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="������� ����������">'.$value.'</label>';
			}			
			elsif ($line->{'field'} eq "������� ����������, V"){
				my $value = modSpec($line->{'value'});
				$label2 ='<label title="������� ����������">'.$value.'</label>';
			}
			if ($line->{'field'} eq "������������ ��������, W" && $line->{'value'}){
				$label3 ='<label title="������������ ��������">'.$line->{'value'}.'</label>';
			}	
			elsif ($line->{'field'} eq "�������� ��������, W" && $line->{'value'}){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="�������� ��������">'.$value.'</label>';
			}			
			elsif ($line->{'field'} eq "������������ ��������, W" && $line->{'value'}){
				my $value = modSpec($line->{'value'});
				$label3 ='<label title="������������ ��������">'.$value.'</label>';
			}
			if ($line->{'field'} eq "��������� �����������, ��/�" && $line->{'value'}){
				my $v = $line->{'value'};
				$v =~ s/\/�$//g;
				$label4 ='<label title="��������� �����������, ��/�">'.$v.'</label>';
			}			
			if ($line->{'field'} eq "��� ��������"){$pack = $line->{'value'};}
			if ($line->{'field'} eq "����� ��������"){$packnorm = $line->{'value'};}
			if ($line->{'field'} eq "������� ���������"){$unit = $line->{'value'};}			
		}
	}
	
	if ($color1 && !$color2 && !$color3){
		$label1 ='<label class="color one" title="'.getColorRus($color1).'"><ins class="'.$color1.'">&nbsp;</ins></label>';
	}
	elsif ($color1 && $color2 && !$color3){
		$label1 ='<label class="color two" title="MIX"><ins class="'.$color1.'">&nbsp;</ins><ins class="'.$color2.'">&nbsp;</ins></label>';
	}
	elsif ($color1 && $color2 && $color3){
		$label1 ='<label class="color three"'.($color1 eq "red" && $color2 eq "green" && $color3 eq "blue"?' title="������������� RGB"':' title="MIX"').'><ins class="'.$color1.'">&nbsp;</ins><ins class="'.$color2.'">&nbsp;</ins><ins class="'.$color3.'">&nbsp;</ins></label>';
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
	
# ������ ��������� ��������

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


# ����� ������������ ���������

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


# ������� ������� � ���������

sub getCountProducts {
	$id = shift;
	my $result = $db->query("SELECT cat_p_id FROM cat_product_rel WHERE cat_id = '".$id."' AND cat_main = '1';");
	return @$result;
}


# ����� �� �������

sub getColorRus {
	
	$color = shift;
	$param = shift;
	
	if ($color eq "day_white"){
		$color = "Day White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "����� ������� <strong>".$color."</strong>";}
		else {return "����� ������� ".$color;}
	}
	elsif ($color eq "warm_white"){
		$color = "Warm White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "����� ������ <strong>".$color."</strong>";}
		else {return "����� ������ ".$color;}
	}
	elsif ($color eq "white"){
		$color = "White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "����� <strong>".$color."</strong>";}
		else {return "����� ".$color;}
	}
	elsif ($color eq "cool_white"){
		$color = "Cool White";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "����� �������� <strong>".$color."</strong>";}
		else {return "����� �������� ".$color;}
	}
	elsif ($color eq "blue"){
		$color = "Blue";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "����� <strong>".$color."</strong>";}
		else {return "����� ".$color;}
	}
	elsif ($color eq "green"){
		$color = "Green";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "������� <strong>".$color."</strong>";}
		else {return "������� ".$color;}
	}
	elsif ($color eq "ir880"){
		$color = "Aluminum";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "����������� <strong>".$color."</strong>";}
		else {return "����������� ".$color;}
	}
	elsif ($color eq "uv400" or $color eq "violet"){
		$color = "Violet";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "���������� <strong>".$color."</strong>";}
		else {return "���������� ".$color;}
	}
	elsif ($color eq "orange"){
		$color = "Orange";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "��������� <strong>".$color."</strong>";}
		else {return "��������� ".$color;}
	}	
	elsif ($color eq "pink"){
		$color = "Pink";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "������� <strong>".$color."</strong>";}
		else {return "������� ".$color;}
	}
	elsif ($color eq "red"){
		$color = "Red";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "������� <strong>".$color."</strong>";}
		else {return "������� ".$color;}
	}
	elsif ($color eq "yellow"){
		$color = "Yellow";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "������ <strong>".$color."</strong>";}
		else {return "������ ".$color;}
	}
	elsif ($color eq "green_yellow"){
		$color = "Green/Yellow";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "��������� <strong>".$color."</strong>";}
		else {return "��������� ".$color;}
	}
	elsif ($color eq "rgb" or $color eq "red|green|blue"){
		$color = "RGB";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "������������� <strong>".$color."</strong>";}
		else {return "������������� ".$color;}
	}
	else {
		$color = "MIX";
		if ($param eq "short") {return $color;}
		elsif ($param eq "bold") {return "��������� <strong>".$color."</strong>";}
		else {return "��������� ".$color;}		
	}
}


# ����� ��������� �� �������

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
			$result ='<p>��������� �����: �����, �������� �����, ������ �����, �����, �������, �������, ���������, �������, �������, ����������, ������, RGB. � ���������: �� 5w �� 60w. </p>';
		}
	}

	return $result;
}

sub categorySidebar {

	my $id = shift;
	
	my $result="";
	
	if ($id == "2"){	
		$result .='<h3 class="name"><span class="h3_1">�����</span> <span class="h3_2">��������</span> <span class="h3_3">��������������</span> <span class="h3_4">�����?</span></h3>
			<img src="/img/man1.jpg" class="man1">
			<ul class="checkbox">
				<li><span>������ ��������</span><br>�����������</li>
				<li><span>������</span> ��������-<br>����� ������</li>
				<li><span>������ ��������</span><br> ���������� �<br> ������� ������</li>
				<li><span class="big">������ ����</span></li>
			</ul>
			<p class="desc">������ �������� ������ �������� ����� ��������, <strong>��� 95% ����� ������������ �� ���������� ����� ������������ � ����� ��� �������.</strong> ��������� ������ �����������, ��� �� ������������ ����� "�����������" ��� "������������" �������� �����. �����, ���� �� ���������, ��� ��� �������, �������, �� "������������" ����� �� ������ ����������� � ������� �������� ��������� ������ (�� 50%), ���������� ��������� ����������� ��� ������ ���� �����, � ����� ������ ������������ ����� ���������� �������. ����� �������� �� ����!</p>';
	}

	return $result;
}

sub categoryFooter {

	my $parent_id = shift;
	
	my $result=""; my $gallery=""; my $name="";
	if ($parent_id eq "2" or $parent_id eq "3" or $parent_id eq "4"){
		my $folder=""; my $counts="";
		if ($parent_id eq "2"){$folder="lenta"; $counts = 27; $name = "������������ ����� � ���������";}
		elsif ($parent_id eq "3"){$folder="lampa"; $counts = 15; $name = "������������ ����� � ���������";}
		elsif ($parent_id eq "4"){$folder="svet"; $counts = 14; $name = "������������ ����������� � ���������";}
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
	
	if ($parent_id eq "1"){$name = "�����������";}
	elsif ($parent_id eq "2"){$name = "������������ ����";}
	elsif ($parent_id eq "3"){$name = "������������ ����";}
	elsif ($parent_id eq "4"){$name = "������������";}
	elsif ($parent_id eq "5"){$name = "LED �������";}
	elsif ($parent_id eq "6"){$name = "LED �����������";}
	elsif ($parent_id eq "7"){$name = "���������� ����������";}
	elsif ($parent_id eq "8"){$name = "���������� �������";}
	elsif ($parent_id eq "9"){$name = "��������";}
	
	if ($parent_id > 10000){
		$result .= '<div class="content-billboard">
			<div class="container">
				<h4>�������� ��������� �����<br> �� ������� '.$name.'<br> �����</h4>
				<button><span>�������� ������</span></button>
			</div>
		</div>';
	}
	
	return $result;
}

1;