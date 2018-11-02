/**
 * Created by dell on 2018/10/20.
 */

$(function () {
    var banner = $("#banner");
    $("#submit-btn").click(function () {
        event.preventDefault();
        var name = $("input[name='name']").val();
        var parent_id = $(this).attr("parent_id");
        var csrf_token = $("meta[name='csrf_token']").attr("content");
        if(!name){
            alert("请输入名称");
            return;
        }
        var submit_type = $(this).attr("submit-type");
        var url = "/cms/add_parent_cate/"
        if(submit_type == "update"){
            url = "/cms/update_parent_cate/"
        }
        $.post({
            "url": url,
            "data": {
                "name": name,
                "parent_id": parent_id,
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

    // 编辑
    $(".update-btn").click(function (event) {
        event.preventDefault();
        var nameInput = banner.find("input[name='name']");
        var name = $(this).parent().parent().attr("parent_name");
        var parent_id = $(this).parent().parent().attr("parent_id");
        banner.modal("show");
        nameInput.val(name);
        var submit = $("#submit-btn");
        submit.attr("submit-type", "update");
        submit.attr("parent_id", parent_id);
    })

    // 删除
    $(".delete-btn").click(function (event) {
        event.preventDefault();
        var parent_id = $(this).parent().parent().attr("parent_id");
        if(confirm("确定删除？")){
            $.get({
                "url": "/cms/delete_parent_cate/",
                "data": {
                    "parent_id": parent_id
                },
                "success": function (data) {
                    if(data["code"] == 200){
                        window.location.reload();
                    }else{
                        alert(code["message"]);
                    }
                },
                "fail": function (error) {
                    alert("网络错误");
                }
            })
        }
    })
})
