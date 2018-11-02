/**
 * Created by dell on 2018/10/19.
 */

$(function () {

    $(".post-submit-btn").click(function (event) {
        event.preventDefault();
        var title = $("input[name='title']").val();
        var cate_id = $("select[name='cate_id']").val();
        editor.sync();
        var content = $('#editor_id').val();
        if(!title || !cate_id || !content){
            alert("请输入完整的有效信息");
        }else{
            $("#post-form").submit();
        }
    })
})