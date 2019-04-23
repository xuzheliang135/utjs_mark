function check_password() {
    let password = form1.password.value;
    let password_valid = form1.password_valid.value;
    if (password === "") {
        alert("请输入密码！");
        form1.password.focus();
    } else if (password_valid === "") {
        alert("请确认密码！");
        form1.password_valid.focus();
    } else if (password !== password_valid) {
        alert("两次密码输入不一致！");
        form1.password_valid.focus();
    } else form1.submit();
}