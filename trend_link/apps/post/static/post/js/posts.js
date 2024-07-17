document.addEventListener('DOMContentLoaded', function () {
    const script = document.querySelector('script[src*="posts.js"]');
    const getPostsUrl = script.dataset.getPostsUrl;
    const updatePostUrl = script.dataset.updatePostUrl;
    const deletePostUrl = script.dataset.deletePostUrl;
    const currentUser = script.dataset.currentUser;
    const profileUrl = script.dataset.profileUrl;

    let nextPageUrl = getPostsUrl;
    let isLoading = false;

    function loadPosts(url) {
        if (isLoading || !url) return;
        isLoading = true;

        $.ajax({
            url: url,
            type: 'GET',
            success: function (response) {
                const postsList = $('#post-list');
                response.results.forEach(post => {
                    postsList.append(createPostCard(post));
                });
                initCommentForms();
                nextPageUrl = response.next;
                isLoading = false;
            },
            error: function () {
                alert('An error occurred while retrieving the posts.');
                isLoading = false;
            }
        });
    }

    function createPostCard(post) {
        const likedClass = post.has_liked ? 'liked' : '';
        return `
        <div class="post-card" data-post-id="${post.id}">
            <div class="post-header">
                <div class="profile-picture">
                    <img src="${post.user.profile.profile_picture}" alt="Profile Picture">
                    <a href="${profileUrl.replace('0', post.user.id)}"><strong>${post.user.username}</strong></a>
                </div>
                <div class="post-buttons">
                    ${post.user.username === currentUser ? createPostButtons(post.id) : ''}
                </div>
            </div>
            <p>${post.text}</p>
            ${post.image ? `<div><img src="${post.image}" alt="Post Image"></div>` : ''}
            <button type="button" class="likeButton ${likedClass}" data-post-id="${post.id}" data-has-liked="${post.has_liked}">Like</button>
            <div class="comments-section">
                <p><strong>Comments:</strong></p>
                <div class="comments">
                    ${loadComments(post)}
                </div>
                <form class="commentForm" method="post">
                    <input type="hidden" name="post" value="${post.id}">
                    <label for="id_text_${post.id}">Comment:</label>
                    <input type="text" id="id_text_${post.id}" name="text">
                    <button type="submit">Add Comment</button>
                </form>
            </div>
        </div>`;
    }

    function createPostButtons(postId) {
        return `
        <button type="button" class="postEdit" data-post-id="${postId}">Edit</button>
        <button type="button" class="postDelete" data-post-id="${postId}">Delete</button>`;
    }

    function loadComments(post) {
        let commentsHtml = post.comments.results.map(comment => createCommentHtml(comment, post.user.username)).join('');
        if (post.comments.next) {
            commentsHtml += `<button type="button" class="loadMoreComments" data-next-url="${post.comments.next}" data-post-id="${post.id}">Load More Comments</button>`;
        }
        return commentsHtml;
    }

    function createCommentHtml(comment, postOwner) {
        return `
        <div class="comment" data-comment-id="${comment.id}">
            <div class="comment-header">
                <img src="${comment.user.profile.profile_picture}" alt="Profile Picture">
                <a href="${profileUrl.replace('0', comment.user.id)}"><strong>${comment.user.username}</strong></a>
                <div class="comment-buttons">
                    ${comment.user.username === currentUser ? `<button type="button" class="commentEdit" data-comment-id="${comment.id}">Edit</button>` : ''}
                    ${comment.user.username === currentUser || postOwner === currentUser ? `<button type="button" class="commentDelete" data-comment-id="${comment.id}">Delete</button>` : ''}
                </div>
            </div>
            <p>${comment.text}</p>
            <p><small>commented on ${comment.created_at}</small></p>
        </div>`;
    }

    $(document).on('click', '.postEdit', function () {
        const postId = $(this).data('post-id');
        const postElement = $(this).closest('.post-card');
        const currentText = postElement.find('p').first().text();
        postElement.append(createUpdateForm(postId, currentText));
    });

    function createUpdateForm(postId, currentText) {
        return `
        <form class="updateForm" data-post-id="${postId}">
            <div>
                <label for="id_text_${postId}">Post:</label>
                <input type="text" id="id_text_${postId}" name="text" value="${currentText}">
            </div>
            <button type="submit">Update</button>
            <button type="button" class="cancelEdit">Cancel</button>
        </form>`;
    }

    $(document).on('submit', '.updateForm[data-post-id]', function (e) {
        e.preventDefault();
        const $form = $(this);
        const postId = $form.data('post-id');
        const updateUrl = updatePostUrl.replace('0', postId);

        $.ajax({
            type: 'PUT',
            url: updateUrl,
            data: $form.serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                const postElement = $(`.post-card[data-post-id="${postId}"]`);
                postElement.find('p').first().text(response.text);
                $form.remove();
            },
            error: function () {
                alert('An error occurred while updating the post.');
            }
        });
    });

    $(document).on('click', '.postDelete', function () {
        const postId = $(this).data('post-id');
        const deleteUrl = deletePostUrl.replace('0', postId);

        $.ajax({
            type: 'DELETE',
            url: deleteUrl,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function () {
                $(`.postDelete[data-post-id="${postId}"]`).closest('.post-card').remove();
            },
            error: function () {
                alert('An error occurred while deleting the post.');
            }
        });
    });

    $(document).on('click', '.cancelEdit', function () {
        $(this).closest('.updateForm').remove();
    });

    $(document).on('click', '.loadMoreComments', function () {
        const button = $(this);
        const nextUrl = button.data('next-url');
        const postId = button.data('post-id');
        const commentsContainer = button.closest('.comments');

        if (!nextUrl) return;

        $.ajax({
            url: nextUrl,
            type: 'GET',
            success: function (response) {
                response.results.forEach(post => {
                    const newCommentsHtml = post.comments.results.map(comment => createCommentHtml(comment, post.user.username)).join('');
                    commentsContainer.append(newCommentsHtml);

                    if (post.comments.next) {
                        button.data('next-url', post.comments.next);
                    } else {
                        button.remove();
                    }
                });
            },
            error: function () {
                alert('An error occurred while loading more comments.');
            }
        });
    });

    loadPosts(nextPageUrl);

    window.addEventListener('scroll', function () {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500 && nextPageUrl && !isLoading) {
            loadPosts(nextPageUrl);
        }
    });
});
