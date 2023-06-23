$('.addBookList').click(
    function () {
        $('.listContent').prepend('<div style="margin: 7px; padding: 4px;">' +
            '<input style="margin: 3px;" name="ISBN" type="text" placeholder="输入ISBN号">' +
            '<input style="margin: 3px;" name="lend_num" type="number" placeholder="输入借阅的数量" min="1">' +
            '<button class="deleteCouple" onclick="deleteCouple(this)" style="margin: 3px; width: 35px; height: 32px;" type="button">-</button>' +
            '</div>');
    }
)

function deleteCouple (this_button){
    $(this_button).parent().remove();
}
