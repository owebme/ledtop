use Core::DB::Pages;
use Core::DB::Work;

my $pages = new Core::DB::Pages();

	$menu_act=param('menu_act');
	$num_edit=param('num_edit');
	$posup=param('posup');
	$posdown=param('posdown');	
	$name=param('name');	
	$par=param('par');
	$settings=param('settings');	
	$lamp=param('lamp');

if ($num_edit eq "") {
$new_pages =qq~<li class="first activetab"><a id="click_pages" href="#"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>~;
} else {
$new_pages =qq~<li class="first activetab"><a id="click_pages" href="#"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>~;
}
if ($par) {
$new_pages =qq~<li class="first"><a id="click_pages" href="#"><span>Страницы сайта</span></a></li>
<li class="activetab"><a id="click_pages_new" href="#"><span>Новая страница</span></a></li>~;
}
if ($settings) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>~;
}

if ($hide_articles ne "1"){
	$new_pages .=qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=articles"><span>Статьи</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=articles&par=new"><span>Новая статья</span></a></li>~;
}
	
$content_html=qq~$content_html<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs">
				<ul>
					$new_pages
				</ul>
			</div>
			
			
			<div id="buttons">
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&settings=set" id="cstmz">Настроить модуль</a>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">
		<div id="pages">
<script type="text/javascript" src="/admin/lib/strukture.js"></script>~;	
	
	
if( param('posup') ne "" ){
	$pages->PosUp($num_edit);
	$num_edit="";
	$sel_option="";
	$sel_option_s="";
	$sel_option_html="";
	$list_older="";
}

if( param('posdown') ne "" ){
	$pages->PosDown($num_edit);
	$num_edit="";
	$sel_option="";
	$sel_option_s="";
	$sel_option_html="";
	$list_older="";	
}

if( $lamp eq "on" ){
	$pages->lamp_on($num_edit);
	$num_edit="";
	$sel_option="";
	$sel_option_s="";
	$sel_option_html="";
	$list_older="";	
}

