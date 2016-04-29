$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: '�������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_sort',
			  intro: '������� ���������� ��������',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_parent',
			  intro: '���������� �������������� ������ �������� � ��� ������������ ���������, �������� ������� ������� �������� �����������. ���� �� ��������� ��������� ���������, �������� �������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_show_menu',
			  intro: '���������, ���������� / �� ���������� �������� � ���� �� �����',
			  position: 'bottom'
			},				
			{
			  element: 'table#page_new tr.help_feedback',
			  intro: '�������� � ����� �������� �������� �����. ������� ����� ��� ������ ����� �������� � ������ �<a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=settings">���������</a>�',
			  position: 'bottom'
			},		
			{
			  element: 'table#page_new tr.help_sitemap',
			  intro: '������� �������� ������ �����',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new td.name a.ext',
			  intro: '�������� ����������� ��������� �������� (���� ��������� � ���)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: '����� �������� (alias)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_maket',
			  intro: '����� �������� ����� ����������� � ������ (HTML-�������). ������� ����� ��������� / ������������� �� <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">������</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: '����������� ������� ������������� �������� (�������� 301)',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_header',
			  intro: '���������� / �� ���������� ��������� �������� (H1). ������ ��������� ������� ������ &lt;h1&gt;���������&lt;/h1&gt; �������� �� �������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide',
			  intro: '����������� ������ �������� �� �����������. �� ������ �������� ���� ����� �������� 404 �������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_hide_child',
			  intro: '����������� �������� �� ���� ���������� ������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide_child_count',
			  intro: '���������� ���������� �����������, ��� �������� ���������� ����� ������ ���',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: '�������������� ������ �������� (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: '�������������� Meta Description ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: '�������������� Meta Keywords ��������',
			  position: 'bottom'
			},
			{
			  element: 'span.mceEditor',
			  intro: '�������� ������. � ��� �������� ���, ��� �������� ������, ��������, ������, ������ � �.�.',
			  position: 'top'
			},
			{
			  element: 'div.save_content div.check_save',
			  intro: '����������� ����������� ���������� ��������, ��� ����� �������� ����� � ������� ���������',
			  position: 'top'
			},
			{
			  element: 'div.save_content a.preview_page',
			  intro: '������������ ��������, �������������� �������� ����������',
			  position: 'top'
			},		
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: '������� � ���������� ������ �������',
			  position: 'bottom'
			},
			{
			  element: 'a#click_pages',
			  intro: '�� ������������ ��������, �������� ������� � ������� �������',
			  position: 'bottom'
			}			
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		$("table.ext_param").fadeIn(600);
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});