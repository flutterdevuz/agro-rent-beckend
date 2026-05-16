/**
 * Agro Rent API Service
 * Handles all network requests with error handling and auth persistence.
 */

const API_BASE_URL = window.location.origin + '/api';

const apiService = {
    async request(endpoint, options = {}) {
        const token = localStorage.getItem('admin_token');
        const lang = localStorage.getItem('admin_lang') || 'uz';

        const headers = {
            'Content-Type': 'application/json',
            'Accept-Language': lang,
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            
            // Handle 401 Unauthorized
            if (response.status === 401 && !endpoint.includes('/users/login/')) {
                this.handleUnauthorized();
                return null;
            }

            const data = await response.json();

            if (!response.ok) {
                throw { status: response.status, data };
            }

            return data;
        } catch (error) {
            console.error(`API Error [${endpoint}]:`, error);
            throw error;
        }
    },

    handleUnauthorized() {
        localStorage.removeItem('admin_token');
        if (!window.location.pathname.includes('/login/')) {
            window.location.href = '/api/admin/login/';
        }
    },

    // Auth
    login: (credentials) => apiService.request('/users/login/', { method: 'POST', body: JSON.stringify(credentials) }),
    register: (data) => apiService.request('/users/register/', { method: 'POST', body: JSON.stringify(data) }),
    getProfile: () => apiService.request('/users/profile/'),

    // Banners
    getBanners: () => apiService.request('/banners/'),

    // Market
    getMarketCategories: () => apiService.request('/market/categories/'),
    getMarketItems: (params = '') => apiService.request(`/market/items/${params}`),
    getPopularEquipment: () => apiService.request('/popular-equipment/'),

    // Rent
    getRentItems: (params = '') => apiService.request(`/rent/items/${params}`),
    
    // Notifications
    getNotifications: () => apiService.request('/notifications/list/'),
    
    // Stats
    getPublicStats: () => apiService.request('/users/public-stats/'),

    // Translation
    translate: (texts) => apiService.request('/translate/', { method: 'POST', body: JSON.stringify({ texts }) })
};

window.apiService = apiService;
