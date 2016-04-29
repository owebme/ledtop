$(document).ready(function(){
	$("input.cb").hide().after('<div class="cb"></div>');
	$(":checked").next().addClass("checked");
	$("div.cb").click(function(){
		var input_cb = $(this).prev("input");
		if (input_cb.is(':checked'))
		{
		 $(this).removeClass("checked");
		 input_cb.attr('checked', false);
		}
		else 
		{
		 $(this).addClass("checked");
		 input_cb.attr('checked', true);
		}
	});
});
