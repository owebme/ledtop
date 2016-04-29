my $db = new Core::DB();


# Страницы сайта (только верхний уровень)

sub build_PagesMenu
{
	my $sort = shift;
	my $pages_menu = "";
	$pages_menu .= '<ul class="pages_menu">';	
	$result = $db->query("SELECT * FROM strukture WHERE parent = '0' ORDER BY $sort");
	foreach my $line(@$result){
		if ($line->{'show_menu'} ne "0" && $line->{'mirror_id'} ne "#!"){
			my $alias=""; my $active;
			if ($line->{'id'} eq "1"){$alias = "/";} else {$alias = "/pages/".$line->{alias};}
			if ($line->{'mirror_link'} ne ""){
				$alias = $line->{'mirror_link'};
				if ($adm_act eq "news" && $line->{'mirror_link'} eq "/news/"){$active = 'class="active"';}
				elsif ($adm_act eq "articles" && $line->{'mirror_link'} eq "/public/"){$active = 'class="active"';}
				elsif ($adm_act eq "gallery" && $line->{'mirror_link'} eq "/gallery/"){$active = 'class="active"';}
				elsif ($adm_act eq "catalog" && $line->{'mirror_link'} eq "/catalog/"){$active = 'class="active"';}
				elsif ($adm_act eq "poleznoe" && $line->{'mirror_link'} eq "/poleznoe/"){$active = 'class="active"';}
				elsif ($adm_act eq "pages" && $line->{'mirror_link'} ne ""){
					my $id = $line->{'mirror_id'};
					$id =~ s/\?adm_act=strukture&num_edit=//g;
					if ($num_edit ne "" && $num_edit==$id){$active = 'class="active"';}
				}
			}
			elsif ($adm_act eq "pages" && $num_edit==$line->{id}) {$active = 'class="active"';}			
			
			$pages_menu .= "<li><a ".$active." href='".($line->{'mirror_link'} ne ""?"".$line->{'mirror_link'}."":"".$alias."")."'>".$line->{'name'}."</a></li>\n";			
		} else {$pages_menu .="";}
	}
	$pages_menu .= '</ul>';	
    return $pages_menu;
}


# Страницы сайта (только верхний уровень)

my $limit_pages = 5; # кол-во отображаемых

sub build_PagesMenuLimit
{
	my $sort = shift;
	my $pages_menu = ""; my $count="";
	my $result = $db->query("SELECT * FROM strukture WHERE parent = '0' ORDER BY $sort");
	foreach my $line(@$result){
		if ($line->{'show_menu'} ne "0" && $line->{'mirror_id'} ne "#!"){
			$count++;
			if ($count <= $limit_pages){
				my $alias=""; my $active;
				if ($line->{'id'} eq "1"){$alias = "/";} else {$alias = "/pages/".$line->{alias};}
				if ($line->{'mirror_link'} ne ""){
					$alias = $line->{'mirror_link'};
					if ($adm_act eq "news" && $line->{'mirror_link'} eq "/news/"){$active = 'class="active"';}
					elsif ($adm_act eq "articles" && $line->{'mirror_link'} eq "/public/"){$active = 'class="active"';}
					elsif ($adm_act eq "gallery" && $line->{'mirror_link'} eq "/gallery/"){$active = 'class="active"';}
					elsif ($adm_act eq "catalog" && $line->{'mirror_link'} eq "/catalog/"){$active = 'class="active"';}
					elsif ($adm_act eq "poleznoe" && $line->{'mirror_link'} eq "/poleznoe/"){$active = 'class="active"';}
					elsif ($adm_act eq "pages" && $line->{'mirror_link'} ne ""){
						my $id = $line->{'mirror_id'};
						$id =~ s/\?adm_act=strukture&num_edit=//g;
						if ($num_edit ne "" && $num_edit==$id){$active = ' class="active"';}
					}
				}
				elsif ($adm_act eq "pages" && $num_edit==$line->{id}) {$active = ' class="active"';}	
				if ($alias eq "/" && $num_edit eq "all") {$active = ' class="active"';}	
			
				$pages_menu .= "<li id='l".$count."' ".$active."><a href='".($line->{'mirror_link'} ne ""?"".$line->{'mirror_link'}."":"".$alias."")."'>".$line->{'name'}."</a></li>\n";
			}
		} else {$pages_menu .="";}
	}

    return $pages_menu;
}


