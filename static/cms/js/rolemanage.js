/**
 * Created by dell on 2018/10/13.
 */

$(function () {
    // 添加角色
    $(".submit-btn").click(function (event) {
        event.preventDefault();

        var name = $("input[name='name']").val();
        var permission = $("select[name='permission']").val();
        var desc = $("input[name='desc']").val();
        var csrf_token = $("meta[name='csrf_token']").attr("content");

        $.post({
            "url": "/cms/add_role/",
            "data": {
                "name": name,
                "permission": permission,
                "desc": desc,
                "csrf_token": csrf_token
            },
            "success": function (data) {
                if(data["code"] == 200){
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

    // 删除角色
    $(".delete-btn").click(function(event){
        event.preventDefault();
        var self = $(this);
        var name = self.parent().parent().attr("role_name");
        if(confirm("确定删除 "+name+" 吗？")){
            $.get({
                "url": "/cms/delete_role/",
                "data": {
                    "name": name
                },
                "success": function (data) {
                    if(data["code"] == 200){
                        window.location.reload();
                    }else{
                        alert(data["message"]);
                    }
                },
                "fail": function (error) {
                    alert("网络错误");
                }
            })
        }
    })
})