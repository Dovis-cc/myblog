/**
 * Created by dell on 2018/10/4.
 */

//获取当前页导航，高亮显示标题
$(function () {
    var url = window.location.href;
    if(url.indexOf('learnlist') >= 0){
        var navLi = $('.learn-page');
        navLi.attr("id", "nav_current");
        navLi.siblings().removeAttr("id");
    }else if(url.indexOf('lifelist') >= 0){
        var navLi = $('.life-page');
        navLi.attr("id", "nav_current");
        navLi.siblings().removeAttr("id");
    }else if(url.indexOf('aboutme') >= 0){
        var navLi = $('.about-page');
        navLi.attr("id", "nav_current");
        navLi.siblings().removeAttr("id");
    }else if(url.indexOf('message') >= 0){
        var navLi = $('.common-page');
        navLi.attr("id", "nav_current");
        navLi.siblings().removeAttr("id");
    }else if(!url.indexOf("/")){
        var navLi = $('.index-page');
        navLi.attr("id", "nav_current");
        navLi.siblings().removeAttr("id");
    }

    $(".search-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var key = $("input[name='key']").val();
        if(!key){
            alert("请输入查询关键字");
        }else{
            window.location = "/search?key="+key;
        }
    })
})