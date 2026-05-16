// Main JS for Admin Dashboard

async function updateUnreadCount() {
    try {
        const response = await fetch('/api/notifications/unread-count/');
        if (response.ok) {
            const data = await response.json();
            const badge = document.getElementById('unread-count');
            if (badge) {
                badge.innerText = data.unread_count;
                badge.style.display = data.unread_count > 0 ? 'inline-block' : 'none';
            }
        }
    } catch (error) {
        console.error('Error updating unread count:', error);
    }
}

// Update count every 30 seconds
setInterval(updateUnreadCount, 30000);
updateUnreadCount();

// Sidebar active state handler (optional if handled by Django)
document.querySelectorAll('.sidebar nav ul li').forEach(li => {
    li.addEventListener('click', () => {
        document.querySelectorAll('.sidebar nav ul li').forEach(el => el.classList.remove('active'));
        li.classList.add('active');
    });
});
