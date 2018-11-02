/**
 * Created by dell on 2018/10/11.
 */

// 获取邮箱验证码
$(function () {
    $("#captcha").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var email = $("input[name='email']").val();
        if(!email){
            alert("请输入邮箱");
            return;
        }
        $.get({
            "url": "/cms/captcha/",
            "data":{
                "email": email
            },
            "success": function (data) {
                if(data["code"] == 200){
                    self.attr("disabled","disabled")
                    var count = 60;
                    self.text(count+"秒后重试")
                    var timmer = setInterval(function () {
                        count --;
                        self.text(count+"秒后重试")
                        if(count<=0){
                            self.text("获取验证码");
                            self.removeAttr("disabled");
                            clearInterval(timmer);
                        }
                    }, 1000);
                }else{
                    alert(data["message"]);
                }
            },
            "fail": function (error) {
                alert("网络错误");
            }
        })
    })

    $("#submit_btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        var captcha = $("input[name='captcha']").val();
        var password = $("input[name='password']").val();
        var repassword = $("input[name='repassword']").val();
        var csrf_token = $("meta[name='csrf_token']").attr("content")
        $.post({
            "url": "/cms/findpassword/",
            "data": {
                "email":email,
                "captcha": captcha,
                "password": password,
                "repassword": repassword,
                "csrf_token": csrf_token
            },
            "success": function(data){
                if(data["code"] == 200){
                    alert("重置密码成功，快去登录吧")
                    window.location = "/cms/login/";
                }else{
                    alert(data["message"]);
                }
            },
            "fail": function (error) {
                alert("网络错误");
            }
        })
    })
})