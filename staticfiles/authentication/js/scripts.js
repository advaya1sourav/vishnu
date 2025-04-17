// Placeholder for future JavaScript
console.log("Authentication script loaded.");
// Enable Bootstrap tooltips
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});




document.getElementById("registerForm").addEventListener("submit", function(event) {
    let username = document.getElementById("id_username").value;
    let phone = document.getElementById("phone").value;
    let password = document.getElementById("id_password1").value;
    let confirmPassword = document.getElementById("id_password2").value;

    // Validate Username (Only letters)
    if (!/^[a-zA-Z]+$/.test(username)) {
        alert("Username should contain only letters.");
        event.preventDefault();
    }

    // Validate Phone (10-digit number)
    if (!/^\d{10}$/.test(phone)) {
        alert("Phone number must be exactly 10 digits.");
        event.preventDefault();
    }

    // Validate Password Match
    if (password !== confirmPassword) {
        alert("Passwords do not match.");
        event.preventDefault();
    }
});