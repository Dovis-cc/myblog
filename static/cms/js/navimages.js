/**
 * Created by dell on 2018/10/14.
 */

$(function () {
    // 添加图片 表单提交
    $(".submit-btn01").click(function (event) {
        event.preventDefault();
        var csrf_token = $("meta[name='csrf_token']").attr("content");
        var csrfInput = $("input[name='csrf_token']");
        csrfInput.attr("value", csrf_token)
        var form = $(".add-form")
        form.submit();
    })

    // 删除
    $(".delete-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var id = self.parent().parent().attr("image_id");
        if(confirm("确定删除？")){
            $.get({
            "url": "/cms/delete_timage/",
            "data": {
                "id": id
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
    
    // 编辑
    $(".update-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var banner = $("#banner02");
        banner.modal("show");
        var mtk = $(".submit-btn02");
        var descInput = banner.find("input[name='desc']");
        var hrefInput = banner.find("input[name='href']");
        var priorityInput = banner.find("input[name='priority']");

        var tr = self.parent().parent();
        var desc = tr.attr("desc");
        var href = tr.attr("href");
        var priority = tr.attr("priority");
        var id = tr.attr("image_id");

        descInput.val(desc);
        hrefInput.val(href);
        priorityInput.val(priority);

        mtk.attr("image_id",id);
    })

    $(".submit-btn02").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var banner = $("#banner02")
        var id = self.attr("image_id");
        var desc = banner.find("input[name='desc']").val();
        var href = banner.find("input[name='href']").val();
        var priority = banner.find("input[name='priority']").val();
        var csrf_token = $("meta[name='csrf_token']").attr("content");
        $.post({
            "url": "/cms/update_timage/",
            "data": {
                "timage_id": id,
                "desc": desc,
                "href": href,
                "priority": priority,
                "csrf_token": csrf_token
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
    })
})