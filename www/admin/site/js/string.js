$(document).ready(function(){

	$("div#content_right div.main_menu div a").each(function(){
		var el = $(this);
		var total_letter = $(this).html().length;
		if (total_letter > 10) {$(el).parent().css("margin", "0px 15px 0px 15px");}
		if (total_letter > 20) {$(el).parent().css("margin", "0px 10px 0px 10px");}		
	});

	
	$("div#content_right div.public_top div a").each(function(){
		var el = $(this);
		var word = $(this).html();		
		var total_letter = $(this).html().length;
		if (total_letter > 18) {$(el).css("font-size", "11px");}		
		if (total_letter > 22) {var word_str = word.substr(0,20)
		$(el).empty().append(word_str+'...');}		
	});
	
	
	$("div#main_footer div.public_bottom div a").each(function(){
		var el = $(this);
		var word = $(this).html();		
		var total_letter = $(this).html().length;
		if (total_letter > 26) {$(el).css("font-size", "11px");}
		if (total_letter > 30) {var word_str = word.substr(0,28)
		$(el).empty().append(word_str+'...');}			
	});	
	
	
	$("div.catalog_list div.product a.name").each(function(){
		var el = $(this);
		var word = $(this).html();	
		var total_letter = $(this).html().length;		
		if (total_letter > 21) {var word_str = word.substr(0,19)
		$(el).empty().append(word_str+'...');}	
	});	
	
	$("div.catalog_list div.product div.descript").each(function(){
		var el = $(this);
		var word = $(this).html();	
		var total_letter = $(this).html().length;		
		if (total_letter > 64) {var word_str = word.substr(0,64)
		$(el).empty().append(word_str+'...');}	
	});	

	$("table.order td.product_info div.description").each(function(){
		var el = $(this);
		var word = $(this).html();	
		var total_letter = $(this).html().length;		
		if (total_letter > 64) {var word_str = word.substr(0,64)
		$(el).empty().append(word_str+'...');}	
	});	

	$("ul.gallery li div.desc_sm").each(function(){
		var el = $(this);
		var word = $(this).html();	
		var total_letter = $(this).html().length;		
		if (total_letter > 44) {var word_str = word.substr(0,44)
		$(el).empty().append(word_str+'...');}	
	});	

});