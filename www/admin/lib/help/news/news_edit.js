$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: '�������� �������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_image',
			  intro: '������� �������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_image_url',
			  intro: '�� ������ �������� ������ �� �������� � ���������, ����� ���� ��� ������������� ����������',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_show_menu',
			  intro: '���������, ���������� / �� ���������� ������� �� �����',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new td.name a.ext',
			  intro: '�������� ����������� ��������� ������� (���� ��������� � ���)',
			  position: 'top'
			},			
			{
			  element: 'table#page_new tr.help_alias',
			  intro: '����� ������� (alias)',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_maket',
			  intro: '����� ������� ����� ����������� � ������ (HTML-�������). ������� ����� ��������� / ������������� �� <a target="_blank" href="/cgi-bin/admin/engine/index.cgi?adm_act=maket&num_edit=1">������</a>',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.autoresize',
			  intro: '�������������� ������ ����������� �������� (������ � ������ � px)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.redirect',
			  intro: '����������� ������� ������������� ������� (�������� 301)',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_header',
			  intro: '���������� / �� ���������� ��������� ������� (H1). ������ ��������� ������� ������ &lt;h1&gt;���������&lt;/h1&gt; �������� �� �������� �������',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_meta-title',
			  intro: '�������������� ������ ������� (title)',
			   position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-desc',
			  intro: '�������������� Meta Description �������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_meta-key',
			  intro: '�������������� Meta Keywords �������',
			  position: 'bottom'
			},
			{
			  element: 'span#elm1_sm_parent',
			  intro: '�������������� �������� ���������� ������� (�����)',
			  position: 'top'
			},
			{
			  element: 'span#elm1_parent',
			  intro: '�������������� ������� ���������� �������',
			  position: 'top'
			},	
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: '������� � ���������� ������ ��������',
			  position: 'bottom'
			},
			{
			  element: 'a#click_pages',
			  intro: '�� ������������ ��������, �������� ������� � ������� ��������',
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