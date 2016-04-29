
var ajax_sendmail = '/cgi-bin/admin/modules/sendmail_ajax.cgi';

$(document).ready(function(){

	var ajaxSave = function(){
		var ed = tinyMCE.get('elm1');
		ed.setProgressState(1);
		window.setTimeout(function(){ed.setProgressState(0);}, 500);
	};

	$("div.content_email a.ajaxSave").live('click', function(){
		ajaxSave();			
		var ed = tinyMCE.get('elm1');
		var content = ed.getContent();
		var params = new Object();
		if (content == ""){content = "clear";}				
			params.content_mail = content;		
			params.content_mail_save = "save";
			$.post(ajax_sendmail, params);
		return false;
	});
	
	$("div.send_email a.send_mail").live('click', function(){
		
		if (!$("div.send_email div.container div.no-data").length){
		
			var interval = parseFloat($("div.send_email input.interval").val());
			var m_count = parseFloat($("div.send_count input").val());
			var no_send = parseFloat($("div.tab_sendmail em.nosend").html());
			
			if (no_send < 1){alert("Для повторной рассылки, нажмите кнопку «Очистить» для очищения статуса рассылки"); return false;}
			else if (m_count == "" || m_count < 1){alert("Установите лимит оправляемых писем"); return false;}
			else if (interval == ""){alert("Установите интервал между письмами"); return false;}
			else if (interval < 2){alert("Мин. допустимый интервал между письмами 2 секунды"); return false;}		
			else if (confirm("Запустить рассылку?")) {
			
			$("div.send_email div.container table").empty();
			
			$("div.send_email h4").empty().append("Идет рассылка...");
			
			var ed = tinyMCE.get('elm1');
			var content = encodeURIComponent(ed.getContent());
			var theme = encodeURIComponent($("div.content_email div.sendmail_theme input").val());
			if (no_send < m_count) {m_count=no_send;}
			for (var i=1; i < m_count+1; i++){
				 $.ajax({
					  async: false,
					  url: ajax_sendmail,
					  type: "POST",
					  data: "content_mail="+content+"&sendmail_theme="+theme+"&sendmail_interval="+interval+"&sendmail=send",
					  success : function(data) {
							$("div.send_email div.container table").prepend(data);
							var nosend = parseFloat($("div.tab_sendmail em.nosend").html());
							var send_ok = parseFloat($("div.tab_sendmail em.send").html());
							nosend = nosend-1;
							send_ok = send_ok+1;
							$("div.tab_sendmail em.nosend").html(nosend);
							$("div.tab_sendmail em.send").html(send_ok);
					  }
				});
			}
			
			$("div.send_email h4").empty().append("Рассылка завершена");
		
			return false;
			
			} else {return false;}
		}
		else {
			alert("В базе отсутствуют пользователи");
		}
		
		return false;
	});
	
	$("div.send_email a.clear_mail").live('click', function(){
		
		if (!$("div.send_email div.container div.no-data").length){
		
			if (confirm("Очистить статус отправления у пользователей?")) {
				$("div.send_email div.container table tr td em.send").each(function(){
					$(this).html("не отправлено").removeClass("send").addClass("nosend");
				});		
				var params = new Object();
				params.email_clear = "clear";
				$.post(ajax_sendmail, params, function(data){
					$("div.tab_sendmail em.nosend").html(data);
				});			
				$("div.tab_sendmail em.send").html("0");
				
			return false;
			
			} else {return false;}
		}
		else {
			alert("В базе отсутствуют пользователи");
		}
		
		return false;
	});	
	
});