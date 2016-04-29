$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.tab_sendmail',
			  intro: '����� ������������ � �� ������������ ���������',
			  position: 'top'
			},
			{
			  element: 'div.send_count',
			  intro: '������������� �����, ���������� ������������ ����� �� ���',
			  position: 'left'
			},
			{
			  element: 'div.send_email',
			  intro: '������ ������ �� ������������ �������',
			  position: 'top'
			},
			{
			  element: 'div.interval',
			  intro: '������������� �������� ����� �������� � ��������',
			  position: 'top'
			},	
			{
			  element: 'a.clear_mail',
			  intro: '�������� ������� ����� ��������',
			  position: 'left'
			},			 
			{
			  element: 'a.send_mail',
			  intro: '��������� ��������',
			  position: 'left'
			},
			{
			  element: 'div.sendmail_theme',
			  intro: '��������� (����) ������ ��� ����������',
			  position: 'top'
			},
			{
			  element: '#elm1_parent',
			  intro: '���������� ������ ��� ��������. �� ����� ��������� �����, ��������, ���� ����������� �������� ��� ��������',
			  position: 'top'
			},
			{
			  element: 'a.ajaxSave',
			  intro: '��������� ���������� ������',
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