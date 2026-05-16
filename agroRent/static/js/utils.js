/**
 * Agro Rent Utilities
 */

const utils = {
    formatPrice(price) {
        return new Intl.NumberFormat('uz-UZ', {
            style: 'currency',
            currency: 'UZS',
            minimumFractionDigits: 0
        }).format(price);
    },

    formatDate(dateStr) {
        const date = new Date(dateStr);
        return date.toLocaleDateString('uz-UZ', {
            day: 'numeric',
            month: 'long',
            year: 'numeric'
        });
    },

    truncateText(text, limit = 100) {
        if (text.length <= limit) return text;
        return text.substring(0, limit) + '...';
    },

    showNotification(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerText = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 500);
            }, 3000);
        }, 100);
    }
};

window.utils = utils;
