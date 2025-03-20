document.addEventListener("DOMContentLoaded", function () {
    let toggleButton = document.querySelector(".toggle"); 
    const sidebar = document.querySelector(".sidebar");
    const homepageURLs = ["/", "/dishcovery/"];

    if (homepageURLs.includes(window.location.pathname)) {
        sidebar.classList.add("sidebar-active");
        toggleButton.classList.add("toggle-active");
    }

    toggleButton.onclick = function () {
        sidebar.classList.toggle("sidebar-active");
        toggleButton.classList.toggle("toggle-active");
    };
});
