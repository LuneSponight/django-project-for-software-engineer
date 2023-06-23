function deleteAccount() {
    let userID = document.querySelector(".user-id").innerHTML;
    $.post(
        "",
        {
            'userID': userID,
            'QDeleteAccount': true,
            'csrfmiddlewaretoken': $("#csrf").val()
        },
        callback
    )
}

function callback(status) {
    if (status === "") {
        alert("账户已注销");
        window.location.pathname = "loginout";
    }
    else
    {
        alert("注销失败");
    }
}

document.querySelector(".deleteAccount").addEventListener('click', deleteAccount);
