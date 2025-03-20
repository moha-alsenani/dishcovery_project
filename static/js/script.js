document.addEventListener("DOMContentLoaded", function () {
    // Function for sidebar menu toggle
    let toggleButton = document.querySelector(".toggle"); 
    let icon = toggleButton.querySelector("i");
    const sidebar = document.querySelector(".sidebar");

    toggleButton.onclick = function () {
        if (icon.classList.contains("fa-bars")) {
            icon.classList.replace("fa-bars", "fa-times");
        } else {
            icon.classList.replace("fa-times", "fa-bars");
        }
    };

    toggleButton.addEventListener("click", function () {
        sidebar.classList.toggle("sidebar-active");
        toggleButton.classList.toggle("toggle-active");
    });
});