# Вывод подразделов страницы

sub build_PagesSubMenu
{
	my $id = shift;
	my $name = shift;
	my $parent= shift;
	my $alias= shift;
	my $sort = shift;
	my $pages_submenu=""; my $submenu=""; my $my_id = $num_edit;
	if ($adm_act eq "pages"){
		my $res_child = $db->query("SELECT strukture.parent FROM strukture WHERE parent = '".$id."' LIMIT 1;");
		if (!$res_child){
			my $res_parent = $db->query("SELECT * FROM strukture WHERE id = '".$parent."' LIMIT 1;");
			if ($res_parent->[0]->{mirror_id} ne "#!" && $res_parent->[0]->{show} ne "0"){
				$id = $parent;
				$name = $res_parent->[0]->{name};
			}
			else {
				my $res_childs = $db->query("SELECT * FROM strukture WHERE mirror_link = '/pages/".$alias."' LIMIT 1;");
				if ($res_childs){
					$my_id = $res_childs->[0]->{id};
					my $res_parent = $db->query("SELECT * FROM strukture WHERE id = '".$res_childs->[0]->{parent}."' LIMIT 1;");
					if ($res_parent->[0]->{mirror_id} ne "#!" && $res_parent->[0]->{show} ne "0"){
						$id = $res_childs->[0]->{parent};
						$name = $res_parent->[0]->{name};
					}
				}
			}
		}	
		if ($res_child or $parent ne "0"){
			$pages_submenu .="<h2>".$name."</h2>";
			my $result = $db->query("SELECT * FROM strukture WHERE parent = '".$id."' ORDER BY $sort;");
			foreach my $line(@$result){	
				if ($line->{'mirror_id'} ne "#!" && $line->{'show'} ne "0" && $line->{'show_menu'} ne "0"){
					if ($adm_act eq "pages" && $my_id==$line->{id}){
						$submenu .="<li class='active'>&mdash; <span>".$line->{'name'}."</span></li>\n";
					}
					else {
					$submenu .="<li>&mdash; <a href='".($line->{'mirror_link'} ne ""?"".$line->{'mirror_link'}."":"/pages/".$line->{'alias'}."")."'>".$line->{'name'}."</a></li>\n";
					}
				}
			}
			if ($submenu ne ""){
				$pages_submenu .='<ul class="submenu">'.$submenu.'</ul>'; 
			}
		}
	}
	
	return $pages_submenu;
}


# Дерево страниц

my $limit_pages_tree = ""; # кол-во отображаемых (верхний уровень)

