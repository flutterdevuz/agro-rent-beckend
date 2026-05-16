/**
 * AgroTerra Core API Service
 * Precision Network Layer
 */

class ApiClient {
    constructor(baseUrl = '/api') {
        this.baseUrl = baseUrl;
    }

    async request(endpoint, options = {}) {
        const token = localStorage.getItem('at_token');
        const lang = localStorage.getItem('at_lang') || 'uz';

        const headers = {
            'Accept': 'application/json',
            'Accept-Language': lang,
            ...options.headers
        };

        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, config);
            
            // Global Interceptors
            if (response.status === 401) {
                this.onUnauthorized();
            }

            const data = await response.json();

            if (!response.ok) {
                return Promise.reject({
                    status: response.status,
                    error: data
                });
            }

            return data;
        } catch (err) {
            console.error(`[AgroTerra API] Network Failure: ${endpoint}`, err);
            return Promise.reject(err);
        }
    }

    onUnauthorized() {
        localStorage.removeItem('at_token');
        localStorage.removeItem('at_user');
        if (!window.location.pathname.includes('/login')) {
            window.location.href = '/login/';
        }
    }

    get(endpoint, params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`${endpoint}${query ? `?${query}` : ''}`, { method: 'GET' });
    }

    post(endpoint, body) {
        return this.request(endpoint, {
            method: 'POST',
            body: body instanceof FormData ? body : JSON.stringify(body)
        });
    }

    put(endpoint, body) {
        return this.request(endpoint, {
            method: 'PUT',
            body: body instanceof FormData ? body : JSON.stringify(body)
        });
    }

    delete(endpoint) {
        return this.request(endpoint, { method: 'DELETE' });
    }
}

window.atApi = new ApiClient();
