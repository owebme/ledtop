$(document).ready(function(){

	var help_search = '��������� ������ � ����� ����������� (����� �����������). �� ���� ����� �� ������ ������������� �������� � ������� ���� � ������� ������������, ����� ������ ������� �������� ������������ ��� ����� �����������, ���������� ����� ����������� � �������� ����� � ���';
	
	if (!$("div.yaimages div.search").length){
		help_search = '������ ������� ������������� ��� ������ ����������� (����� �����������). ���������� ����� ����������� � �������� ����� � ���. �� ���� ����� �� ������ ������������� �������� � ������� ���� � ������� ������������';
	}

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.products_add_table table',
			  intro: '������� ��� ������ � ��������',
			  position: 'top'
			},
			{
			  element: 'div.yaimages div.search',
			  intro: '����� �� ���� �����������',
			  position: 'bottom'
			},
			{
			  element: 'div.yaimages div.container_slider div.images',
			  intro: help_search,
			  position: 'top'
			},
			{
			  element: 'div.yaimages div.add_images div.input',
			  intro: '���������� �������� � ����� ����������� ����� ������',
			  position: 'left'
			},			
			{
			  element: 'div.products_add_table table tr#first td.foto',
			  intro: '�������� ��� ����� �������� ��� ���������� �������� �� �������� �����, ����� �������� ������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'div.products_add_table td.help_foto',
			  intro: '��������� �������� �������� 4-�� ���������: 1) �������� � ��� ������� � ������� ���� 2) ���������� �������� �� ����� ����������� ���� 3) ���������� ���� ����������� � �������� �����<br> 4) ����������� ����� �������� � ��������� � �������� �� ��������� Ctrl+V',
			  position: 'bottom'
			},
			{
			  element: 'div.products_add_table div.batch_add',
			  intro: '����� ��������� ������������� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.batch_csv',
			  intro: '� ��� ����� ���� ����������� ��������� � ��������� ����� ������ �������� � ������� CSV',
			  position: 'left'
			},	
			{
			  element: 'a.multi-add.back',
			  intro: '��������� � �������� �������',
			  position: 'bottom'
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
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});