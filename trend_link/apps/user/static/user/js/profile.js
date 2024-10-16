$(document).ready(function () {
    function getUserIdFromPath() {
        let pathArray = window.location.pathname.split('/');
        return pathArray[pathArray.length - 2];
    }

    const userId = getUserIdFromPath();
    const script = document.querySelector('script[src*="profile.js"]');
    const currentUserId = script.dataset.currentUserId
    const retrieveUrlApi = script.dataset.retrieveProfileApiUrl.replace('0', userId);
    const retrieveUrl = script.dataset.retrieveProfileUrl.replace('0', userId);
    const updateUrl = script.dataset.updateProfileUrl.replace('0', userId);
    const loginUrl = script.dataset.loginUrl
    const connectUrl = script.dataset.connectUrl

    $.ajax({
        url: retrieveUrlApi,
        type: 'GET',
        success: function (response) {
            $('#profile-picture').attr('src', response.profile.profile_picture);
            $('#user-username').text(response.username);
            $('#user-email').text(response.email);
            $('#user-bio').text(response.profile.bio);
            $('#user-birth-date').text(response.profile.birth_date);
            $('#id_bio').val(response.profile.bio);
            $('#id_birth_date').val(response.profile.birth_date);

            if (currentUserId == userId) {
                $('#edit-button').show();
                $('#uploadForm').show();
            }

            if (!response.connected && !response.pending && userId !== currentUserId){
                $('#connect-button').show();
            }
            
            
        },
        error: function (response) {
            if (response.status === 403) {
                localStorage.setItem('redirectAfterLogin', retrieveUrl);
                window.location.href = loginUrl;
            } else {
                alert('An error occurred while retrieving the profiles.');
            }
        }
    });

    $('#fileInput').change(function () {
        const formData = new FormData($('#uploadForm')[0]);
        $.ajax({
            url: updateUrl,
            type: 'PATCH',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                $('#profile-picture').attr('src', response.profile_picture);
            },
            error: function (response) {
                alert('An error occurred while uploading the profile picture.');
            }
        });
    });

    $('#updateForm').submit(function (e) {
        e.preventDefault();
        $.ajax({
            url: updateUrl,
            type: 'PATCH',
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function (response) {
                $('#user-bio').text(response.bio);
                $('#user-birth-date').text(response.birth_date);
                $('#updateForm').hide();
            },
            error: function (response) {
                alert('An error occurred while updating the profile.');
            }
        });
    });

    $('#connect-button').click(function() {
        $.ajax({
            url: connectUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data: {
                recipient: userId,
            },
            success: function(response) {
                alert('Connection request sent successfully!');
            },
            error: function(error) {
                alert('Error sending connection request.');
            }
        });
    });
});

function toggleEditForm() {
    $('#updateForm').toggle();
}