sub build_PagesTree
{
	my $sort = shift;
	my $tree = "";
	my $count="";
	my $point="";
	$tree .= '<ul class="pages_tree">';	
	my $result = $db->query("SELECT * FROM strukture WHERE parent = '0' ORDER BY $sort;");
	foreach my $item(@$result){
		if ($item->{show_menu} == 1) {
			my $subs ="";
			if( my $sub = recMenuPages($item->{id}, 0) ){
			$subs = $sub;
			}
			my $alias=""; my $class; $count++;
			if ($item->{'id'} eq "1"){$alias = "/";} else {$alias = "/pages/".$item->{alias};}
			if ($item->{'mirror_link'} ne ""){
				$alias = $item->{'mirror_link'};
				if ($adm_act eq "news" && $item->{'mirror_link'} eq "/news/"){$class = 'class="active"';}
				elsif ($adm_act eq "articles" && $line->{'mirror_link'} eq "/public/"){$active = 'class="active"';}
				elsif ($adm_act eq "gallery" && $item->{'mirror_link'} eq "/gallery/"){$class = 'class="active"';}
				elsif ($adm_act eq "catalog" && $line->{'mirror_link'} eq "/catalog/"){$active = 'class="active"';}
				elsif ($adm_act eq "poleznoe" && $line->{'mirror_link'} eq "/poleznoe/"){$active = 'class="active"';}
				elsif ($adm_act eq "pages" && $item->{'mirror_link'} ne ""){
					my $id = $item->{'mirror_id'};
					$id =~ s/\?adm_act=strukture&num_edit=//g;
					if ($num_edit ne "" && $num_edit==$id){$class = 'class="active"';}
				}
			}
			elsif ($adm_act eq "pages" && $num_edit==$item->{id}) {$class = 'class="active"';}
			if ($limit_pages_tree > 0 && $count <= $limit_pages_tree or $limit_pages_tree eq ""){
				$tree .= '<li>';			
				$tree .= '<a '.$class.' '.($subs ne "" && $item->{html} eq ""?'href="#"':'href="'.$alias.'"').'>'.$item->{name}.'</a>';
				$tree .= $subs;
				$tree .= '</li>';
			}
		}
		else {
			$tree .= '';
		}

	}
	
	sub recMenuPages{

		my $id = shift;
		my $level = shift;
		
			my $parent_id="";
			$result_parent = $db->query("SELECT * FROM strukture WHERE id='".$id."'");
			my $hide_child = ""; my $open="";
			my $show_child_count="";
			if($result_parent){
				foreach my $items(@$result_parent){
					$hide_child = $items->{hide_child};
					$show_child_count = $items->{show_child_count};
					$parent_id = $items->{parent};
				}
			}
			if ($hide_child == 0) {$hide_child="";}
			if ($hide_child == 1) {$hide_child="style='display:none;'"; $open="id='close'";}
			if ($adm_act eq "pages" && $num_edit == $id) {$hide_child=""; $open="id='open'";}
			if ($adm_act eq "pages" && $parent_sid == $id) {$hide_child=""; $open="id='open'";}
			if ($adm_act eq "pages" && $parent_id eq "0" && $point eq ""){
				my $res = $db->query("SELECT strukture.id, strukture.parent FROM strukture WHERE id='".$parent_sid."'");
				foreach my $line(@$res){
					my $result = $line->{id};
					if ($line->{parent} ne "0"){
						if (my $ids = recParentPages($line->{parent})){
							$result = $ids;
						}
					}
					if ($result == $id){$hide_child=""; $open="id='open'"; last;}
				}
				sub recParentPages {
					my $parent = shift;
					my $result="";
					my $res_parent = $db->query("SELECT strukture.id, strukture.parent FROM strukture WHERE id='".$parent."'");
					if ($res_parent){
						foreach my $line(@$res_parent){
							$result = $line->{id};
							if (my $ids = recParentPages($line->{parent})){
								$result = $ids;
							}
							if ($result == $id){$hide_child=""; $open="id='open'"; $point="end"; last;}
						}
					} else {
						return 0;
					}
					return $result;
				}
			}
			
		my $text = '<ul '.$hide_child.' '.$open.' class="level'.($level+1).'">';
		my $cat_level=$level+1;
		
		my $result = $db->query("SELECT * FROM strukture WHERE parent='".$id."' ORDER BY $sort");
		if($result){
			my $cat_more=""; my $i="";
			foreach my $item(@$result){
				if ($item->{show_menu} == 1) {				
					$i++;
					if ($show_child_count < $i && $show_child_count !=0) {
						if ($adm_act eq "pages" && $num_edit==$item->{id}) {

						my $subs ="";
						if( my $sub = recMenuPages($item->{id}, $level+1) ){
							$subs = $sub;
						}
						my $alias=""; my $class="";
						if ($item->{'mirror_link'} ne ""){
							$alias = $item->{'mirror_link'};
							if ($adm_act eq "news" && $item->{'mirror_link'} eq "/news/"){$class = 'class="active"';}
							elsif ($adm_act eq "articles" && $line->{'mirror_link'} eq "/public/"){$active = 'class="active"';}
							elsif ($adm_act eq "gallery" && $item->{'mirror_link'} eq "/gallery/"){$class = 'class="active"';}
							elsif ($adm_act eq "catalog" && $line->{'mirror_link'} eq "/catalog/"){$active = 'class="active"';}
							elsif ($adm_act eq "poleznoe" && $line->{'mirror_link'} eq "/poleznoe/"){$active = 'class="active"';}
							elsif ($adm_act eq "pages" && $item->{'mirror_link'} ne ""){
								my $id = $item->{'mirror_id'};
								$id =~ s/\?adm_act=strukture&num_edit=//g;
								if ($num_edit ne "" && $num_edit==$id){$class = 'class="active"';}
							}						
						}
						else {$alias = "/pages/".$item->{alias};}
						if ($adm_act eq "pages" && $num_edit==$item->{id}) {$class = 'class="active"';}						
						$text .= '<li>';
						$text .= '<a '.$class.' '.($subs ne "" && $item->{html} eq ""?'href="#"':'href="'.$alias.'"').'>'.$item->{name}.'</a>';

						$text .= $subs;
						$text .= '</li>';							
						
						} else {

						my $subs ="";
						if( my $sub = recMenuPages($item->{id}, $level+1) ){
							$subs = $sub;
						}
						my $alias=""; my $class="";
						if ($item->{'mirror_link'} ne ""){
							$alias = $item->{'mirror_link'};
							if ($adm_act eq "news" && $item->{'mirror_link'} eq "/news/"){$class = 'class="active"';}
							elsif ($adm_act eq "articles" && $line->{'mirror_link'} eq "/public/"){$active = 'class="active"';}
							elsif ($adm_act eq "gallery" && $item->{'mirror_link'} eq "/gallery/"){$class = 'class="active"';}
							elsif ($adm_act eq "catalog" && $line->{'mirror_link'} eq "/catalog/"){$active = 'class="active"';}
							elsif ($adm_act eq "poleznoe" && $line->{'mirror_link'} eq "/poleznoe/"){$active = 'class="active"';}
							elsif ($adm_act eq "pages" && $item->{'mirror_link'} ne ""){
								my $id = $item->{'mirror_id'};
								$id =~ s/\?adm_act=strukture&num_edit=//g;
								if ($num_edit ne "" && $num_edit==$id){$class = 'class="active"';}
							}						
						}
						else {$alias = "/pages/".$item->{alias};}
						if ($adm_act eq "pages" && $num_edit==$item->{id}) {$class = 'class="active"';}						
						$cat_more .= '<li>';
						$cat_more .= '<a '.$class.' '.($subs ne "" && $item->{html} eq ""?'href="#"':'href="'.$alias.'"').'>'.$item->{name}.'</a>';

						$cat_more .= $subs;
						$cat_more .= '</li>';						
						}
						
					} else {
						
						my $subs ="";
						if( my $sub = recMenuPages($item->{id}, $level+1) ){
							$subs = $sub;
						}
						my $alias=""; my $class="";
						if ($item->{'mirror_link'} ne ""){
							$alias = $item->{'mirror_link'};
							if ($adm_act eq "news" && $item->{'mirror_link'} eq "/news/"){$class = 'class="active"';}
							elsif ($adm_act eq "articles" && $line->{'mirror_link'} eq "/public/"){$active = 'class="active"';}
							elsif ($adm_act eq "gallery" && $item->{'mirror_link'} eq "/gallery/"){$class = 'class="active"';}
							elsif ($adm_act eq "catalog" && $line->{'mirror_link'} eq "/catalog/"){$active = 'class="active"';}
							elsif ($adm_act eq "poleznoe" && $line->{'mirror_link'} eq "/poleznoe/"){$active = 'class="active"';}
							elsif ($adm_act eq "pages" && $item->{'mirror_link'} ne ""){
								my $id = $item->{'mirror_id'};
								$id =~ s/\?adm_act=strukture&num_edit=//g;
								if ($num_edit ne "" && $num_edit==$id){$class = 'class="active"';}
							}						
						}
						else {$alias = "/pages/".$item->{alias};}
						if ($adm_act eq "pages" && $num_edit==$item->{id}) {$class = 'class="active"';}						
						$text .= '<li>';
						$text .= '<a '.$class.' '.($subs ne "" && $item->{html} eq ""?'href="#"':'href="'.$alias.'"').'>'.$item->{name}.'</a>';

						$text .= $subs;
						$text .= '</li>';
					}
				}
				else {
					$text .= '';
				}				

			}

			if ($show_child_count < $i && $show_child_count !=0) {$text .='<div class="more_cat" style="display:none;" id_more_cat="'.$id.'"><ul class="more_catalog">'.$cat_more.'</ul></div><div class="more"><a href="#" id_more="'.$id.'">Еще...</a></div>';}
			
		} else {
			return 0;
		}
		$text .= '</ul>'; 
		return $text;
	};
	$tree .= '</ul>';
	return $tree;
}

