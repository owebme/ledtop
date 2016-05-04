/**
* Name: jSboxUploads
* Date: January 2014
* Autor: UpleCMS (http://uplecms.ru)
* Version: 1.0.3
* Licence: http://uplecms.ru
**/

var dirs = '/cgi-bin/admin/modules';

$(document).ready(function(){

	$("body").append('<div style="border: 3px dashed rgb(177, 206, 229); background-color: rgba(234, 242, 248, 0.8); z-index: 3000; position: fixed; left: 5px; right: 5px; top: 5px; bottom: 5px; border-radius:6px; z-index:1001;" id="uplecms-dropzone"><div class="container" style="color: #069; position: absolute; width: 600px; top: 50%; left: 50%; margin-top: -72px; margin-left: -300px; text-shadow: 0 1px 0 #fff; font-size: 30px; line-height:35px; text-align: center; height: 50px;"><span>Перетащите файлы сюда, чтобы<br> загрузить на сайт</span></div></div>');
	
	if (getUrlVars()["adm_act"] !== "catalog" && getUrlVars()["adm_act"] !== "products" && getUrlVars()["adm_act"] !== "products_multi"){
		var intervalTimer="";
		$("body").bind({
			dragover: function() {
				$("div#uplecms-dropzone").addClass("dragover");
				return false;
			},
			dragleave: function() {
				intervalTimer = setTimeout(function(){
					$("div#uplecms-dropzone").removeClass("dragover");
					return false;
				}, 1);
			},
			drop: function(e) {
				var dt = e.originalEvent.dataTransfer;
				if (dt){
					if ($("div#uplecms-dropzone").attr("class") != "drop" && !$("div#elfinder_container").length){
						$("div#uplecms-dropzone").addClass("drop").removeClass("dragover");
						$("div#uplecms-dropzone div.container").prepend('<div class="loading-files"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
						addImgUpload(dt.files);
						return false;
					}
				}
			}
		});
		$("div#uplecms-dropzone").bind({
			dragover: function() {
				clearInterval(intervalTimer);
				$(this).addClass("dragover");
				return false;
			},
			dragleave: function() {
				$(this).removeClass("dragover");
				return false;
			}
		});		
	}

	$("div#header div#menu2 div.upload input").bind({
		change: function() {
			if ($("div#uplecms-dropzone").attr("class") != "drop"){
				$("div#uplecms-dropzone").addClass("drop").removeClass("dragover");
				$("div#uplecms-dropzone div.container").prepend('<div class="loading-files"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>');
				addImgUpload(this.files, this);
				return false;
			}
		}
	});

	function addImgUpload(files) {
		var php = /.*\.php/;
		var cgi = /.*\.cgi/;
		var pl = /.*\.pl/;
		var pm = /.*\.pm/;
		var exe = /.*\.exe/;
		var lnk = /.*\.lnk/;
		var js = /.*\.js/;
		var folder = /.*\.(.+?)$/;

		var fileCount=0; var fileSize=0;		
		$.each(files, function(i, file) {
			if (file.name.match(php) || file.name.match(cgi) || file.name.match(pl) || file.name.match(pm) || file.name.match(exe) || file.name.match(lnk) || file.name.match(js) || !file.name.match(folder)) {
				return true;
			}
			fileCount++;
			var div = $('<input class="file" data-name="'+file.name+'"/>');
			$("div#uplecms-dropzone div.container").append(div);
			div.get(0).file = file;
			
			fileSize = fileSize+(file.size/1024)/1024;
			var reader = new FileReader();
			reader.onload = (function(aDiv) {
				return function(e) {
					aDiv.val(e.target.result);
				};
			})(div);
			
			reader.readAsDataURL(file);
		});
		if (fileCount > 0){
			var cnt=0;
			fileSize = parseFloat(fileSize).toFixed(2);
			$("div#uplecms-dropzone div.container span").html('Идет подготовка к загрузке...');
			setTimeout(function(){
				observeUploads(fileCount, fileSize, cnt);
			}, 500);
		}
		else {
			$("div#uplecms-dropzone div.container div.loading-files").remove();
			$("div#uplecms-dropzone").removeClass("drop");
			$("div#uplecms-dropzone div.container span").html("Перетащите файлы сюда, чтобы<br> загрузить на сайт");
		}
	}
	
	function observeUploads(fileCount, fileSize, cnt){
		var intervalTimer=""; 
		$("div#uplecms-dropzone div.container input.file:not(.upload)").each(function(){
			var el = $(this);
			var file = $(this).val();
			var name = $(this).attr("data-name");
			if (file != "" && name != ""){
				$(el).addClass("upload");
				var params = new Object();
				params.filesUpload = file;
				params.filesUploadName = name;
				$.post(dirs+'/save_ajax.cgi', params, function(data){
					if (data){
						if (data == "upload"){
							cnt++;
						}
						$(el).remove();
						if (fileCount > 0){
							var ext = "файлов";
							if (cnt == 1 || cnt == 21 || cnt == 31 || cnt == 41 || cnt == 51 || cnt == 61 || cnt == 71 || cnt == 81 || cnt == 91 || cnt == 101){ext = "файл";}
							else if (cnt > 1 && cnt < 5 || cnt > 21 && cnt < 25 || cnt > 31 && cnt < 35 || cnt > 41 && cnt < 45 || cnt > 51 && cnt < 55 || cnt > 61 && cnt < 65 || cnt > 71 && cnt < 75 || cnt > 81 && cnt < 85 || cnt > 91 && cnt < 95 || cnt > 101 && cnt < 105){ext = "файла";}
							$("div#uplecms-dropzone div.container span").html('Загружено '+cnt+' '+ext+' из '+fileCount+' на '+fileSize+' мб...');
						}
						if (fileCount == cnt || !$("div#uplecms-dropzone div.container input.file").length){
							if (cnt < 1){ext = "файлов";}
							$("div#uplecms-dropzone div.container div.loading-files").remove();
							$("div#uplecms-dropzone div.container span").html('<em>Загружено '+cnt+' '+ext+'...</em>');
							setTimeout(function(){
								$("div#uplecms-dropzone").fadeOut(250, "easeOutSine", function(){
									$("div#uplecms-dropzone").removeClass("drop");
									$("div#uplecms-dropzone div.container span").html("Перетащите файлы сюда, чтобы<br> загрузить на сайт");
								});
							}, 500);
						}
						clearInterval(intervalTimer);
						if ($("div#uplecms-dropzone div.container input.file:not(.upload)").length){
							intervalTimer = setTimeout(function(){
								observeUploads(fileCount, fileSize, cnt);
							}, 2000);
						}
					}
					if (data != "upload"){
						$(el).remove();
					}
				});
			}
		});
	}
	
	function getUrlVars() {
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
			vars[key] = value;
		});
		return vars;
	}		
	
});