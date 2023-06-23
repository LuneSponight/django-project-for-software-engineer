function callback(status){
    alert(status)
}

$(document).ready(
    $(".deleteBook").click(
        function () {
            let csrf = $("#csrf").val();
            let index = $('.deleteBook').index($(this));
            let ISBN = $('.ISBN').get(index).innerHTML;
            $.post('',
                {
                    'delete': true,
                    'ISBN': ISBN,
                    "csrfmiddlewaretoken": csrf,
                },
                callback
            )
        }
    )
)