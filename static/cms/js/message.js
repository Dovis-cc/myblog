/**
 * Created by dell on 2018/10/27.
 */
$(function () {
    $(".cate-filter").change(function (event) {
        var cate_id = $(".cate-filter").val();
        if (cate_id == "0"){
            window.location = "/cms/message/";
        }else{
            window.location = "/cms/message?cate_id="+cate_id;
        }
    })

    $(".dele-btn").click(function (event) {
        event.preventDefault();
        var tr = $(this).parent().parent();
        var post_id = tr.attr("post_id");
        var post_title = tr.attr("post_name");
        if(post_id){
            if(confirm('您确定要删除文章"'+post_title+'"')){
                $.get({
                    "url": "/cms/delete_post/",
                    "data": {
                        "post_id": post_id
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
        }else{
            alert("没有找到这篇文章")
        }
    })

    $(".update-btn").click(function (event) {
        event.preventDefault();
        alert("该功能还没有实现");
    })
})