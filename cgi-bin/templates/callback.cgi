# �������� ������

$callback='	
	<link href="/js/jSbox/style.css" rel="stylesheet" type="text/css"/>
	<script src="/js/jSbox/jquery.jSbox-1.0.2.js" type="text/javascript"></script>
	
	<div class="callback-container">
		<div class="body-callback">
			<h3>�������� ������</h3>
			<form action="#">
				<fieldset>
					<label>���� ��� <span>*</span></label>
					<div class="text-wrap">
						<input type="text" name="NAME" value="�������" class="text requried">
					</div>
					<label>��� ���������� ����� <span>*</span></label>
					<div class="text-wrap">
						<input type="text" name="PHONE" value="�������" class="text requried">
					</div>
					<span class="note">�������� �������� ������ � ���� ����������� ���������������� ��� �� ����� ��������.</span>
					<input type="submit" value="��������� ������" class="submit callback">
					<a id="jSbox-close" href="#">��������</a>
				</fieldset>
			</form>
		</div>
	</div>
	
	<script type="text/javascript">
	$(function(){
		$("a#callback").jSbox({
			width : 423,
			speed : 300,
			theme : "green",
			autoclear : true,
			border : true,
			maskphone : "input.text[name=PHONE]",
			box : ".callback-container"
		});	
		$("div#jSbox-container input[type=submit].callback").live("click", function(e){

			var hBox = $("div#jSbox-wrap").height();
			var name = $("div#jSbox-container input[name=NAME]").attr("value");
			var phone = $("div#jSbox-container input[name=PHONE]").attr("value");
				
			if (name != "" && name != "�������" && phone != "" && phone != "�������"){			
				var params = new Object();
				params.name = name;
				params.phone = phone;
				$.get("/cgi-bin/send_callback.cgi", params, function(data){
					if (data != ""){
						$("div#jSbox-wrap").css("height", hBox+"px");
						$("div#jSbox-wrap").append(\'<div id="jSbox-message-send">\'+data+\'</div>\');
						$("div#jSbox-wrap div#jSbox-container").fadeOut(400, function(){
							$("div#jSbox-wrap div#jSbox-message-send").fadeIn(600, function(){
								window.setTimeout(function(){
									$().jSboxClose();
								}, 2500);
							});
						});
					}
				});			
			}
			else {
				return false;
			}
			e.preventDefault();
		});	
	});
	</script>';
	
1;