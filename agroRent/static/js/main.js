// Main JS for Admin Dashboard

// Global fetch wrapper to include JWT token
async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('admin_token');
    if (!token && !window.location.pathname.includes('/login/')) {
        window.location.href = '/api/admin/login/';
        return;
    }

    const headers = {
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    // If it's not FormData, set Content-Type to application/json
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401 && !window.location.pathname.includes('/login/')) {
        localStorage.removeItem('admin_token');
        window.location.href = '/api/admin/login/';
    }

    return response;
}

async function updateUnreadCount() {
    try {
        const response = await apiFetch('/api/notifications/unread-count/');
        if (response && response.ok) {
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

function logout() {
    console.log('Logging out...');
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_user');
    window.location.replace('/api/admin/login/');
}

// Check auth on load
if (!localStorage.getItem('admin_token') && !window.location.pathname.includes('/login/')) {
    window.location.href = '/api/admin/login/';
}

// Update count every 30 seconds
setInterval(updateUnreadCount, 30000);
updateUnreadCount();

// Sidebar active state handler
document.querySelectorAll('.sidebar nav ul li').forEach(li => {
    li.addEventListener('click', () => {
        document.querySelectorAll('.sidebar nav ul li').forEach(el => el.classList.remove('active'));
        li.classList.add('active');
    });
});
