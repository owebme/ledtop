$(document).ready(function(){

	var help_desc = '�������������� �������� �������� ������ (�����)';
	if ($("textarea").length == "2"){
		help_desc = '�������������� ������� �������� ������';
	}

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'a.multi-add',
			  intro: '�������� ���������� �������',
			  position: 'bottom'
			},
			{
			  element: 'td.help_photo_big',
			  intro: '������� ���������� ������. �� ������ ����� � ��������� ���������� � ������, ����������� �� ����� � �����, ����� ������� ������ �� ��� ���� � ������ Ctrl+V, ����� ���� ���������� ������������� ����������',
			  position: 'right'
			},			
			{
			  element: 'p.help_auto_small',
			  intro: '�������� ��������� ���������� �� �������',
			  position: 'bottom'
			},
			{
			  element: 'td.help_photo_small',
			  intro: '����� ���������� ������. ����� ���������� ���������� �� ������� �������� � ����������� �����������, � ����� �������� ����������� ��� �������������',
			  position: 'right'
			},		
			{
			  element: 'table#page_new tr.help_name',
			  intro: '�������� ������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_parent',
			  intro: '�������� �������������� ������� ������ � ���������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_price',
			  intro: '���� ������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_price_old',
			  intro: '������ ���� ������',
			  position: 'bottom'
			},				
			{
			  element: 'table#page_new tr.help_art',
			  intro: '������� ������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_avail',
			  intro: '������� ������ �� ������',
			  position: 'bottom'
			},				
			{
			  element: 'table#page_new tr.help_show',
			  intro: '���������, ���������� / �� ���������� ����� �� �����',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_hit',
			  intro: '�������� ����� � ���� �� ������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_spec',
			  intro: '�������� ����� � ����. ����������� �� ������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_new',
			  intro: '�������� ����� � ������� �� ������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new a.open_settings',
			  intro: '�������� ��������� �����������',
			  position: 'top'
			},
			{
			  element: 'table#page_new div.foto_settings',
			  intro: '����������� ���������� ��� ������ � �������������: ����������� �����, ��������������� ������ ������, ������ �������� ����� �����������',
			  position: 'top'
			},
			{
			  element: 'table#page_new a.show_autoresize',
			  intro: '�������� ��������� ��������������� ��������� ����������� (���� ��������� � ���)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_resize_big',
			  intro: '�������������� ������ ����������� ������� ���������� (������ / ������)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_resize_small',
			  intro: '�������������� ������ ����������� ����� ���������� (������ / ������)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new span.help_crop',
			  intro: '�������� ��� ������������� ���� �����������, ������� ������������� ������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_resize_more',
			  intro: '�������������� ������ �������������� ���������� (������ / ������)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_desc_small',
			  intro: '������� �������� ������ (�����������)',
			  position: 'bottom'
			},	
			{
			  element: 'tr.help_recomend',
			  intro: '���������� ������������� ������� � ��������� � ������� ������ (������������ � ��������� �������� ������)',
			  position: 'right'
			},
			{
			  element: 'table#page_new tr.help_add_params a.ext',
			  intro: '�������� ����������� ��������� ������ (���� ��������� � ���)',
			  position: 'top'
			},
			{
			  element: 'table#page_new tr.help_add_photo',
			  intro: '�������������� ���������� � ������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_products_reviews',
			  intro: '������ �����������. ��� ����� ��������� ������ � ����� ��� ���������. �� ����� ����� ��������� ���� ������',
			  position: 'left'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: '����� ������ (alias)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_maket',
			  intro: '����� ����� ����� ����������� � ������ (HTML-�������). ������� ����� ��������� / ������������� �� <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">������</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: '����������� ������� ������������� ������ (�������� 301)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_header',
			  intro: '���������� / �� ���������� ��������� ������ (H1). ������ ��������� ������� ������ &lt;h1&gt;���������&lt;/h1&gt; �������� �� �������� ������',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: '�������������� ������ ������ (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: '�������������� Meta Description ������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: '�������������� Meta Keywords ������',
			  position: 'bottom'
			},			
			{
			  element: 'span#elm1_sm_parent',
			  intro: help_desc,
			  position: 'top'
			},
			{
			  element: 'span#elm1_parent',
			  intro: '�������������� ������� �������� ������',
			  position: 'top'
			},	
			{
			  element: 'div.save_content div.check_save',
			  intro: '����������� ����������� ���������� ��������, ��� ����� �������� ����� � ������� ���������',
			  position: 'top'
			},
			{
			  element: 'div.save_content a.preview_page',
			  intro: '������������ ������, �������������� �������� ����������',
			  position: 'top'
			},			
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: '������� � ���������� ������ ������� �������',
			  position: 'bottom'
			}
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		$("div.foto_settings").fadeIn(600);
		$("table.ext_param").fadeIn(600);
		$("table.autoresize").fadeIn(600);
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});