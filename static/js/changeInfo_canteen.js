function hashvalue(word) {
    //这部分是哈希函数，看你数据库里是怎么储存定义的了，我暂时就先不写这个哈希函数
    return word
}

function callback(data, status) {
    if (status === "success") {
        alert("账户已注销");
        window.location.pathname = "logout";
    }
    else
    {
        alert("注销失败");
    }
}

$("#delete").click(
    function () {
        let csrf = $("#csrf").val();
        $.post("", {"delete_canteen": true, "csrfmiddlewaretoken": csrf}, callback);
    }
)

function callback_pwd(data, status) {
    if (status === "")
        alert("密码修改成功");
    else
        alert("密码修改失败");
}

$("#modify_password").click(
    function () {
        let csrf = $("#csrf").val();
        let old_password = $("#old_password").val();
        let new_password = $("#new_password").val();
        $.post("", {
            "modify_password": true,
            "old_password": old_password,
            "new_password": new_password,
            "csrfmiddlewaretoken": csrf
        }, callback_pwd);
    }
)