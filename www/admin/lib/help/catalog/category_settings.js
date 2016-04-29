$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_sort_category',
			  intro: '����� ������� ���������� ��� ���������: �� ��������, ��������, ����',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_sort_products',
			  intro: '����� ������� ���������� ��� �������: �� ��������, ��������, ����, ����',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new tr.help_wide_review',
			  intro: '�������� ������� �� ��� ������ ��������, ������ ��������� ���������� � Select',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_count_products_cms',
			  intro: '���������� ��������� ������� �� ����� �������� � CMS',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_count_products_site',
			  intro: '���������� ��������� ������� �� ����� �������� �� �����',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_add_photo',
			  intro: '���������� �������������� ���������� � ������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_desc',
			  intro: '����������� ������������� �������� ��������� ��� �������� � ��� ��������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_ext_desc_products',
			  intro: '��� ������, �������� ������ ����������� �� ��� ����������: ������ �� ���������� ������ (������� ��������) � ���� ��� ����������� (������ ��������). �������� �����, �������� � ������ ����� ��������� ������ ��� ��� �����������.',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new div.help_hide_photo_settings',
			  intro: '�� ��������� �������� ��������� ����������� ������: HDR, ��������, �������������, ������������ � �.�.',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new tr.help_quick_save',
			  intro: '����������� �������� ���������� �������� ��� ������������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new div.watermark-settings div.watermark-img',
			  intro: '�������� � ��� ����, ����� ������� ���� �������� ����� ��� ������� ���� ����� ������',
			  position: 'top'
			},	
			{
			  element: 'table#page_new div.watermark-fonts div.container',
			  intro: '�� ������ ������������ ���� ����� ��� ��������� �������� ����� �� ����������',
			  position: 'left'
			},	
			{
			  element: 'table#page_new tr.help_watermark_pos',
			  intro: '������������ ��������� �������� �����',
			  position: 'top'
			},	
			{
			  element: 'table#page_new tr.help_opacity',
			  intro: '�������� ������������',
			  position: 'top'
			},	
			{
			  element: 'table#page_new tr.help_watermark_type',
			  intro: '����������� ��������� �� �������, ������� � ��������� ����������',
			  position: 'top'
			}			
		]
	});
	
	$("a#help-tour").live('click', function(){
		introguide.start();
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});