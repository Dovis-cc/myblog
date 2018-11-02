
$(function () {
    var banner = $("#banner");
    // 添加
    $(".add-category").click(function (event) {
        event.preventDefault();
        banner.modal("show");
    })
    // 模态框清除内容
    banner.on('show.bs.modal', function (event) {
       $(this).find("form")[0].reset();
    })
})