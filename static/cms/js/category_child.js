
$(function () {
    var banner = $("#banner");
    $("#submit-btn").click(function (event) {
        event.preventDefault();
        var name = banner.find("input[name='name']").val();
        var parent_id = $("#second-cate").val()
        var csrf_token = $("meta[name='csrf_token']").attr("content");
        var child_id = $(this).attr("child_id");

        if(!name){
            alert("请输入名称");
            return;
        }
        var submit_type = $(this).attr("submit-type");
        var url = "/cms/add_child_cate/"
        if(submit_type == "update"){
            url = "/cms/update_child_cate/"
        }
        $.post({
            "url": url,
            "data": {
                "name": name,
                "parent_id": parent_id,
                "child_id": child_id,
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

    $(".update-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var nameInput = banner.find("input[name='name']");

        var tr = self.parent().parent();
        var name = tr.attr("child_name");
        var child_id = tr.attr("child_id");
        var parent_id = tr.attr("parent_id");

        banner.modal("show");
        nameInput.val(name);
        $("#second-cate option[value='"+parent_id+"']").attr("selected", true)

        var submit = $("#submit-btn");
        submit.attr("submit-type", "update");
        submit.attr("child_id", child_id);
    })

    $(".delete-btn").click(function (event) {
        var child_id = $(this).parent().parent().attr("child_id");
        if(confirm("确定删除吗")){
            $.get({
                "url": "/cms/delete_child_cate/",
                "data": {
                    "child_id": child_id
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
