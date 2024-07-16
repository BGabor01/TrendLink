const socket = new WebSocket(`ws://${window.location.host}/ws/notifications/`);

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const message = data['message'];

    showNotification(message);
};

socket.onclose = function(e) {
        console.error('Socket closed unexpectedly');
};


function showNotification(message) {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerText = message;

    container.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('fade-out');
        notification.addEventListener('transitionend', () => {
            notification.remove();
        });
    }, 5000);
}