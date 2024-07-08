$(document).ready(function() {
    function loadProfiles(membersUrl, membersUrlApi, profileDetailsUrl, loginUrl) {
        $.ajax({
            url: membersUrlApi,
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
                if (response.status === 403) {
                    localStorage.setItem('redirectAfterLogin', membersUrl);
                    window.location.href = loginUrl;
                } else {
                    alert('An error occurred while retrieving the profiles.');
                }

            }
        });
    }
    let profileDetailsUrl = $('#profile-details').data('url');
    const membersUrlApi = $('#members-url-api').data('url');
    const membersUrl = $('#members-url').data('url');
    const loginUrl = $('#login-url').data('url');
    loadProfiles(membersUrl, membersUrlApi, profileDetailsUrl, loginUrl);
});
