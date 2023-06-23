const login_button = document.querySelector('.test-button');

function SendLoginMsg() {
    const account = document.querySelector('.account');
    const password = document.querySelector('.password');
    let json = {
        'account':account,
        'password':password
    }

    let post_url = ""
    let msg = JSON.stringify(json);

    $.post(
        post_url,
        msg,
        success()
    )
}

login_button.addEventListener('click', SendLoginMsg);
