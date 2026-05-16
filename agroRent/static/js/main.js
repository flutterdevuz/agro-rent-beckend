// Main JS for Admin Dashboard

// Global fetch wrapper to include JWT token and Language
async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('at_token');
    const lang = localStorage.getItem('at_lang') || 'uz';

    if (!token && !window.location.pathname.includes('/login/')) {
        window.location.href = '/login/';
        return;
    }

    const headers = {
        'Authorization': `Bearer ${token}`,
        'Accept-Language': lang,
        ...options.headers
    };

    // If it's not FormData, set Content-Type to application/json
    if (!(options.body instanceof FormData)) {
        headers['Content-Type'] = 'application/json';
    }

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401 && !window.location.pathname.includes('/login/')) {
        localStorage.removeItem('at_token');
        window.location.href = '/login/';
    }

    return response;
}

function changeLanguage(lang) {
    localStorage.setItem('admin_lang', lang);
    window.location.reload();
}

async function translateUI() {
    const lang = localStorage.getItem('admin_lang') || 'uz';
    if (lang === 'uz') return; // Default is Uzbek, no need to translate

    const elements = document.querySelectorAll('[data-i18n]');
    const textsToTranslate = [];
    elements.forEach(el => {
        const text = el.innerText.trim();
        if (text) {
            textsToTranslate.push(text);
        }
    });

    const placeholders = document.querySelectorAll('[data-i18n-placeholder]');
    placeholders.forEach(el => {
        const text = el.placeholder.trim();
        if (text) {
            textsToTranslate.push(text);
        }
    });

    if (textsToTranslate.length === 0) return;

    try {
        const translations = await window.apiService.translate([...new Set(textsToTranslate)]);
        if (translations) {
            elements.forEach(el => {
                const text = el.innerText.trim();
                if (translations[text]) {
                    el.innerText = translations[text];
                }
            });
            placeholders.forEach(el => {
                const text = el.placeholder.trim();
                if (translations[text]) {
                    el.placeholder = translations[text];
                }
            });
        }
    } catch (error) {
        console.error('Translation error:', error);
    }
}

// Translate UI when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    translateUI();
});

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
    localStorage.removeItem('at_token');
    localStorage.removeItem('at_user');
    window.location.replace('/login/');
}

// Check auth on load
if (!localStorage.getItem('at_token') && !window.location.pathname.includes('/login/')) {
    window.location.href = '/login/';
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
