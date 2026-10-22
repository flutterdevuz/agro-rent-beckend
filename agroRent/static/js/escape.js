// Foydalanuvchi kiritgan ma'lumotni innerHTML ga qo'yishdan oldin xavfsiz holatga keltiradi (XSS himoyasi)
function escapeHtml(value) {
    if (value === null || value === undefined) return '';
    return String(value).replace(/[&<>"'`]/g, ch => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '`': '&#96;'
    }[ch]));
}
