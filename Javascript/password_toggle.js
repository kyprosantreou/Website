function togglePasswordVisibility() {
    var passwordField = document.getElementById('password');
    var toggleButton = document.querySelector('.toggle-password');

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleButton.style.backgroundImage = "url('../Assets/eye-off.svg')"; // Replace 'eye-off.svg' with your eye-off icon image
    } else {
        passwordField.type = "password";
        toggleButton.style.backgroundImage = "url('../Assets/eye.svg')"; // Replace 'eye.svg' with your eye icon image
    }
}