sub build_CalcDelivery {

	my ($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
	if ($mday < 10 ) {$mday ="0".$mday;}
	if ($hour < 10 ) {$hour ="0".$hour;}
	if ($min < 10 ) {$min ="0".$min;}
	if ($sec < 10 ) {$sec ="0".$sec;}
	$mon++; if ($mon < 10) {$mon ="0".$mon;}
	$year=1900+$year; 
	my $today="$year-$mon-$mday\T$hour:$min:$sec";

	use Digest::MD5 qw(md5_hex);

	my $authLogin = "84e481b64f9955ff19d1dcd7a33b720c";
	my $secure = md5_hex("$today&f6e83a2f6b273a1cbb168e1289ffd6a9");

	return '<div class="order-delivery section">
		<i></i>
		<strong>Воспользуйтесь расчетом доставки</strong>
		<form method="GET" id="formParamsDelivery" action="">
			<input name="senderCityId" value="44" autocomplate="off" type="hidden">
			<label><span>Город-получатель:</span><input id="cityDelivery" class="input-text" type="text" value="" placeholder="Начните вводить и выберите из списка" autocomplate="off"><a id="sendParamsDelivery" href="#">Рассчитать</a></label>
			<input id="receiverCityId" name="receiverCityId" value="" autocomplate="off" type="hidden">
			<input name="version" value="1.0" hidden />
			<input name="dateExecute" value="'.$today.'" hidden />
			<input name="authLogin" value="'.$authLogin.'" hidden />
			<input name="secure" value="'.$secure.'" hidden />		
			<input name="tariffId" value="137" hidden />
			<div class="result-block" style="display:block">
				<label><span>Вес места, кг.</span><input class="input-text" name="goods[0].weight" type="text" data-value="3" value="3" autocomplate="off"></label>
				<label><span>Длина места, см.</span><input class="input-text" name="goods[0].length" type="text" data-value="30" value="30" autocomplate="off"></label>
				<label><span>Ширина места, см.</span><input class="input-text" name="goods[0].width" type="text" data-value="30" value="30" autocomplate="off"></label>
				<label><span>Высота места, см.</span><input class="input-text" name="goods[0].height" type="text" data-value="30" value="30" autocomplate="off"></label>
				<div class="order-delivery-result">
				</div>
			</div>
		</form>
	</div>'
	
}

sub shareLinks {

	return '<div id="share-links">
				<div class="smaller">Поделиться:</div>
				<div class="social-likes social-likes_light">
					<div class="vkontakte" title="Поделиться ссылкой во Вконтакте">Вконтакте</div>
					<div class="facebook" title="Поделиться ссылкой в Facebook">Facebook</div>
					<div class="twitter" title="Поделиться ссылкой в Twitter">Twitter</div>
					<div class="plusone" title="Поделиться ссылкой в Google+">Google+</div>
				</div>
			</div>';
}

1;