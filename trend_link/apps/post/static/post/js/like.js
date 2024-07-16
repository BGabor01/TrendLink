$(document).ready(function () {
    const script = document.querySelector('script[src*="like.js"]');
    const unlikePostUrl = script.dataset.unlikePostUrl;
    const likePostUrl = script.dataset.likePostUrl;

    $(document).on('click', '.likeButton', function () {
        const postId = $(this).data('post-id');
        const hasLiked = $(this).data('has-liked');
        if (hasLiked) {
            const unlikeUrlFormatted = unlikePostUrl.replace('0', postId);
            $.ajax({
                type: 'DELETE',
                url: unlikeUrlFormatted,
                headers: {
                    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (response) {
                    $(`.likeButton[data-post-id="${postId}"]`).removeClass('liked').data('has-liked', false);
                },
                error: function (response) {
                    alert('An error occurred while unliking the post.');
                }
            });
        } else {
            $.ajax({
                type: 'POST',
                url: likePostUrl,
                data: { post: postId },
                headers: {
                    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (response) {
                    $(`.likeButton[data-post-id="${postId}"]`).addClass('liked').data('has-liked', true);
                },
                error: function (response) {
                    alert('An error occurred while liking the post.');
                }
            });
        }
    });
});
