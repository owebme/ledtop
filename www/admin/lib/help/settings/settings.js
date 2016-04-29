$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_title',
			  intro: '�������� ����� �����. �� ������������� � ������ �������� ���� ����� �� ����� ��� ��� �������������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_cache',
			  intro: '�������� ��� �����, ��� ������� ������� ������ �����, ������������ ������������� ��� ��������-���������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_main_page',
			  intro: '�������� �� �������� ��������, ������� ���������� � �� ������� ��������� ����� ������� �������� ��� ������ �����',
			  position: 'bottom'
			},				
			{
			  element: 'div#pages div.help_contacts',
			  intro: '���������� ������, ����������� �� ���� ��������� �����',
			  position: 'left'
			},
			{
			  element: 'div#pages div.help_social',
			  intro: '�� ������ ������������ ���� � UpleCMS ����� ���� ������� ���������� ����, ��� �� �������� ������ ��� ������� ����� � ������ ��� ����� � �������',
			  position: 'bottom'
			},			
			{
			  element: 'table#page_new table.help_maket',
			  intro: '����� ������� �� ��������� ��� ������� �� �������',
			  position: 'right'
			},
			{
			  element: 'table#page_new table.help_mysql',
			  intro: '��������� �������� � MySQL ����',
			  position: 'right'
			},
			{
			  element: 'table#page_new tr.help_feedback',
			  intro: '����� ��� ������ ����� ����� �������� ����� �� �����. ���������� �������� ����� �� �������� �������� � ������ ������� ��� �������� / �������������� ��������, ����� ��������� ������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_orders',
			  intro: '����� ��� ������ ������� ��������-��������',
			  position: 'bottom'
			},	
			{
			  element: 'table#page_new table.help_yamarket',
			  intro: '��������� �������� � ������ ������.������, ������ � ������� YML ������������� ����������� �� ������: <a target="_blank" href="http://'+location.hostname+'/products.xml">http://'+location.hostname+'/products.xml</a>. ���������� �� ������ � �����-������ ������.������� �� ������ ���������� <a target="_blank" href="http://help.yandex.ru/partnermarket/export/feed.xml">�����</a>',
			  position: 'right'
			},
			{
			  element: 'table#page_new table.help_payment',
			  intro: '��������� �������� � ��������� ������� Robokassa. ��������� ��������� ������� �� <a target="_blank" href="http://www.robokassa.ru/ru/Support/SendMsg.aspx">������</a>',
			  position: 'right'
			},			
			{
			  element: 'table#page_new div.slideshow',
			  intro: '�������������� �������� ����������� �� ������� ��������. ������� �� ��������� ����� � �������� ���� � ������������',
			  position: 'top'
			},	
			{
			  element: 'table#page_new div.slideshow div.help_slides.options',
			  intro: '�������������� ������ ����������� ������� (������ / ������ � px)',
			  position: 'left'
			},
			{
			  element: 'table#page_new td.help_counter',
			  intro: '���� ��� ������� ���������: liveinternet, ������.�������, google.adwords � �.�.',
			  position: 'left'
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