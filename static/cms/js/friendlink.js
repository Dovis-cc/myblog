/**
 * Created by dell on 2018/10/13.
 */

$(function () {
    // 添加按钮
    $(".add-btn").click(function (event) {
        event.preventDefault();
        $("input[name='name']").val("");
        $("input[name='link']").val("");
        $("input[name='priority']").val("");
        $("input[name='remark']").val("");
        var btn = $(".submit-btn");
        btn.removeAttr("sub-type");
        btn.removeAttr("fl-id");
        $("#banner").modal('show');
    })

    // 提交按钮
    $(".submit-btn").click(function (event) {
        event.preventDefault();
        var self = $(this)
        var name = $("input[name='name']").val();
        var link = $("input[name='link']").val();
        var priority = $("input[name='priority']").val();
        var remark = $("input[name='remark']").val();
        var csrf_token = $("meta[name='csrf_token']").attr("content")

        var url = "/cms/add_friendlink/"
        if(self.attr("sub-type") == "update"){
            url = "/cms/update_fl/";
        }
        var fl_id = self.attr("fl-id");

        $.post({
            "url": url,
            "data": {
                "name": name,
                "link": link,
                "priority": priority,
                "remark": remark,
                "fl_id": fl_id,
                "csrf_token": csrf_token
            },
            "success": function (data) {
                if(data["code"] == 200){
                    alert(data["message"])
                    window.location.reload();
                }else{
                    alert(data["message"])
                }
            },
            "fail": function (error) {
                alert("网络错误");
            }
        })
    })

    // 编辑按钮
    $(".update-btn").click(function (event) {
        event.preventDefault();
        $("#banner").modal('show');
        var self = $(this);
        var btn = $(".submit-btn");

        var tr = self.parent().parent();
        var name = tr.attr("name");
        var link = tr.attr("link");
        var priority = tr.attr("priority");
        var remark = tr.attr("remark");
        var fl_id = tr.attr("fl_id");

        $("input[name='name']").val(name);
        $("input[name='link']").val(link);
        $("input[name='priority']").val(priority);
        $("input[name='remark']").val(remark);

        btn.attr("sub-type", "update");
        btn.attr("fl-id", fl_id);
    })

    // 删除按钮
    $(".delete-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var fl_id = self.parent().parent().attr("fl_id");
        if(confirm("确定删除？")){
            // window.location.href = "/cms/delete_fl/"+fl_id;
            $.get({
                "url": "/cms/delete_fl/",
                "data": {
                    "fl_id": fl_id
                },
                "success": function (data) {
                    if(data["code"] == 200){
                        window.location.reload();
                    }else{
                        alert(data["message"])
                    }
                },
                "fail": function (error) {
                    alert("网络错误");
                }
            })
        }
    })
})