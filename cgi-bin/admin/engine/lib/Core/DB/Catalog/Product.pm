package Core::DB::Catalog::Product;

require Core::DB::Work;
@ISA=qw(Core::DB::Work);

use Core::DB::Catalog::Category;
use Core::DB::Catalog::Product::Rel;
use Core::DB::Catalog::Product::Type;
use Core::DB::Catalog::Product::Rec;
use Core::DB::Catalog::Product::Hit;
use strict;

my %FIELDS = (
				'p_id' => "NULL",
				'p_name' => "NULL",
				'p_price' => "NULL",
				'p_price_opt' => "NULL",
				'p_price_opt_large' => "NULL",
				'p_price_cost' => "NULL",
				'p_price_old' => "NULL",
				'p_count' => "NULL",
				'p_hit' => "NULL",
				'p_spec' => "NULL",
				'p_news' => "NULL",
				'p_art' => "NULL",
  				'p_desc_sm' => "NULL",
				'p_img_url' => "NULL",
				'p_supplier' => 0,
				'p_desc_top' => "NULL",
				'p_desc_bottom' => "NULL",
				'p_title' => "NULL",
				'p_meta_desc' => "NULL",
				'p_meta_key' => "NULL",
				'p_date_add' => "NOW()",
				'p_date_up' => "NOW()",
				'p_show' => 1,
				'p_show_head' => 1,
				'p_alias' => "NULL",
				'p_redirect' => "NULL",
				'p_type_id' => "NULL",
				'p_color_rel' => "NULL",
				'p_raiting' => 0,
				'p_raiting_count' => 0,
				'p_maket' => "NULL",
			);
			
my $TABLE = 'cat_product';
			
my %params = (
			_FIELDS => \%FIELDS,
			TABLE => $TABLE
			);
			
sub new {
	my $class = shift;
	my $self = $class->SUPER::new( \%params ) || return undef;
	return $self;
}

sub getAllProduct {
	my $self = shift;
	my $id = shift;
	
	my $query = "SELECT p.*, DATE_FORMAT(p_date_add, \"%Y-%m-%d\") as p_date_add, DATE_FORMAT(p_date_up, \"%Y-%m-%d\") as p_date_up FROM ".$self->{TABLE}." AS p ORDER BY p_name ASC LIMIT 0,".$id."";
	my $result = $self->query($query);
	return $result if($result);
}

sub getAllProductCat {
	my $self = shift;
	my $id = shift;
	my $rel = new Core::DB::Catalog::Product::Rel;
	my $cat = new Core::DB::Catalog::Category;
		
	my $query = "SELECT p.*, pl.p_pos, pl.cat_id FROM ".$self->{TABLE}." AS p JOIN ".$rel->{TABLE}." AS pl ON(pl.cat_p_id=p.p_id) JOIN ".$cat->{TABLE}." AS c ON(c.c_id = pl.cat_id) WHERE pl.cat_id ='".$id."' ORDER BY pl.p_pos ASC";
	my $result = $self->query($query);
	return $result if($result);
}

sub addProduct {
	my $self = shift;
	my $params = shift;

	my ($rows, $id);
	$self->getFields($params);

	my $keys = "`".join("`, `",keys %{$self->{FIELDS}} )."`";
	my $values = join(", ", values %{$self->{FIELDS}} );

	my $query = "INSERT INTO `".$self->{TABLE}."`($keys) VALUES($values);";
	my $res = $self->insert($query);
	
	if(ref($res) eq 'ARRAY'){
		$self->clearFields;
		return $res if($rows);
	} else {
		$self->clearFields;
		return \$res;
	} 
	
}

sub delProduct {
	my $self = shift;
	my $id = shift;
	my $rel = new Core::DB::Catalog::Product::Rel;
	$self->delete("DELETE FROM ".$self->{TABLE}." WHERE p_id = '".$id."'");
	return $self->delete("DELETE FROM ".$rel->{TABLE}." WHERE cat_p_id = '".$id."'");
}

sub editProduct {
	my $self = shift;
	my $id = shift;
	my $params = shift;

	my %hash;
	my $query = "UPDATE `".$self->{TABLE}."` SET ";
	my @query;
	foreach my $item(keys %$params){
		if($self->{_FIELDS}->{$item} ne ""){
			$hash{$item} = $self->checked( $params->{$item} );
		}
	}
	
	foreach my $item(keys %hash){
		push(@query , "`$item` = ".$self->ignored( $hash{$item} ) );
	}
	$query .= join(",", @query)." WHERE p_id = '".$id."';";
	my $res = $self->update($query) if(scalar keys %hash > 0);
	return $res;
}

