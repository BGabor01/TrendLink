$(document).ready(function() {
    const connectionReqsUrl = $('#connectionreq-url-api').data('url');
    let profileDetailsUrl = $('#profile-details').data('url');
    let acceptConnectionReqUrl = $('#accept-connectionreq-url-api').data('url');
    let rejectConnectionReqUrl = $('#reject-connectionreq-url-api').data('url');
    
    $.ajax({
        url: connectionReqsUrl,
        type: 'GET',
        success: function(response) {
            const connectionReqsList = $('#connectionreq-list');
            connectionReqsList.empty();

            response.results.forEach(function(connectionReqs) {
                let currentProfileDetailsUrl = profileDetailsUrl.replace('0', connectionReqs.sender.id);
                const profileCard = `
                    <div class="profile-card" data-connectionreq-id="${connectionReqs.id}">
                        <div class="profile-picture">
                            <img src="${connectionReqs.sender.profile.profile_picture}" alt="${connectionReqs.sender.profile.username}'s profile picture">
                        </div>
                        <div class="profile-details">
                            <p><strong>Username:</strong> ${connectionReqs.sender.username}</p>
                            <p><strong>Email:</strong> ${connectionReqs.sender.email}</p>
                            <a href="${currentProfileDetailsUrl}">View Profile</a>
                            <button type="button" class="accept-button" data-connectionreq-id="${connectionReqs.id}">Accept</button> 
                            <button class="reject-button" data-connectionreq-id="${connectionReqs.id}">Reject</button>
                        </div>
                    </div>`;

                connectionReqsList.append(profileCard);
            });
        },
        error: function(response) {
            if (response.status === 403) {
                localStorage.setItem('redirectAfterLogin', membersUrl);
                window.location.href = loginUrl;
            } else {
                alert('An error occurred while retrieving the profiles.');
            }
        }
    });

    $(document).on('click', '.accept-button', function() {
        const requestId = $(this).data('connectionreq-id');
        const acceptCurrentRequestUrl = acceptConnectionReqUrl.replace('0', requestId);
        
        $.ajax({
            url: acceptCurrentRequestUrl,
            type: 'PUT',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                alert('Connection request accepted successfully!');
                $(`.profile-card[data-connectionreq-id="${requestId}"]`).remove();
            },
            error: function(error) {
                alert('Error accepting connection request.');
            }
        });
    });

    $(document).on('click', '.reject-button', function() {
        const requestId = $(this).data('connectionreq-id');
        const rejectCurrentRequestUrl = rejectConnectionReqUrl.replace('0', requestId);
        
        $.ajax({
            url: rejectCurrentRequestUrl,
            type: 'DELETE',
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                alert('Connection request rejected successfully!');
                $(`.profile-card[data-connectionreq-id="${requestId}"]`).remove();
            },
            error: function(error) {
                alert('Error rejecting connection request.');
            }
        });
    });
});
