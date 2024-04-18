function toggleRepeatPasswordVisibility() {
    var repeatPasswordField = document.getElementById('repeat_password');
    var toggleButton = document.querySelector('.toggle-repeat-password');

    if (repeatPasswordField.type === "password") {
        repeatPasswordField.type = "text";
        toggleButton.style.backgroundImage = "url('../Assets/eye-off.svg')"; 
    } else {
        repeatPasswordField.type = "password";
        toggleButton.style.backgroundImage = "url('../Assets/eye.svg')"; 
    }
}
