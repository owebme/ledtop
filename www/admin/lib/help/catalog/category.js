$(document).ready(function(){

	var introguide = introJs();
	introguide.setOptions({
		steps: [
			{
			  element: 'div.three_pages',
			  intro: '������ ��������� ��������',
			  position: 'top'
			},
			{
			  element: 'div.three_pages ul li a.del',
			  intro: '������� ���������',
			  position: 'bottom'
			},
			{
			  element: 'div.three_pages ul li a.lamp',
			  intro: '������� �������� / �� �������� ��������� ��� ����������� �� �����',
			  position: 'bottom'
			},
			{
			  element: 'div.three_pages ul li span.move',
			  intro: '���������� �������� ���������� ���������',
			  position: 'bottom'
			},	
			{
			  element: 'div.three_pages ul li a.name',
			  intro: '�������� �� �������� ��������� � �� ������� �� �����, ������� �� ��� �� ��������� � ��������������',
			  position: 'bottom'
			},			 
			{
			  element: 'div#sheettop div#buttons a#cstmz',
			  intro: '������� � ���������� ������ �������� �������',
			  position: 'bottom'
			}
		]
	});
	
	$("a#help-tour").live('click', function(){
		if ($("div.three_pages ul").html() == ""){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>�������� ���� �� ���� ���������</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}
		else {
			introguide.start();
			setTimeout(function(){
				$("div.three_pages.introjs-relativePosition ul.level0 li[c_pid=0] div.point.last").each(function(){
					var height = $(this).parent().parent().height();
					if (!$(this).parent().parent().parent().next().length){
						$(this).css("height", (height-15)+"px");
					}				
					else {
						$(this).css("height", height+"px");
					}
				});
			}, 5);
		}
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});