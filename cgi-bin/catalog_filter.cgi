#!/usr/bin/perl
BEGIN {push (@INC, 'admin/engine/lib');} 

use CGI qw/:standard/;
use CGI::Carp qw (fatalsToBrowser);
use POSIX qw(locale_h);
require "templates/connection/require.cgi";
use CGI::FastTemplate; 
use Core::Config;
use Core::DB;
use Core::DB::Work;

$cid=param('cid');
$c_ids=param('ids');
$gid=param('gid');
$price_from=param('price_from');
$price_to=param('price_to');
$find_parent=param('find_parent');
$adm_act = "catalog";

my $db = new Core::DB();

print header( -charset=>'windows-1251');

if ($cid && $c_ids && $gid){

	if (!$find_parent){
		$c_ids = $cid;
	}	

	$parent_cid = findParentCat($cid);
	my $result = $db->query("SELECT c_name, c_name_short FROM cat_category WHERE c_id = '".$parent_cid."';");
	my $cat_name = $result->[0]->{'c_name_short'}." ";
	
	my $titles .= $result->[0]->{'c_name'}.", ";
	my $proizvoditel_1 = param('proizvoditel_1');
	my $proizvoditel_2 = param('proizvoditel_2');
	if ($proizvoditel_1) {$titles .= "производитель Alright, ";}
	if ($proizvoditel_2) {$titles .= "производитель Geniled, ";}
	
	my $p_ids=""; my $query="";
	if ($ENV{'QUERY_STRING'} =~/f_/){
		$query = getParams(); my %params; my $fields="";
		while (my($alias,$ids) = each(%{$query})){
			my $res = $db->query("SELECT field FROM cat_product_filters WHERE f_alias = '".$alias."' AND gid = '".$gid."'");
			my $field = $res->[0]->{'field'};
			my $field_ = $field;
			$field_ =~ s/,.+$//g;
			$titles .= Core::DB::Work::lowerString($field_)." ";
			my $param=""; my $values="";
			$ids = $ids.",";
			while ($ids =~ m/(\d+),/g) {
				my $result = $db->query("SELECT field FROM cat_product_filters WHERE filter_id = '".$1."'");
				foreach my $line(@$result){
					$param .= $line->{'field'}."|";
					$titles .= $line->{'field'}.", ";
					$values .= $line->{'field'}." ";
				}
			}
			$fields .= "'".$field."',";
			%params = (%params, $field => $param);			
			$cat_name .= $values;
		}
		
		$fields =~ s/,$//g;
		
		my %product=(); my $count = keys(%params); my %buffer=(); my $p_id="";
		my $result = $db->query("SELECT p.p_id, p.p_alias, f.field, f.value FROM cat_product AS p JOIN cat_product_rel AS r ON(r.cat_p_id=p.p_id) JOIN cat_product_fields AS f ON(f.p_id=p.p_id) WHERE r.cat_id IN (".$c_ids.") AND p.p_show = '1' AND f.field IN (".$fields.") ".($proizvoditel_1 eq "on" && !$proizvoditel_2?" AND p.p_supplier = '1'":"")."".($proizvoditel_2 eq "on" && !$proizvoditel_1?" AND p.p_supplier = '2'":"")." ORDER BY p.p_id ASC");
		foreach my $line(@$result){
			if ($p_id ne $line->{'p_id'}){%buffer=();}
			if (!$product{$line->{'p_id'}} && !$buffer{$line->{'field'}}){
				while ($params{$line->{'field'}} =~ m/(.+?)\|/g) {
					if ($line->{'value'} eq $1){
						%buffer = (%buffer, $line->{'field'});
					}
				}
				if (keys(%buffer) eq $count){
					$p_ids .= $line->{'p_id'}.",";
					%product = (%product, $line->{'p_id'});
					%buffer=();
				}				
			}
			$p_id = $line->{'p_id'};
		}
	}
	else {
		my %product=();
		my $result = $db->query("SELECT p.p_id FROM cat_product AS p JOIN cat_product_rel AS r ON(r.cat_p_id=p.p_id) WHERE r.cat_id IN (".$c_ids.") AND p.p_show = '1' ".($proizvoditel_1 eq "on" && !$proizvoditel_2?" AND p.p_supplier = '1'":"")."".($proizvoditel_2 eq "on" && !$proizvoditel_1?" AND p.p_supplier = '2'":"")."");
		foreach my $line(@$result){
			if (!$product{$line->{'p_id'}}){
				$p_ids .= $line->{'p_id'}.",";
				%product = (%product, $line->{'p_id'});
			}
		}
	}
	
	# Фильтр по цвету
	if (param('color') && $p_ids){
		$p_ids =~ s/,$//g; my $p_id=""; my $num="";
		my $color = param('color')."|"; my $p_ids_color="";
		my $count=""; my $c1=""; my $c2=""; my $c3="";
		my $color1=""; my $color2=""; my $color3="";
		while ($color =~ m/(.+?)\|/g) {
			$count++;
			if ($count eq "1"){$c1 = $1;}
			elsif ($count eq "2"){$c2 = $1;}
			elsif ($count eq "3"){$c3 = $1;}
		}
		if ($c1 && $c2 && $c3){$titles .= "цвет RGB, "; $cat_name .= "RGB ";}
		else {$titles .= "цвет ".$c1.", "; $cat_name .= getColorRus($c1, "short")." ";}
		my $result = $db->query("SELECT p.p_id, f.field, f.value FROM cat_product AS p JOIN cat_product_fields AS f ON(f.p_id=p.p_id) WHERE p.p_id IN (".$p_ids.") AND f.field IN ('Цвет 1', 'Цвет 2', 'Цвет 3') ORDER BY p.p_id ASC");
		my $counts = @$result;
		foreach my $line(@$result){
			$num++;
			if ($p_id ne $line->{'p_id'} && $num ne "1" or $counts eq $num){
				if ($counts eq $num){$p_id = $line->{'p_id'};}
				if ($c1 eq $color1 && $c2 eq $color2 && $c3 eq $color3){
					$p_ids_color .= $p_id.",";	
					
				}
				$color1=""; $color2=""; $color3="";
			}
			if ($line->{'field'} eq "Цвет 1"){$color1 = $line->{'value'};}
			elsif ($line->{'field'} eq "Цвет 2"){$color2 = $line->{'value'};}
			elsif ($line->{'field'} eq "Цвет 3"){$color3 = $line->{'value'};}
			
			$p_id = $line->{'p_id'};
		}
		$p_ids = $p_ids_color;
	}	
	
	if ($p_ids){
	
		my $limit_count="";
		open(BO, "$dirs_catalog_www2/page_settings.txt"); my @pages_count = <BO>; close(BO);
		foreach my $line(@pages_count){chomp($line);
		my ($pages_admin, $pages_site) = split(/\|/, $line);
		$limit_count=qq~$pages_site~;}	
	
		my $products=""; $p_ids =~ s/,$//g; my $count=""; my $counts=""; my $i="";
		my $result = $db->query("SELECT * FROM cat_product WHERE p_id IN (".$p_ids.") AND p_price > ".($price_from-1)." AND p_price < ".($price_to+1)." ORDER BY p_price ASC");
		$p_ids="";
		if ($result){
			foreach my $line(@$result){
				$count++; $i++; my $mark="";
				if ($line->{'p_news'} eq "1"){$mark="new";}
				if ($line->{'p_hit'} eq "1"){$mark="hit";}
				if ($line->{'p_spec'} eq "1"){$mark="spec";}
				my $label = 0;
				if ($count == 3) {$label = "reflect"; $count="";}
				if ($i < ($limit_count+1)){
					$products .= build_TemplateProduct($line->{'p_id'}, $line->{'p_art'}, $line->{'p_name'}, $line->{'p_alias'}, "", $line->{'p_price'}, $line->{'p_price_old'}, $line->{'p_desc_sm'}, 0, $label, $mark, $line->{'p_raiting'}, $line->{'p_raiting_count'}, "catalog", $line->{'p_img_url'}, $cat_name, $parent_cid, "", "", $line->{'p_color_rel'});
				}
				else {
					$counts++;
					$p_ids .= $line->{'p_id'}.",";
				}
			}
			my $more_products="";
			if ($counts > 0){
				$p_ids =~ s/,$//g;
				$more_products = '<div class="more_products" data-limit="'.($limit_count*2).'" data-ids="'.$p_ids.'">Показать еще товары (<span>'.$counts.'</span>)</div>';
			}
			$cat_name =~ s/\s$//g;
			$name = '<div class="title"><h1>'.$cat_name.'</h1>
					<div class="filter-views">
						<ul>
							<li class="list'.(cookie("view_products") ne "table"?' active':'').'"><a href="#">list</a></li>
							<li class="table'.(cookie("view_products") eq "table"?' active':'').'"><a href="#">table</a></li>
						</ul>
						<span>Найдено: <strong>'.scalar @$result.'</strong></span>
					</div>
				</div>';		
			$content .= build_ProductTags(1,0,"catalog").''.$products.''.build_ProductTags(0,1,"catalog").$more_products;		
			$products_filter = filterProducts($cid, $gid, \%{$query});
		}
		else {
			$name = '<div class="title"><h1>'.$cat_name.'</h1></div>';
			$content .= '<div class="no_result"><p>Товаров нет удовлетворяющих параметрам фильтра, попробуйте поменять параметры поиска.</p></div>';
			$products_filter = filterProducts($cid, $gid, \%{$query});
		}
	}
	else {
		$name = '<div class="title"><h1>'.$cat_name.'</h1></div>';
		if ($find_parent){	
			$content .= '<div class="no_result"><p>Товаров нет удовлетворяющих параметрам фильтра, попробуйте поменять параметры поиска.</p></div>';
		}
		else {
			$content .= '<div class="no_result"><p>Товары не найдены, попробуйте <a href="/catalog/filter/?'.$ENV{'QUERY_STRING'}.'&find_parent=on">поискать</a> во всем разделе.</p></div>';
		}
		$products_filter = filterProducts($cid, $gid, \%{$query});
	}
	$titles =~ s/,\s$//g;
	$title = $titles;
}
else {
	$name = '<div class="title"><h1>Пустой запрос</h1></div>';
	$content = '<div class="no_result"><p>Не заданы параметры поиска.</p></div>';
	if ($cid){
		$products_filter = filterProducts($cid);	
	}
}

