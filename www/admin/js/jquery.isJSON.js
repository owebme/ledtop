(function ($) {

    $.isJSON = function (json) {
        json = json.replace(/\\["\\\/bfnrtu]/g, '@');
        json = json.replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']');
        json = json.replace(/(?:^|:|,)(?:\s*\[)+/g, '');
        return (/^[\],:{}\s]*$/.test(json))
    }

    $.fn.isJSON = function () {
        var json = this;
        if (jQuery(json).is(":input")) {
            json = jQuery(json).val();
            json = new String(json);
            return jQuery.isJSON(json)
        } else {
            throw new SyntaxError("$(object).isJSON only accepts fields!");
        }
    }
	
    String.prototype.isJSON = function () {
        var y = this;
        return jQuery.isJSON(y);
    }

})(jQuery);