sub getProduct {
	my $self = shift;
	my $id = shift;
	my $rel = new Core::DB::Catalog::Product::Rel;
	my $cat = new Core::DB::Catalog::Category;
		
	my $query = "SELECT p.*, pl.p_pos, pl.cat_id, DATE_FORMAT(p_date_add, \"%Y-%m-%d\") as date_add, DATE_FORMAT(p_date_up, \"%Y-%m-%d\") as date_up FROM ".$self->{TABLE}." AS p JOIN ".$rel->{TABLE}." AS pl ON(pl.cat_p_id=p.p_id) JOIN ".$cat->{TABLE}." AS c ON(c.c_id = pl.cat_id) WHERE p.p_id = '".$id."' LIMIT 1;";
	my $result = $self->query($query);
	return $result->[0] if($result && ref $result eq 'ARRAY');
	
}

sub getPrivateGroups {
	
	my $self = shift;
	my $id = shift;
	my $brand = shift;
	
	my $select="";
	my $result = $self->query("SELECT * FROM catalog_alright WHERE c_pid ='".$id."'");
	if ($result){
		my $i = 0;
		foreach my $item(@$result){
			my $res = $self->query("SELECT * FROM catalog_alright WHERE c_pid ='".$item->{'c_id'}."' ORDER BY c_id ASC");
			if ($res){
				$select .= '<option value="'.$item->{'c_id'}.'" style="font-weight:bold; color:#bb418c" disabled>'.$item->{'c_name'}.'</option>';
				foreach my $line(@$res){
					$select .= '<option value="'.$line->{'c_id'}.'">&nbsp; &nbsp; — '.$line->{'c_name'}.'</option>';
				}
			}
			else {
				$select .= '<option value="'.$item->{'c_id'}.'" style="font-weight:bold; color:#bb418c">'.$item->{'c_name'}.'</option>';
			}
		}
	}
	$select = '<option value="0" selected>Выберите раздел</option>'.$select;
	
	return $select;
}

