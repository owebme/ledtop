$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'a.save_maket.button',
			  intro: '��� �������� �������� ���������� ��������� ����������� ������ Ctrl+S',
			  position: 'left'
			},		
			{
			  element: 'div.template a#help_articles',
			  intro: '������ ������� (����������)',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_auth',
			  intro: '������ ������������ �������������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_banners',
			  intro: '������ ���������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_basket',
			  intro: '������ �������� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_basket_ajax',
			  intro: '������ �������� ������� ���� (���������� ������)',
			  position: 'bottom'
			},	
			{
			  element: 'div.template a#help_callback',
			  intro: '������ ��������� ������',
			  position: 'bottom'
			},	
			{
			  element: 'div.template a#help_catalog',
			  intro: '������ ���������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_contacts',
			  intro: '������ ����������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_feedback',
			  intro: '������ ��������� ������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_gallery',
			  intro: '������ ���������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_name',
			  intro: '�������� ���������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_news',
			  intro: '������ ��������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_pages',
			  intro: '������ ����������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_private',
			  intro: '������ ������� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products',
			  intro: '������ ������� ��������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_hit',
			  intro: '������ ����� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_random',
			  intro: '������ ���������� �������',
			  position: 'bottom'
			},	
			{
			  element: 'div.template a#help_products_recomend',
			  intro: '������ �������������� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_related',
			  intro: '������ ��������� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_products_viewed',
			  intro: '������ �������������� �������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_questions',
			  intro: '������ ����������',
			  position: 'bottom'
			},
			{
			  element: 'div.template a#help_slideshow',
			  intro: '������ ������-���',
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