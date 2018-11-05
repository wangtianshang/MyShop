$(function(){
	mobileApp();
	function mobileApp(){
		var timer=null;
		$('.moblieApp').hover(function(){
			clearTimeout(timer);
			$(this).addClass('moblieAppA');
			$('.mobileApp_QR').stop(true,true).slideDown();
		},function(){
			timer=setTimeout(function(){$(this).removeClass('moblieAppA');
				$('.mobileApp_QR').slideUp();
			},400)
		})
		$('.mobileApp_QR').hover(function(){
			clearTimeout(timer);
		},function(){
			timer=setTimeout(function(){$('.moblieApp').removeClass('moblieAppA');
				$('.mobileApp_QR').slideUp();
			},400)
		})
	}
	/****购物车*******/
	$('.header_gwc').hover(function(){
		$('.header_goods,.header_nogoods').stop(true,true);
		$('.header_gwc .bgfff').show();
		if($(this).find('.i_num').html()!=0){
			$('.header_goods').slideDown(300);
		}else{
			$('.header_nogoods').slideDown(300);
		}
	},function(){
		$('.header_goods,.header_nogoods').filter(':visible').slideUp(300,function(){
			$('.header_gwc .bgfff').hide();
		})
	})
	$('.header_goods li').hover(function(){
		$('.header_goods li').css('background','#fff');
		$(this).css('background','#fafafa');
	})

	/*****************/

	/*********首页导航**************/
	IndexNav();
	function IndexNav(){
		var timer=null;
		$('.nav_snav li').mouseover(function(){
			$('.nav_snav li').removeClass('active');
			$('.nav_snav_con').hide();
			$(this).addClass('active');
			$('.nav_snav_con').eq($(this).index()).show();
		})
		$('.nav_l').hover(function(){
			clearTimeout(timer);
		},function(){
			timer=setTimeout(function(){
				$('.nav_snav li').removeClass('active');
				$('.nav_snav_con').fadeOut(200);
			},1000)
		})
	}

	
	
/******首页轮播图*********/	
	var marginLeft=$('.cont').offset().left+$('.nav_l').width()
	$('.imgs img').css('margin-left',marginLeft)
	$('.banner_tab').css('margin-left',marginLeft)
	$('.dotshadow').css('min-width',$('.dot').width())
	
	$('.banner_w').hover(function(){
		clearInterval(timer);
		$('.banner_tab').fadeIn();
		
	},function(){
		$('.banner_tab').fadeOut();
		autoPlay()
		
	})
	var imgs=$('.imgs li');
	var imgsLength=imgs.length;
	var sum=imgsLength-1;
	var timer=null;
	for(var i=0; i<imgsLength; i++){
		$('.dot ul').append('<li></li>')
	}
	var dots=$('.dot li');
	dots.eq(sum).animate({'width':'42px'},3000);
	$('.dotshadow').css('min-width',dots.outerWidth(true)*imgsLength)
	$('.dotshadow').css('max-width',dots.outerWidth(true)*imgsLength+42)
	$('.pre').click(function(){
		sum--;
		if(sum<0){
			sum=imgsLength-1;
		}
		imgs.hide();
		dots.stop().css('width',13);
		imgs.eq(sum).fadeIn();
		dots.eq(sum).animate({'width':'42px'},3000);
	})
	
	$('.next').click(function(){
		playFn();
	})
	
	autoPlay();
	function playFn(){
		sum++;
		if(sum>imgsLength-1){
			sum=0;
		}
		imgs.hide();
		//dots.removeClass('active');
		dots.stop().css('width',13)
		imgs.eq(sum).fadeIn();
		dots.eq(sum).animate({'width':'42px'},3000)
		//dots.eq(sum).addClass('active');
	}
	
	function autoPlay(){
		timer=setInterval(playFn,3000)
	}



	/****购物车*******/
	$('.header_goods li').hover(function(){
		$('.header_goods li').css('background','#fff');
		$(this).css('background','#fafafa');
	})


})