sub getPrivateProducts {
	
	my $self = shift;
	my $id = shift;
	my $brand = shift;
	my $params = shift;
	my $group_id = shift;
	
	my %group = ();
	if ($group_id > 0){
		my $result = $self->query("SELECT * FROM users_group_category WHERE group_id = '".$group_id."'");
		if ($result){
			foreach my $item(@$result){
				%group = (%group,
					$item->{'cat_id'} => $item->{'type'}
				);
			}
		}
	}
	
	my $products=""; my $result="";
	
	if ($params eq "search"){
	
		use Lingua::Stem2::Ru;
		use URI::Escape;
		
		my $q = stemmer(uri_unescape($id));
		
		$result = $self->query("SELECT * FROM products_alright WHERE p_art LIKE '%".$q."%'");
		if (!$result){
			$result = $self->query("SELECT * FROM products_alright WHERE p_name LIKE '%".$q."%'");
		}
	}
	elsif ($params eq "related"){
	
		$result = $self->query("SELECT * FROM products_alright WHERE p_art IN (".$id.")");
	}	
	else {
		$result = $self->query("SELECT * FROM products_alright WHERE cat_id ='".$id."'");
	}
	if ($result){
		my %category = ();
		foreach my $item(@$result){
			my $i = 0; my $colors="";
			my $color = $item->{'p_color'}."|";
			while ($color =~ m/(.+?)\|/g) {
				$i++;
				my $title="";
				if ($1 eq "blue"){$title = "Синий";}
				elsif ($1 eq "cool_white"){$title = "Холодный белый";}
				elsif ($1 eq "day_white"){$title = "Дневной белый";}
				elsif ($1 eq "green"){$title = "Зеленый";}
				elsif ($1 eq "green_yellow"){$title = "Зеленый (желт. отт.)";}
				elsif ($1 eq "ir850"){$title = "Алюминевый";}
				elsif ($1 eq "orange"){$title = "Оранжевый";}
				elsif ($1 eq "pink"){$title = "Розовый";}
				elsif ($1 eq "red"){$title = "Красный";}
				elsif ($1 eq "violet"){$title = "Фиолетовый";}
				elsif ($1 eq "warm_white"){$title = "Теплый белый";}
				elsif ($1 eq "white"){$title = "Белый";}
				elsif ($1 eq "yellow"){$title = "Желтый";}
				
				$colors .='<ins'.($title?' title="'.$title.'"':'').' class="'.$1.'">&nbsp;</ins>';
			}
			if ($colors){
				$colors = '<label class="color'.($i eq "1"?' one':'').''.($i eq "2"?' two':'').''.($i eq "3"?' three':'').'">'.$colors.'</label>';
			}
			
			my $pack = "Норма упак.";
			if ($item->{'p_pack'}){
				$pack = $item->{'p_pack'};
			}	

			my $desc = $item->{'p_desc'};
			my $string = length($item->{'p_desc'});
			if ($string > 150){
				$desc = substr($item->{'p_desc'}, 0, 150); $desc = $desc.'...';
			}
			
			my $res_art="";
			if ($desc){
				$res_art = $self->query("SELECT p_art FROM cat_product WHERE p_art ='".$item->{'p_art'}."'");
				if ($res_art){
					$desc .= ' <a target="_blank" href="/products/'.$item->{'p_art'}.'">Подробнее</a>';
				}
			}		

			my $price = $item->{'p_price'};
			
			if ($group_id > 0){
				if (!$category{$item->{'cat_id'}}){
					my $group_price = getPrivateGroupPrice($self, $item->{'cat_id'}, \%group);
					if ($group_price){
						if ($group_price eq "opt_small"){
							$price = $item->{'p_price_opt'};
							%category = (%category, $item->{'cat_id'} => "opt_small");
						}
						elsif ($group_price eq "opt_large"){
							$price = $item->{'p_price_opt_large'};
							%category = (%category, $item->{'cat_id'} => "opt_large");
						}
					}
				}
				elsif ($category{$item->{'cat_id'}}){
					if ($category{$item->{'cat_id'}} eq "opt_small"){
						$price = $item->{'p_price_opt'};
					}
					elsif ($category{$item->{'cat_id'}} eq "opt_large"){
						$price = $item->{'p_price_opt_large'};
					}
				}
			}
			
			$products .= '
				<tr data-art="'.$item->{'p_art'}.'" data-price="'.$price.'"'.($params eq "related"?' class="related"':'').'>
					<td class="art">'.$item->{'p_art'}.'</td>								
					<td class="img">'.($res_art?'<a target="_blank" href="/products/'.$item->{'p_art'}.'"><img src="/files/catalog/'.$item->{'p_art'}.'.jpg" onerror="this.src=\'/admin/site/img/no_photo.png\'; this.setAttribute(\'id\', \'empty\')"></a>':'<img src="/files/catalog/'.$item->{'p_art'}.'.jpg" onerror="this.src=\'/admin/site/img/no_photo.png\'; this.setAttribute(\'id\', \'empty\')">').'</td>
					<td class="name">'.($res_art?'<a target="_blank" href="/products/'.$item->{'p_art'}.'">'.$item->{'p_name'}.'</a>':$item->{'p_name'}).'</td>
					<td class="color">'.$colors.'</td>
					<td class="price">'.$price.'</td>
					<td class="count">
						<div class="p-count">
							<input class="count" name="'.$item->{'p_art'}.'" value="'.($item->{'p_packnorm'}?$item->{'p_packnorm'}:'1').'" data-value="'.($item->{'p_packnorm'}?$item->{'p_packnorm'}:'1').'" autocomplete="off">
							<i title="Добавить к заказу" class="fa fa-shopping-cart basket"></i>
							'.($item->{'p_packnorm'} > 0?'<em>'.$pack.' '.$item->{'p_packnorm'}.' '.$item->{'p_unit'}.'</em>':'').'
						</div>
					</td>
					<td class="unit">'.$item->{'p_unit'}.'</td>';
			
			my $related = $item->{'p_related'};
			if ($related){
				$related =~ s/\s/, /g;
				$related =~ s/,\s$//g;
				$related =~ s/,,/,/g;
			}
			
			$products .= '
					<td class="stock">'.getProductStock($item->{'p_stock'}, $item->{'p_waiting'}, $item->{'p_possible'}).'</td>
					<td class="desc">'.$desc.''.($params ne "related" && $related?'&nbsp; <a class="related" href="#" data-related="'.$related.'">Сопутствующие товары</a>':'').'</td>
				</tr>';
		}
		return $products;
	}
}

sub getPrivateGroupPrice {

	my $self = shift;
	my $id = shift;
	my $group_ = shift;
	
	my %group = ();
	while (my($key,$value) = each(%{$group_})){
		%group = (%group, $key => $value);
	}	
	
	my $result="";
	if ($group{$id} eq "opt_small"){$result = "opt_small";}
	elsif ($group{$id} eq "opt_large"){$result = "opt_large";}
	else {
		my $cat_id="";
		my $res_ = $self->query("SELECT c_pid FROM catalog_alright WHERE c_id ='".$id."'");
		my $res = $self->query("SELECT c_id, c_pid FROM catalog_alright WHERE c_id ='".$res_->[0]->{"c_pid"}."'");
		if ($res){
			foreach my $item(@$res){
				if ($group{$item->{'c_id'}} eq "opt_small"){$result = "opt_small"; last;}
				elsif ($group{$item->{'c_id'}} eq "opt_large"){$result = "opt_large"; last;}
				else {
					if ($group{$item->{'c_pid'}} eq "opt_small"){$result = "opt_small"; last;}
					elsif ($group{$item->{'c_pid'}} eq "opt_large"){$result = "opt_large"; last;}				
				}
			}
		}
	}
	if (!$result){
		return 0;
	}
	else {
		return $result;
	}
}

