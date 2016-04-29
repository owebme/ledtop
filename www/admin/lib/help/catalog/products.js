$(document).ready(function(){

	function guide(){
	
		var items = [
			{
			  element: 'div.main_button',
			  intro: '�������� ��� ������ ��������',
			  position: 'bottom'
			},
			{
			  element: 'div.search_catalog',
			  intro: '����� ������� �� ��������. ������� ����� � �����������: ������� ������ ����� � �������� ������',
			  position: 'bottom'
			}
		];
		
		if ($("div.select_category select.category").length){
			items.push(
						{
						  element: 'div.select_category',
						  intro: '��������� ��������. �������� ������ ��� ���������, � ��� �� �������� �����, �� ������� �� ������',
						  position: 'bottom'
						}		
					);
		}
		
		items.push(
			{
			  element: 'div.main_button.list',
			  intro: '����� ������� ������� ��� ����������',
			  position: 'bottom'
			},
			{
			  element: 'div.main_button.foto',
			  intro: '����� ������� c ������������',
			  position: 'bottom'
			},	
			{
			  element: 'a.multi-add',
			  intro: '�������� ���������� �������',
			  position: 'bottom'
			}	
		);

		if (!$("div.select_category select.category").length && $("div#category_products").length){
			items.push(
						{
						  element: 'div#category_products',
						  intro: '��������� ��������',
						  position: 'top'
						},
						{
						  element: 'div#category_products ul li span.move',
						  intro: '���������� �������� ���������� ���������',
						  position: 'bottom'
						},
						{
						  element: 'div#category_products ul li a.show_cat',
						  intro: '�������� �� ������ ��� ���������, � ��� �� �������� �����, �� ������� �� ������',
						  position: 'bottom'
						}				
					);
		}
				
		items.push(
					{
					  element: 'div#allProducts ul#product_foto li',
					  intro: '������� ������ ������ �� ������ � �� ������ ������� ����� ������. �� ����� ������ ������ �������������� ������ ������������ ��� � ����� �� �����, ����� �� ������ ���������� ����� � ������ ��� ���������, �������� ������ �� ����� ������� ����� ������ ���� � ������ ��� ����� � ���������, ����� ���������',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_foto li span.price',
					  intro: '������ �������� ���� �� ������ � �����, �������� �� ���� � ������� ��',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_foto li span.name',
					  intro: '������� �������� ������ �� ������ � ����',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_foto li a.product_del',
					  intro: '������� �����',
					  position: 'bottom'
					}			
				);

		items.push(
					{
					  element: 'div#allProducts ul#product_list li a.product_del',
					  intro: '������� �����',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_list li a.product_lamp',
					  intro: '������� �������� / �� �������� ����� ��� ����������� �� �����',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_list li span.move',
					  intro: '���������� �������� ���������� �������',
					  position: 'bottom'
					},				
					{
					  element: 'div#allProducts ul#product_list li a#p_name',
					  intro: '������� �� �������� �� ��������� � �������������� ������',
					  position: 'bottom'
					},
					{
					  element: 'div#allProducts ul#product_list li span.price',
					  intro: '������ �������� ���� �� ������ � �����, �������� �� ���� � ������� ��',
					  position: 'bottom'
					}			
				);	

		items.push(
					{
					  element: 'div.pages',
					  intro: '�������� ���������',
					  position: 'top'
					}
				);
			
		return items;
	}
	
	$("a#help-tour").live('click', function(){
		if (!$("div#category_products").length && !$("div.select_category select.category").length){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>�������� ��������� � ������</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}	
		else if ($("div#allProducts ul").html() == ""){
			var el = $(this).parent();
			$(el).html('<div class="warning">'+$(el).html()+'<span>�������� ��������� � ��������</span></div>');
			$(el).find("div.warning").find("span").animate({"opacity": "1"}, 200, "easeInSine");
			$(el).find("a#help-tour").remove();
		}
		else {
			var introguide = introJs();
			introguide.setOptions({
				steps: guide()
			})			
			introguide.start();
		}
		return false;
	});
	
	$("div#uple-help").attr("data-guide", "true");
  
});