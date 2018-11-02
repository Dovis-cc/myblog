/**
 * Created by dell on 2018/10/18.
 */


$(function () {
    // 动态插入回复框
    $(".reply-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var div = self.parent().parent().parent().parent().next();
        // 隐藏所有回复框 ----------------------
        var reply_btns = $(".reply-btn");
        var objdivs = $(".child-message-block");
        for(var i=0; i<reply_btns.length; i++){
            if(self.is(reply_btns.eq(i))){
                continue;
            }
            reply_btns.eq(i).text("回复");  // 必须用eq(i)来取
        }
        for(var j=0; j<objdivs.length; j++){
            if(div.is(objdivs.eq(j))){
                continue;
            }
            objdivs.eq(j).children().remove();
            objdivs.eq(j).removeAttr("flag");
            objdivs.eq(j).hide();
        }
        // ---------------------- ----------------------
        if(!div.attr("flag")){
            div.append(
                "<form>"+
                    "<textarea class='form-control' rows='5' name='message' placeholder='欢迎吐槽...'></textarea>"+
                    "<div class='requried'>"+
                        "<div class='input-group form-group'>"+
                          "<span class='input-group-addon'>昵称（必填）</span>"+
                          "<input type='text' name='nickname' class='form-control' placeholder='昵称'>"+
                        "</div>"+
                        "<div class='input-group'>"+
                          "<span class='input-group-addon'>邮箱（必填）</span>"+
                          "<input type='email' name='email' class='form-control' placeholder='邮箱'>"+
                        "</div>"+
                    "</div>"+
                    "<div class='sub-btn'>"+
                        "<button type='button' class='btn btn-info reply-sub-btn'>立即提交</button>"+
                    "</div>"+
                "</form>"
            );
            div.attr("flag", "false");
            div.show();
            self.text("取消回复");
        }else{
            div.children().remove();
            self.text("回复");
            div.removeAttr("flag");
            div.hide();
        }
    })

    // 提交评论
    $(".message-sub-btn").click(function (event) {
        event.preventDefault();
        var message = $("textarea[name='message1']").val();
        var nickname = $("input[name='nickname1']").val();
        var email = $("input[name='email1']").val();
        var csrf_token = $("meta[name='csrf_token']").attr("content");

        if(!message || !nickname || !email){
            alert("请输入完整的有效信息");
            return;
        }
        $.post({
            "url": "/add_message/",
            "data": {
                "message": message,
                "nickname": nickname,
                "email": email,
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

    //提交回复
    $("body").on("click", ".reply-sub-btn" ,function (event) {
        event.preventDefault();
        var self = $(this);
        var base = self.parent().parent().parent().parent();
        var message = base.find("textarea[name='message']").val();
        var nickname = base.find("input[name='nickname']").val();
        var email = base.find("input[name='email']").val();
        var prev_id = base.attr("message-id");
        var csrf_token = $("meta[name='csrf_token']").attr("content");
        if(!message || !nickname || !email || !prev_id ){
            alert("请输入完整信息");
            return;
        }
        $.post({
            "url": "/reply_message/",
            "data": {
                "message": message,
                "nickname": nickname,
                "email": email,
                "prev_id": prev_id,
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
})

