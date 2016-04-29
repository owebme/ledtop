use Core::DB::News;
use Core::DB::Work;

my $pages = new Core::DB::News();

	$menu_act=param('menu_act');
	$num_edit=param('num_edit');
	$posup=param('posup');
	$posdown=param('posdown');	
	$name=param('name');	
	$par=param('par');
	$settings=param('settings');
	$lamp=param('lamp');

if ($num_edit eq "") {
$new_pages =qq~<li class="first activetab"><a id="click_pages" href="#"><span>Новости сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=news&par=new"><span>Новая новость</span></a></li>~;
} else {
$new_pages =qq~<li class="first activetab"><a id="click_pages" href="#"><span>Новости сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=news&par=new"><span>Новая новость</span></a></li>~;
}
if ($par) {
$new_pages =qq~<li class="first"><a id="click_pages" href="#"><span>Новости сайта</span></a></li>
<li class="activetab"><a id="click_pages_new" href="#"><span>Новая новость</span></a></li>~;
}
if ($settings) {
$new_pages =qq~<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=news"><span>Новости сайта</span></a></li>
<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=news&par=new"><span>Новая новость</span></a></li>~;
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
				<a href="/cgi-bin/admin/engine/index.cgi?adm_act=news&settings=set" id="cstmz">Настроить модуль</a>
			</div>
		
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">
		<div id="pages">
<script type="text/javascript" src="/admin/lib/news.js"></script>~;
	
	
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
		$content_html=qq~$content_html<div class="delete_page">Новость удалена.</div>~;
		$num_edit="";
		$sel_option="";
		$sel_option_s="";
		$sel_option_html="";
		$list_older="";		
		$menu_act="";
	}

	if ($menu_act eq "") {
		$list_older="";
		
		$result = $pages->query("SELECT * FROM news WHERE news.id = '".$num_edit."' LIMIT 1");
		
		if($result){
			foreach my $line(@$result){
				$ok_name_old = $line->{name};
				$ok_name_old=Core::DB::Work::trans_edit($ok_name_old);				
				$ok_title_old = $line->{title};
				$ok_meta_desc_old = $line->{meta_desc};
				$ok_meta_key_old = $line->{meta_key};					
				$ok_alias_old = $line->{alias};
				$ok_redirect_old = $line->{n_redirect};
				$ok_sort_old = $line->{pos};
				$ok_elm_old[0] = $line->{html};
				$ok_elm_sm_old[0] = $line->{html_sm};				
				$ok_show_old = $line->{show};
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
		$list_older="<div id=red>ПОЛЕ НАЗАНИЕ НЕ ДОЛЖНО БЫТЬ ПУСТЫМ!</div>";
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
		$elm1_sm=param('elm1_sm');	
		$elm1_sm=Core::DB::Work::trans_html($elm1_sm);		
		$parent=param('parent');
		$sort=param('sort');
		$alias=param('alias');
		if ( $alias eq "" ) {$alias=Core::DB::Work::translit( $name )} else {$alias=Core::DB::Work::translit( $alias )};
		$redirect=param('redirect');
		if ( $redirect ne "" ) {$redirect =~ s/^\///g; $redirect = "/".$redirect;}
		$image=param('image');
		$img_ox=param('img_ox');
		$img_oy=param('img_oy');
		$maket=param('maket');
		$show=param('show');
		$show_head=param('show_head');
		
		if($maket eq "") {$maket="1";};

		my %params = (
				'pos' => $sort,
				'parent' => $parent,
				'title' => "$title",
				'meta_desc' => "$meta_desc",
				'meta_key' => "$meta_key",				
				'name' => "$name",
				'date' => "$date",
				'alias' => "$alias",
				'n_redirect' => "$redirect",
				'html' => "$elm1",
				'html_sm' => "$elm1_sm",				
				'show' => $show,
				'show_head' => $show_head,
				'maket' => "$maket"
			);
			
		if ($hide_news_photo ne "1"){
		
				open OUT, (">$dirs_news/settings.txt");
					print OUT "$img_ox|$img_oy"; 
				close(OUT);		
				
			if ($image ne ""){
			
				my $db = new Core::DB();		
			
				my $max_num=""; my $name_file_max="";
				my $result = $db->query("SHOW TABLE STATUS FROM `".%Core::Config::DB->{db}."` LIKE 'news';");
				foreach my $item(@$result){	
					$max_num = $item->{Auto_increment};
					$name_file_max = $max_num+1000;			
				}

				if ($num_edit != "") {$name_file_max=$num_edit+1000;} else {if ($max_num eq "") {$name_file_max="1001"}}	
			
				open OUT, (">$dirs_news/$name_file_max\.jpg");
				 binmode (OUT);
				 while (<$image>) { print OUT "$_"; } 
				close(OUT);
				
				%configconsts = (
					'img_resize' => [$img_ox,$img_oy]	
				);

				use Image::Magick;
				
				my $image = Image::Magick->new;
				$image->Read("$dirs_news/$name_file_max\.jpg"); 
				($ox,$oy)=$image->Get('base-columns','base-rows'); 				
			
				my $size_ox = $ox;
				my $size_oy = $oy;
				
				my $division = $configconsts{'img_resize'}[0]/$configconsts{'img_resize'}[1];
				if ($configconsts{'img_resize'}[0] < $size_ox or $configconsts{'img_resize'}[1] < $size_oy) {

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
					$image->Write("$dirs_news/$name_file_max\.jpg");
				}
				else {
					$image->UnsharpMask(geometry=>geometry, radius=>0.3, sigma=>0.4, amount=>0.6, threshold=>0);
					$image->Write("$dirs_news/$name_file_max\.jpg");
				}
			}
		}
		
		my $res;
		if($num_edit) {
			$res = $pages->edit($num_edit, \%params);
			ClearCache("../..");
		} else {
			$res = $pages->add(\%params);
			ClearCache("../..");
		}		
		
		if( ref($res) eq 'ARRAY' ){
			$content_html=qq~$content_html<div class="save_page">Новость "$name" сохранена.</div>~;
			$num_edit="";
			$sel_option="";
			$sel_option_s="";
			$sel_option_html="";
			$list_older="";
		} else {
			$content_html=qq~$content_html<div class="save_page">Новость "$name" сохранена.</div>~;
			$num_edit="";
			$sel_option="";
			$sel_option_s="";
			$sel_option_html="";
			$list_older="";			
		}
		old_saves ();
		menu_listing ();
	}
	elsif ($menu_act eq "set_settings")  {
	
		$select_sort=param('select_sort');
		$limit_news=param('limit_news');
		$news_type=param('news_type');
		open OUT, (">../$dirs/sort_news");
			print OUT "$select_sort"; 
		close(OUT);
		open OUT, (">../$dirs/set_news");
			print OUT "$limit_news|$news_type"; 
		close(OUT);	

		ClearCache("../..");
	
		$content_html=qq~$content_html<div class="save_page">Настройки сохранены.</div>~;		
		old_saves();
		menu_listing ();	
	
	}
	
sub old_settings {

		open(BO, "../$dirs/sort_news"); my $select_sort = <BO>; close(BO);
		open(BO, "../$dirs/set_news"); @set_news = <BO>; close(BO);
		foreach my $line(@set_news){chomp($line);
		my ($limit_news_, $type_news_) = split(/\|/, $line);
		$ok_limit_news_old = qq~$limit_news_~; $news_type_old=qq~$type_news_~;}
		
		my $name_asc="name ASC";
		my $date_asc="date ASC";
		my $date_desc="date DESC";	

		$sort_type ='
		<option value="name ASC" '.($name_asc eq $select_sort?'selected':'').'>Названию</option>
		<option value="date ASC" '.($date_asc eq $select_sort?'selected':'').'>Дате по возрастанию</option>
		<option value="date DESC" '.($date_desc eq $select_sort?'selected':'').'>Дате по убыванию</option>';
				
}		

sub old_saves {
	use Core::DB;
	
	open(BO, "../$dirs/sort_news"); my $sort = <BO>; close(BO);	
	
	sub buildMenub
	{
		my $db = new Core::DB();
		
		my $menub = "";
		$sel_option = "";
		$result = $db->query("SELECT * FROM news WHERE parent=0 ORDER BY ".$sort.";");
		foreach my $item(@$result){
			$menub .= '<ul class="level0">';
			$menub .= '<li name="'.$item->{name}.'" c_id="'.$item->{id}.'" '.($item->{show}==1?'':'class="off"').'><span class="move" id="off"></span><a class="lamp" href="#" '.($item->{show}==1?' title="Скрыть новость"':'title="Сделать активной" style="opacity:0.5"').'></a><a href="#" class="del" title="Удалить новость '.$item->{name}.'"></a>';
			$menub .= '<a class="name" title="Страница: /news/'.$item->{alias}.'" href="?adm_act=news&num_edit='.$item->{id}.'"><em style="color:#999; font-style:normal;">'.$item->{date}.'</em> &mdash; '.$item->{name}.'</a>';
			$sel_option .= '<option value="'.$item->{id}.'" '.($parent==$item->{id}?'selected':'').'>'.$item->{name}.'</option>';
			if( my $sub = recMenu($item->{id}, 0) ){
				$menub .= $sub;
			}
			$menub .= '</li>';
			$menub .= "</ul>";
		}
		
		sub recMenu{
			my $id = shift;
			my $level = shift;
			sub nbsp { my $level = shift;my $t;for(my $i=0;$i<=($level+1)*5;$i++ ){$t.='&nbsp;';}return $t.'&mdash; ';}
			my $text = '<ul class="level'.($level+1).'">';
			
			$result = $db->query("SELECT * FROM news WHERE parent='".$id."' ORDER BY ".$sort.";");
			if($result){
				my $i_cat_old="";
				foreach my $item2(@$result){
					$i_cat_old++;
				}
				my $i_cat="";
				foreach my $item(@$result){
					$i_cat++;
					$text .= '<li name="'.$item->{name}.'" c_id="'.$item->{id}.'" '.($item->{show}==1?'':'class="off"').'><span class="move" id="off"></span><a class="lamp" href="#" '.($item->{show}==1?' title="Скрыть новость"':'title="Сделать активной" style="opacity:0.5"').'></a><a href="#" class="del" title="Удалить новость '.$item->{name}.'"></a><div class="point'.($i_cat==$i_cat_old?' last':'').'"></div>';
					$text .= '<a class="name" title="Страница: /news/'.$item->{alias}.'" href="?adm_act=news&num_edit='.$item->{id}.'"><em style="color:#999; font-style:normal;">'.$item->{date}.'</em> &mdash; '.$item->{name}.'</a>';
					#$sel_option .= '<option value="'.$item->{id}.'" '.($parent==$item->{id}?'selected':'').'>'.nbsp($level).$item->{name}.'</option>';
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
				if ($ok_maket_old ne ""){$select = $ok_maket_old;} else {$select = $maket_news;}
				$maket_item .= '<option value="'.$num.'" '.($num==$select?'selected':'').'>'.$name_old.'</option>';
			}
		}
	}

	if ($maket_item ne "" && $hide_makets ne "1"){
		$maket_list = '
			<tr class="help_maket">
				<td class="name">Привязать новость к макету</td>
				<td>
					<select class="category" name="maket" style="width:197px;">
						'.$maket_item.'
					</select>
				</td>
			</tr>';
	}	
	
	if ($hide_news_photo ne "1"){
	open(BO, "$dirs_news/settings.txt"); my @categories = <BO>; close(BO);
		foreach my $linee(@categories)
			{
		chomp($linee);
		my ($img_ox_, $img_oy_) = split(/\|/, $linee);
		$img_ox=qq~$img_ox_~;
		$img_oy=qq~$img_oy_~;
			}		
	}

	$img_load=""; $img_load_param="";
	if ($hide_news_photo ne "1"){
		$rand_num=rand(1);
		my $img_num = $num_edit+1000;
		if(-e "$dirs_news/$img_num.jpg")
		{$image =qq~<img src="$dirs_news_www/$img_num.jpg?$rand_num" border="0">~;}
		else { $image = "";}
		
		$img_load ='
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
				
		$img_load_param =qq~
				<tr class="autoresize">
					<td class="name">Авторазмер картинки</td><td><input class="size" type="text" name="img_ox" value="$img_ox" size=10><input class="size" type="text" name="img_oy" value="$img_oy" size=10></td>
				</tr>~;
	}	

}


sub menu_listing {

$dshfgkjdf=qq~<td class="name">Соответствие разделу<em>*</em></td><td><select name="parent" id="category"><option value="0">Верхний уровень</option>$sel_option</select></td>~;

if ($settings eq "set") {

	sub menu_settings {

		$list_older="";
		old_settings();

		$content_html.= '
		<script type="text/javascript" src="/admin/lib/help/news/news_settings.js"></script>
		<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
		<input type="hidden" name="adm_act" value="news">
		<input type="hidden" name="menu_act" value="set_settings">
					<table id="page_new" style="margin-bottom:0px;">
					<tr>
						<td class="name"></td><td class="name_main">Настройки модуля</td>
					</tr>
					<tr class="help_count">
						<td class="name">Выводить новостей</td><td><input type="text" name="limit_news" value="'.$ok_limit_news_old.'" class="normal"></td>
					</tr>					
					<tr class="help_sort">
						<td class="name">Сортировать новости по</td><td><select name="select_sort" id="category">'.$sort_type.'</select></td>
					</tr>
					<tr class="help_theme">
						<td class="name">Тема оформления</td>
						<td>
							<select class="category" name="news_type" style="width:197px;">
								<option value="gray"'.($news_type_old eq "gray"?' selected':'').'>Серый</option>
								<option value="green"'.($news_type_old eq "green"?' selected':'').'>Зеленый</option>
								<option value="blue"'.($news_type_old eq "blue"?' selected':'').'>Синий</option>
								<option value="purple"'.($news_type_old eq "purple"?' selected':'').'>Фиолетовый</option>
								<option value="red"'.($news_type_old eq "red"?' selected':'').'>Красный</option>								
							</select>
						</td>
					</tr>					
					</table>
					
		<input style="margin-left:554px;" type="submit" name="save" value="Сохранить" class="button" />			
		</form>
		';
	}
	menu_settings();
}

if ($par eq "new") {$content_html.= qq~
<script type="text/javascript" src="/admin/lib/help/news/news_edit.js"></script>
<div class="three_pages" style="display:none;">$list_older</div>
<div id="pages_new" style="margin-left:23px;">
$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">
			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Новая новость</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
$img_load			
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>				
			<tr>
				<td class="name">Дата публикации</td><td><input name="date" id="date_edit" value="$today" type="text" class="date"></td>
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
				<td class="name">Адрес новости</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>
				$maket_list
				$img_load_param		
			<tr>
				<td class="name"></td><td class="show"></td>
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

	<h3 style="margin-top:0px;">Краткое содержание</h3>		
	<textarea id="elm1_sm" name="elm1_sm" rows="15" cols="80" class="tinymce">@ok_elm_sm_old</textarea>
	
	<h3>Полное содержание</h3>
	<textarea id="elm1" name="elm1" rows="20" cols="80" class="tinymce">@ok_elm_old</textarea>
	
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<input type="submit" name="save" value="Сохранить" class="button" />
	<input type="reset" name="reset" value="Очистить" class="button" />
</form>
</div>~;
} else {


	if ($num_edit eq ""){
		if ($settings ne "set"){
			$content_html .=qq~<script type="text/javascript" src="/admin/lib/help/news/news.js"></script>
			<div class="three_pages">$list_older</div>~;	
		}
	} else {
		$content_html=qq~$content_html
		<script type="text/javascript" src="/admin/lib/help/news/news_edit.js"></script>
		<div class="three_pages" style="display:none;">$list_older</div>
		<div id="pages_old" style="margin-left:23px;">
		$tiny_mce
<form method="post" action="/cgi-bin/admin/engine/index.cgi" enctype="multipart/form-data">
<input type="hidden" name="num_edit" value="$num_edit">
<input type="hidden" name="adm_act" value="$adm_act">
<input type="hidden" name="menu_act" value="ok">

			<table id="page_new">
			<tr>
				<td class="name"></td><td class="name_main">Редактирование новости</td>
			</tr>
			<tr class="help_name">
				<td class="name">Название<em>*</em></td><td><input type="text" name="name" format=".+" notice="Введите название" value="$ok_name_old"></td>
			</tr>
$img_load			
			<tr style="display:none;">
				<td class="name">Порядок сортировки</td><td><input type="text" name="sort" value="$ok_sort_old" class="sort"></td>
			</tr>			
			<tr>
				<td class="name">Дата публикации</td><td><input name="date" id="date_edit" value="$today" type="text" class="date"></td>
			</tr>
			<tr class="help_show_menu">
		<td class="name">Показывать новость</td><td class="show"><input name="show" type="checkbox" class="cb" ~;
		if($ok_show_old){
			$content_html.= qq~ checked > </td></tr> ~;
		} 




	}
	
		if($num_edit){
$content_html.= qq~
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
				<td class="name">Адрес новости</td><td><input name="alias" value="$ok_alias_old" type="text"></td>
			</tr>
			
				$maket_list
				$img_load_param	
				
			<tr class="redirect">
				<td class="name">Редирект 301</td><td>
					<div>Например: <em><span>/</span>news<span>/</span>novaya</em></div>
					<input name="redirect" type="text" value="$ok_redirect_old"></td>
			</tr>			
			<tr class="help_header">

				<td class="name">Отображать заголовок новости</td><td class="show"><input name="show_head" type="checkbox" class="cb"~;
		if($ok_show_head_old){
			$content_html.= qq~ checked~;
		} 
			$content_html.= qq~></td></tr> 
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
			
	<h3 style="margin-top:0px;">Краткое содержание</h3>		
	<textarea id="elm1_sm" name="elm1_sm" rows="15" cols="80" class="tinymce">@ok_elm_sm_old</textarea>
	
	<h3>Полное содержание</h3>
	<textarea id="elm1" name="elm1" rows="20" cols="80" class="tinymce">@ok_elm_old</textarea>
	
	<div class="field"><span class="st">*</span> поля обязательные для заполнения.</div>
	<input type="submit" name="save" value="Сохранить" class="button" />
	<input type="reset" name="reset" value="Очистить" class="button" />
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