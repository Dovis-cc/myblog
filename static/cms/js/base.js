/**
 * Created by Administrator on 2016/12/17.
 */

$(function () {
    $('.nav-sidebar>li>a').click(function (event) {
        var that = $(this);
        if(that.children('a').attr('href') == '#'){
            event.preventDefault();
        }
        if(that.parent().hasClass('unfold')){
            that.parent().removeClass('unfold');
        }else{
            that.parent().addClass('unfold').siblings().removeClass('unfold');
        }
        console.log('coming....');
    });

    $('.nav-sidebar a').mouseleave(function () {
        $(this).css('text-decoration','none');
    });
});


$(function () {
    var url = window.location.href;
    if(url.indexOf('profile') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(0).addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('resetpwd') >= 0){
        var profileLi = $('.profile-li');
        profileLi.addClass('unfold').siblings().removeClass('unfold');
        profileLi.children('.subnav').children().eq(1).addClass('active').siblings().removeClass('active');
    }else if(url.indexOf('navimage') >= 0){
        var navimageLi = $('.navimage-manage');
        navimageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('friendlink') >= 0){
        var friendlinkLi = $('.friendlink-manage');
        friendlinkLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('message') >= 0){
        var messageLi = $('.message-manage');
        messageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('comments') >= 0) {
        var commentsManageLi = $('.comments-manage');
        commentsManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('category') >= 0){
        var tagManageLi = $('.cate-manage');
        tagManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('rolemanage') >= 0){
        var roleManageLi = $('.role-manage');
        roleManageLi.addClass('unfold').siblings().removeClass('unfold');
    }else if(url.indexOf('usermanage') >= 0){
        var userManageLi = $('.user-manage');
        userManageLi.addClass('unfold').siblings().removeClass('unfold');
    }
});