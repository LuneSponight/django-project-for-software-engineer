function hashvalue(word) {
    //�ⲿ���ǹ�ϣ�������������ݿ�������ô���涨����ˣ�����ʱ���Ȳ�д�����ϣ����
    return word
}

function callback(data, status) {
    if (status === "success") {
        alert("�˻���ע��");
        window.location.pathname = "logout";
    }
    else
    {
        alert("ע��ʧ��");
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
        alert("�����޸ĳɹ�");
    else
        alert("�����޸�ʧ��");
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