sub getPrivateBasket {

	my $self = shift;
	my $ids = shift;

	if (!$ids){
		use CGI::Session;
		my $session = CGI::Session->load( ) or die CGI::Session->errstr();				
		$ids = $session->param('ids');
	}
	
	my %idTS; my $basket=""; my $product_orders=""; my $counts = 0; my $totalcena = 0;
	
	if ($ids){
		while($ids =~ m/\|(\d+)[=]*(\d+[.]\d+)*/g){
			$idTS{$1}{'cena'} = $2;
			if (!$idTS{$1}{'price'}){
				$idTS{$1}{'price'} = $2;
			}
			if ($idTS{$1}{'count'}){
				$idTS{$1}{'count'}++;
				$idTS{$1}{'cena'} = $2*$idTS{$1}{'count'};
			}
			else {
				$counts++;
				$idTS{$1}{'count'} = 1;
			}
		}
		
		while (my ($key, $value) = each(%idTS)){
			my $result = $self->query("SELECT p_name, p_stock, p_waiting, p_possible FROM products_alright WHERE p_art ='".$key."'");
			if (!$result){
				$result = $self->query("SELECT * FROM cat_product WHERE p_art ='".$key."'");
			}
			if ($result){
				foreach my $item(@$result){
					$product_orders .='
						<tr data-art="'.$key.'" data-price="'.$value->{'price'}.'">
							<td class="name"><strong>'.$key.'</strong> '.$item->{'p_name'}.'</td>
							<td><input class="count" type="text" value="'.$value->{'count'}.'" data-value="'.$value->{'count'}.'"></td>
							<td class="stock">'.getProductStock($item->{'p_stock'}, $item->{'p_waiting'}, $item->{'p_possible'}).'</td>
							<td class="price">'.priceSpace($value->{'price'}).'</td>
							<td class="cena">'.priceSpace($value->{'cena'}).'</td>
							<td><i class="fa fa-remove delete"></i></td>
						</tr>';
				}
			}
		}					
		while (my ($key, $value) = each(%idTS)){
			 $totalcena += $value->{'cena'};
		}					
	}
	
	if ($product_orders){
	
		$totalcena = priceSpace($totalcena);
		
		my $word = "позиции";
		if ($counts == 1){$word = "позиция";}
		elsif ($counts > 4){$word = "позиций";}
	
		$basket = '<div id="private-basket">
			<a href="/basket/">
				<i class="fa fa-shopping-cart"></i><span>Оформить заказ <strong><em id="basket_counts">'.$counts.'</em> '.$word.'</strong></span>
			</a>
			<div class="container">
				<table>
					<thead>
						<th class="name">Наименование</th>
						<th>Заказ</th>
						<th>Склад</th>
						<th>Цена</th>
						<th>Итого</th>
						<th></th>
					</thead>
					<tbody>
						'.$product_orders.'					
					</tbody>
				</table>
				<div class="total">Итого: <strong><span id="total_price">'.$totalcena.'</span> руб.</strong></div>
				<p>Отгрузка производится только упаковками.<br> Возможна доставка в Ваш регион.</p>
			</div>
		</div>';
	}
	else {
		$basket ='<div id="private-basket" class="disabled">
				<a><i class="fa fa-shopping-cart"></i><span>Корзина заказа пустая</span></a>
			</div>';
	}

	return $basket;
}

sub getProductStock {

	my $stock = shift;
	my $waiting = shift;
	my $possible = shift;

	my $result="";
	if ($stock eq "0" or $stock eq ""){
		if ($waiting eq "-1" or $possible eq "-1"){
			$result = '<i title="Ожидается поступление" class="fa fa-history"></i>';
		}
		elsif ($waiting eq "0" or $waiting eq ""){
			$result = '<span>под заказ</span>';
		}							
	}						
	else {
		$result = $stock;
	}
	return $result;
}

sub priceSpace {

	my $string = shift;
	
	if ($string > 0){
		$string =~ s/(\d)(?=((\d{3})+)(\D|$))/$1 /g;
		return $string;
	}
}

sub stemmer {
	my $query = shift;
	if ($query){
		my @words = split / /, $query;
		my $result="";
		foreach my $item(@words){
			$result .= stem_word($item)." ";
		}
		$result =~s/\s$//g;
		$result =~s/\s/\%/gi;
		return $result;
	}
}

sub lamp_on_product {
	my $self = shift;
	my $id = shift;
	$self->update("UPDATE `".$self->{TABLE}."` SET `p_show`='1' WHERE p_id='".$id."'");
}

sub lamp_off_product {
	my $self = shift;
	my $id = shift;
	$self->update("UPDATE `".$self->{TABLE}."` SET `p_show`='0' WHERE p_id='".$id."'");
}

1;