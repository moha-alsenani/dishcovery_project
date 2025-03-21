//Side bar
// For toggle bar
document.addEventListener("DOMContentLoaded", function () {
    // Function for sidebar menu toggle
    let toggleButton = document.querySelector(".toggle");
    let icon = toggleButton.querySelector("i");
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

//Commenting (JS with AJAX)
document.addEventListener('DOMContentLoaded', function () {
    const commentForm = document.getElementById('ajax-comment-form');
    const commentsContainer = document.getElementById('comments-container');
    const noCommentsMessage = document.getElementById('no-comments-message');
    const commentStatus = document.getElementById('comment-status');

    if (commentForm) {
        commentForm.addEventListener('submit', function (e) {
            e.preventDefault();

            // Show loading message
            commentStatus.textContent = 'Posting comment...';
            commentStatus.className = 'alert alert-info';

            // Get the CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Get the comment text
            const commentText = commentForm.querySelector('textarea[name="text"]').value;

            // Create form data
            const formData = new FormData();
            formData.append('text', commentText);
            formData.append('csrfmiddlewaretoken', csrfToken);

            // Send AJAX request
            fetch(window.location.origin + addCommentURL, {
                method: 'POST',
                headers: { 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value },
                body: formData,
                credentials: 'same-origin'
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Clear the form
                        commentForm.reset();

                        // Remove "no comments" message if it exists
                        if (noCommentsMessage) {
                            noCommentsMessage.remove();
                        }

                        // Create and add the new comment to the DOM
                        const newComment = document.createElement('div');
                        newComment.className = 'comment';
                        newComment.innerHTML = `
                        <p><strong>${data.comment.user}</strong> - ${data.comment.created_at}</p>
                        <p>${data.comment.text}</p>
                    `;

                        // Add the comment to the top of the list
                        commentsContainer.insertBefore(newComment, commentsContainer.firstChild);

                        // Show success message
                        commentStatus.textContent = 'Comment added successfully!';
                        commentStatus.className = 'alert alert-success';

                        // Clear status after 3 seconds
                        setTimeout(() => {
                            commentStatus.textContent = '';
                            commentStatus.className = '';
                        }, 3000);
                    } else {
                        // Show error message
                        commentStatus.textContent = 'Error: ' + (data.message || 'Could not add comment');
                        commentStatus.className = 'alert alert-danger';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    commentStatus.textContent = 'Network error: Could not add comment';
                    commentStatus.className = 'alert alert-danger';
                });
        });
    }
});
// Alert message if wrong username and password is entered.
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const formData = new FormData(loginForm);

            fetch("/dishcovery/login/", {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
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
