$(document).ready(function () {
    const script = document.querySelector('script[src*="members.js"]');
    const getMembersUrl = script.dataset.getMembersUrl;
    const profileDetailsUrl = script.dataset.profileDetailsUrl 
    $.ajax({
            url: getMembersUrl,
            type: 'GET',
            success: function (response) {
                const profilesList = $('#profiles-list');
                profilesList.empty();

                response.results.forEach(function (profile) {
                    let currentProfileDetailsUrl = profileDetailsUrl.replace('0', profile.id);
                    const profileCard = `
                        <div class="profile-card">
                            <div class="profile-picture">
                                <img src="${profile.profile.profile_picture}" alt="${profile.username}'s profile picture">
                            </div>
                            <div class="profile-details">
                                <p><strong>Username:</strong> ${profile.username}</p>
                                <p><strong>Email:</strong> ${profile.email}</p>
                                <a href="${currentProfileDetailsUrl}">View Profile</a>
                            </div>
                        </div>`;

                    profilesList.append(profileCard);
                });
            },
            error: function (response) {
                if (response.status === 403) {
                } else {
                    alert('An error occurred while retrieving the profiles.');
                }

            }
        });
    }
);
