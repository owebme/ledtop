			$(function() {

				var $el = $( '#random-items' ),
					windy = $el.windy( {
						// rotation and translation boundaries for the items transitions
						boundaries : {
							rotateX : { min : 40 , max : 90 },
							rotateY : { min : -15 , max : 45 },
							rotateZ : { min : -10 , max : 10 },
							translateX : { min : -400 , max : 400 },
							translateY : { min : -400 , max : 400 },
							translateZ : { min : 350 , max : 550 }
						}
					} ),
					allownavnext = false,
					allownavprev = false;

				$( '#nav-prev' ).on( 'mousedown', function( event ) {

					allownavprev = true;
					navprev();
				
				} ).on( 'mouseup mouseleave', function( event ) {

					allownavprev = false;
				
				} );

				$( '#nav-next' ).on( 'mousedown', function( event ) {

					allownavnext = true;
					navnext();
				
				} ).on( 'mouseup mouseleave', function( event ) {

					allownavnext = false;
				
				} );

				function navnext() {
					if( allownavnext ) {
						windy.next();
						setTimeout( function() {	
							navnext();
						}, 150 );
					}
				}

				function navprev() {
					if( allownavprev ) {
						windy.prev();
						setTimeout( function() {	
							navprev();
						}, 150 );
					}
				}

			});