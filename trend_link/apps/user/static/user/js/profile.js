$(document).ready(function() {
    function getUserIdFromPath() {
        var pathArray = window.location.pathname.split('/');
        return pathArray[pathArray.length - 2];
    }

    var userId = getUserIdFromPath();
    var currentUserId = $('#current-user-id').data('id'); 

    var retrieveUrl = $('#retrieve-url').data('url').replace('0', userId);
    var updateUrl = $('#update-url').data('url').replace('0', userId);

    $.ajax({
        url: retrieveUrl,
        type: 'GET',
        success: function(response) {
            $('#username').text(response.user.username + "'s Profile");
            $('#profile-picture').attr('src', response.profile_picture);
            $('#user-username').text(response.user.username);
            $('#user-email').text(response.user.email);
            $('#user-bio').text(response.bio);
            $('#user-birth-date').text(response.birth_date);
            $('#id_bio').val(response.bio);
            $('#id_birth_date').val(response.birth_date);

            if (currentUserId == userId) {
                $('#edit-button').show();
                $('#uploadForm').show();
            }
        },
        error: function(response) {
            alert('An error occurred while retrieving the profile data.');
        }
    });

    $('#fileInput').change(function() {
        var formData = new FormData($('#uploadForm')[0]);
        $.ajax({
            url: updateUrl,
            type: 'PATCH',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $('#profile-picture').attr('src', response.profile_picture);
            },
            error: function(response) {
                alert('An error occurred while uploading the profile picture.');
            }
        });
    });

    $('#updateForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: updateUrl,
            type: 'PATCH',
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $('#user-bio').text(response.bio);
                $('#user-birth-date').text(response.birth_date);
                $('#updateForm').hide();
            },
            error: function(response) {
                alert('An error occurred while updating the profile.');
            }
        });
    });
});

function toggleEditForm() {
    $('#updateForm').toggle();
}
