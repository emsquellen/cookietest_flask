function activate_modal() {
    document.getElementById('notificationCentre').classList.add("active");
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