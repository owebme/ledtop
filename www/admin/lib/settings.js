var dirs_modules = '/cgi-bin/admin/modules';

$(document).ready(function(){

	$("a.change_main_page").click(function(){
		var el = $(this);
		$(el).parent().addClass("active");
		var select = $(this).parent().parent().next();
		$(select).empty().append('<div class="ajax-td"></div>');
		$(this).prev("span").animate({"margin-top":"0px"}, 250, function(){
			$(el).remove();
		});
		var params = new Object();
		params.select_main_page = "load";		
		$.post(dirs_modules+'/settings_ajax.cgi', params, function(data){
			if (data != ""){
				$(select).empty().append(data);
			}
		});
		
		return false;
	});
	
	$("table.settings div.slideshow input.file").bind({
		change: function() {
			addSlide(this.files, this);
		}
	});

	function addSlide(files, el) {
		var input = el; 
		var imageType = /image.*/;
		var num = 0;
		$.each(files, function(i, file) {
			if (!file.type.match(imageType)) {
				alert('Добавляемый файл "'+file.name+'" не является картинкой');
				return true;
			}
			num++;
			if (num == 1){
				if ($(input).parent().attr("class") == "slide"){
					$(input).parent().find("div.foto").children("img").replaceWith('<div class="ajax"></div>');
				}
				else if ($(input).parent().attr("class") == "slide add"){
					$(input).parent().find("div.foto").children("span").replaceWith('<div class="ajax"></div>');
					$(input).parent().removeClass("add");
					$(input).parent().append('<a href="#" class="del"></a>');
					var id = parseInt($("table.settings div.slideshow div.slide:last").attr("data-index"));
					id = id+1; if (id == ""){id = 1001;}
					$(input).parent().parent().append('<div class="slide add" data-index="'+id+'"><div class="foto"><span><em>Добавить слайд</em></span></div><input title="Добавить слайд" type="file" class="file"><a title="Удалить слайд" href="#" class="del"></a></div>');
					$("table.settings div.slideshow input.file").unbind();
					$("table.settings div.slideshow input.file").bind({
						change: function() {
							addSlide(this.files, this);
						}
					});
				}
				var img = $('<img class="paste"/>');
				$(input).parent().find("div.foto").prepend(img);
				img.get(0).file = file;
				
				var reader = new FileReader();
				reader.onload = (function(aImg) {
					return function(e) {
						aImg.attr('src', e.target.result);
					};
				})(img);
				
				reader.readAsDataURL(file);
			}
		});
		
		setTimeout(function(){
			$(input).parent().find("div.foto").find('img.paste').each(function(){
				var uploadItem = $(this);
				var id = $(uploadItem).parent().parent().attr("data-index");
				var params = new Object();
				params.add_slide_id = id;
				params.add_slide_ox = $("table.settings div.slideshow div.options input[name=slide_ox]").val();
				params.add_slide_oy = $("table.settings div.slideshow div.options input[name=slide_oy]").val();
				params.add_slide = $(uploadItem).attr("src");
				$.post(dirs_modules+'/settings_ajax.cgi', params, function(data){
					if (data != ""){
						$(uploadItem).parent().find("div.ajax").replaceWith(data);
						alignImgSlide($(uploadItem).parent());
						$(uploadItem).remove();
					}
				});
			});
		}, 200);
	}
	
	$("table.settings div.slideshow div.slide div.foto").each(function(){
		var div = $(this);
		var heightDiv = parseInt($(div).height());
		var heightImg ="";
		$(div).find("img").load(function(){
			heightImg = parseInt($(this).height());
			if (heightImg < heightDiv){
				var def = (heightDiv-heightImg)/2;
				$(div).find("img").css("marginTop", def+"px");
			}
		});
	});
	
	function alignImgSlide(el) {
		var div = el;
		var heightDiv = parseInt($(div).height());
		var heightImg ="";
		$(div).find("img").load(function(){
			heightImg = parseInt($(this).height());
			if (heightImg < heightDiv){
				var def = (heightDiv-heightImg)/2;
				$(div).find("img").css("marginTop", def+"px");
			}
		});
	}	
	
	$("table.settings div.slideshow div.slide a.del").live('click', function(){
		var el = $(this);
		var id = $(el).parent().attr("data-index");
		var params = new Object();
		params.del_slide = id;
		$.post(dirs_modules+'/settings_ajax.cgi', params);
		if ($(el).parent().next().attr("class") == "slide add"){
			$(el).parent().next().attr("data-index", id);
		}
		$(el).parent().fadeOut(200, function(){
			$(el).parent().remove();
		});
		
		return false;
	});
	
});