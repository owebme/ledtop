$(document).ready(function(){

$("div#backup_files a.name").click(function(){
	var name_zip = $(this).html();
	if (confirm('Вы хотите восстановить бэкап "'+name_zip+'"?'))
	{return true} else {return false}	
});

$("div#backup_files a.del").click(function(){
	var name_zip = $(this).prev().html();
	if (confirm('Вы хотите удалить бэкап "'+name_zip+'"?'))
	{return true} else {return false}	
});


});