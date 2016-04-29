/*jslint  browser: true, white: true, plusplus: true */
/*global $: true */

$(function () {
    'use strict';

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
				params.give_cat_alias = suggestion.data;
				$.post('/cgi-bin/product_ajax.cgi', params, function(data){
					if (data != "") {
						location.replace("/products/"+data+"/"+suggestion.data);			
					}
				});
            }
        });
        
    });

});