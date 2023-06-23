function callback(data){
    window.location.reload();
    alert(data);
}

$(document).ready(
    $(".deleteReader").click(
        function () {
            let csrf = $("#csrf").val();
            let index = $('.deleteReader').index($(this));
            let ID = $('.ID').get(index).innerHTML;
            $.post('',
                {
                    'delete': true,
                    'ID': ID,
                    "csrfmiddlewaretoken": csrf,
                },
                callback
            )
        }
    )
)