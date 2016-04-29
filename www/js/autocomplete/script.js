/*jslint  browser: true, white: true, plusplus: true */
/*global $: true */

$(function () {
    'use strict';

	if (!('ontouchstart' in document.documentElement) && document.getElementById("private-basket") === null){
		// Load countries then initialize plugin:
		$.ajax({
			url: '/cgi-bin/product_ajax.cgi?autocomplete=load',
			dataType: 'json'
		}).done(function (source) {

			var countriesArray = $.map(source, function (value, key) { return { value: value, data: key }; }),
				countries = $.map(source, function (value) { return value; });

			$('input#word_search').autocomplete({
				lookup: countriesArray,
				onSelect: function (suggestion) {
					var params = new Object();
					var alias = suggestion.data.replace(/(.+?)\[(.+?)\]/g, '$1');
					params.give_cat_alias = alias;
					$.post('/cgi-bin/product_ajax.cgi', params, function(data){
						if (data != "") {
							location.replace("/products/"+data+"/"+alias);			
						}
					});
				}
			});
			
		});
	}

});