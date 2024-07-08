$(document).ready(function() {
    function loadProfiles(membersUrl, profileDetailsUrl) {
        $.ajax({
            url: membersUrl,
            type: 'GET',
            success: function(response) {
                var profilesList = $('#profiles-list');
                profilesList.empty();

                response.results.forEach(function(profile) {
                    profileDetailsUrl = profileDetailsUrl.replace('0',profile.user.id )
                    var profileCard = `
                        <div class="profile-card">
                            <div class="profile-picture">
                                <img src="${profile.profile_picture}" alt="${profile.user.username}'s profile picture">
                            </div>
                            <div class="profile-details">
                                <p><strong>Username:</strong> ${profile.user.username}</p>
                                <p><strong>Email:</strong> ${profile.user.email}</p>
                                <a href="${profileDetailsUrl}">View Profile</a>
                            </div>
                        </div>`;
                    
                    profilesList.append(profileCard);
                });
            },
            error: function(response) {
                alert('An error occurred while retrieving the profiles.');
            }
        });
    }
    var membersUrl = $('#members-url').data('url');
    var profileDetailsUrl = $('#profile-details').data('url');
    loadProfiles(membersUrl, profileDetailsUrl);
});
