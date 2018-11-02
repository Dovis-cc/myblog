/**
 * Created by dell on 2018/10/11.
 */

$(function () {
    $("#submit_btn").click(function (event) {
        event.preventDefault();
        var oldpwdInput = $("input[name='oldpwd']");
        var newpwdInput = $("input[name='newpwd']");
        var renewpwdInput = $("input[name='renewpwd']");
        var csrf_token = $("meta[name='csrf_token']").attr("content");

        var oldpwd = oldpwdInput.val();
        var newpwd = newpwdInput.val();
        var renewpwd = renewpwdInput.val();

        if(!oldpwd){
            alert("请输入旧密码");
        }else if(!newpwd){
            alert("请输入新密码");
        }else if(!renewpwd){
            alert("请确认新密码");
        }else{
            $.post({
                "url": "/cms/resetpwd/",
                "data": {
                    "oldpwd": oldpwd,
                    "newpwd": newpwd,
                    "renewpwd": renewpwd,
                    "csrf_token": csrf_token
                },
                "success": function (data) {
                    oldpwdInput.val("");
                    newpwdInput.val("");
                    renewpwdInput.val("");
                    alert(data["message"]);
                },
                "fail": function (error) {
                    alert("网络错误");
                }
            })
        }
    })
})