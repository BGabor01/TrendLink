document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector('#tags');
    const tagify = new Tagify(input);

    $('#postForm').on('submit', function (e) {
        e.preventDefault();
        const $form = $(this);
        const url = $form.data('url');
        const formData = new FormData(this);

        const tagsArray = tagify.value.map(tag => tag.value);
        formData.delete('tags');
        tagsArray.forEach(tag => {
            formData.append('tags', tag);
        });

        console.log(tagsArray);

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                const redirectUrl = localStorage.getItem('redirectAfterLogin');
                if (redirectUrl !== null) {
                    localStorage.removeItem('redirectAfterLogin');
                    window.location.href = redirectUrl;
                }
            },
            error: function (response) {
                const errors = response.responseJSON;
                let errorMessage = '';
                for (const field in errors) {
                    errorMessage += errors[field] + ' ';
                }
                $('#error-message').text(errorMessage);
            }
        });
    });
});
