$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: '��������� ��� ������� ���������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_theme',
			  intro: '���� ���������� ������������� ����',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_script',
			  intro: '����������� ������������� ���, �������� ����� ��� ����������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_show_all',
			  intro: '�������� ��� ���������� �� ���� ����������� �� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_hide_resize',
			  intro: '��������� �������������� ����������� ��� ����������� ����������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new div.watermark-settings div.watermark-img',
			  intro: '�������� � ��� ����, ����� ������� ���� �������� ����� ��� ������� ���� ����� ������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new div.watermark-fonts div.container',
			  intro: '�� ������ ������������ ���� ����� ��� ��������� �������� ����� �� ����������',
			  position: 'left'
			},	
			{
			  element: 'table#page_new tr.help_watermark_pos',
			  intro: '������������ ��������� �������� �����',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_opacity',
			  intro: '�������� ������������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_watermark_type',
			  intro: '����������� ��������� �� ������� � ��������� ����������',
			  position: 'bottom'
			}			
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});