use Core::DB::Articles;
use Core::DB::Work;

my $articles = new Core::DB::Articles();
my $db = new Core::DB();

	$menu_act=param('menu_act');
	$num_edit=param('num_edit');
	$name=param('name');	
	$par=param('par');
	$settings=param('settings');
	$image=param('image');

if ($num_edit eq "") {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>
<li class="activetab"><a id="click_pages" href="#"><span>Статьи</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=articles&par=new"><span>Новая статья</span></a></li>~;
} else {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>
<li class="activetab"><a id="click_pages" href="#"><span>Статьи</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=articles&par=new"><span>Новая статья</span></a></li>~;
}
if ($par) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>
<li><a id="click_pages" href="#"><span>Статьи</span></a></li>
<li class="activetab"><a id="click_pages_new" href="#"><span>Новая статья</span></a></li>~;
}
if ($settings) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture"><span>Страницы сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=strukture&par=new"><span>Новая страница</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=articles"><span>Статьи</span></a></li>
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
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=articles&settings=set" id="cstmz">Настроить модуль</a>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">
		<div id="pages">
<script type="text/javascript" src="/admin/lib/articles.js"></script>~;	
	
	($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
	if ($mday < 10 ) { $mdays="0"; $mday="$mdays$mday";}
	$mon++; if ($mon < 10 ) { $mon="0$mon";}
	$year=1900+$year; 
	$today="$year-$mon-$mday";

	if ($menu_act eq "") {
		$list_older="";
		
		$result = $articles->query("SELECT * FROM articles WHERE articles.id = '".$num_edit."' LIMIT 1");
		
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
				$ok_maket_old = $line->{maket};
				$today=$line->{date};
				$parent = $line->{parent};
			}	
		}
		
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
		$maket=param('maket');

		if($show eq "on") {$show="0";} else {$show="1";};
		if($maket eq "") {$maket="1";};	
		
		if ($num_edit eq ""){
			my $result = $db->query("SELECT alias FROM articles WHERE alias = '".$alias."';");
			if (ref($result) eq 'ARRAY'){$alias = $alias."2";}
			elsif ($parent ne "0" && $hide_articles_parent ne "1"){
				my $p_alias ="";
				my $res = $db->query("SELECT id, alias FROM articles WHERE id = '".$parent."';");		
				foreach my $item(@$res){
					$p_alias = $item->{alias};
				}
				$alias = $p_alias."/".$alias;
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
				'maket' => "$maket"	
			);
			
		if ($image ne ""){
	
			my $max_num=""; my $name_file_max="";
			my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'articles';");
			foreach my $item(@$result){	
				$max_num = $item->{Auto_increment};
				$name_file_max = $max_num+1000;			
			}

			if ($num_edit != "") {$name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$name_file_max="1001"}}

			open OUT, (">$dirs_img/public/$name_file_max\.jpg");
			 binmode (OUT);
			 while (<$image>) { print OUT "$_"; } 
			close(OUT);
			
			use File::Copy;
			copy("$dirs_img/public/$name_file_max\.jpg", "$dirs_img/public/$name_file_max\_big.jpg");
			
			%configconsts = (
				'img_resize' => [362,272]
			);

			use Image::Magick;
			
			my $image = Image::Magick->new;
			$image->Read("$dirs_img/public/$name_file_max\.jpg"); 
			($ox,$oy)=$image->Get('base-columns','base-rows'); 				
		
			$division = $configconsts{'img_resize'}[0]/$configconsts{'img_resize'}[1];
			
			if(($ox/$oy)>$division)
				
			{$nx=int(($ox/$oy)*$configconsts{'img_resize'}[1]);			
			$ny=$configconsts{'img_resize'}[1];
			$cropx = int(($nx-$configconsts{'img_resize'}[0])/2);
			$cropy = 0;
			
			} else {
			
				$ny=int(($oy/$ox)*$configconsts{'img_resize'}[0]);	
				$nx=$configconsts{'img_resize'}[0];
				$cropy = int(($ny-$configconsts{'img_resize'}[1])/2);
				$cropx = 0;		
			}
			
			$image->Resize(geometry=>'geometry', width=>$nx, height=>$ny);
			$image->Crop(x=>$cropx, y=>$cropy);
			$image->Crop($configconsts{'img_resize'}[0], $configconsts{'img_resize'}[1]);
			$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
			$image->Write("$dirs_img/public/$name_file_max\.jpg");
		}
			
		my $res;
		if($num_edit) {
			$res = $articles->edit($num_edit, \%params);
		} else {
			$res = $articles->add(\%params);
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
		$limit_articles=param('limit_articles');
		$ajax_save=param('ajax_save');
		if($ajax_save eq "on") {$ajax_save="1";} else {$ajax_save="0";};
		
		open OUT, (">../$dirs/sort_articles");
			print OUT "$select_sort"; 
		close(OUT);	
		open OUT, (">../$dirs/set_articles");
			print OUT "$limit_articles|$ajax_save"; 
		close(OUT);			
	
		$content_html=qq~$content_html<div class="save_page">Настройки сохранены.</div>~;		
		old_saves();
		menu_listing ();	
	
	}
	
