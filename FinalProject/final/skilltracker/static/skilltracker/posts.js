document.addEventListener('DOMContentLoaded', function () {
    let blogpost = document.getElementById("blogpost").value
    let user = document.getElementById("user").value

    // On click, change like status
    document.getElementById("like").addEventListener('click', () => like_click(blogpost, user));

    // On load, check for like status
    like_check(blogpost);

});

/*
    Checks the post's object and see if the user has already liked the post. If so, it will unlike the post.
 */

function like_check(blogpost) {
    fetch(`likes/${blogpost}`, {
        // Add GET request to update if post is already liked by user
    })
        .then(response => response.json())
        .then(entry => {

            const likeButton = document.getElementById("like");

            if (entry.liked) {
                likeButton.innerHTML = "Liked <i class=\"bi bi-hand-thumbs-up-fill\"></i>";
            } else {
                likeButton.innerHTML = "Like <i class=\"bi bi-hand-thumbs-up\"></i>";
            }
        })
}

function like_click(blogpost, user) {
    fetch(`likes/${blogpost}`, {
        method: 'PUT',
        body: JSON.stringify({user: user})
    })
        .then(response => response.json())
        .then(entry => {

            const likeButton = document.getElementById("like");

            if (entry.liked) {
                likeButton.innerHTML = "Like <i class=\"bi bi-hand-thumbs-up\"></i>";
            } else {
                likeButton.innerHTML = "Liked <i class=\"bi bi-hand-thumbs-up-fill\"></i>";
            }
        })
}

// fetch(`likes/${blogpost}`, {
//     method: 'PUT',
//     body: JSON.stringify({user: user}),

// function go_to_tag() {
//     // Take button's innerhtml
//     // Pass it in to another url

