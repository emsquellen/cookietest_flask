function activate_modal() {
    document.getElementById('notificationCentre').classList.add("active");
}

function delete_notifs() {
    document.cookie = "notifications=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    location.reload();
    activate_modal();
}

window.onload = () => {
    document.querySelectorAll('a[aria-label="Close"]').forEach(el => {
        el.addEventListener('click', () => {
            document.querySelectorAll('.modal').forEach(modal => {
                modal.classList.remove('active');
            })
        })
    })
}