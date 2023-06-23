function callback(data, status){
    alert(status)
    window.location.reload();
}

$(".finishOrder").click(
    function () {
        let csrf = $("#csrf").val();
        let index = $(".finishOrder").index($(this));
        let orderID = parseInt($(".orderID").get(index).innerHTML);
        $.post("", {"finishOrder": true, "csrfmiddlewaretoken": csrf, "orderID": orderID}, callback);
    }
)