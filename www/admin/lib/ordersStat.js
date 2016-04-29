var ajax_scripts = '/admin/scripts/stat';

$(function(){

	var params = new Object();
	params.period = getUrlVars()["period"];
	params.method = "traffic_summary";
	$.get(ajax_scripts+'/yametrika.php', params, function(data){
		if (data !=""){			
			$(".stat-traffic").append('<div style="opacity:0">'+data+'</div>');
			var visitors = parseInt($(".stat-traffic").find("div").find("p:first").find("strong").text());
			var order = parseInt($(".stat-blocks").find(".one").find("span").text());
			if (order > 0 && visitors > 0){
				$(".stat-traffic").find("div").prepend('<p>Посетители/заказы: <strong style="color:#EC6700">'+(visitors/order).toFixed(0)+'</strong></p>');
			}
			$(".stat-traffic").find("div").css("opacity", "1");
		}
	});	

	var params = new Object();
	params.getCampaignsList = true;
	$.get(ajax_scripts+'/yadirect.php', params, function(data){
		if (data !=""){
			$(".stat-direct").hide(0).html('<h3>Баланс директ</h3>'+data);
			var num="";
			$(".stat-direct").find("p").each(function(){
				num++;
				if (num == 14){
					$(this).after('<a href="#" class="opener">Показать все</a>');
				}
				if (num > 14){
					$(this).css("display", "none");
				}
			});
			$(".stat-direct").show(0);
			$(".stat-direct").find(".opener").click(function(){
				$(this).remove();
				$(".stat-direct").find("p").show(0);
				return false;
			});
		}
	});
	
	$(".stat-products").find(".opener").click(function(){
		$(this).next().show(0);
		$(this).remove();
		return false;
	});	

});

function getUrlVars() {
	var vars = {};
	var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
		vars[key] = value;
	});
	return vars;
}
