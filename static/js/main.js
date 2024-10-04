/*  ---------------------------------------------------
    Template Name: Dreams
    Description: Dreams wedding template
    Author: Colorib
    Author URI: https://colorlib.com/
    Version: 1.0
    Created: Colorib
---------------------------------------------------------  */

'use strict';

(function ($) {

    /*------------------
        Preloader
    --------------------*/
    $(window).on('load', function () {
        $(".loader").fadeOut();
        $("#preloder").delay().fadeOut("slow");

        /*------------------
            Portfolio filter
        --------------------*/
        $('.portfolio__filter li').on('click', function () {
            $('.portfolio__filter li').removeClass('active');
            $(this).addClass('active');
        });
        if ($('.portfolio__gallery').length > 0) {
            var containerEl = document.querySelector('.portfolio__gallery');
            var mixer = mixitup(containerEl);
        }
    });

    
    /*------------------
        Background Set
    --------------------*/
    $('.set-bg').each(function () {
        var bg = $(this).data('setbg');
        $(this).css('background-image', 'url(' + bg + ')');
    });


    $('nav a').click(function(e) {

        // 클릭한 링크의 href 속성 값을 통해 목표 섹션 선택
        const target = $(this.hash);

        // 해당 섹션으로 부드럽게 스크롤
        $('html, body').animate({
            scrollTop: target.offset().top
        }, 800);

        // 모든 네비게이션 링크에서 활성화 클래스 제거
        $('nav a').removeClass('active');

        // 클릭된 링크에 활성화 클래스 추가
        $(this).addClass('active');
    });

    // 스크롤 시 현재 위치에 따라 네비게이션 버튼 활성화 업데이트
    $(window).on('scroll', function() {
        const scrollPosition = $(this).scrollTop();

        $('section').each(function() {
            const sectionTop = $(this).offset().top - 100; // 오차 보정
            const sectionBottom = sectionTop + $(this).outerHeight();

            // 스크롤 위치가 섹션 안에 있으면 해당 섹션의 네비게이션 버튼 활성화
            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                const currentSection = $(this).attr('id');
                setTimeout(() => {
                    console.log(currentSection)
                    $('nav li').removeClass('active');
                    $('nav li.'+currentSection).addClass('active');
                }, 10);
            }
        });
    });


    
    //Masonary
    $('.work__gallery').masonry({
        itemSelector: '.work__item',
        columnWidth: '.grid-sizer',
        gutter: 10
    });

    /*------------------
		Navigation
	--------------------*/
    $(".mobile-menu").slicknav({
        prependTo: '#mobile-menu-wrap',
        allowParentLinks: true
    });

    /*------------------
		Hero Slider
	--------------------*/
    $('.hero__slider').owlCarousel({
        loop: true,
        dots: true,
        mouseDrag: true,
        nav:true,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        items: 1,
        margin: 0,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: false,
    });
    

    var dot = $('.hero__slider .owl-dot');
    dot.each(function () {
        var index = $(this).index() + 1;
        if (index < 10) {
            $(this).html('0').append(index);
        } else {
            $(this).html(index);
        }
    });

    /*------------------
        Testimonial Slider
    --------------------*/
    $(".testimonial__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        dotsEach: 2,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 3
            },
            768: {
                items: 2
            },
            320: {
                items: 1
            }
        }
    });

    /*------------------
        Latest Slider
    --------------------*/
    $(".latest__slider").owlCarousel({
        loop: true,
        margin: 0,
        items: 3,
        dots: true,
        dotsEach: 2,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 3
            },
            768: {
                items: 2
            },
            320: {
                items: 1
            }
        }
    });

    /*------------------
        Logo Slider
    --------------------*/
    $(".logo__carousel").owlCarousel({
        loop: true,
        margin: 100,
        items: 6,
        dots: false,
        smartSpeed: 1200,
        autoHeight: false,
        autoplay: true,
        responsive: {
            992: {
                items: 5
            },
            768: {
                items: 4
            },
            480: {
                items: 3
            },
            20: {
                items: 2
            }
        }
    });

    /*------------------
        Video Popup
    --------------------*/
    // $('.video-popup').magnificPopup({
    //     type: 'iframe'
    // });

    /*------------------
        Counter
    --------------------*/
    $('.counter_num').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 4000,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

})(jQuery);

function check() {
    document.getElementsById("emailForm").action = "https://script.google.com/macros/s/AKfycbyG_ModAoFQxq3BnOKjts0N9GPHVGK5sMiOeEyeu8nRruhE6dJE67NgrVBaOybSYxUU/exec";
    var email = document.getElementById("email").value;
    if (email != "") {
        var exptext = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;
        if (exptext.test(email) == false) {
            //이메일 형식이 알파벳+숫자@알파벳+숫자.알파벳+숫자 형식이 아닐경우			
            alert("입력한 메일형식이 올바르지 않습니다.");
            document.formtag.email.focus();
            document.getElementById("form태그의 id").action = " ";
        }
    }
}