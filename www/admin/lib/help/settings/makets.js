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
			  element: 'div.makets',
			  intro: '����� ������ �������� ����������� ������������� � ��������, �������, ������ � �.�.',
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