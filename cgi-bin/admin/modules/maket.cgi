	$menu_act=param('menu_act');
	$num_edit=param('num_edit');
	$css_edit=param('css_edit');

if ($css_edit eq "ok") {$active_css=qq~activetab~;} elsif ($num_edit) {$active_maket=qq~activetab~;} else {$active_css=qq~activetab~;}	

open IN, ("../$dirs/set_screen");
my $result = <IN>; close(IN);
if ($result eq "1"){	
	$content_html .=qq~
	<script type="text/javascript">
	\$(function(){
			var maketsH = parseInt(\$("div.makets").height())-46;
			var windowH = parseInt(\$(window).height()-96-maketsH);
			\$("div.CodeMirror").height(windowH+"px");
			\$('html, body').animate({scrollTop:0}, 0);
			\$("div#content").css("min-height", "0");
			\$("body").css("overflow", "hidden");
	});
	</script>~;
}
	
$content_html=qq~$content_html
<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs" class="wide">
				<ul>
					<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=settings"><span>Настройки</span></a></li>
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=backup"><span>Восстановление</span></a></li>~;
	if ($hide_banners ne "1") {
		$content_html=qq~$content_html<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=banners"><span>Баннеры</span></a></li>~;
	}
	$content_html=qq~$content_html						
					<li class="$active_maket"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1"><span>Макет сайта</span></a></li>
					<li class="$active_css"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&css_edit=ok"><span>Cтили сайта</span></a></li>~;
	if ($hide_templates ne "1") {
		$content_html=qq~$content_html<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=template"><span>Модули</span></a></li>~;
	}
$content_html=qq~$content_html	
				</ul>
			</div>
			
			
		</div>

		</td>
		<td rowspan="3" id="rside"><div id="rtbg"></div></td>
	</tr>
	<tr>
		<td id="contenttd">
		<div id="content">
		<div id="pages" class="template~; if ($result eq "1"){$content_html .=qq~ fullscreen~;}
		$content_html .=qq~">~;	

	
	($sec, $min, $hour, $mday, $mon, $year, $nedela, )=localtime;
	if ($mday < 10 ) { $mdays="0"; $mday="$mdays$mday";}
	$mon++; if ($mon < 10 ) { $mon="0$mon";}
	$year=1900+$year; 
	$today="$year-$mon-$mday";

	if ($menu_act eq "") {
		$list_older="";
		old_saves ();
		menu_listing ();
	} elsif ($menu_act eq "ok")  {

		$name=param('name');	
		$elm1=param('elm1');

		if ($num_edit ne "") {$max_num=$num_edit} else {$max_num++;}

		open OUT, (">../$dirs/$adm_act.$max_num");
			print OUT "$name|$key"; 
		close(OUT);
		open OUT, (">../$dirs/$adm_act\_html.$max_num");
			print OUT "$elm1"; 
		close(OUT);
		$content_html=qq~$content_html<div class="save_page">Шаблон "$name" сохранен.</div>~;
		$list_older="";
		old_saves ();
		menu_listing ();

	} elsif ($menu_act eq "css")  { 	

		$name=param('name');	
		$elm1=param('elm1');
		
		open OUT, (">$dirs_css");
			print OUT "$elm1"; 
		close(OUT);
		$content_html=qq~$content_html<div class="save_page">Стили сохранены.</div>~;
		$list_older=""; 	
		old_saves_css (); 
		menu_listing ();
	} 
	
sub old_saves_css {
	$css1=qq~$css1<input type="hidden" name="menu_act" value="css">~;
	open (BO, "$dirs_css"); @ok_elm_old = <BO>; close (BO);
	foreach my $text(@ok_elm_old) {$ok_elm_old=qq~$ok_elm_old$text~;}

}	