sub old_sort {

		open(BO, "../$dirs/set_articles"); @set_articles = <BO>; close(BO);
		foreach my $line(@set_articles){chomp($line);
		my ($limit_articles_, $set_ajax_) = split(/\|/, $line);
		$ok_limit_articles_old = qq~$limit_articles_~; $ok_ajax_save_old=qq~$set_ajax_~;}
		open(BO, "../$dirs/sort_articles"); my $select_sort = <BO>; close(BO);

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
	
	open(BO, "../$dirs/sort_articles"); my $sort = <BO>; close(BO);
	
	sub buildMenub
	{
		my $menub = "";
		$menub .= '<ul class="level0">';
		$sel_option = "";
		$result = $db->query("SELECT * FROM articles WHERE parent=0 ORDER BY ".$sort.";");
		foreach my $item(@$result){
			my $title="";
			if ($item->{redirect} ne ""){$title = "Редирект: /public/".$item->{alias}." на ".$item->{redirect};}
			else {$title = "Статья: /public/".$item->{alias};}
			$menub .= '<li name="'.$item->{name}.'" c_id="'.$item->{id}.'" c_pid="'.$item->{parent}.'" c_pos="'.$item->{pos}.'" '.($item->{show_menu}==1?'':'class="off"').'><span class="move" '.($sort eq "pos ASC"?'><a class="up" href="#" title="Поднять вверх '.$item->{name}.'"></a><a class="down" href="#" title="Опустить вниз '.$item->{name}.'"></a>':'id="off">').'</span><a class="lamp" href="#" '.($item->{show_menu}==1?'title="Скрыть статью"':'title="Сделать активной" style="opacity:0.5"').'></a><a href="#" class="del" title="Удалить статью '.$item->{name}.'"></a>';
			$menub .= '<a title="'.$title.'" href="?adm_act=articles&num_edit='.$item->{id}.'">'.$item->{name}.'</a>';
			if ($num_edit == $item->{id}) {$sel_option .='';}
			else {$sel_option .= '<option value="'.$item->{id}.'" '.($parent==$item->{id}?'selected':'').'>'.$item->{name}.'</option>';}
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
			
			$result = $db->query("SELECT * FROM articles WHERE parent='".$id."' ORDER BY ".$sort.";"); 
			if($result){
				my $i_cat_old="";
				foreach my $item2(@$result){
					$i_cat_old++;
				}
				my $i_cat="";
				foreach my $item(@$result){
					$i_cat++;
					my $title="";
					if ($item->{redirect} ne ""){$title = "Редирект: /public/".$item->{alias}." на ".$item->{redirect};}
					else {$title = "Статья: /public/".$item->{alias};}
					$text .= '<li name="'.$item->{name}.'" c_id="'.$item->{id}.'" c_pid="'.$item->{parent}.'" c_pos="'.$item->{pos}.'" '.($item->{show_menu}==1?'':'class="off"').'><span class="move" '.($sort eq "pos ASC"?'><a class="up" href="#" title="Поднять вверх '.$item->{name}.'"></a><a class="down" href="#" title="Опустить вниз '.$item->{name}.'"></a>':'id="off">').'</span><a class="lamp" href="#" '.($item->{show_menu}==1?'title="Скрыть статью"':'title="Сделать активной" style="opacity:0.5"').'></a><a href="#" class="del" title="Удалить статью '.$item->{name}.'"></a><div class="point'.($i_cat==$i_cat_old?' last':'').'"></div>';
					$text .= '<a title="'.$title.'" href="?adm_act=articles&num_edit='.$item->{id}.'">'.$item->{name}.'</a>';
					if ($num_edit == $item->{id}) {$sel_option .='';}
					else {$sel_option .= '<option value="'.$item->{id}.'" '.($parent==$item->{id}?'selected':'').'>'.nbsp($level).$item->{name}.'</option>';}			
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
				if ($ok_maket_old ne ""){$select = $ok_maket_old;} else {$select = $maket_article;}
				$maket_item .= '<option value="'.$num.'" '.($num==$select?'selected':'').'>'.$name_old.'</option>';
			}
		}
	}

	if ($maket_item ne "" && $hide_makets ne "1"){
		$maket_list = '
			<tr>
				<td class="name">Привязать статью к макету</td>
				<td>
					<select class="category" name="maket" style="width:197px;">
						'.$maket_item.'
					</select>
				</td>
			</tr>';
	}	

}

sub menu_listing {

my $select_parent="";
if ($hide_articles_parent ne "1"){
	$select_parent =qq~<tr><td class="name">Соответствие разделу<em>*</em></td><td><select name="parent" id="category"><option value="0">Верхний уровень</option>$sel_option</select></td></tr>~;
}

if ($settings eq "set") {

	sub menu_settings {

		$list_older="";
		old_sort();

		$content_html.= qq~
		<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
		<input type="hidden" name="adm_act" value="articles">
		<input type="hidden" name="menu_act" value="set_sort">
					<table id="page_new" style="margin-bottom:0px;">
					<tr>
						<td class="name"></td><td class="name_main">Настройки модуля</td>
					</tr>
					<tr>
						<td class="name">Сортировать статьи по</td><td><select name="select_sort" id="category">$sort_type</select></td>
					</tr>
					<tr>
						<td class="name">Выводить статей на странице</td><td><input type="text" name="limit_articles" value="$ok_limit_articles_old" class="normal"></td>
					</tr>						
					<tr>
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
<div class="three_pages" style="display:none;">$list_older</div>
<div id="pages_new" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">
			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Новая статья</td>
			</tr>
			<tr>

				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>~;
		
		$content_html .='
				<tr class="help_image">
					<td class="name">Загрузить картинку</td>
					<td class="img_load">
					<div class="prev_img no_show get_image"></div>
					<input multiple="multiple" class="fileInput" type="file" name="image" size="21" onchange="document.getElementById(\'fileInputbg\').value = this.value;">
					<div class="browse" style="margin-left:2px;">
						<input type="text" id="fileInputbg" class="browse_input"/>
					</div>
					</td>
				</tr>
				<tr class="help_image_url">
					<td class="name">Загрузить картинку по ссылке</td>
					<td class="img_load">	
						<div class="b-help">
							<input type="text" cat_id="" value="" class="give_url_big show">
							<div class="help">
								Для загрузки картинки из интернета скопируйте<br>
								адрес картинки в буфер и вставьте в это поле
							</div>
						</div>
					</td>
				</tr>';			
			
$content_html.= qq~			
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>

$select_parent

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
				<td class="name">Адрес статьи</td><td><input name="alias" type="text"></td>
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
} else {


	if($num_edit eq ""){
$content_html=qq~$content_html<div class="three_pages">$list_older</div>
~;	
	} else {
	
	open(BO, "../$dirs/sort_articles"); my $set_sort = <BO>; close(BO);
	if ($set_sort ne "pos ASC") {$sort_none ="style='display:none;'";} else {$sort_none ="";}
	
		open(BO, "../$dirs/set_articles"); @set_articles = <BO>; close(BO);
		foreach my $line(@set_articles){chomp($line);
		my ($limit_articles_, $set_ajax_) = split(/\|/, $line);
		$ok_ajax_save=qq~$set_ajax_~;}
	if ($ok_ajax_save == "0" or $ok_ajax_save == "") {$button_save = '<input type="submit" name="save" value="Сохранить" class="button save" />'; $check_ajax='';}
	else {$button_save = '<a class="ajaxSave" href="#">Сохранить</a>'; $check_ajax='checked';}
	
	
		$content_html=qq~$content_html
		<div class="three_pages" style="display:none;">$list_older</div>
		<div id="pages_old" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">

			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Редактирование статьи</td>
			</tr>
			<tr>

				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>~;
			
		$rand_num=rand(1);
		my $img_num = $num_edit+1000;
		if(-e "$dirs_img/public/$img_num.jpg")
		{$image =qq~<img src="/uploads/public/$img_num.jpg?$rand_num" border="0">~;}
		else { $image = "";}
		
		$content_html .='
				<tr class="help_image">
					<td class="name">'.($image ne ""?'Поменять картинку':'Загрузить картинку').'</td>
					<td class="img_load">
					'.($image ne ""?'<div class="prev_img get_image">'.$image.'</div>':'<div class="prev_img no_show get_image"></div>').'
					<input multiple="multiple" class="fileInput" type="file" name="image" size="21" onchange="document.getElementById(\'fileInputbg\').value = this.value;">
					<div class="browse" style="margin-left:2px;">
						<input type="text" id="fileInputbg" class="browse_input"/>
					</div>
					</td>
				</tr>
				<tr class="help_image_url">
					<td class="name">Загрузить картинку по ссылке</td>
					<td class="img_load">	
						<div class="b-help">
							<input type="text" cat_id="'.$num_edit.'" value="" class="give_url_big show">
							<div class="help">
								Для загрузки картинки из интернета скопируйте<br>
								адрес картинки в буфер и вставьте в это поле
							</div>
						</div>
					</td>
				</tr>';				
			
		$content_html .=qq~	
			<tr $sort_none>
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>

$select_parent

			<tr>
		<td class="name">Показывать статью</td><td class="show"><input name="show_menu" type="checkbox" class="cb" ~;
		if($ok_show_menu_old){
			$content_html.= qq~ checked ~;
		} 
		
$content_html.= qq~> </td></tr>
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
				<td class="name">Адрес статьи</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>
				
				$maket_list
				
			<tr class="redirect">
				<td class="name">Редирект 301</td><td>
					<div>Например: <em><span>/</span>public<span>/</span>new_article</em></div>
					<input name="redirect" type="text" value="$ok_redirect_old"></td>
			</tr>			
			<tr>
				<td class="name">Дата </td><td><input name="date" id="date_edit" value="$today" type="text" class="date"></td>
			</tr>
			<tr>
				<td class="name">Отображать заголовок статьи</td><td class="show"><input name="show_head" type="checkbox" class="cb"~;
		
		if($ok_show_head_old){
			$content_html .= qq~ checked~;
		} 
		
		$content_html .= qq~></td></tr>
		<tr>
		<td class="name">Скрывать от поисковиков</td><td class="show"><input name="show" type="checkbox" class="cb" ~;
		if($ok_show_old eq "0"){
			$content_html.= qq~ checked ~;
		} 
		
$content_html.= qq~> </td></tr>
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
	
	<img style="display:none;" src="/admin/js/tiny_mce/themes/advanced/skins/default/img/progress.gif" alt="">
	<textarea id="elm1" name="elm1" rows="25" cols="80" class="tinymce">@ok_elm_old</textarea>
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<div class="save_content">$button_save
	<a class="preview_page" id="$num_edit" target="_blank" href="/public/$ok_alias_old">Посмотреть</a><div class="check_save"><input type="checkbox" class="cb ajaxSave" $check_ajax>Быстрое сохранение контента</div></div>
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