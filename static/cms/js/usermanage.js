/**
 * Created by dell on 2018/10/13.
 */


$(function () {
    var csrf_token = $("meta[name='csrf_token']").attr('content');
    // 添加用户
    $("#submit-btn1").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var email = $("input[name='email']").val();
        var password = $("input[name='password']").val();
        var remark = $("input[name='remark']").val();
        var role = $("select[name='role']").val();

        $.post({
            "url": "/cms/add_user/",
            "data": {
                "email": email,
                "password": password,
                "remark": remark,
                "role": role,
                "csrf_token": csrf_token,
            },
            "success": function (data) {
                if(data["code"] == 200){
                    $("#banner1").modal('hide');
                    alert(data["message"]);
                    window.location.reload();
                }else{
                    alert(data["message"]);
                }
            },
            "fail": function (error) {
                alert("网络错误");
            }
        })
    })

    // 删除用户
    $(".dele-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr("user_id");
        var email = tr.attr("email");
        if(confirm("确定删除用户："+email+" 吗?")){
            $.get({
                "url": "/cms/delete_user/",
                "data": {
                    "user_id": user_id
                },
                "success": function (data) {
                    if(data["code"] == 200){
                        window.location.reload();
                    }else{
                        alert(data["message"])
                    }
                },
                "fail": function (error) {
                    alert("网络错误")
                }
            })
        }
    })

    // 编辑用户
    $(".update-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr = self.parent().parent();
        var user_id = tr.attr("user_id");  // 绑定
        var btn = $(".submit-btn2");
        btn.attr("user_id", user_id);
        var oldremark = tr.attr("remark");  // 回显
        var oldrole = tr.attr("role");
        $("input[name='remark2']").val(oldremark);
        $("#role2 option[value='"+oldrole+"']").attr("selected", true)
    })

    $(".submit-btn2").click(function (event) {
        event.preventDefault();
        var self = $(this)
        var user_id = self.attr("user_id");
        var remark = $("input[name='remark2']").val();
        var role = $("#role2").val();

        $.post({
            "url": "/cms/update_user/",
            "data": {
                "user_id": user_id,
                "remark": remark,
                "role": role,
                "csrf_token": csrf_token
            },
            "success": function (data) {
                if(data["code"] == 200){
                    window.location.reload();
                }else{
                    alert(data["message"])
                }
            },
            "fail": function (error) {
                alert("网络错误")
            }
        })
    })

    // 拉黑
    $(".lahei").click(function (event) {
        event.preventDefault();
        var user_id = $(this).parent().parent().attr("user_id");
        $.get({
            "url": "/cms/lahei/",
            "data": {
                "user_id": user_id
            },
            "success": function (data) {
                if(data["code"] == 200){
                    window.location.reload();
                }else{
                    alert(data["message"]);
                }
            }
        })
    })

    // 可用
    $(".keyong").click(function (event) {
        event.preventDefault();
        var user_id = $(this).parent().parent().attr("user_id");
        $.get({
            "url": "/cms/keyong/",
            "data": {
                "user_id": user_id
            },
            "success": function (data) {
                if(data["code"] == 200){
                    window.location.reload();
                }else{
                    alert(data["message"]);
                }
            }
        })
    })
})