sub old_saves {
			
	opendir (DBDIR, "../$dirs"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $num) = split(/\./, $line_wall);
			if ($max_num < $num) {$max_num=$num;}
			if ($name_file eq "$adm_act") { 
				open (BO, "../$dirs/$line_wall"); @b = <BO>; close (BO);
				($name_old, $date_old) = split(/\|/, $b[0]);
				if ($num_edit eq $num) {
					open (BO, "../$dirs/$name_file\_html.$num"); @ok_elm_old = <BO>; close (BO);
					foreach my $text(@ok_elm_old) {$ok_elm_old=qq~$ok_elm_old$text~;}
					$ok_elm_old =~ s/</&lt;/g;
					$ok_elm_old =~ s/>/&gt;/g;
					$ok_elm_old =~ s/	/    /g;
					$ok_name_old=$name_old;
					$today=$date_old;
				}
				$list_older .= '<a '.($num_edit==$num?'class="active"':'').' href="?adm_act='.$adm_act.'&num_edit='.$num.'">'.$name_old.'</a>';
			}
		}
	}
	
	if ($list_older ne ""){
		$list_older = '<div class="makets">'.$list_older.'';
		if ($hide_makets ne "1"){$list_older .= '<a href="#" class="create">Создать макет</a>';}
		$list_older .= '<div class="clear"></div></div>';
	}

	if ($css_edit eq "ok") {

		$save_button='save_css';

		open (BO, "$dirs_css"); @ok_elm_old = <BO>; close (BO);
		foreach my $text(@ok_elm_old) {$ok_elm_old=qq~$ok_elm_old$text~;}
		$css1=qq~$css1<input type="hidden" name="menu_act" value="css">~;
		
				$script_js=qq~<script type="text/javascript" src="/admin/lib/help/settings/styles.js"></script>
				<link rel="stylesheet" href="/admin/js/codemirror/mode/css/css.css">
				<script src="/admin/js/codemirror/mode/css/css.js"></script>
				<script>			
				var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
						mode: {name: "css"},		
						lineNumbers: true,
						matchBrackets: false,
						enterMode: 'keep',
						indentWithTabs: false,
						indentUnit: 1,
						tabMode: 'classic',
						continuousScanning: 500,
						onCursorActivity: function() {
							editor.setLineClass(hlLine, null);
							hlLine = editor.setLineClass(editor.getCursor().line, "activeline");
						}
					});
					var hlLine = editor.setLineClass(0, "activeline");
				</script>~;
			
	} else {

		$save_button='save_maket';
		$css1=qq~$css1<input type="hidden" name="menu_act" value="ok">~;

		$script_js=qq~<script type="text/javascript" src="/admin/lib/help/settings/makets.js"></script>
		<link rel="stylesheet" href="/admin/js/codemirror/mode/xml/xml.css">
		<script src="/admin/js/codemirror/mode/xml/xml.js"></script>
		<script>
		var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
				mode: {name: "xml", htmlMode: true},				
				lineNumbers: true,
				matchBrackets: false,
				enterMode: 'keep',
				indentWithTabs: false,
				indentUnit: 1,
				tabMode: 'classic',
				continuousScanning: 500,
				onCursorActivity: function() {
					editor.setLineClass(hlLine, null);
					hlLine = editor.setLineClass(editor.getCursor().line, "activeline");
				}
			});
			var hlLine = editor.setLineClass(0, "activeline");
				
		</script>~;
	}

}


sub menu_listing {

	if ($css_edit ne "ok") {
		$content_html .=qq~$list_older~;
	}
		$content_html=qq~$content_html
		<link rel="stylesheet" href="/admin/js/codemirror/lib/codemirror.css">
		<script src="/admin/js/codemirror/lib/codemirror.js"></script>
		<script src="/admin/js/codemirror/lib/overlay.js"></script>
		<script src="/admin/lib/maket.js"></script>	
		
		<div class="maket"><div style="text-align:right; margin-top:-8px; margin-bottom:7px;"><div class="save_maket"></div>~;
	if ($css_edit ne "ok" && $num_edit ne "1" && $num_edit ne "404") {
		$content_html .=qq~<a href="#" name="del" class="del_maket button" id_maket="$num_edit" />Удалить макет</a>~;
	}	
		$content_html=qq~$content_html
		<a href="#" name="save" class="$save_button button" id_maket="$num_edit" />Сохранить</a></div>
		<div class="clear"></div><div class="bg"><textarea id="code" name="elm1">$ok_elm_old</textarea></div></div><br>

		$script_js

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