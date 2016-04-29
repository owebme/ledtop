use Core::DB::Catalog;
use Core::DB::Work;

my $catalog = new Core::DB::Catalog();
my $db = new Core::DB();

my $edit_group = param("edit");

if (cookie("private_enter") ne "true"){

	print '<script type="text/javascript">
		<!--
		location.replace("http://'.$ENV{"HTTP_HOST"}.'/cgi-bin/admin/engine/index.cgi?adm_act=clients");
		//-->
		</script>
		<noscript>
		<meta http-equiv="refresh" content="0; url=http://'.$ENV{"HTTP_HOST"}.'/cgi-bin/admin/engine/index.cgi?adm_act=clients">
		</noscript>';

}

$new_pages =qq~<li class="first activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients"><span>Наши клиенты</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=new"><span>Новые заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=1"><span>Выполненные заказы</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=2"><span>Корзина заказов</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=orders&status=3"><span>Перезвонить</span></a></li>~;
	
$content_html=qq~$content_html<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
			<div id="tabs" style="width:960px;">
				<ul>
					$new_pages
				</ul>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content" style="position:relative">
		<link rel="stylesheet" type="text/css" href="/admin/css/bootstrap/bootstrap.min.css" />~;
	
	$content_html .='	
		<div id="pages" class="clients">
<script type="text/javascript" src="/admin/lib/clients_group.js"></script>
		<div class="btn-group left">
			<a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients" class="btn">Все клиенты</a>
			<a href="/cgi-bin/admin/engine/index.cgi?adm_act=clients_group" class="btn active">Группы клиентов</a>
		</div>';
		
	my $groups=""; my $group_name=""; my $group1=""; my $group2=""; my %hash = (); 
	my $result = $db->query("SELECT * FROM users_group ORDER BY g_id ASC");
	if ($result){
		foreach my $group(@$result){
			$groups .= '<a href="?adm_act=clients_group&edit='.$group->{'g_id'}.'" class="a-button'.($edit_group eq $group->{'g_id'}?' active':' not-active').'">'.$group->{'g_name'}.'</a>';
			if ($edit_group eq $group->{'g_id'}){
				$group_name = $group->{'g_name'};
			}
		}
	}
	if ($edit_group > 0){
		my $result = $db->query("SELECT * FROM users_group_category WHERE group_id = '".$edit_group."' ORDER BY cat_id ASC");
		if ($result){
			foreach my $item(@$result){
				if ($item->{'type'} eq "opt_small"){
					my $res = $db->query("SELECT c_name FROM catalog_alright WHERE c_id = '".$item->{'cat_id'}."'");
					if ($res->[0]->{"c_name"}){
						$group1 .='<em data-id="'.$item->{'cat_id'}.'">'.$res->[0]->{"c_name"}.'</em>';
					}
				}
				elsif ($item->{'type'} eq "opt_large"){
					my $res = $db->query("SELECT c_name FROM catalog_alright WHERE c_id = '".$item->{'cat_id'}."'");
					if ($res->[0]->{"c_name"}){
						$group2 .='<em data-id="'.$item->{'cat_id'}.'">'.$res->[0]->{"c_name"}.'</em>';
					}
				}				
				%hash = (%hash,
					$item->{'cat_id'} => $item->{'group_id'}
				);
			}
		}
	}
	
	my $category="";
	if ($edit_group){
		my $result = $db->query("SELECT c_id, c_name FROM catalog_alright WHERE c_pid = '0' ORDER BY c_id ASC");
		foreach my $item(@$result){
			$category .= '<li class="parent subCat'.($hash{$item->{c_id}}?' hide':'').'" data-id="'.$item->{c_id}.'"><button class="a-button a-button-little plus">+</button><em data-id="'.$item->{c_id}.'">'.$item->{c_name}.'</em></li>';
			if (my $sub = recMenuCategory($item->{c_id}, 0) ){
				$category .= $sub;
			}
		}
	}
	sub recMenuCategory {
		my $id = shift;
		my $level = shift;
		my $result = $db->query("SELECT c_id, c_name FROM catalog_alright WHERE c_pid = '".$id."' ORDER BY c_id ASC");
		my $text = '<ul class="level'.($level+1).'">';
		if ($result){
			foreach my $item(@$result){
				if (my $sub = recMenuCategory($item->{c_id}, $level)){
					$text .= '<li class="subCat'.($hash{$item->{c_id}}?' hide':'').'" data-id="'.$item->{c_id}.'"><button class="a-button a-button-little plus">+</button><em data-id="'.$item->{c_id}.'">'.$item->{c_name}.'</em></li>';
					$text .= $sub;
				}
				else {
					$text .= '<li'.($hash{$item->{c_id}}?' class="hide"':'').' data-id="'.$item->{c_id}.'"><em data-id="'.$item->{c_id}.'">'.$item->{c_name}.'</em></li>';
				}
			}
		}
		else {
			return 0;
		}
		$text .= '</ul>';
		return $text;
	}
	if ($category){
		$category ='<ul id="category">'.$category.'</ul>';
	} 	
	
	$content_html .='<div id="clients-group">
		<div class="tab-left">
			'.($edit_group?'<input id="group-name" class="normal" type="text" value="'.$group_name.'" placeholder="Введите название группы">':'<a href="?adm_act=clients_group&edit=new" class="a-button light"><span>Создать новую группу</span></a>').'
			<div class="groups">
				'.$groups.'
			</div>
			'.($edit_group?'<div class="category">'.$category.'</div>':'').'
		</div>
		<div class="tab-right">';
		
	if ($edit_group){
		$content_html .='
			<div class="save-group">
				<button id="save-group" class="a-button light"><span>Сохранить группу</span></button>
			</div>
			<div class="tab-groups">
				<div class="tab tab1">
					<h4>Мелкий опт</h4>
					<ul class="container">	
						'.$group1.'
					</ul>
				</div>
				<div class="tab tab2">
					<h4>Крупный опт</h4>
					<ul class="container">	
						'.$group2.'
					</ul>					
				</div>				
			</div>';
	}
	
	$content_html .='		
		</div>
	</div>';

$content_html.= qq~
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;


-1;