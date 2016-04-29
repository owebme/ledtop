$(document).ready(function(){

	var introguide_gallery = introJs();
	introguide_gallery.setOptions({
		steps: [
			{
			  element: 'div#tabs ul li a#click_addfoto',
			  intro: '������� � ���������� ����������',
			  position: 'bottom'
			},		
			{
			  element: 'div#fotogal ul',
			  intro: '�������� ����������',
			  position: 'top'
			},
			{
			  element: 'div#fotogal ul li a.zoom_foto',
			  intro: '���������� ����������',
			  position: 'bottom'
			},
			{
			  element: 'div#fotogal ul li a.del_foto',
			  intro: '������� ����������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_name',
			  intro: '�������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'table#page_new tr.help_show',
			  intro: '���������, ���������� / �� ���������� ����������� �� �����',
			  position: 'bottom'
			},			
			{
			  element: 'span.mceEditor',
			  intro: '�������������� �������� �������',
			  position: 'top'
			},
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: '������� � ���������� ������ �����������',
			  position: 'bottom'
			}
		]
	});
	
	var introguide_gallery_new = introJs();
	introguide_gallery_new.setOptions({
		steps: [
			{
			  element: 'table#page_new tr.help_name',
			  intro: '�������� �����������',
			  position: 'bottom'
			},
			{
			  element: 'span.mceEditor',
			  intro: '�������������� �������� �������',
			  position: 'top'
			},
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: '������� � ���������� ������ �����������',
			  position: 'bottom'
			}
		]
	});	
	
	var introguide_photo = introJs();
	introguide_photo.setOptions({
		steps: [
			{
			  element: 'div#addfoto p.help_auto_small',
			  intro: '�������� ��������� ���������� �� �������',
			  position: 'bottom'
			},		
			{
			  element: 'div#addfoto textarea.help_desc_big',
			  intro: '��������� �������� ����������, ��� ���������� (�����������)',
			  position: 'bottom'
			},
			{
			  element: 'div#addfoto div.help_desc_small',
			  intro: '������� �������� ����������, ��� ��������� (�����������)',
			  position: 'top'
			},
			{
			  element: 'div#addfoto div.help_resize_big',
			  intro: '�������������� ������ ����������� ������� ���������� (������ / ������ ��� ������������ ���� / ������ ��� ��������������)',
			  position: 'bottom'
			},
			{
			  element: 'div#addfoto div.help_resize_small',
			  intro: '�������������� ������ ����������� ����� ���������� (������ / ������)',
			  position: 'bottom'
			},
			{
			  element: 'div#addfoto div.hdr',
			  intro: '����������� ���������� ��� ������ � �������������: ����������� �����, ��������������� ������ ������, ������ �������� ����� �����������',
			  position: 'top'
			}
		]
	});	
	
	$("a#help-tour").live('click', function(){
		if ($("table#page_new td.name_main").html() == "����� �����������"){
			introguide_gallery_new.start();
		}
		else if ($("div#tabs ul li a#click_fotogal").parent().attr("class") == "activetab"){
			introguide_gallery.start();
		}
		else if ($("div#tabs ul li a#click_addfoto").parent().attr("class") == "activetab"){
			introguide_photo.start();
		}
		$("div.highslide-container").css("z-index", "9999999999");
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});