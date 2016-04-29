    
    var $header = document.getElementsByTagName("header")[0],
        $header_bg = document.getElementById("header-bg"),
        $lines_section2 = document.getElementById("lines-section2"),
        $lines_section4 = document.getElementById("lines-section4"),
        $lines_section6 = document.getElementById("lines-section6"),
        $callback_phone = document.getElementById("callback-phone"),
        $phone = $callback_phone.getElementsByClassName("phone")[0],
        $phone_tooltip = $callback_phone.getElementsByClassName("tooltip")[0],
        $order_popup = document.getElementById("order_popup"),
        $openCallbackPhone = document.getElementById("openCallbackPhone"),
        offsetFooter = document.getElementById("section7").offsetTop,
        startScroll = document.documentElement.scrollTop || document.body.scrollTop,
        w = window,
        bodyNode = document.body,
        isTouch = false,
        hasClass = function(elem, className) {
          return new RegExp(' ' + className + ' ').test(' ' + elem.className + ' ');
        },
        addClass = function(elem, className) {
          if (!hasClass(elem, className)) {
            elem.className += ' ' + className;
          }
        },
        removeClass = function(elem, name) {
            elem.className = trim((elem.className || '').replace((new RegExp('(\\s|^)' + name + '(\\s|$)')), ' '));
        },
        trim = function(text) {
            return (text || '').replace(/^\s+|\s+$/g, ''); 
        };    
      
    
    if ('ontouchstart' in document.documentElement){
        isTouch = true;
    }

    var image = $header_bg.firstChild;
    var imgSrc = image.getAttribute("src")+"?"+Math.random();
    image.setAttribute("src", imgSrc);
    
    image.onload = function(){
        addClass(document.getElementById("section1"), "show");
        if (!isTouch && window.innerWidth > 1219){
            setTimeout(function(){
                animHeader();
            }, 1000);
        }
        else {
            bodyNode.attributes.removeNamedItem("id");    
        }
    };

    function animHeader(){
        var phone = $header.getElementsByClassName("phone")[0];
        var h1 = $header.getElementsByTagName("H1")[0];
        var h2 = $header.getElementsByTagName("H2")[0];
        var h3_left = $header.getElementsByClassName("left")[0];
        var h3_right = $header.getElementsByClassName("right")[0];
        var light = $header.getElementsByClassName("light")[0];
        var lines = $header.getElementsByClassName("line");

        for (var i=0; i < lines.length; i++){
            removeClass(lines[i], "anim");
        }
        addClass(light, "show");
        setTimeout(function(){
            addClass(h1, "rollIn");
            removeClass(h1, "anim");
            setTimeout(function(){
                addClass(h2, "bounceInDown");
                removeClass(h2, "anim");
                setTimeout(function(){
                    removeClass(phone, "anim");
                    setTimeout(function(){
                        removeClass(h3_left, "anim");
                        setTimeout(function(){
                            removeClass(h3_right, "anim");
                            setTimeout(function(){
                                $header.getElementsByClassName("arrow-down")[0].style.display = "block";
                                //bodyNode.attributes.removeNamedItem("id");
                            }, 500);
                        }, 300);
                    }, 600);
                }, 1200);
            }, 600);
        }, 600);
    }

    $openCallbackPhone.onclick = function(){
        openPopup();
        return false;
    };

    // parallax header
    if (!isTouch && window.innerWidth > 1219){
        
        var section2 = document.getElementById("section2"),
            headerSlide2 = section2.getElementsByTagName("h2")[0],
            animHeaderSlide2 = false,
            itemsSlide2 = section2.getElementsByClassName("items-container-num"),
            animItemsSlide2 = false,
            section3 = document.getElementById("section3"),
            headerSlide3 = section3.getElementsByTagName("h2")[0],
            animHeaderSlide3 = false,
            itemsSlide3 = section3.getElementsByClassName("items-container-item"),
            animItemsSlide3 = false;
            section4 = document.getElementById("section4"),
            headerSlide4 = section4.getElementsByTagName("h2")[0],
            animHeaderSlide4 = false,
            itemsSlide4 = section4.getElementsByClassName("items-container-cover"),
            animItemsSlide4 = false;
            section5 = document.getElementById("section5"),
            headerSlide5 = section5.getElementsByTagName("h2")[0],
            animHeaderSlide5 = false,
            itemsSlide5 = section5.getElementsByClassName("items-container-product"),
            animItemsSlide5 = false;
            section6 = document.getElementById("section6"),
            headerSlide6 = section6.getElementsByTagName("h2")[0],
            animHeaderSlide6 = false,
            itemsSlide6 = section6.getElementsByClassName("items-container")[0],
            animItemsSlide6 = false;        
        
            var defScroll = window.innerHeight-600;
        
        window.onscroll = function(){
            var scroll = document.documentElement.scrollTop || document.body.scrollTop,
            delta = 15*(scroll/1080);            
            $header_bg.setAttribute("style", "transform: translate3d(0px, "+delta+"%, 0px); -webkit-transform: translate3d(0px, "+delta+"%, 0px");
            if (scroll > 300-defScroll && !animHeaderSlide2){
                animHeaderSlide2 = true;
                addClass(headerSlide2, "bounceInUp");
                addClass(headerSlide2, "show");
            }
            if (startScroll > 600 && !animItemsSlide2){
                animItemsSlide2 = true;  
                for (var i=0; i < itemsSlide2.length; i++){
                    addClass(itemsSlide2[i], "show");
                }                
            }
            else if (scroll > 600-defScroll && !animItemsSlide2){
                animItemsSlide2 = true; var interval = 0, j = 0;             
                for (var i=0; i < itemsSlide2.length; i++){
                    setTimeout(function(){
                        addClass(itemsSlide2[j], "flipInX");
                        addClass(itemsSlide2[j], "show");
                        j++;
                    }, interval);
                    interval += 150;
                }
            }            
            if (scroll > 1550-defScroll && !animHeaderSlide3){
                animHeaderSlide3 = true;
                addClass(headerSlide3, "bounceInUp");
                addClass(headerSlide3, "show");
            }
            if (startScroll > 1800 && !animItemsSlide3){
                animItemsSlide3 = true;  
                for (var i=0; i < itemsSlide3.length; i++){
                    addClass(itemsSlide3[i], "show");
                }                
            }
            else if (scroll > 1800-defScroll && !animItemsSlide3){
                animItemsSlide3 = true; var interval = 0, j = 0;             
                for (var i=0; i < itemsSlide3.length; i++){
                    setTimeout(function(){
                        addClass(itemsSlide3[j], "zoomIn");
                        addClass(itemsSlide3[j], "show");
                        j++;
                    }, interval);
                    interval += 150;
                }
            }
            if (scroll > 2800-defScroll && !animHeaderSlide4){
                animHeaderSlide4 = true;
                addClass(headerSlide4, "lightSpeedIn");
                addClass(headerSlide4, "show");
            } 
            if (startScroll > 1800 && !animItemsSlide4){
                animItemsSlide4 = true;  
                for (var i=0; i < itemsSlide4.length; i++){
                    addClass(itemsSlide4[i], "show");
                }                
            }
            else if (scroll > 2940-defScroll && !animItemsSlide4){
                animItemsSlide4 = true; var interval = 0, j = 0;             
                for (var i=0; i < itemsSlide4.length; i++){
                    setTimeout(function(){
                        addClass(itemsSlide4[j], "flipInY");
                        addClass(itemsSlide4[j], "show");
                        j++;
                    }, interval);
                    interval += 150;
                }
            } 
            if (scroll > 3500-defScroll && !animHeaderSlide5){
                animHeaderSlide5 = true;
                addClass(headerSlide5, "lightSpeedIn");
                addClass(headerSlide5, "show");
            } 
            if (startScroll > 1800 && !animItemsSlide5){
                animItemsSlide5 = true;  
                for (var i=0; i < itemsSlide5.length; i++){
                    addClass(itemsSlide5[i], "show");
                }                
            }
            else if (scroll > 3700-defScroll && !animItemsSlide5){
                animItemsSlide5 = true; var interval = 0, j = 0;             
                for (var i=0; i < itemsSlide5.length; i++){
                    setTimeout(function(){
                        addClass(itemsSlide5[j], "fadeInUp");
                        addClass(itemsSlide5[j], "show");
                        j++;
                    }, interval);
                    interval += 150;
                }
            }
            if (scroll > 4900-defScroll && !animHeaderSlide6){
                animHeaderSlide6 = true;
                addClass(headerSlide6, "fadeInUp");
                addClass(headerSlide6, "show");
            }
            if (scroll > 5050-defScroll && !animItemsSlide6){
                animItemsSlide6 = true;
                addClass(itemsSlide6, "fadeInUp");
                addClass(itemsSlide6, "show");
            }            
            if (scroll > 840){
                var delta = 20*((scroll-840)/1292);
                $lines_section2.setAttribute("style", "transform: translate3d(0px, "+delta+"%, 0px); -webkit-transform: translate3d(0px, "+delta+"%, 0px");
            }
            if (scroll > 2800){
                var delta = 20*((scroll-2800)/1292);
                $lines_section4.setAttribute("style", "transform: translate3d(0px, "+delta+"%, 0px); -webkit-transform: translate3d(0px, "+delta+"%, 0px");
            }
            if (scroll > 5080){
                var delta = 20*((scroll-5080)/1429);
                $lines_section6.setAttribute("style", "transform: translate3d(0px, "+delta+"%, 0px); -webkit-transform: translate3d(0px, "+delta+"%, 0px");
            }
            var t = scroll + w.innerWidth / 2;
            if (t >= 2000 && t <= offsetFooter) {
                $callback_phone.style.opacity = 1;
            } else {
                $callback_phone.style.opacity = 0;
            }            
        };
        
        var scene = document.getElementById('scene');
        if (scene !== null){
            var parallax = new Parallax(scene); 
        }  
        
        $phone.onmouseover = function(){
            $callback_phone.setAttribute("class", "hover");
        };
        $phone.onmouseout = function(){
            $callback_phone.attributes.removeNamedItem("class"); 
        };        
        $phone.onclick = function(){
            openPopup();
        };
        
    }

    function openPopup(){
        $order_popup.style.display = "block";
        setTimeout(function(){
            addClass($order_popup, "active-popup");
            $order_popup.getElementsByClassName("popup_close")[0].onclick = function(){
                removeClass($order_popup, "active-popup");
                setTimeout(function(){
                    $order_popup.style.display = "none";   
                }, 400);
                return false;
            };
            $order_popup.onclick = function(e){
                if (e.target.getAttribute("class") == "popup_v"){
                    removeClass($order_popup, "active-popup");
                    setTimeout(function(){
                        $order_popup.style.display = "none";   
                    }, 400);                
                }
            };
        }, 20);
    }