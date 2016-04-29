$(function(){
	var alias = window.location.href;
	var p_id = String(alias.replace(/(.+?)\/(\d+)$/,"$2"));
	var viewed = $.cookie("viewed_products");
	var count="";
	if (viewed){
		var reg	= /(\d+)/g;
		count = viewed.match(reg);
		count = count.length;
		viewed = viewed.replace(p_id+"\|","");
		if (count > 12){viewed = viewed.replace(/(.+?)(\d+)\|$/,"$1");}
		$.cookie('viewed_products', p_id+'|'+viewed, {expires: 1, path: '/'});
	}
	else {
		$.cookie('viewed_products', p_id+'|', {expires: 1, path: '/'});
	}
});