if( $lamp eq "off" ){
	$pages->lamp_off($num_edit);
	$num_edit="";
	$sel_option="";
	$sel_option_s="";
	$sel_option_html="";
	$list_older="";	
}

	($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
	if ($mday < 10 ) { $mdays="0"; $mday="$mdays$mday";}
	$mon++; if ($mon < 10 ) { $mon="0$mon";}
	$year=1900+$year; 
	$today="$year-$mon-$mday";

	if ($menu_act eq "del"){
		$pages->del($num_edit);
		$content_html=qq~$content_html<div class="delete_page">Страница удалена.</div>~;
		$num_edit="";
		$sel_option="";
		$sel_option_s="";
		$sel_option_html="";
		$list_older="";		
		$menu_act="";
	}

	if ($menu_act eq "") {
		$list_older="";
		
		$result = $pages->query("SELECT * FROM strukture WHERE strukture.id = '".$num_edit."' LIMIT 1");
		
		if($result){
			foreach my $line(@$result){
				$ok_name_old = $line->{name};
				$ok_name_old=Core::DB::Work::trans_edit($ok_name_old);
				$ok_title_old = $line->{title};
				$ok_meta_desc_old = $line->{meta_desc};
				$ok_meta_key_old = $line->{meta_key};					
				$ok_alias_old = $line->{alias};
				$ok_redirect_old = $line->{redirect};
				$ok_sort_old = $line->{pos};
				$ok_elm_old[0] = $line->{html};
				$ok_show_old = $line->{show};
				$ok_show_menu_old = $line->{show_menu};
				$ok_show_head_old = $line->{show_head};
				$ok_hide_child_old = $line->{hide_child};
				$ok_show_child_count_old = $line->{show_child_count};				
				$ok_sitemap_old = $line->{sitemap};
				$ok_feedback_old = $line->{feedback};
				$ok_maket_old = $line->{maket};
				$today=$line->{date};
				$parent = $line->{parent};
			}	
		}
				if ($ok_show_child_count_old eq "0") {$ok_show_child_count_old="";}
		
		old_saves ();
		if ($num_edit eq "") { $ok_name_old=""; $ok_show_old = 1; $ok_show_head_old = 1;}
		menu_listing ();

	} elsif ($menu_act eq "ok" && $name eq "")  {
		$content_html=qq~$content_html<div class="delete_page">Поле "Название" не должно быть пустым.</div>~;
		$num_edit="";
		$sel_option="";
		$sel_option_s="";
		$sel_option_html="";
		$list_older="";		
		old_saves ();
		new_page ();
		menu_listing ();		

	} elsif ($menu_act eq "ok" && $name ne "")  {
	
		$name=param('name');
		$name=Core::DB::Work::trans_new($name);		
		$date=param('date');
		$title=param('title');
		$meta_desc=param('meta_desc');	
		$meta_key=param('meta_key');		
		$elm1=param('elm1');
		$elm1=Core::DB::Work::trans_html($elm1);	
		$parent=param('parent');
		$sort=param('sort');
		$alias=param('alias');
		if ( $alias eq "" ) {$alias=Core::DB::Work::translit( $name )} elsif ($alias eq "/") {$alias="";} else {$alias=Core::DB::Work::translit( $alias )};
		$redirect=param('redirect');
		if ( $redirect ne "" ) {$redirect =~ s/^\///g; $redirect = "/".$redirect;}
		$show=param('show');
		$show_head=param('show_head');
		$show_menu=param('show_menu');
		$feedback=param('feedback');
		$sitemap=param('sitemap');
		$maket=param('maket');
		$hide_child=param('hide_child');
		$show_child_count=param('show_child_count');
		$mirror_id=param('mirror_id');
		$mirror_link=param('mirror_link');

		if($show eq "on") {$show="0";} else {$show="1";};
		if($feedback eq "on") {$feedback="1";} else {$feedback="0";};
		if($sitemap eq "on") {$sitemap="1"; $alias="sitemap";} else {$sitemap="0";};
		if($hide_child eq "on") {$hide_child="1";} else {$hide_child="0";};
		if($show_child_count == 0 or $show_child_count < 0) {$show_child_count="";};
		if($show_child_count ne "" && $hide_child == 1) {$hide_child="0";};	
		if($maket eq "") {$maket="1";};	
		
		if ($num_edit eq ""){
			my $db = new Core::DB();
			my $result = $db->query("SELECT alias FROM strukture WHERE alias = '".$alias."';");
			if (ref($result) eq 'ARRAY'){$alias = $alias."2";}
			elsif ($parent ne "0"){
				my $p_alias ="";
				my $res = $db->query("SELECT id, alias, mirror_id, mirror_link FROM strukture WHERE id = '".$parent."';");		
				foreach my $item(@$res){
					$p_alias = $item->{alias};
				}
				if ($res->[0]->{mirror_id} ne "#!" && $res->[0]->{mirror_id} eq ""){
					$alias = $p_alias."/".$alias;
				}
			}
		}
		
		my %params = (
				'pos' => $sort,
				'parent' => $parent,
				'title' => "$title",
				'meta_desc' => "$meta_desc",
				'meta_key' => "$meta_key",				
				'name' => "$name",
				'date' => "$date",
				'alias' => "$alias",
				'redirect' => "$redirect",
				'html' => "$elm1",
				'show' => $show,
				'show_head' => $show_head,
				'show_menu' => $show_menu,
				'hide_child' => "$hide_child",
				'show_child_count' => "$show_child_count",				
				'feedback' => "$feedback",
				'sitemap' => "$sitemap",
				'mirror_id' => "$mirror_id",
				'mirror_link' => "$mirror_link",
				'maket' => "$maket"	
			);
		my $res;
		if($num_edit) {
			$res = $pages->edit($num_edit, \%params);
			ClearCache("../..");
		} else {
			$res = $pages->add(\%params);
			ClearCache("../..");
		}
		if( ref($res) eq 'ARRAY' ){
			$content_html=qq~$content_html<div class="save_page">Страница "$name" сохранена.</div>~;
			$num_edit="";
			$sel_option="";
			$sel_option_s="";
			$sel_option_html="";
			$list_older="";
		} else {
			$content_html=qq~$content_html<div class="save_page">Страница "$name" сохранена.</div>~;
			$num_edit="";
			$sel_option="";
			$sel_option_s="";
			$sel_option_html="";
			$list_older="";			
		}
		old_saves ();
		menu_listing ();
	}
	elsif ($menu_act eq "set_sort")  {
	
		$select_sort=param('select_sort');
		$ajax_save=param('ajax_save');
		if($ajax_save eq "on") {$ajax_save="1";} else {$ajax_save="0";};
		
		open OUT, (">../$dirs/sort_strukture");
			print OUT "$select_sort"; 
		close(OUT);	
		open OUT, (">../$dirs/set_strukture");
			print OUT "$ajax_save"; 
		close(OUT);			
		
		ClearCache("../..");
	
		$content_html=qq~$content_html<div class="save_page">Настройки сохранены.</div>~;		
		old_saves();
		menu_listing ();	
	
	}
	
sub old_sort {

		open(BO, "../$dirs/set_strukture"); my $set_pages = <BO>; close(BO); $ok_ajax_save_old = $set_pages;
		open(BO, "../$dirs/sort_strukture"); my $select_sort = <BO>; close(BO);

		my $pos_asc="pos ASC";
		my $name_asc="name ASC";
		my $date_asc="date ASC";
		my $date_desc="date DESC";	

		$sort_type ='
		<option value="pos ASC" '.($pos_asc eq $select_sort?'selected':'').'>Позициям</option>
		<option value="name ASC" '.($name_asc eq $select_sort?'selected':'').'>Названию</option>
		<option value="date ASC" '.($date_asc eq $select_sort?'selected':'').'>Дате по возрастанию</option>
		<option value="date DESC" '.($date_desc eq $select_sort?'selected':'').'>Дате по убыванию</option>';
}	

sub old_saves {
	use Core::DB;
	
	open(BO, "../$dirs/sort_strukture"); my $sort = <BO>; close(BO);
	
	sub buildMenub
	{
		my $db = new Core::DB();
		my $menub = "";
		$menub .= '<ul class="level0">';
		$sel_option = "";
		$result = $db->query("SELECT * FROM strukture WHERE parent=0 ORDER BY ".$sort.";");
		foreach my $item(@$result){
			my $del_button="";
			if ($item->{hide_del} eq "0") {$del_button = '<a href="#" class="del" title="Удалить страницу '.$item->{name}.'"></a>';}
			else {$del_button = '<a href="#" class="del off" title="Удалить страницу '.$item->{name}.'"></a>';}
			my $title="";
			if ($item->{redirect} ne ""){$title = "Редирект: /pages/".$item->{alias}." на ".$item->{redirect};}
			elsif ($item->{mirror_id} ne "" && $item->{mirror_link} ne ""){$title = "Зеркало страницы: ".$item->{mirror_link};}
			elsif ($item->{mirror_id} eq "#!"){$title = "";}
			else {$title = "Страница: /pages/".$item->{alias};}
			$menub .= '<li name="'.$item->{name}.'" c_id="'.$item->{id}.'" c_pid="'.$item->{parent}.'" c_pos="'.$item->{pos}.'" '.($item->{show_menu}==1?'':'class="off"').'><span class="move" '.($sort eq "pos ASC"?'><a class="up" href="#" title="Поднять вверх '.$item->{name}.'"></a><a class="down" href="#" title="Опустить вниз '.$item->{name}.'"></a>':'id="off">').'</span><a class="lamp" href="#" '.($item->{show_menu}==1?'title="Скрыть страницу"':'title="Сделать активной" style="opacity:0.5"').'></a>'.$del_button.'';
			$menub .= '<a'.($item->{mirror_id} eq "#!"?' class="point"':' class="name"').' title="'.$title.'" href="'.($item->{mirror_id} ne ""?''.$item->{mirror_id}.'':'?adm_act=strukture&num_edit='.$item->{id}.'').'">'.$item->{name}.''.($item->{mirror_id} ne "" && $item->{mirror_id} ne "#!"?' <em class="mirror">(зеркало)</em>':'').'</a>
			<div class="controls left">
				<div class="item" id="mirror">';
			if ($item->{mirror_id} ne "" && $item->{mirror_id} ne "#!"){
				my $m_link = "";
				if ($item->{mirror_link} eq ""){$m_link = "/pages/".$item->{alias};}
				else {$m_link = $item->{mirror_link};}
				$menub .= '<em style="padding-top:4px;">Зеркало страницы:</em><select name="mirror"><option>'.$m_link.'</option></select><span class="reset">Сбросить</span>';
			} else {$menub .= '<em>Сделать зеркалом:</em><span class="choice">Выбрать раздел</span>';}
			
			$menub .= '		
				</div><div class="clear"></div>
				<div class="item" id="remove_link"><em>Убрать ссылку:</em><span>Да</span><input type="checkbox" name="yes" class="cb"'.($item->{mirror_id} eq "#!"?' checked':'').'><span>Нет</span><input type="checkbox" name="no" class="cb"'.($item->{mirror_id} ne "#!"?' checked':'').'></div>						
			</div>					
			<div class="controls right">
				<div class="item" id="del">
					<em>Отменить удаление:</em><span>Да</span><input type="checkbox" name="yes" class="cb"'.($item->{hide_del} eq "1"?' checked':'').'><span>Нет</span><input type="checkbox" name="no" class="cb"'.($item->{hide_del} eq "0"?' checked':'').'>
				</div>			
			</div>';
			if ($num_edit == $item->{id}) {$sel_option .='';}
			else {$sel_option .= '<option'.($item->{mirror_id} eq "#!"?' class="point"':'').' value="'.$item->{id}.'" '.($parent==$item->{id}?'selected':'').'>'.$item->{name}.'</option>';}
			if( my $sub = recMenu($item->{id}, 0) ){
				$menub .= $sub;
			}
			$menub .= '</li>';
		}
		
		sub recMenu{
			my $id = shift;
			my $level = shift;
			sub nbsp { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
			my $text = '<ul class="level'.($level+1).'">';
					
			$result_parent = $db->query("SELECT * FROM strukture WHERE id='".$id."'");
			my $hide_child="";
			my $show_child_count="";
			if($result_parent){
				foreach my $items(@$result_parent){
					$hide_child = $items->{hide_child};
					$show_child_count = $items->{show_child_count};
				}
			}
			if ($hide_child == 1) {$hide_child="class='hide'"} else {$hide_child=""};
			
			$result = $db->query("SELECT * FROM strukture WHERE parent='".$id."' ORDER BY ".$sort.";"); 
			if($result){
				my $i_cat_old="";
				foreach my $item2(@$result){
					$i_cat_old++;
				}
				my $i_cat="";
				foreach my $item(@$result){
					$i_cat++;
					my $del_button="";
					if ($item->{hide_del} eq "0") {$del_button = '<a href="#" class="del" title="Удалить страницу '.$item->{name}.'"></a>';}
					else {$del_button = '<a href="#" class="del off" title="Удалить страницу '.$item->{name}.'"></a>';}
					my $title="";
					if ($item->{redirect} ne ""){$title = "Редирект: /pages/".$item->{alias}." на ".$item->{redirect};}
					elsif ($item->{mirror_id} ne "" && $item->{mirror_link} ne ""){$title = "Зеркало страницы: ".$item->{mirror_link};}
					elsif ($item->{mirror_id} eq "#!"){$title = "";}
					else {$title = "Страница: /pages/".$item->{alias};}
					$text .= '<li name="'.$item->{name}.'" c_id="'.$item->{id}.'" c_pid="'.$item->{parent}.'" c_pos="'.$item->{pos}.'" '.($item->{show_menu}==1?'':'class="off"').'><span class="move" '.($sort eq "pos ASC"?'><a class="up" href="#" title="Поднять вверх '.$item->{name}.'"></a><a class="down" href="#" title="Опустить вниз '.$item->{name}.'"></a>':'id="off">').'</span><a class="lamp" href="#" '.($item->{show_menu}==1?'title="Скрыть страницу"':'title="Сделать активной" style="opacity:0.5"').'></a>'.$del_button.'<div class="point'.($i_cat==$i_cat_old?' last':'').'"></div>';
					$text .= '<a'.($item->{mirror_id} eq "#!"?' class="point"':' class="name"').' title="'.$title.'" '.$hide_child.' '.($show_child_count < $i_cat && $show_child_count !=0?'class="hide"':'').' href="'.($item->{mirror_id} ne ""?''.$item->{mirror_id}.'':'?adm_act=strukture&num_edit='.$item->{id}.'').'">'.$item->{name}.''.($item->{mirror_id} ne "" && $item->{mirror_id} ne "#!"?' <em class="mirror">(зеркало)</em>':'').'</a>
					<div class="controls left">
						<div class="item" id="mirror">';
					if ($item->{mirror_id} ne "" && $item->{mirror_id} ne "#!"){
						my $m_link = "";
						if ($item->{mirror_link} eq ""){$m_link = "/pages/".$item->{alias};}
						else {$m_link = $item->{mirror_link};}
						$text .= '<em style="padding-top:4px;">Зеркало страницы:</em><select name="mirror"><option>'.$m_link.'</option></select><span class="reset">Сбросить</span>';
					} else {$text .= '<em>Сделать зеркалом:</em><span class="choice">Выбрать раздел</span>';}
					
					$text .= '		
						</div><div class="clear"></div>
						<div class="item" id="remove_link"><em>Убрать ссылку:</em><span>Да</span><input type="checkbox" name="yes" class="cb"'.($item->{mirror_id} eq "#!"?' checked':'').'><span>Нет</span><input type="checkbox" name="no" class="cb"'.($item->{mirror_id} ne "#!"?' checked':'').'></div>						
					</div>					
					<div class="controls right">
						<div class="item" id="del">
							<em>Отменить удаление:</em><span>Да</span><input type="checkbox" name="yes" class="cb"'.($item->{hide_del} eq "1"?' checked':'').'><span>Нет</span><input type="checkbox" name="no" class="cb"'.($item->{hide_del} eq "0"?' checked':'').'>
						</div>			
					</div>';
					if ($num_edit == $item->{id}) {$sel_option .='';}
					else {$sel_option .= '<option'.($item->{mirror_id} eq "#!"?' class="point"':'').' value="'.$item->{id}.'" '.($parent==$item->{id}?'selected':'').'>'.nbsp($level).$item->{name}.'</option>';}			
					if( my $sub = recMenu($item->{id}, $level+1) ){
						$text .= $sub;
					}
					$text .= '</li>'; 
				} 

			} else { 
				return 0;
			} 
			$text .= '</ul>';  
			return $text; 

		};
		$menub .= "</ul>";
	    return $menub;
								
	}

	$list_older = buildMenub();
	#require "../engine/lib/LWP/Protocol/GHTTPS.pm";	
	$maket_list=""; $maket_item="";
	opendir (DBDIR, "../$dirs"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $num) = split(/\./, $line_wall);
			if ($name_file eq "maket" && $num ne "404") { 
				open (BO, "../$dirs/$line_wall"); @b = <BO>; close (BO);
				($name_old, $date_old) = split(/\|/, $b[0]);
				my $select="";
				if ($ok_maket_old ne ""){$select = $ok_maket_old;} else {$select = $maket_page;}
				$maket_item .= '<option value="'.$num.'" '.($num==$select?'selected':'').'>'.$name_old.'</option>';
			}
		}
	}

	if ($maket_item ne "" && $hide_makets ne "1"){
		$maket_list = '
			<tr class="help_maket">
				<td class="name">Привязать страницу к макету</td>
				<td>
					<select class="category" name="maket" style="width:197px;">
						'.$maket_item.'
					</select>
				</td>
			</tr>';
	}	

}


sub new_page {

$dshfgkjdf=qq~<td class="name">Соответствие разделу<em>*</em></td><td><select name="parent" id="category"><option value="0">Верхний уровень</option>$sel_option</select></td>~;

$content_html.= qq~
<div class="three_pages" style="display:none;">$list_older</div>
<div id="pages_new" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">
			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Новая страница</td>
			</tr>
			<tr>

				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>
			<tr>

$dshfgkjdf

			</tr>
			<tr>
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>

			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr>
				<td class="name">Адрес страницы</td><td><input name="alias" type="text"></td>
			</tr>
				$maket_list
			<tr>
				<td class="name">Дата </td><td><input name="date" id="date_edit" value="$today" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name"></td><td class="name_main">Настройки SEO</td>
			</tr>
			<tr>
				<td class="name">Meta Title</td><td><input name="title" value="$ok_title_old" type="text"></td>

			</tr>
			<tr>
				<td class="name">Meta Description</td><td><input name="meta_desc" value="$ok_meta_desc_old" type="text"></td>
			</tr>
			<tr>
				<td class="name">Meta Keywords</td><td><input name="meta_key" value="$ok_meta_key_old" type="text"></td>
			</tr>
			</table>


				</td>
			</tr>
			</table>


	<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<input type="submit" name="save" value="Сохранить" class="button" />
	<input type="reset" name="reset" value="Очистить" class="button" />
</form>
</div>~;
}

sub menu_listing {

$dshfgkjdf=qq~<td class="name">Соответствие разделу<em>*</em></td><td><select name="parent" id="category"><option value="0">Верхний уровень</option>$sel_option</select></td>~;

if ($settings eq "set") {

	sub menu_settings {

		$list_older="";
		old_sort();

		$content_html.= qq~
		<script type="text/javascript" src="/admin/lib/help/pages/pages_settings.js"></script>
		<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
		<input type="hidden" name="adm_act" value="strukture">
		<input type="hidden" name="menu_act" value="set_sort">
					<table id="page_new" style="margin-bottom:0px;">
					<tr>
						<td class="name"></td><td class="name_main">Настройки модуля</td>
					</tr>
					<tr class="help_sort">
						<td class="name">Сортировать страницы по</td><td><select name="select_sort" id="category">$sort_type</select></td>
					</tr>
					<tr class="help_quick_save">
						<td class="name">Быстрое сохранение контента</td><td><input type="checkbox" class="cb" name="ajax_save"~;
		if($ok_ajax_save_old eq "1"){
			$content_html.= qq~ checked ~;
		}			
		
	$content_html.= qq~></td>
					</tr>					
					</table>
					
		<input style="margin-left:554px; margin-top:-15px;" type="submit" name="save" value="Сохранить" class="button" />			
		</form>
		~;
	}
	menu_settings();
}


if ($par eq "new") {
	
$content_html.= qq~
<script type="text/javascript" src="/admin/lib/help/pages/pages_edit.js"></script>
<div class="three_pages" style="display:none;">$list_older</div>
<div id="pages_new" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">
			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Новая страница</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>
			<tr class="help_parent">

$dshfgkjdf

			</tr>
			<tr class="help_feedback">
				<td class="name">Обратная связь</td><td><input type="checkbox" class="cb" name="feedback"></td>
			</tr>
			<tr class="help_sitemap">
				<td class="name">Карта сайта</td><td><input type="checkbox" class="cb" name="sitemap"></td>
			</tr>
			<tr>
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>

			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr class="help_alias">
				<td class="name">Адрес страницы</td><td><input name="alias" type="text"></td>
			</tr>
				$maket_list
			<tr>
				<td class="name">Дата </td><td><input name="date" id="date_edit" value="$today" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name"></td><td class="name_main">Настройки SEO</td>
			</tr>
			<tr class="help_meta-title">
				<td class="name">Meta Title</td><td><input name="title" value="$ok_title_old" type="text"></td>
			</tr>
			<tr class="help_meta-desc">
				<td class="name">Meta Description</td><td><input name="meta_desc" value="$ok_meta_desc_old" type="text"></td>
			</tr>
			<tr class="help_meta-key">
				<td class="name">Meta Keywords</td><td><input name="meta_key" value="$ok_meta_key_old" type="text"></td>
			</tr>
			</table>


				</td>
			</tr>
			</table>


	<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<input type="submit" name="save" value="Сохранить" class="button" />
	<input type="reset" name="reset" value="Очистить" class="button" />
</form>
</div>~;
} else {


	if ($num_edit eq ""){
		if ($settings ne "set"){
			$content_html .=qq~<script type="text/javascript" src="/admin/lib/help/pages/pages.js"></script>
			<div class="three_pages">$list_older</div>~;	
		}
	} else {
	
	open(BO, "../$dirs/sort_strukture"); my $set_sort = <BO>; close(BO);
	if ($set_sort ne "pos ASC") {$sort_none ="style='display:none;'";} else {$sort_none ="";}
	
	open(BO, "../$dirs/set_strukture"); my $ok_ajax_save = <BO>; close(BO);
	if ($ok_ajax_save == "0" or $ok_ajax_save == "") {$button_save = '<input type="submit" name="save" value="Сохранить" class="button save" />'; $check_ajax='';}
	else {$button_save = '<a class="ajaxSave" href="#">Сохранить</a>'; $check_ajax='checked';}
	
	
		$content_html=qq~$content_html
		<script type="text/javascript" src="/admin/lib/help/pages/pages_edit.js"></script>
		<div class="three_pages" style="display:none;">$list_older</div>
		<div id="pages_old" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">

			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Редактирование страницы</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
			<tr class="help_sort" $sort_none>
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>
			<tr class="help_parent">

$dshfgkjdf

			</tr>
			<tr class="help_show_menu">
		<td class="name">Показывать страницу в меню</td><td class="show"><input name="show_menu" type="checkbox" class="cb" ~;
		if($ok_show_menu_old){
			$content_html.= qq~ checked ~;
		} 
		
$content_html.= qq~> </td></tr>
			<tr class="help_feedback">
				<td class="name">Обратная связь</td><td><input type="checkbox" class="cb" name="feedback"~;
		if($ok_feedback_old eq "1"){
			$content_html.= qq~ checked ~;
		}			
		
$content_html.= qq~></td>
			</tr>
			<tr class="help_sitemap">
				<td class="name">Карта сайта</td><td><input type="checkbox" class="cb" name="sitemap"~;
		if($ok_sitemap_old eq "1"){
			$content_html.= qq~ checked ~;
		}			
		
$content_html.= qq~></td>
			</tr>			
			<tr>
				<td class="name"><a href="#" class="ext">Расширенные настройки</a></td><td></td>
			</tr>

			<tr>
				<td colspan="2">

			<table id="page_new" class="ext_param">
			<tr>
				<td class="name"></td><td class="name_main">Расширенные</td>
			</tr>
			<tr class="help_alias">
				<td class="name">Адрес страницы</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>
				
				$maket_list
				
			<tr class="redirect">
				<td class="name">Редирект 301</td><td>
					<div>Например: <em><span>/</span>pages<span>/</span>new_page</em></div>
					<input name="redirect" type="text" value="$ok_redirect_old"></td>
			</tr>			
			<tr>
				<td class="name">Дата </td><td><input name="date" id="date_edit" value="$today" type="text" class="date"></td>
			</tr>
			<tr class="help_header">
				<td class="name">Отображать заголовок страницы</td><td class="show"><input name="show_head" type="checkbox" class="cb"~;
		
		if($ok_show_head_old){
			$content_html .= qq~ checked~;
		} 
		
		$content_html .= qq~></td></tr>
		<tr class="help_hide">
		<td class="name">Скрывать от поисковиков</td><td class="show"><input name="show" type="checkbox" class="cb" ~;
		if($ok_show_old eq "0"){
			$content_html.= qq~ checked ~;
		} 
		
$content_html.= qq~> </td></tr>~;	
			
	my $db = new Core::DB();
	my $res = $db->query("SELECT * FROM strukture WHERE parent=".$num_edit.";");

	if(ref($res) eq "ARRAY") {			
		$content_html.= qq~
			<tr class="help_hide_child">
				<td class="name">Скрывать вложенные категории</td><td><input type="checkbox" class="cb" name="hide_child"~;
		if($ok_hide_child_old eq "1"){
			$content_html.= qq~ checked ~;
		}			
		
			$content_html.= qq~></td>
			</tr>
			<tr class="help_hide_child_count">
				<td class="name">Кол-во отображаемых категорий</td><td><input type="text" value="$ok_show_child_count_old" class="sort" name="show_child_count"></td>
			</tr>~;
	}
		
$content_html.= qq~			
			<tr>
				<td class="name"></td><td class="name_main">Настройки SEO</td>
			</tr>
			<tr class="help_meta-title">
				<td class="name">Meta Title</td><td><input name="title" value="$ok_title_old" type="text"></td>
			</tr>
			<tr class="help_meta-desc">
				<td class="name">Meta Description</td><td><input name="meta_desc" value="$ok_meta_desc_old" type="text"></td>
			</tr>
			<tr class="help_meta-key">
				<td class="name">Meta Keywords</td><td><input name="meta_key" value="$ok_meta_key_old" type="text"></td>
			</tr>
			</table>


				</td>
			</tr>
			</table>
	
	<img style="display:none;" src="/admin/js/tiny_mce/themes/advanced/skins/default/img/progress.gif" alt="">
	<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<div class="save_content">$button_save
	<a class="preview_page" id="$num_edit" target="_blank" href="/pages/$ok_alias_old">Посмотреть</a><div class="check_save"><input type="checkbox" class="cb ajaxSave" $check_ajax>Быстрое сохранение контента</div></div>
</form>
</div>
~;
}
}


$content_html.= qq~
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;

}


-1;