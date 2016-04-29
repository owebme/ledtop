$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div#choice-banner',
			  intro: '����� �������������� �������',
			  position: 'bottom'
			},		
			{
			  element: 'table.banners-img td.help_img1',
			  intro: '������ ������� �����������, ����� ��� �������� �����������. ������� �� �����������, �������� ���������� ��� ������ �������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-img td.help_img2',
			  intro: '������ ������� �����������, ����� ��� �������� �����������. ������� �� �����������, �������� ���������� ��� ������ �������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-img td.help_bg div.img div.foto',
			  intro: '������ �������� ����������� �������. ������� �� �����������, �������� ���������� � ����� ������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-text',
			  intro: '��������� ����������',
			  position: 'top'
			},
			{
			  element: 'div.repeat',
			  intro: '����� ���������, ����� ������� ������ �������� ���� �������� �� ����� ��� ����. �������� ������',
			  position: 'bottom'
			},
			{
			  element: 'div.choice-border',
			  intro: '����������� ����� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.banner_container div.banner',
			  intro: '����� ������� ���� �� ������ ���������� ����������� � �����, ������� �� ���� ������������',
			  position: 'top'
			},			
			{
			  element: 'div.banner_container div.roulette-width input',
			  intro: '��������� ������ �������',
			  position: 'top'
			},
			{
			  element: 'div.banner_container div.roulette-height input',
			  intro: '��������� ������ �������',
			  position: 'left'
			},
			{
			  element: 'div.panel-buttons input.create',
			  intro: '�������� ������������ �������',
			  position: 'left'
			},
			{
			  element: 'div.panel-buttons input.reset',
			  intro: '�������� ��������� ������� �� ���������',
			  position: 'bottom'
			},
			{
			  element: 'table.banners-img td.bg div.link',
			  intro: '����������� ���������� ������ �� ������',
			  position: 'bottom'
			},
			{
			  element: 'div.top-panel ul li.upload',
			  intro: '����� ���� ����������� ��������� ���� ������ � ������� png, jpg, gif, bmp',
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