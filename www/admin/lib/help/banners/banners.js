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
			  element: 'div.banner_container div.banner',
			  intro: '�������� � ��� ����, ����� ������� ���� ����������� ������ ������� � �������: png, jpg, gif, bmp',
			  position: 'bottom'
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
			  element: 'div.top-panel ul li.designs',
			  intro: '��������� � ������������ ��������',
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