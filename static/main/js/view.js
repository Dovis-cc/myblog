/**
 * Created by dell on 2018/10/24.
 */
$(function () {
    // 点赞
    $(".like-btn").click(function (event) {
        event.preventDefault();
        var self = $(this)
        var post_id = self.parent().attr("post_id");
        $.get({
            "url": "/to_star/",
            "data":{
                "post_id": post_id
            },
            "success": function (data) {
                if(data["code"] == 200){
                    var star = data["data"].star
                    console.log(star);
                    self.text("喜欢（"+star+"）");
                    alert(data["message"]);
                }else{
                    alert(data["message"]);
                }
            },
            "fail": function () {
                alert("网络错误");
            }
        })
    })

    //评论
    $(".comment-sub-btn").click(function (event) {
        event.preventDefault();
        var self  =$(this);
        var post_id = self.parent().attr("post_id");
        var nickname = $("input[name='nickname']").val();
        var email = $("input[name='email']").val();
        var content = $("textarea[name='comment']").val();
        var csrf_token = $("meta[name='csrf_token']").attr("content");
        console.log(nickname+email+content)
        if(!nickname || !email || !content){
            alert("请输入完整的有效信息");
            return;
        }

        $.post({
            "url": "/comment/",
            "data": {
                "post_id": post_id,
                "nickname": nickname,
                "email": email,
                "content": content,
                "csrf_token": csrf_token
            },
            "success": function (data) {
                if(data["code"]){
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
})