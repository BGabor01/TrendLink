document.addEventListener('DOMContentLoaded', function() {
    const script = document.querySelector('script[src*="fetch-posts.js"]');
    const getPostsUrl = script.dataset.getPostsUrl;
    const updatePostUrl = script.dataset.updatePostUrl;
    const deletePostUrl = script.dataset.deletePostUrl;
    const currentUser = script.dataset.currentUser;
    const profileUrl = script.dataset.profileUrl;

    $.ajax({
        url: getPostsUrl,
        type: 'GET',
        success: function (response) {
            const postsList = $('#post-list');
            postsList.empty();
            response.results.forEach(function (post) {
                const likedClass = post.has_liked ? 'liked' : '';
                const postCard = `
                    <div class="post-card" data-post-id="${post.id}">
                        <div class="post-header">
                            <div class="profile-picture">
                                <img src="${post.user.profile.profile_picture}" alt="Profile Picture">
                                <a href="${profileUrl.replace('0', post.user.id)}"><strong>${post.user.username}</strong></a>
                            </div>
                            <div class="post-buttons">
                                ${post.user.username === currentUser ? `<button type="button" class="postEdit" data-post-id="${post.id}">Edit</button>` : ''}
                                ${post.user.username === currentUser ? `<button type="button" class="postDelete" data-post-id="${post.id}">Delete</button>` : ''}
                            </div>
                        </div>
                        <p>${post.text}</p>
                        ${post.image ? `<div><img src="${post.image}" alt="Post Image"></div>` : ''}
                        <button type="button" class="likeButton ${likedClass}" data-post-id="${post.id}" data-has-liked="${post.has_liked}">Like</button>
                        <div class="comments-section">
                            <p><strong>Comments:</strong></p>
                            <div class="comments">
                                ${post.comments.results.map(comment => `
                                    <div class="comment" data-comment-id="${comment.id}">
                                        <div class="comment-header">
                                            <img src="${comment.user.profile.profile_picture}" alt="Profile Picture">
                                            <a href="${profileUrl.replace('0', comment.user.id)}"><strong>${comment.user.username}</strong></a>
                                            <div class="comment-buttons">
                                                ${comment.user.username === currentUser ? `<button type="button" class="commentEdit" data-comment-id="${comment.id}">Edit</button>` : ''}
                                                ${comment.user.username === currentUser || post.user.username === currentUser ? `<button type="button" class="commentDelete" data-comment-id="${comment.id}">Delete</button>` : ''}
                                            </div>
                                        </div>
                                        <p>${comment.text}</p>
                                        <p><small>commented on ${comment.created_at}</small></p>
                                    </div>`).join('')}
                            </div>
                            <form class="commentForm" method="post">
                                <input type="hidden" name="post" value="${post.id}">
                                <label for="id_text_${post.id}">Comment:</label>
                                <input type="text" id="id_text_${post.id}" name="text">
                                <button type="submit">Add Comment</button>
                            </form>
                        </div>
                    </div>`;
                postsList.append(postCard);
            });

            initCommentForms();
        },
        error: function (response) {
            alert('An error occurred while retrieving the posts.');
        }
    });
    $(document).on('click', '.postEdit', function () {
        const postId = $(this).data('post-id');
        const postElement = $(this).closest('.post-card');
        const currentText = postElement.find('p').first().text();
        const updateFormHtml = `
            <form class="updateForm" data-post-id="${postId}">
                <div>
                    <label for="id_text_${postId}">Post:</label>
                    <input type="text" id="id_text_${postId}" name="text" value="${currentText}">
                </div>
                <button type="submit">Update</button>
                <button type="button" class="cancelEdit">Cancel</button>
            </form>
        `;
        postElement.append(updateFormHtml);
    });

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
            error: function (response) {
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
            error: function (response) {
                alert('An error occurred while deleting the post.');
            }
        });
    });

    $(document).on('click', '.cancelEdit', function () {
        $(this).closest('.updateForm').remove();
    });
});