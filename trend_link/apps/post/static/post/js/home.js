$(document).ready(function () {
    const postsUrl = $('#posts-url').data('url');
    const createCommentUrl = $('#create-comment-url-api').data('url');
    const currentUser = $('#current-user').data('user');
    const profileUrl = $('#profile-url').data('url');
    let deleteCommentUrl = $('#delete-comment-url-api').data('url');
    let updateCommentUrl = $('#update-comment-url-api').data('url');

    $.ajax({
        url: postsUrl,
        type: 'GET',
        success: function (response) {
            const postsList = $('#post-list');
            postsList.empty();
            response.results.forEach(function (post) {
                const postCard = `
                    <div class="post-card">
                        <div class="profile-picture">
                            <img src="${post.user.profile.profile_picture}" alt="Profile Picture">
                            <a href="${profileUrl.replace('0', post.user.id)}"><strong>${post.user.username}</strong></a>
                        </div>
                        <p>${post.text}</p>
                        ${post.image ? `<div><img src="${post.image}" alt="Post Image"></div>` : ''}
                        <div class="comments-section">
                            <p><strong>Comments:</strong></p>
                            <div class="comments">
                                ${post.comments.map(comment => `
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
                            <form class="commentForm" method="post" action="${createCommentUrl}">
                                <input type="hidden" name="post_id" value="${post.id}">
                                <label for="id_text_${post.id}">Comment:</label>
                                <input type="text" id="id_text_${post.id}" name="text">
                                <button type="submit">Add Comment</button>
                            </form>
                        </div>
                    </div>`;
                postsList.append(postCard);
            });

            $('.commentForm').on('submit', function (e) {
                e.preventDefault();
                const $form = $(this);
                $.ajax({
                    type: 'POST',
                    url: $form.attr('action'),
                    data: $form.serialize(),
                    headers: {
                        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    success: function (response) {
                        const newComment = `<div class="comment" data-comment-id="${response.id}">
                            <div class="comment-header">
                                <img src="${response.user.profile.profile_picture}" alt="Profile Picture">
                                <a href="${profileUrl.replace('0', response.user.id)}"><strong>${response.user.username}</strong></a></a>
                                <div class="comment-buttons">
                                    ${response.user.username === currentUser ? `<button class="commentEdit" data-comment-id="${response.id}">Edit</button>` : ''}
                                    ${response.user.username === currentUser || response.user.username === currentUser ? `<button type="button" class="commentDelete" data-comment-id="${response.id}">Delete</button>` : ''}
                                </div>
                            </div>
                            <p>${response.text}</p>
                            <p><small>commented on ${response.created_at}</small></p>
                        </div>`;
                        $form.closest('.post-card').find('.comments').append(newComment);
                        $form.find('input[type=text]').val('');
                    },
                    error: function (response) {
                        if (response.status === 404) {
                            let responseData = JSON.parse(response.responseText);
                            alert(responseData.detail);
                        } else {
                            alert('An error occurred: ' + response.status);
                        }
                        $form[0].reset();
                    }
                });
            });
        },
        error: function (response) {
            alert('An error occurred while retrieving the posts.');
        }
    });

    $(document).on('click', '.commentDelete', function () {
        const commentId = $(this).data('comment-id');
        const deleteUrl = deleteCommentUrl.replace('0', commentId);
        deleteComment(deleteUrl, commentId);
    });

    $(document).on('click', '.commentEdit', function () {
        const commentId = $(this).data('comment-id');
        const commentElement = $(this).closest('.comment');
        const currentText = commentElement.find('p').first().text();
        const updateFormHtml = `
            <form class="updateForm" data-comment-id="${commentId}">
                <div>
                    <label for="id_text_${commentId}">Comment:</label>
                    <input type="text" id="id_text_${commentId}" name="text" value="${currentText}">
                </div>
                <button type="submit">Update</button>
                <button type="button" class="cancelEdit">Cancel</button>
            </form>
        `;
        commentElement.append(updateFormHtml);
    });

    $(document).on('submit', '.updateForm', function (e) {
        e.preventDefault();
        const $form = $(this);
        const commentId = $form.data('comment-id');
        const updateUrl = updateCommentUrl.replace('0', commentId);
        $.ajax({
            type: 'PUT',
            url: updateUrl,
            data: $form.serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                const commentElement = $(`.comment[data-comment-id="${commentId}"]`);
                commentElement.find('p').first().text(response.text);
                $form.remove();
            },
            error: function (response) {
                alert('An error occurred while updating the comment.');
            }
        });
    });

    $(document).on('click', '.cancelEdit', function () {
        $(this).closest('.updateForm').remove();
    });

    function deleteComment(url, commentId) {
        $.ajax({
            type: 'DELETE',
            url: url,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function () {
                $(`.commentDelete[data-comment-id="${commentId}"]`).closest('.comment').remove();
            },
            error: function (response) {
                alert('An error occurred while deleting the comment.');
            }
        });
    }
});
