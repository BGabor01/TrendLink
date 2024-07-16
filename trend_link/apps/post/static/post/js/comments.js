function initCommentForms() {
    const script = document.querySelector('script[src*="comments.js"]');
    const currentUser = script.dataset.currentUser;
    const profileUrl = script.dataset.profileUrl;
    const createCommentUrl = script.dataset.createCommentUrl;
    const updateCommentUrl = script.dataset.updateCommentUrl;
    const deleteCommentUrl = script.dataset.deleteCommentUrl;

    $('.commentForm').on('submit', function (e) {
        e.preventDefault();
        const $form = $(this);
        $.ajax({
            type: 'POST',
            url: createCommentUrl,
            data: $form.serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                const newComment = `<div class="comment" data-comment-id="${response.id}">
                    <div class="comment-header">
                        <img src="${response.user.profile.profile_picture}" alt="Profile Picture">
                        <a href="${profileUrl.replace('0', response.user.id)}"><strong>${response.user.username}</strong></a>
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

    $(document).on('submit', '.updateForm[data-comment-id]', function (e) {
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
}
