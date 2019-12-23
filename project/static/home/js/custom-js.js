$(document).ready(function(){
	function centerModals(){
	  $('.modal').each(function(i){
		var $clone = $(this).clone().css('display', 'block').appendTo('body');
		var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
		top = top > 0 ? top : 0;
		$clone.remove();
		$(this).find('.modal-content').css("margin-top", top);
	  });
	}
	$('.modal').on('show.bs.modal', centerModals);
	$(window).on('resize', centerModals);
});
/*******************  Mixitup ************************/	
//Property Page
jQuery(document).ready(function(){
	"use strict";
	jQuery(".property-type li a").on('click',function(){
		var property_type = jQuery(this).attr('data-id');
		jQuery(".property-type li a").removeClass("active");
		jQuery(this).addClass("active");
		jQuery(".carousel.slide.carousel-slide-recent-property").css('display','none');
		jQuery("div[data-target="+property_type+"]").css('display','block');

		if( property_type == 'All'){
			jQuery(".carousel.slide.carousel-slide-recent-property").css('display','block');
		}

		if( property_type == 'All'){
			jQuery(".property-list-list").css('display','block');
			jQuery(".carousel-slide-recent-property").css('display','block');
		} else {
			jQuery(".property-list-list").css('display','none');
			jQuery(".carousel-slide-recent-property").css('display','none');
			jQuery("div[data-target="+property_type+"]").css('display','block');
		}		
	});
});
/********************  MENU RESPONSIVE  ************************/	
	$(function() {
		var $menu = $("#navigation").clone();
		$menu.attr( "id", "mobile-menu" );
		$menu.mmenu({
			extensions	: [ 'effect-slide', 'pageshadow' ],
			header		: true,
			searchfield	: true,
			counters	: false
		});
	});

//For Dropdown Hovers
$(function($){
	//open/close mega-navigation
	$('.cd-dropdown-trigger').on('click', function(event){
		event.preventDefault();
		toggleNav();
	});

	//close meganavigation
	$('.cd-dropdown .cd-close').on('click', function(event){
		event.preventDefault();
		toggleNav();
	});

	//on mobile - open submenu
	$('.has-children').children('a').on('click', function(event){
		//prevent default clicking on direct children of .has-children 
		event.preventDefault();
		var selected = $(this);
		selected.next('ul').removeClass('is-hidden').end().parent('.has-children').parent('ul').addClass('move-out');
	});

	//on desktop - differentiate between a user trying to hover over a dropdown item vs trying to navigate into a submenu's contents
	var submenuDirection = ( !$('.cd-dropdown-wrapper').hasClass('open-to-left') ) ? 'right' : 'left';
	$('.cd-dropdown-content').menuAim({
        activate: function(row) {
        	$(row).children().addClass('is-active').removeClass('fade-out');
        	if( $('.cd-dropdown-content .fade-in').length == 0 ) $(row).children('ul').addClass('fade-in');
        },
        deactivate: function(row) {
        	$(row).children().removeClass('is-active');
        	if( $('li.has-children:hover').length == 0 || $('li.has-children:hover').is($(row)) ) {
        		$('.cd-dropdown-content').find('.fade-in').removeClass('fade-in');
        		$(row).children('ul').addClass('fade-out')
        	}
        },
        exitMenu: function() {
        	$('.cd-dropdown-content').find('.is-active').removeClass('is-active');
        	return true;
        },
        submenuDirection: submenuDirection,
    });

	//submenu items - go back link
	$('.go-back').on('click', function(){
		var selected = $(this),
			visibleNav = $(this).parent('ul').parent('.has-children').parent('ul');
		selected.parent('ul').addClass('is-hidden').parent('.has-children').parent('ul').removeClass('move-out');
	}); 

	function toggleNav(){
		var navIsVisible = ( !$('.cd-dropdown').hasClass('dropdown-is-active') ) ? true : false;
		$('.cd-dropdown').toggleClass('dropdown-is-active', navIsVisible);
		$('.cd-dropdown-trigger').toggleClass('dropdown-is-active', navIsVisible);
		if( !navIsVisible ) {
			$('.cd-dropdown').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',function(){
				$('.has-children ul').addClass('is-hidden');
				$('.move-out').removeClass('move-out');
				$('.is-active').removeClass('is-active');
			});	
		}
	}

	//IE9 placeholder fallback
	//credits http://www.hagenburger.net/BLOG/HTML5-Input-Placeholder-Fix-With-jQuery.html
	if(!Modernizr.input.placeholder){
		$('[placeholder]').focus(function() {
			var input = $(this);
			if (input.val() == input.attr('placeholder')) {
				input.val('');
		  	}
		}).blur(function() {
		 	var input = $(this);
		  	if (input.val() == '' || input.val() == input.attr('placeholder')) {
				input.val(input.attr('placeholder'));
		  	}
		}).blur();
		$('[placeholder]').parents('form').submit(function() {
		  	$(this).find('[placeholder]').each(function() {
				var input = $(this);
				if (input.val() == input.attr('placeholder')) {
			 		input.val('');
				}
		  	})
		});
	}
});


