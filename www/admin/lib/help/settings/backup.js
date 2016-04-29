$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'iframe.help_mysql',
			  intro: '�������������� / �������������� ���� MySQL.<br> <b>��� ����������� ������������ ������������ ������ �� �������������</b>',
			  position: 'top'
			},
			{
			  element: 'iframe.help_files',
			  intro: '�������������� / �������������� ����������� �������: ��������, �������, �����������, ��������, ��������',
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