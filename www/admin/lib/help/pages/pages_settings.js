$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_sort',
			  intro: '����� ������� ����������: �� ��������, ��������, ����',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_quick_save',
			  intro: '����������� �������� ���������� ������� ��� ������������',
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