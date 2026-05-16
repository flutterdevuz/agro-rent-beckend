/**
 * AgroTerra Auth Service
 * Identity & Session Management
 */

const AuthService = {
    async login(credentials) {
        try {
            const res = await window.atApi.post('/users/login/', credentials);
            localStorage.setItem('at_token', res.access);
            localStorage.setItem('at_user', JSON.stringify(res.user));
            return res;
        } catch (err) {
            throw err;
        }
    },

    async register(data) {
        try {
            const res = await window.atApi.post('/users/register/', data);
            localStorage.setItem('at_token', res.access);
            localStorage.setItem('at_user', JSON.stringify(res.user));
            return res;
        } catch (err) {
            throw err;
        }
    },

    logout() {
        localStorage.removeItem('at_token');
        localStorage.removeItem('at_user');
        window.location.href = '/login/';
    },

    getUser() {
        const user = localStorage.getItem('at_user');
        return user ? JSON.parse(user) : null;
    },

    isAuthenticated() {
        return !!localStorage.getItem('at_token');
    },

    isStaff() {
        const user = this.getUser();
        return user ? user.is_staff : false;
    }
};

window.atAuth = AuthService;
