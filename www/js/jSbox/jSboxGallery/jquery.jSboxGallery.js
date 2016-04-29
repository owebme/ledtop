/**
* Name: jSboxGallery
* Date: November 2013
* Autor: UpleCMS (http://uplecms.ru)
* Version: 2.0.5
* Licence: http://uplecms.ru
**/
(function($) {
    $.fn.jSboxGallery = function(opt) {
		opt = jQuery.extend({
			maxHeight: "100%",
			openEffect: 'easeInOutQuint',
			openSpeed: 250,			
			nextEffect: 'easeInOutQuint',
			nextSpeed: 650,
			prevEffect: 'easeInOutQuint',
			prevSpeed: 650,
			shadowImg: false,
			innerShadow: false,
			socialButton: false,
			showOneImage: false
				}, opt);

if ((navigator.userAgent.match(/iPad/i)==null) && (navigator.userAgent.match(/iPhone/i)==null)) {
}
else {
	// для iPad, iPhone
}

imgOpenPopup = function(soc) {
	var link="";
	var url = location.href.replace(/\#img([0-9]+)$/,"img=$1"); url = url.replace(/\?jSbox/,"");
	if (soc == "fb"){link = 'https://www.facebook.com/login.php?next=http://www.facebook.com/sharer/sharer.php?u='+url+'?social=fb';}
	else if (soc == "vk"){link = 'http://vk.com/share.php?url='+url+'?social=vk';}
	else if (soc == "mail"){link = 'http://connect.mail.ru/share?share_url='+url+'?social=mail';}
	else if (soc == "dk"){link = 'http://www.odnoklassniki.ru/dk/?st.cmd=addShare&st._surl='+url+'?social=dk';}
	else if (soc == "tw"){link = 'https://twitter.com/intent/tweet?original_referer='+url+'&text='+encodeURIComponent(document.title)+'&url='+url+'?social=tw';}
	window.open(link,"displayWindow","width=520,height=300,left=350,top=170,status=no,toolbar=no,menubar=no");
}

var jPhotos = [];
var jSlides = {
    current: null,

    init: function() {
		var num=0;
		$(".jSbox-gallery").each(function(){
			jPhotos.push($(this).attr("href"));
			$(this).attr("data-id", num);
			num++;
		});	
		$("div#jSbox-gallery-container").remove();
		$("body").append('<div id="jSbox-gallery-container"><span class="slider-helper"></span>'+(opt.innerShadow?'<span class="slider-shadow"></span>':'')+''+(jPhotos.length > 1 && !opt.showOneImage?'<a class="slider-link slider-link_prev" href="#prev"><span class="slider-link-text">Предыдущее фото</span></a><a class="slider-link slider-link_next" href="#next"><span class="slider-link-text">Следующее фото</span></a><span class="slider-closer"></span>':'')+'</div>');
		var social="";
		if (opt.socialButton){
			social +='<span class="slider-social">';
			social +='<a class="soc-fb" title="Поделиться в Facebook" href="javascript:void(0)" onClick=\'imgOpenPopup("fb")\'></a>';
			social +='<a class="soc-vk" title="Поделиться ВКонтакте" href="javascript:void(0)" onClick=\'imgOpenPopup("vk")\'></a>';
			social +='<a class="soc-mail" title="Поделиться в Моем Мире" href="javascript:void(0)" onClick=\'imgOpenPopup("mail")\'></a>';
			social +='<a class="soc-dk" title="Поделиться в Одноклассниках" href="javascript:void(0)" onClick=\'imgOpenPopup("dk")\'></a>';
			social +='<a class="soc-tw" title="Поделиться в Twitter" href="javascript:void(0)" onClick=\'imgOpenPopup("tw")\'></a>';			
			social +='</span>';
			$("#jSbox-gallery-container").append(social);
		}
	
        var _this = this;
		if (jPhotos.length < 2 || opt.showOneImage){
			 $(document).on('click', '#jSbox-gallery-container', function(event){_this.hide()});
		}
        $(document)
        .on('click', '.jSbox-gallery', function(){
            var id = $(this).attr("data-id");
            _this.show(id);
            return false;
        })
        .on('click', '.slider-link_prev', function(event){_this.prev(); event.preventDefault();})
        .on('click', '.slider-link_next', function(event){_this.next(); event.preventDefault();})
        .on('click', '.slider-closer', function(event){_this.hide()})
        .on('keydown', function(event){

            if (!_this.visible) {
                return;
            }

            switch (event.keyCode) {
                case 27:
                    _this.hide();
                    break;
                case 32:
                case 39:
                    _this.next();
                    event.preventDefault();
                    break;
                case 37:
                    _this.prev();
            }
        });

        this.$slider = $('#jSbox-gallery-container');

        try {
            var id = window.location.hash.match(/^#img([0-9]+)$/);
            if (id && id[1]) {
                jSlides.show(id[1]);
            }
        } catch (e) {}
    },
    show: function(id){
        this.visible = true;
        this.current = id;
        this.$slider.show();
		var slide = this.$slider;
		var winHeight = $("#jSbox-gallery-container").height();
		if (!this.$slider.find('.slider-photo').length){
			this.$slider.find('.slider-helper').after('<div id="box-loader" style="display:block;"><div id="loader"></div><div id="loader-back"></div></div><img class="slider-photo'+(opt.shadowImg?' sh':'')+'" '+(opt.maxHeight?'style="max-height:'+opt.maxHeight+'"':'')+' src="'+jPhotos[id]+'" alt="">');
		} else {
			var rand = parseInt(Math.random()*1000);
			this.$slider.find('.slider-photo').css("opacity", "0").attr('src', jPhotos[id]+"?"+rand);
			if (opt.maxHeight){this.$slider.find('.slider-photo').css("max-height", opt.maxHeight);}
			if (opt.shadowImg){this.$slider.find('.slider-photo').addClass("sh");}
		}
		if (opt.socialButton){
			slide.find('.slider-social').stop(true, true).attr("style", "");
		}
		slide.find('.slider-photo').load(function(){
			var img = $(this);
			$(img).prev("#box-loader").remove();
			$(img).animate({"opacity": "1"}, opt.openSpeed, opt.openEffect);
			var width = $(img).width();
			var height = $(img).height();
			var left = $(img).offset().left;
			if (opt.innerShadow){
				slide.find('.slider-shadow').stop(true, true).attr("style", "");
				if (height < winHeight){
					slide.find('.slider-shadow').css({"top": ((winHeight-height)/2)+"px", "height": height+"px"});
				}
				slide.find('.slider-shadow').css({"width": width+"px", left: left+"px"});
			}
			if (opt.socialButton){
				if (height < winHeight){
					slide.find('.slider-social').css({"top": (((winHeight-height)/2)+17)+"px", "left": left+"px"});
				}
				else {slide.find('.slider-social').css({"top": "17px", "left": left+"px"});}
				slide.find('.slider-social').animate({"margin-left": "-40px", "opacity": "1"});
			}			
		});
		
        this.preload(id, 1);
        this.setHash();
    },
    next: function(){	
		if (this.$slider.attr("class") != "loading"){
			var id = jPhotos[parseInt(this.current) + 1] ? parseInt(this.current) + 1 : 0;
			this.current = id;
			this.$slider.addClass("loading");
			
			jSlides.move("next", this.$slider, id, opt.nextSpeed, opt.nextEffect);
			
			this.preload(id, 1);
			this.setHash();			
		}
    },
    prev: function(){
		if (this.$slider.attr("class") != "loading"){
			var id = jPhotos[parseInt(this.current) - 1] ? parseInt(this.current) - 1 : jPhotos.length - 1;
			this.current = id;
			this.$slider.addClass("loading");
			
			jSlides.move("prev", this.$slider, id, opt.prevSpeed, opt.prevEffect);

			this.preload(id, -1);
			this.setHash();			
		}
    },
	move: function(change, slide, id, speed, effect){
		var moveProc1=""; var moveProc2="";
		if (change == "next"){moveProc1 = "100%"; moveProc2 = "-100%";}
		else if (change == "prev"){moveProc1 = "-100%"; moveProc2 = "100%";}
		var width = slide.find('.slider-photo').width();
		var height = slide.find('.slider-photo').height();
		var winHeight = $("#jSbox-gallery-container").height();
		if (height < winHeight){
			slide.find('.slider-photo').css("margin-top", ((winHeight-height)/2)+"px");
		}
		slide.find('.slider-photo').addClass("old").css({"margin-left": "-"+(width/2)+"px", "left":"50%"}).after('<img style="left:'+moveProc1+''+(opt.maxHeight?';max-height:'+opt.maxHeight+'"':'')+'" class="slider-photo new'+(opt.shadowImg?' sh':'')+'" src="'+jPhotos[id]+'" alt="">');
		
		slide.find('.slider-photo.new').load(function(){
			var img = $(this);
			if (opt.socialButton){	
				slide.find('.slider-social').animate({"opacity": "0"});
			}		
			slide.find('.slider-photo.old').animate({"left":moveProc2, "opacity": "0"}, speed, effect, function(){
				$(this).remove();
			});			
			var width = $(img).width();
			var height = $(img).height();
			if (opt.innerShadow){
				slide.find('.slider-shadow').addClass("old").after('<span class="slider-shadow new"></span>');
				slide.find('.slider-shadow.old').fadeOut(400, effect, function(){
					$(this).remove();
				});
			}
			if (height < winHeight){
				if (opt.innerShadow){
					slide.find('.slider-shadow.new').css({"width": width+"px", "height": height+"px", "left": moveProc1, "margin-top":"-"+(height/2)+"px", "top":"50%"});
				}
				slide.find('.slider-photo.new').css({"opacity": "1", "margin-top":"-"+(height/2)+"px", "top":"50%"}).animate({"margin-left":"-"+(width/2)+"px", "left":"50%"}, speed, effect, function(){
					$(this).removeClass("new").attr("style", "opacity:1");
					if (opt.maxHeight){$(this).css("max-height", opt.maxHeight);}
					slide.removeClass("loading");
				});
				if (opt.innerShadow){
					slide.find('.slider-shadow.new').animate({"margin-left":"-"+(width/2)+"px", "left":"50%"}, speed, effect, function(){
						var top = parseInt((winHeight-height)/2);
						var left = slide.find('.slider-photo').offset().left;
						$(this).removeClass("new").css({"margin-left":"0px", "left": left+"px", "margin-top":"0px", "top": top+"px"});
					});	
				}
				if (opt.socialButton){
					var left = ($(document).width()-width)/2;
					setTimeout(function(){
						slide.find('.slider-social').css({"top": (((winHeight-height)/2)+17)+"px", "left": left+"px"});
						slide.find('.slider-social').animate({"opacity": "1"}, (speed/2.25));
					}, (speed/3.6));
				}				
			}
			else {
				if (opt.innerShadow){
					slide.find('.slider-shadow.new').css({"width": width+"px", "left": moveProc1});
				}
				slide.find('.slider-photo.new').css("opacity", "1").animate({"margin-left":"-"+(width/2)+"px", "left":"50%"}, speed, effect, function(){
					$(this).removeClass("new").attr("style", "opacity:1");
					if (opt.maxHeight){$(this).css("max-height", opt.maxHeight);}
					slide.removeClass("loading");
				});
				if (opt.innerShadow){
					slide.find('.slider-shadow.new').animate({"margin-left":"-"+(width/2)+"px", "left":"50%"}, speed, effect, function(){
						var left = slide.find('.slider-photo').offset().left;
						$(this).removeClass("new").css({"margin-left":"0px", "left": left+"px"});
					});
				}
				if (opt.socialButton){
					var left = ($(document).width()-width)/2;
					setTimeout(function(){
						slide.find('.slider-social').css({"top": "17px", "left": left+"px"});
						slide.find('.slider-social').animate({"opacity": "1"}, (speed/2.25));
					}, (speed/3.6));
				}				
			}
		});		
	},
    hide: function(){
        this.visible = false;
        this.$slider.hide();
        window.location.hash = '#closejSBox';
    },
    setHash: function(){
        try {
            window.location.hash = '#img' + this.current;
        } catch(e) {}
    },
    preload: function(id, n){
        // Предзагружаем следующую фоторафию
        if (jPhotos[id + n]) {
            var preload = document.createElement('img');
            preload.src = jPhotos[id + n];
        }
    }
};

jSlides.init();

}	
})(jQuery);
