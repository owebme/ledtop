var dirs_que = '/cgi-bin/admin/modules';

	function auto_update(){
		var que_date = $("div.questions div.body-que div.item.que:nth-child(1)").attr("date");
		if ($("div.questions div.body-que").html() == ""){que_date="none";}
		if ($("div.questions div.body-que").attr("id") == "loader"){que_date="";}
		var params = new Object();
		params.auto_update = "update";
		params.que_date = que_date;		
		$.post(dirs_que+'/questions_ajax.cgi', params, function(data){
			if (data != ""){
				$("div.questions div.body-que").prepend(data);
				$("div.questions div.body-que div.item.que:nth-child(1)").fadeIn(600);
				$("div.questions div.body-que").css("height", "auto");
			}
			setTimeout("auto_update()", 25000);			
		});
	}

	auto_update()