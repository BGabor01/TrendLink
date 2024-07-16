$(document).ready(function() {
    $('#postForm').on('submit', function(e) {
        e.preventDefault();
        var $form = $(this);
        var url = $form.data('url');
        var formData = new FormData(this);
        console.log(url)

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                const redirectUrl = localStorage.getItem('redirectAfterLogin');
                if (redirectUrl !== null) {
                    localStorage.removeItem('redirectAfterLogin');
                    window.location.href = redirectUrl;
                } else {
                    window.location.href = "/home";
                }
            },
            error: function(response) {
                var errors = response.responseJSON;
                var errorMessage = '';
                for (var field in errors) {
                    errorMessage += errors[field] + ' ';
                }
                $('#error-message').text(errorMessage);
            }
        });
    });
});
