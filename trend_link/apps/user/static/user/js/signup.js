$(document).ready(function () {
    $('#signupForm').on('submit', function (e) {
        e.preventDefault();
        const $form = $(this);
        const url = $form.data('url');

        $.ajax({
            type: 'POST',
            url: url,
            data: $form.serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                window.location.href = "/home";
            },
            error: function (response) {
                const errors = response.responseJSON;
                let errorMessage = '';
                for (var field in errors) {
                    errorMessage += errors[field] + ' ';
                }
                $('#error-message').text(errorMessage);
            }
        });
    });
});
