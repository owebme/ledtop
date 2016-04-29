	$menu_act=param('menu_act');
	
$content_html=qq~$content_html
<table id="sheet">
	<tr>
		<td rowspan="3" id="lside"><div id="ltbg"></div></td>
		<td id="sheettoptd">

		<div id="sheettop">
		
		
			<div id="tabs" class="wide">
				<ul>
					<li class="first"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=settings"><span>Настройки</span></a></li>
					<li class="activetab"><a href="/cgi-bin/admin/engine/index.cgi?adm_act=backup"><span>Восстановление</span></a></li>~;
	if ($hide_banners ne "1") {
		$content_html=qq~$content_html<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=banners"><span>Баннеры</span></a></li>~;
	}
	$content_html=qq~$content_html					
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1"><span>Макет сайта</span></a></li>
					<li><a href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&css_edit=ok"><span>Cтили сайта</span></a></li>~;
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
		<div id="backup">~;	

		
$content_html=qq~$content_html
<script type="text/javascript" src="/admin/lib/help/settings/backup.js"></script>
<iframe class="help_mysql" src="/admin/backup/backup_base.php" style="width:413px; height:600px; border:none;" frameborder="0"></iframe>
<iframe class="help_files" src="/admin/backup/backup_files.php" style="width:483px; height:600px; border:none;" frameborder="0"></iframe>
	
		</div>
		</div>
		</td>
	</tr>
	<tr>
		<td id="sheetbottomtd"></td>
	</tr>
</table>~;


ClearCache("../..");

-1;