/**
 * Created by dell on 2018/10/10.
 */

$(function () {
    $("#submit_btn").click(function (event) {
        event.preventDefault();
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();
        var rememberme = $("#remember").get(0).checked ? 1: 0
        var csrf_token = $("meta[name='csrf_token']").attr("content")
        if(!email){
            alert("请输入邮箱");
            return;
        }else if(!password){
            alert("请输入密码");
            return;
        }
        $.post({
            "url": "/cms/login/",
            "data": {
                "email": email,
                "password": password,
                "rememberme": rememberme,
                "csrf_token": csrf_token
            },
            "success": function (data) {
                if(data["code"] == 200){
                    window.location = "/cms/"
                }else{
                    alert(data["message"])
                }
            },
            "fail": function (error) {
                alert("网络错误")
            }
        })
    })
})