/********************  OWL  Sliders ************************/
//About US
$("#owl-testimonial-1").owlCarousel({
	autoPlay: true, //Set AutoPlay to 3 seconds
    items : 1,
	navigation : true
});



//Main Slider Home Page
  $('#main-slider.carousel').carousel({
	  interval: 8000,
	  singleItem : true,
	  transitionStyle : "goDown"
	   
  });

//Testinomial						  
    $("#owl-demo").owlCarousel({
		autoPlay: true,
        items : 4,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:2
            },
            1024:{
                items:3
            }
        }
    });	
     
	var sync1 = $("#sync1");
	var sync2 = $("#sync2");
     
	sync1.owlCarousel({
	  singleItem : true,
	  slideSpeed : 1000,
	  navigation: true,
	  pagination:false,
	  afterAction : syncPosition,
	  responsiveRefreshRate : 200,
	});
   
	sync2.owlCarousel({
	  items : 5,
	  itemsDesktop      : [1199,10],
	  itemsDesktopSmall     : [979,10],
	  itemsTablet       : [768,8],
	  itemsMobile       : [479,4],
	  pagination:false,
	  responsiveRefreshRate : 100,
	  afterInit : function(el){
		el.find(".owl-item").eq(0).addClass("synced");
	  }
	});
     
	function syncPosition(el){
	  var current = this.currentItem;
	  $("#sync2")
		.find(".owl-item")
		.removeClass("synced")
		.eq(current)
		.addClass("synced")
	  if($("#sync2").data("owlCarousel") !== undefined){
		center(current)
	  }
	}
     
      $("#sync2").on("click", ".owl-item", function(e){
        e.preventDefault();
        var number = $(this).data("owlItem");
        sync1.trigger("owl.goTo",number);
      });
     
      function center(number){
        var sync2visible = sync2.data("owlCarousel").owl.visibleItems;
        var num = number;
        var found = false;
        for(var i in sync2visible){
          if(num === sync2visible[i]){
            var found = true;
          }
        }
     
        if(found===false){
          if(num>sync2visible[sync2visible.length-1]){
            sync2.trigger("owl.goTo", num - sync2visible.length+2)
          }else{
            if(num - 1 === -1){
              num = 0;
            }
            sync2.trigger("owl.goTo", num);
          }
        } else if(num === sync2visible[sync2visible.length-1]){
          sync2.trigger("owl.goTo", sync2visible[1])
        } else if(num === sync2visible[0]){
          sync2.trigger("owl.goTo", num-1)
        }
        
      }
     



/********************  popup Form ************************/	
	$('.form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

	});
/********************  Tab ************************/	
	$('.tab a').on('click', function (e) {
	  
	  e.preventDefault();
	  
	  $(this).parent().addClass('active');
	  $(this).parent().siblings().removeClass('active');
	  
	  target = $(this).attr('href');
	
	  $('.tab-content > div').not(target).hide();
	  
	  $(target).fadeIn(600);
	  
	});


/*******************  SELECTBOX ************************/
        // change style for select box
        $(".selectbox").selectbox();

        $('.nstSlider').nstSlider({
            "left_grip_selector": ".leftGrip",
            "right_grip_selector": ".rightGrip",
            "value_bar_selector": ".bar",
            "value_changed_callback": function(cause, leftValue, rightValue) {
                $(this).parent().find('.leftLabel').text(leftValue);
                $(this).parent().find('.rightLabel').text(rightValue);
            }
        });
/*******************  SHOW FILTER ************************/
        // show more filter - Search form
        $('.more-filter').on('click',function(){
            $('.more-filter').toggleClass('show-more');
            $('.more-filter .text-1').toggleClass('hide');
            $('.more-filter .text-2').toggleClass('hide');
        });
/*******************  SELECT 2 ************************/
        $(".select-featured").select2({
            tags: true,
            tokenSeparators: [',', ' '],
        })
		

/******************* ScrollUp ************************/

$(function () {
		$.scrollUp({
	        scrollName: 'scrollUp', // Element ID
	        scrollDistance: 300, // Distance from top/bottom before showing element (px)
	        scrollFrom: 'top', // 'top' or 'bottom'
	        scrollSpeed: 300, // Speed back to top (ms)
	        easingType: 'linear', // Scroll to top easing (see http://easings.net/)
	        animation: 'fade', // Fade, slide, none
	        animationSpeed: 200, // Animation in speed (ms)
	        scrollTrigger: false, // Set a custom triggering element. Can be an HTML string or jQuery object
					//scrollTarget: false, // Set a custom target element for scrolling to the top
	        scrollText: '<i class="fa fa-angle-up"></i>', // Text for element, can contain HTML
	        scrollTitle: false, // Set a custom <a> title if required.
	        scrollImg: false, // Set true to use image
	        activeOverlay: false, // Set CSS color to display scrollUp active point, e.g '#00FFFF'
	        zIndex: 2147483647 // Z-Index for the overlay
		});
	});

