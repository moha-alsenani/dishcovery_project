document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ JavaScript Loaded!");

    // 🔵 Sidebar Toggle
    let toggleButton = document.querySelector(".toggle");
    const sidebar = document.querySelector(".sidebar");
    const homepageURLs = ["/", "/dishcovery/"];

    if (toggleButton && sidebar) {
        if (homepageURLs.includes(window.location.pathname)) {
            sidebar.classList.add("sidebar-active");
            toggleButton.classList.add("toggle-active");
        }

        toggleButton.onclick = function () {
            sidebar.classList.toggle("sidebar-active");
            toggleButton.classList.toggle("toggle-active");
        };
    }

    // 🔵 Commenting (JS with AJAX)
    const commentForm = document.getElementById("ajax-comment-form");
    const commentsContainer = document.getElementById("comments-container");
    const noCommentsMessage = document.getElementById("no-comments-message");
    const commentStatus = document.getElementById("comment-status");

    if (commentForm) {
        commentForm.addEventListener("submit", function (e) {
            e.preventDefault();

            commentStatus.textContent = "Posting comment...";
            commentStatus.className = "alert alert-info";

            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            const commentText = commentForm.querySelector("textarea[name='text']").value;

            const formData = new FormData();
            formData.append("text", commentText);
            formData.append("csrfmiddlewaretoken", csrfToken);

            fetch(window.location.origin + "/dishcovery/add_comment/", {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
                body: formData,
                credentials: "same-origin"
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "success") {
                        commentForm.reset();
                        if (noCommentsMessage) noCommentsMessage.remove();

                        const newComment = document.createElement("div");
                        newComment.className = "comment";
                        newComment.innerHTML = ` 
                            <p><strong>${data.comment.user}</strong> - ${data.comment.created_at}</p>
                            <p>${data.comment.text}</p>
                        `;

                        commentsContainer.insertBefore(newComment, commentsContainer.firstChild);
                        commentStatus.textContent = "Comment added successfully!";
                        commentStatus.className = "alert alert-success";

                        setTimeout(() => {
                            commentStatus.textContent = "";
                            commentStatus.className = "";
                        }, 3000);
                    } else {
                        commentStatus.textContent = "Error: " + (data.message || "Could not add comment");
                        commentStatus.className = "alert alert-danger";
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    commentStatus.textContent = "Network error: Could not add comment";
                    commentStatus.className = "alert alert-danger";
                });
        });
    }

    // 🔵 Login Form Handling
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const formData = new FormData(loginForm);

            fetch("/dishcovery/login/", {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        window.location.href = data.redirect_url;
                    } else {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error("Login error:", error);
                    alert("Something went wrong. Please try again.");
                });
        });
    }
});
