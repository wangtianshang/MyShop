$(function(){
	
	/********** 列表页 ************/
	// 列表页导航下方标签选择
	listTagFn();
	function listTagFn(){
		var array=[];
		var onOffArr=[];
		$('.l_select dl').each(function(index){
			array[index]=$(this).height();
		})
		$('.l_select dl').height(42);
		$('.more').click(function(){
			var index=$(this).parent().index();
			if(onOffArr[index]){
				onOffArr[index]=false;
				$(this).parent().stop(true,true).animate({'height':42},400);
				$(this).find('span').removeClass('active').text('更多 ');
			}else{
				onOffArr[index]=true;
				$(this).parent().stop(true,true).animate({'height':array[index]},400);
				$(this).find('span').addClass('active').text('收起');
			}
		})	
		
	}
	
	$('.listL li').hover(function(){
		$(this).addClass('active');
	},function(){
		$(this).removeClass('active');	
	})
	/********** 列表页 end ************/
	
	
	/************ 详情页  ****************/
	/***** 详情页放大镜 ********/
	Magnifier();
	function Magnifier(){
		if(!$('#float-box')){return false;}
		//切换图片
		$(".allImg li").mouseover(function() {   
			$(".allImg li").removeClass("current");   
			$(this).addClass("current");    
			var src = $(this).find('img').attr("src");    
			$("#small-box img").attr("src", src.replace("_s", "_m"));    
			$("#big-box img").attr("src", src.replace("_s", "_b"));   
		});
		
		var boxWidth=$('.allImg').width();
		var liWidth=$('.allImg li').outerWidth(true);
		var ulWidth=liWidth*$('.allImg li').length;
		
		$('.allImg ul').width(ulWidth)	
		
		$('.allImg_w .d_pre').hover(function(){
			if(parseInt($('.allImg ul').css('left'))<0){
				$(this).removeClass('d_pre').addClass('d_pre_a');	
			}
		},function(){
			$(this).removeClass('d_pre_a').addClass('d_pre');
		})
		
		$('.allImg_w .d_pre').click(function(){
			if(parseInt($('.allImg ul').css('left'))<0){
				$('.allImg ul').animate({'left':'+='+liWidth},400);
				if(-parseInt($('.allImg ul').css('left'))< liWidth+1 ){
					$(this).removeClass('d_pre_a').addClass('d_pre');
				}		
			}		
		})
		
		$('.allImg_w .d_next').hover(function(){
			var n1=-parseInt($('.allImg ul').css('left'))+boxWidth;
			if(n1<=ulWidth){
				$(this).removeClass('d_next').addClass('d_next_a');	
			}
		},function(){
			$(this).removeClass('d_next_a').addClass('d_next')
		})
		$('.allImg_w .d_next').click(function(){
			var n1=-parseInt($('.allImg ul').css('left'))+boxWidth;
			if(n1<=$('.allImg ul').width()){
				$('.allImg ul').animate({'left':'-='+liWidth},400);
				if(n1> (ulWidth-liWidth-1)){
					$(this).removeClass('d_next_a').addClass('d_next');
				}		
		
			}
		})
			
		// 放大镜	
		$('#mark').hover(function(){
			$('#float-box').show();	
			$('#big-box').show();	
			$('.i_magnifier').hide();
		},function(){
			$('#float-box').hide();
			$('#big-box').hide();
			$('.i_magnifier').show();
		})
		$('#mark').mousemove(function(evt){
			var left=evt.pageX-$('#small-box').offset().left-$('#float-box').width()/2;
			var top=evt.pageY-$('#small-box').offset().top-$('#float-box').height()/2;
			if(left<0){
				left=0;
			}else if(left>$('#mark').width()-$('#float-box').width()){
				left=$('#mark').width()-$('#float-box').width();
			}
			if(top<0){
				top=0;
			}else if(top>$('#mark').height()-$('#float-box').height()){
				top=$('#mark').height()-$('#float-box').height()
			}
			$('#float-box').css({
				left:left,
				top:top
			});
			var percentX=left/($('#small-box').width()-$('#float-box').width())
			var percentY=top/($('#small-box').height()-$('#float-box').height())
			$('#big-box img').css({
				left:-percentX*($('#big-box img').width()-$('#big-box').width()),
				top:-percentY*($('#big-box img').height()-$('#big-box').height())
			})
				
		})
	}
	
	/***** 详情页放大镜  end ********/
	
	/************* 收藏 **************/	
	$('.s_m1_collect').click(function(){
		$(this).find('i').toggleClass('star_o','star_w')
	})
	
	$('.s_m1r_div2 a').click(function(){
		$(this).parents('.s_m1r_divC').find('a').removeClass('active');
		$(this).addClass('active');
		return false;
	})
	
	/********* 购物车跟随 ***************/
	followingCart();
	function followingCart(){
		if(!document.getElementById('tabBar')){return false;}
		
		var scrollT=$('.s_m2_r').offset().top;
		$(window).scroll(function(){
			if($(window).scrollTop()>scrollT){
				$('.tabBar').addClass('fixed_tabBar')
				$('.fixed_tabBar').css({
					'right':0,
					'width':$(window).width()
				})
				$('.fixed_tabBar ul').css({
					'width':'968px',
					'margin-left':$('.s_m2_r').offset().left+1,
					'border-left':'1px solid #e5e5e5'
				})
				$('.tabBar div').show();
			}else{
				$('.tabBar').removeClass('fixed_tabBar')
				$('.tabBar').css({
					'right':0,
					'width':''
				})
				$('.tabBar ul').css({
					'width':'968px',
					'margin-left':0,
					'border-left':'0'
				})
				$('.tabBar div').hide();
			}
		})
	}
	/********* 购物车跟随 end ***************/
	
	/********** 产品展示导航跟随 ***************/
	detail_content_tab();
	function detail_content_tab(){
		if(!$('.s_d_nav')){return false;}
		var lineHeight=$('.s_d_nav li').height()*$('.s_d_nav li').length-30;	
		$('.s_dr_line').height(lineHeight);
		var scrollTop=[];
		$('.s_dl .section').each(function(index){
			scrollTop.push( $(this).offset().top );
		})
		$(window).scroll(function(){
			var y=$(window).scrollTop();
			if( y <scrollTop[0]-42){
				$('.s_d_nav').css('right',0).removeClass('fixed_s_nav');
				return;
			}
			for(var j=0;j<scrollTop.length; j++){
				if(y<scrollTop[j]){
					break;
				}
				
			}
			$('.s_d_nav').css('right',$('.cont').offset().left+1).addClass('fixed_s_nav')
			$('.s_d_nav a').removeClass('active');
			if(j<1){j=1;}
			$('.s_d_nav a').eq(j-1).addClass('active');
		})
		
		$('.s_d_nav a').click(function(){
			var i=$(this).parent().index();
			$('html,body').animate({'scrollTop':scrollTop[i]},400);
			return false;
		})
	}
	/********** 产品展示导航跟随 end ***************/
	
	
	$('.s_m2_rt_h li').click(function(){
		if($(this).index()<$('.s_m2_rt_h li').length-1){}
		$('.s_m2_rt_h li').removeClass('active');
		$('.s_m2_r_content').hide();
		$(this).addClass('active');
		$('.s_m2_r_content').eq($(this).index()).show();
		$('html,body').animate({'scrollTop':$('.s_m2_r').offset().top},400)
	})
	
	
	/*******评价图片 *************/
	$('.review_img li').click(function(){
		$('.review_img li').removeClass('active');
		$(this).addClass('active');	
		var box=$(this).parents('.review_img').siblings('.review_img_l');
		box.show().animate({
			'width':'404px',
			'height':'404px'	
		},400)
		box.find('img').attr('src',$(this).find('img').attr('src'))
	})
	/************/
	$('.s_review_tab span').click(function(){
		$('.s_review_tab span').removeClass('active');
		$('.s_review_tabDiv').hide();
		$(this).addClass('active');
		$('.s_review_tabDiv').eq($(this).index()).show();
		
	})

	/*************** 详情页 end*******************/


	/********  登录页  *************/
	$('.signIn_autoM').click(function(){
		$(this).find('i').toggleClass('checked');
	})
	/********  登录页 end  *************/

	/********  个人中心     **************/
	$('.user_4 tr').hover(function(){
		$(this).find('.hide').css('display','block');
	},function(){
		$(this).find('.hide').css('display','none');
	})
	// 优惠券与我的订单切换
	$('.zgright-nav-ul li').hover(function(){
		$('.zgright-nav-ul li').find('a').removeClass('active');
		$('.zg-right-tabC').removeClass('active');
		$(this).find('a').addClass('active');
		$('.zg-right-tabC').eq($(this).index()).addClass('active');
	})

	//商品评价
	$('.evaluateD_mr textarea').focus(function(){
		var str='商品是否给力？快分享你的购买心得吧';
		$(this).css('border-color','#f36b11')
		if($(this).html()==str){
			$(this).html('');
		}
	})
	$('.evaluateD_mr textarea').blur(function(){
		var str='商品是否给力？快分享你的购买心得吧';
		$(this).css('border-color','#e9e9e9')
		if($(this).html()==''){
			$(this).html(str);
		}
	})
	
	$('.user_5 a.evaluate').click(function(){
		$('.user_5 a.evaluate').fadeIn().parents('li').find('.evaluateD').slideUp();
		$(this).fadeOut().parents('li').find('.evaluateD').slideDown();
	})
	$('.delivery').click(function(evt){
		$(this).parents('.evaluateD').slideUp();
		$(this).parents('li').find('.evaluate').fadeIn();
		evt.preventDefault();
	})
	// 商品评价-->star
	evaluateSFn();
	function evaluateSFn(){
		var onOff=true;
		var classNameC='';
		var classNameA='';
		var scoreAIndex=5;
		var classList='review_star1 review_star2 review_star3 review_star4 review_star5'+classNameA;
		var score=['1分','2分','3分','4分','5分','']
		$('.evaluteS i').mouseover(function(){
			classNameC='review_star'+( $(this).index()+1 );
			$(this).parents('.review_star').removeClass(classList).addClass(classNameC);
			$(this).parents('.review_star').next('.star_score').html(score[$(this).index()]);
		})
		$('.evaluteS').mouseout(function(){
			if(onOff){
				$(this).removeClass(classList);
				
			}else{
				$(this).removeClass(classList).addClass(classNameA);
			}
			$(this).next('.star_score').html(score[scoreAIndex]);
		})
		$('.evaluteS i').click(function(){
			onOff=false;
			classNameA='review_star'+( $(this).index()+1 );
			scoreAIndex=$(this).index();
			$(this).parents('.review_star').removeClass(classList).addClass(classNameA);
			$(this).parents('.review_star').next('.star_score').html(score[scoreAIndex]);
		})
	}	
	//个人信息内容
	$('.userInfo_radio').click(function(){
		$(this).find('i').toggleClass('checked',true);
		$(this).siblings('.userInfo_radio').find('i').toggleClass('checked',false);
	})

	/*******  订单  ****************/

	// 购物车页
	order1Fn();
	function order1Fn(){
		var onOff=true;
		$('.order1_c dd .order1_checkbox').click(function(){
			$(this).find('i').toggleClass('checked');
			$(this).parents('dd').toggleClass('active');
		})
		$('.order1_c dd .order1_checkbox').click(function(){
			var totalLength=$('.order1_c dd').length;
			var checkedLength=$('.order1_c dd .order1_checkbox i.checked').length;
			if(totalLength>checkedLength){
				$('.order1_checkbox_total i').removeClass('checked');
				onOff=true;
			}else if(totalLength==checkedLength){
				$('.order1_checkbox_total i').addClass('checked');
				onOff=false;
			}
		})
		$('.order1_checkbox_total').click(function(){
			$('.order1_checkbox_total').find('i').toggleClass('checked');
			$('.order1_c dd').toggleClass('active',onOff);
			$('.order1_c dd .order1_checkbox i').toggleClass('checked',onOff);
			if(onOff==true){
				onOff=false;
			}else{
				onOff=true;
			}
		})
	}
	//订单确认
	$('.order2_yhq_tabN li').hover(function(){
		$('.order2_yhq_tabN li').removeClass('active');
		$('.order2_yhq_tabC').hide();
		$(this).addClass('active');
		$('.order2_yhq_tabC').eq($(this).index()).show();
	})
	//订单支付页
	$('.order3_tabNav li').mouseover(function(){
		$('.order3_tabNav li').find('a').removeClass('active');
		$('.order3_tabC').hide();
		$(this).find('a').addClass('active')
		$('.order3_tabC').eq($(this).index()).show();
	})
	$('.order3_tabC li').hover(function(){
		$(this).addClass('active');
	},function(){
		$(this).removeClass('active');
	})
	
	$('.pay').click(function(){
		$('.pay_info_W').show();	
		$('.pay_info_shadow,.pay_info').fadeIn();	
	})
	$('.pay_info_close,.pay_finished,.changeMethod').click(function(){
		$('.pay_info_W').fadeOut();	
	})

	//订单确认页	
	$('.U_shdz li').hover(function(){
		$('.U_shdz li .order2_defalteSet').hide();
		$(this).css('background-color','#fcf7f4').find('.order2_defalteSet').fadeIn(100);
	},function(){
		$(this).css('background-color','').find('.order2_defalteSet').hide();
	})
	
	$('.U_wlxx li span').click(function(){
		$('.U_wlxx li span').removeClass('u_xz')
		$(this).addClass('u_xz')
	})
	
	$('.model_select').click(function(evt){
		if($(this).find('.select_so').css('display')=='none'){
			$('.model_select .select_so').hide();
			$(this).find('.select_so').slideDown();
		}else{
			
			$(this).find('.select_so').slideUp();
		}
		evt.stopPropagation();
	})
	
	$('.model_select li').live('mouseover',function(){
        $(this).siblings('li').removeClass('active');
        $(this).addClass('active')
    }).live("mouseout",function(){
        $(this).removeClass('active');
    });

	if(document.getElementById('js_modelSelect')){
		$(document).on('click',function(){
			$('.select_so').hide();
		})
	}


	$('.pay_info_close,.fixed_ipt').click(function(){
		$(this).parents('.fixed_shadow_c').fadeOut();
		$(this).parents('.fixed_shadow_w').fadeOut();
	})
	$('.addAddressBtn,.add_addr').click(function(){
		$('.fixed_shadow_w').fadeIn();
		$('.addAddress').fadeIn();
	})
	$('.cancle_address_b').click(function(){
		$('.fixed_shadow_w').fadeIn();
		$('.cancel_address').fadeIn();
	})
	$('.order2_yhq_submit').click(function(){
		$('.fixed_shadow_w').fadeIn();
		$('.yhq_exchange').fadeIn();
	})
});
function getcontent(obj){
    $('.model_select li').removeClass('active');
    $(obj).addClass('active');
    $(obj).siblings('li').removeClass('activeS');
    $(obj).addClass('activeS');
    $(obj).parents('.select_c').find('.select_cs').html($(obj).text())
}
