var dirs_ajax = '/cgi-bin/admin/modules';

$(document).ready(function(){

	"use strict";

	var $clientsTable = $("#clients-table");

	if ($("#private_enter").length){
		$.cookie('private_enter', true, {expires: 1/2, path: '/'});
	}
	
	var $datatable = $clientsTable.find("#datatable-buttons");
	
	$datatable.length !== 0 && $datatable.DataTable({
		order:[[0,"desc"]],
		dom: "Bfrtilp",
		buttons: [{
			extend: "copy",
			className: "btn-sm"
		}, {
			extend: "csv",
			className: "btn-sm"
		}, {
			extend: "excel",
			className: "btn-sm"
		}, {
			extend: "pdf",
			className: "btn-sm"
		}, {
			extend: "print",
			className: "btn-sm"
		}],	
        language: {
			"search": "Поиск",
            "lengthMenu": "Показано _MENU_ записей на странице",
            "zeroRecords": "Совпадающих записей не найдено",
            "info": "Страницы _PAGE_ из _PAGES_",
            "infoEmpty": "Нет записей в наличии",
            "infoFiltered": "(отфильтровано из _MAX_ записей)"
        },		
		initComplete: function(){}			
	});
	
	$datatable.on('order.dt search.dt page.dt length.dt', debounce(tableRefresh, 300));
	
	function tableRefresh(){
		console.log("refresh");
		$selectInit.status();
		$openPopup.popup();		
	};
	
	var fnActions = function(){};
	
	fnActions.prototype = {
		status: function(){
			if (this.el) this.el.off("change");
			this.el = $clientsTable.find(".select.groups > select");
			this.el.on("change", function(){
				var $row = $(this).parent().parent().parent();
				var id = $row.data("id");
				var group = $(this).val();
				$row.addClass("saved");
				var params = new Object();
				params.client_id = id;
				params.change_group = group;
				$.post(dirs_ajax+'/clients_ajax.cgi', params, function(data){	
					if (data == "true"){
						setTimeout(function(){
							$row.removeClass("saved");
						}, 50);			
					}
				});				
			});
		},
		
		popup: function(){
			if (this.el) this.el.destroyMfpFastClick();
			this.el = $clientsTable.find(".ajax-popup-link").magnificPopup({
				type: "ajax",
				removalDelay: 250,
				callbacks: {
					ajaxContentAdded: function() {
						var $content = $(".mfp-content");
						checkbox_init($content);
						$content.find("input[name=user_person]").on("click", function(){
							var value = $(this).val();
							if (value == "2"){
								$("table.form").removeClass("hide");
							}
							else {
								$("table.form").addClass("hide");
							}
						});	
						$content.find("button.submit").on("click", function(){
							var user_id = $content.find(".white-popup-block").data("id");
							var company = $content.find("input.u_company").val();
							var person = $content.find("input[name=user_person]:checked").val();
							if (person == "2" && company.length < 2){
								alert("Введите название компании");
								return false;
							}
							else {
								$(".button-submit").prepend('<div class="ajax">Cохранение данных...</div>');
								var params = new Object();
								params.saveClientData = true;
								params.user_id = user_id;
								params.user_person = person;
								params.u_company = company;
								params.u_ogrn = $content.find("input.u_ogrn").val();
								params.u_inn = $content.find("input.u_inn").val();
								params.u_kpp = $content.find("input.u_kpp").val();
								params.u_okpo = $content.find("input.u_okpo").val();
								params.u_raschet = $content.find("input.u_raschet").val();
								params.u_korchet = $content.find("input.u_korchet").val();
								params.u_bik = $content.find("input.u_bik").val();
								$.post(dirs_ajax+'/clients_ajax.cgi', params, function(data){
									if (data == "true"){
										setTimeout(function(){
											$(".button-submit").find(".ajax").fadeOut(300, function(){
												$(this).remove();
											});
										}, 50);
										var $row = $clientsTable.find("tr[data-id='"+user_id+"']");
										$row.find("td.person").text(person == 2?'Юр. лицо':'Физ. лицо');
										if (person == "2"){
											$row.find("td.name").text(company);
										}
									}
								});
							}
						});
					}
				}
			});
		}
	};
	
	var $selectInit = new fnActions(),
		$openPopup = new fnActions();
	
	$selectInit.status();
	$openPopup.popup();
	
	function debounce(fn, timeout, invokeAsap, ctx) {
		if (arguments.length == 3 && typeof invokeAsap != 'boolean') {
			ctx = invokeAsap;
			invokeAsap = false;
		}

		var timer;

		return function() {

			var args = arguments;
            ctx = ctx || this;

			invokeAsap && !timer && fn.apply(ctx, args);

			clearTimeout(timer);

			timer = setTimeout(function() {
				!invokeAsap && fn.apply(ctx, args);
				timer = null;
			}, timeout);

		};
	};	
	
});
