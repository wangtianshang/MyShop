$(function(){
	
	/*********非首页导航**************/
	mobileApp();
	function mobileApp(){
		var timer=null;
		$('.moblieApp').hover(function(){
			clearTimeout(timer);
			$(this).addClass('moblieAppA');
			$('.mobileApp_QR').stop(true,true).slideDown();
		},function(){
			timer=setTimeout(function(){$('.moblieApp').removeClass('moblieAppA');
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
	Nav();
	function Nav(){
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
				$('.nav_snav').fadeOut(200);
				$('.nav_l h3 i').removeClass('show').addClass('hide');
			},1000)
		})
				
		$('.nav_l h3').mouseover(function(){
			clearTimeout(timer);
			$('.nav_snav').fadeIn();
			$('.nav_l h3 i').removeClass('hide').addClass('show');
			
		})
		
	}

	/****购物车*******/
	$('.header_gwc').hover(function(){
		$('.header_goods,.header_nogoods').stop(true,true);
		$('.header_gwc .bgfff').show().css('display','block');
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
	$('.ipt_mail').focus(function(){
		$(this).parents('.ipt_mail_c').addClass('active');
		if($(this).val()=='请输入账号'){
			$(this).val('');
		}
	})
	$('.ipt_mail').blur(function(){
		$(this).parents('.ipt_mail_c').removeClass('active');
		if($(this).val()==''){
			$(this).val('请输入账号');
		}
	})
	$('.ipt_code').focus(function(){
		$(this).addClass('active');
		if($(this).val()=='验证码'){
			$(this).val('');
		}
	})
	$('.ipt_code').blur(function(){
		$(this).removeClass('active');
		if($(this).val()==''){
			$(this).val('验证码');
		}
	})

	$('.password_t').focus(function(){
		$(this).hide();
		$(this).siblings('.ipt_password').show().focus().addClass('active');
		$(this).parents('.ipt_password_c').addClass('active');
	})
	$('.ipt_password').blur(function(){
		if($(this).val()==''){
			$(this).hide();
			$(this).siblings('.password_t').show();
		}
		$(this).parents('.ipt_password_c').removeClass('active');
		$(this).removeClass('active');
	})

	$('.ipt_password').focus(function(){
		$(this).addClass('active');
		$(this).parents('.ipt_password_c').addClass('active');
	})
	//修改密码

	$('.ipt_pass,.focusBorder,input:password').focus(function(){
		$(this).css('border-color','#f36b11');
	})
	$('.ipt_pass,.focusBorder,input:password').blur(function(){
		$(this).css('border-color','');
	})
})