$catalog_submenu = build_CatalogSubMenu($cid, $parent_cid);

require "templates/connection/variables.cgi";

$tpl = new CGI::FastTemplate("admin/$dirs/"); 
	$tpl->define( index     => "maket_html.$maket_catalog",
);

require "templates/connection/variables_assign.cgi";

$tpl->parse(MAIN => "index");
$tpl->print();


sub getParams {
	
	my (%query, $a, $ids, $q_sz, $i, $qtext, @q, @cmd);
	$qtext = $ENV{'QUERY_STRING'};
	@q    = split("&", $qtext);
	$q_sz = scalar(@q);

	for ($i=0; $i<$q_sz; $i++) {
		@cmd = split("=", $q[$i]);
		$cmd[1] =~ s/\+/ /g;
		$cmd[1] =~ s/%([0-9A-Fa-f]{2})/chr(hex($1))/eg;
		my $alias=""; my $id="";
		#if ($cmd[0] ne "cid" && $cmd[0] ne "gid" && $cmd[0] ne "ids" && $cmd[0] ne "price_from" && $cmd[0] ne "price_to" && $cmd[0] ne "find_parent" && $cmd[0] ne "color"){		
		if ($cmd[0] =~ /f_/){
			my $p = $cmd[0]; $p =~ s/%5B/[/g; $p =~ s/%5D/]/g;
			while ($p =~ m/f_(.+?)\[(\d+)\]/g) {
				$alias = $1; $id = $2;
			}
			if ($query{$alias}){
				my $ids = $query{$alias}.",".$id;
				%query = (%query, $alias => $ids);
			}
			else {
				%query = (%query, $alias => $id);
			}
		}
	}	
	return \%query;
}
