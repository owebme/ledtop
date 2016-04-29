	
	$file=param('file');
	
open IN, ("../$dirs/set_screen");
my $result = <IN>; close(IN);
if ($result eq "1"){	
	$content_html .=qq~
	<script type="text/javascript">
	\$(function(){
			var maketsH = parseInt(\$("div.makets").height())-46;
			var windowH = parseInt(\$(window).height()-96-maketsH);
			\$("div.CodeMirror").height(windowH+"px");
			\$("div.CodeMirror .CodeMirror-scroll").css("max-height", windowH+"px");
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
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1"><span>Макет сайта</span></a></li>
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&css_edit=ok"><span>Cтили сайта</span></a></li>
					<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=template"><span>Модули</span></a></li>					
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
	
	my $num="";
	if ($dirs_img eq "../../../uploads"){$dirs_main = "../../..";} else {$dirs_main = "../../../$dirs_site";}
	opendir (DBDIR, "../../templates"); @list_dir = readdir(DBDIR); close DBDIR;
	foreach $line_wall(@list_dir) {
		chomp ($line_wall);
		if ($line_wall ne "." && $line_wall ne "..") {
			($name_file, $exec) = split(/\./, $line_wall);
			if ($exec eq "cgi") {
				if ($name_file eq "pages" && !-e "../modules/strukture.cgi"){$list_older .='';}
				elsif ($name_file eq "news" && !-e "../modules/news.cgi"){$list_older .='';}
				elsif ($name_file eq "articles" && !-e "../modules/articles.cgi"){$list_older .='';}
				elsif ($name_file eq "catalog" && !-e "../modules/category.cgi"){$list_older .='';}
				elsif ($name_file eq "products" && !-e "../modules/products.cgi"){$list_older .='';}
				elsif ($name_file eq "products_hit" && !-e "../modules/products.cgi"){$list_older .='';}
				elsif ($name_file eq "products_hit" && -e "../modules/products.cgi" && $hide_products_hit eq "1" && $hide_products_spec eq "1" && $hide_products_new eq "1"){$list_older .='';}
				elsif ($name_file eq "products_compare" && $hide_products_compare eq "1"){$list_older .='';}
				elsif ($name_file eq "products_recomend" && $hide_products_recomend eq "1"){$list_older .='';}
				elsif ($name_file eq "products_related" && $hide_products_navigation eq "1" && $hide_products_related eq "1"){$list_older .='';}
				elsif ($name_file eq "products_viewed" && $hide_products_viewed eq "1"){$list_older .='';}
				elsif ($name_file eq "products_random" && $hide_products_random eq "1"){$list_older .='';}
				elsif ($name_file eq "basket" && !-e "../modules/orders.cgi"){$list_older .='';}
				elsif ($name_file eq "basket_ajax" && !-e "../modules/orders.cgi"){$list_older .='';}
				elsif ($name_file eq "gallery" && !-e "../modules/fotolist.cgi"){$list_older .='';}
				elsif ($name_file eq "gallery_lite" && $hide_gallery_lite eq "1"){$list_older .='';}
				elsif ($name_file eq "banners" && $hide_banners eq "1"){$list_older .='';}
				elsif ($name_file eq "slideshow" && $hide_slideshow_edit eq "1"){$list_older .='';}
				elsif ($name_file eq "questions" && !-e "../modules/questions.cgi"){$list_older .='';}
				elsif ($name_file eq "valuta" && !-e "$dirs_main/valuta"){$list_older .='';}
				elsif ($name_file eq "pogoda" && !-e "$dirs_main/pogoda"){$list_older .='';}
				elsif ($name_file eq "metal" && !-e "$dirs_main/metal"){$list_older .='';}
				elsif ($name_file eq "fadepage"){$list_older .='';}
				elsif ($name_file eq "sitemap"){$list_older .='';}
				elsif ($name_file eq "callback" && $hide_callback eq "1"){$list_older .='';}
				elsif ($name_file eq "auth" && $hide_private eq "1"){$list_older .='';}
				elsif ($name_file eq "private" && $hide_private eq "1"){$list_older .='';}
				else {
					$num++;
					if ($file ne ""){$n_file = $file;}
					if ($num eq "1"){
						if ($file eq ""){$n_file = $name_file;}
						open (BO, "../../templates/$n_file.cgi"); @ok_elm_old = <BO>; close (BO);
						foreach my $text(@ok_elm_old) {$ok_elm_old=qq~$ok_elm_old$text~;}
						$ok_elm_old =~ s/</&lt;/g;
						$ok_elm_old =~ s/>/&gt;/g;
						$ok_elm_old =~ s/	/    /g;
						if ($file eq ""){$file = $name_file;}
					}					
					$list_older .= '<a id="help_'.$name_file.'" '.($file eq $name_file?'class="active"':'').' href="?adm_act='.$adm_act.'&file='.$name_file.'">'.$name_file.'.cgi</a>';
				}
			}
		}
	}
	
	if ($list_older ne ""){
		$list_older = '<div class="makets">'.$list_older.'';
		if ($hide_templates_opt ne "1"){$list_older .= '<a href="#" class="create">Создать еще...</a>';}
		$list_older .= '<div class="clear"></div></div>';
	}

	$script_js=qq~
	<script type="text/javascript" src="/admin/lib/help/settings/templates.js"></script>
	<script src="/admin/js/codemirror/mode/perl/perl.js"></script>
	<script>
		var editor = CodeMirror.fromTextArea(document.getElementById("code"), {				
				lineNumbers: true,
				lineWrapping: true,
				matchBrackets: false,
				enterMode: 'keep',
				indentWithTabs: false,
				indentUnit: 1,
				tabMode: 'classic',
				continuousScanning: 500,
  onCursorActivity: function() {
    editor.setLineClass(hlLine, null, null);
    hlLine = editor.setLineClass(editor.getCursor().line, null, "activeline");
  }
});
var hlLine = editor.setLineClass(0, "activeline");
			\$("div.CodeMirror").addClass("CodeMirror-wrap");
	</script>~;
	
	if ($hide_templates eq "1"){
		$content_html ='
		<script type="text/javascript">
		<!--
		location.replace("http://'.$ENV{"HTTP_HOST"}.'/cgi-bin/admin/engine/index.cgi?adm_act=template_none");
		//-->location.replace(
		</script>
		<noscript>
		<meta http-equiv="refresh" content="0; url=http://'.$ENV{"HTTP_HOST"}.'/cgi-bin/admin/engine/index.cgi?adm_act=template_none">
		</noscript>';
	}	

	$content_html=qq~$content_html $list_older
	<link rel="stylesheet" href="/admin/js/codemirror/lib/perl/codemirror.css">
	<script src="/admin/js/codemirror/lib/perl/codemirror.js"></script>
	<script src="/admin/lib/template.js"></script>	
	
	<div class="maket">
		<div style="text-align:right; margin-top:-8px; margin-bottom:7px;">
			<div class="save_maket"></div>~;
			if ($hide_templates_opt ne "1"){$content_html .=qq~<a href="#" name="del" class="del_maket button" file="$file" />Удалить</a>~;}
			$content_html .=qq~<a href="#" name="save" class="save_maket button" file="$file" />Сохранить</a>
		</div>
		<div class="clear"></div>
		<div class="bg"><textarea id="code" name="elm1">$ok_elm_old</textarea></div>
	</div><br>

	$script_js

		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;


-1;