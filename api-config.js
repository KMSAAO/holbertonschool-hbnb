/**
 * ملف: api-config.js
 * الوصف: إعدادات الاتصال بالـ API الخلفي (Flask-RESTx)
 *
 * ⚠️ ملاحظة مهمة:
 * - Frontend و Backend يعملان على نفس السيرفر (Flask) على المنفذ 5000
 * - جميع نقاط النهاية تطابق بنية Flask-RESTx في part3/
 * - المصادقة عبر JWT (Flask-JWT-Extended)
 */

// ==================== إعدادات الـ API ====================

// عنوان API الأساسي — نسبي لأن Frontend و Backend على نفس السيرفر
const API_BASE_URL = '/api/v1';

// نقاط النهاية للـ API (تطابق backend routes)
const API_ENDPOINTS = {
    // المصادقة (auth.py)
    login: '/auth/login',           // POST {email, password} → {access_token}

    // المستخدمين (users.py)
    register: '/users',             // POST {first_name, last_name, email, password}
    getUser: '/users/:id',          // GET → user object
    updateUser: '/users/:id',       // PUT {first_name, last_name, email}
    getAllUsers: '/users',           // GET → [users]

    // الأماكن / الفنادق (places.py)
    getPlaces: '/places',           // GET → [places]
    getPlace: '/places/:id',        // GET → place object
    createPlace: '/places',         // POST {title, description, price, status, latitude, longitude}
    updatePlace: '/places/:id',     // PUT
    deletePlace: '/places/:id',     // DELETE
    uploadPlaceImages: '/places/:id/images', // POST multipart/form-data

    // المراجعات (reviews.py)
    getReviews: '/reviews',         // GET → [reviews]
    getReview: '/reviews/:id',      // GET → review object
    createReview: '/reviews',       // POST {place_id, rating, comment}
    updateReview: '/reviews/:id',   // PUT
    deleteReview: '/reviews/:id',   // DELETE

    // الحجوزات (bookings.py)
    getBookings: '/bookings',                   // GET → [bookings]
    createBooking: '/bookings',                 // POST {guest_id, place_id, check_in, check_out, status}
    getBookingsByGuest: '/bookings/guest/:guestId', // GET → [bookings]
    updateBookingStatus: '/bookings/:id/status', // PUT {status}

    // النزلاء (guests.py)
    registerGuest: '/guests',       // POST
    getGuest: '/guests/:id',        // GET

    // المرافق (amenities.py)
    getAmenities: '/amenities',     // GET → [amenities]
    createAmenity: '/amenities',    // POST {amenity_name, description, status}
    getAmenity: '/amenities/:id',   // GET
    updateAmenity: '/amenities/:id', // PUT
    deleteAmenity: '/amenities/:id'  // DELETE
};

// ==================== دوال مساعدة للـ API ====================

/**
 * معالجة أخطاء المصادقة (401)
 */
function handleAuthError() {
    console.warn('جلسة انتهت صلاحيتها (401). جاري توجيه المستخدم لصفحة الدخول...');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    localStorage.removeItem('userId');
    window.location.href = 'login.html';
}

/**
 * الحصول على التوكن من localStorage
 * يقرأ access_token الذي يعيده backend عند تسجيل الدخول
 */
function getAuthToken() {
    return localStorage.getItem('access_token') || '';
}

/**
 * استبدال المعاملات في الـ URL
 * مثال: replaceUrlParams('/places/:id', { id: 'abc123' }) => '/places/abc123'
 */
function replaceUrlParams(endpoint, params) {
    let url = endpoint;
    Object.keys(params).forEach(key => {
        url = url.replace(`:${key}`, params[key]);
    });
    return url;
}

/**
 * دالة لإرسال طلب GET
 */
async function apiGet(endpoint, params = {}) {
    try {
        let url = `${API_BASE_URL}${endpoint}`;
        const searchParams = new URLSearchParams(params).toString();
        if (searchParams) url += `?${searchParams}`;

        const headers = { 'Content-Type': 'application/json' };
        const token = getAuthToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(url, { method: 'GET', headers });

        if (!response.ok) {
            if (response.status === 401) {
                handleAuthError();
                throw new Error('جلسة غير صالحة');
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API GET Error:', error);
        throw error;
    }
}

/**
 * دالة لإرسال طلب POST
 */
async function apiPost(endpoint, data) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        const token = getAuthToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers,
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleAuthError();
                throw new Error('جلسة غير صالحة');
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API POST Error:', error);
        throw error;
    }
}

/**
 * دالة لإرسال طلب PUT (للتحديث)
 */
async function apiPut(endpoint, data) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        const token = getAuthToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers,
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleAuthError();
                throw new Error('جلسة غير صالحة');
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API PUT Error:', error);
        throw error;
    }
}

/**
 * دالة لإرسال طلب DELETE
 */
async function apiDelete(endpoint) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        const token = getAuthToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleAuthError();
                throw new Error('جلسة غير صالحة');
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        if (response.status === 204) {
            return true;
        }

        return await response.json();
    } catch (error) {
        console.error('API DELETE Error:', error);
        throw error;
    }
}

/**
 * دالة لرفع ملفات (multipart/form-data)
 * لا نحدد Content-Type — المتصفح يضيفه تلقائياً مع boundary
 */
async function apiUploadFiles(endpoint, formData) {
    try {
        const headers = {};
        const token = getAuthToken();
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers,
            body: formData
        });

        if (!response.ok) {
            if (response.status === 401) {
                handleAuthError();
                throw new Error('جلسة غير صالحة');
            }
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Upload Error:', error);
        throw error;
    }
}

// ==================== API Wrappers لكل نوع بيانات ====================

// دوال الأماكن (Places / الفنادق)
const PlacesAPI = {
    getAll: () => apiGet(API_ENDPOINTS.getPlaces),
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getPlace, { id })),
    create: (placeData) => apiPost(API_ENDPOINTS.createPlace, placeData),
    update: (id, placeData) => apiPut(replaceUrlParams(API_ENDPOINTS.updatePlace, { id }), placeData),
    delete: (id) => apiDelete(replaceUrlParams(API_ENDPOINTS.deletePlace, { id })),
    uploadImages: (id, files) => {
        const formData = new FormData();
        for (const file of files) {
            formData.append('images', file);
        }
        return apiUploadFiles(replaceUrlParams(API_ENDPOINTS.uploadPlaceImages, { id }), formData);
    }
};

// دوال المستخدمين
const UsersAPI = {
    login: (email, password) => apiPost(API_ENDPOINTS.login, { email, password }),
    register: (userData) => apiPost(API_ENDPOINTS.register, userData),
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getUser, { id })),
    update: (id, userData) => apiPut(replaceUrlParams(API_ENDPOINTS.updateUser, { id }), userData),
    getAll: () => apiGet(API_ENDPOINTS.getAllUsers)
};

// دوال المراجعات
const ReviewsAPI = {
    getAll: () => apiGet(API_ENDPOINTS.getReviews),
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getReview, { id })),
    create: (reviewData) => apiPost(API_ENDPOINTS.createReview, reviewData),
    update: (id, reviewData) => apiPut(replaceUrlParams(API_ENDPOINTS.updateReview, { id }), reviewData),
    delete: (id) => apiDelete(replaceUrlParams(API_ENDPOINTS.deleteReview, { id }))
};

// دوال الحجوزات
const BookingsAPI = {
    getAll: () => apiGet(API_ENDPOINTS.getBookings),
    create: (bookingData) => apiPost(API_ENDPOINTS.createBooking, bookingData),
    getByGuest: (guestId) => apiGet(replaceUrlParams(API_ENDPOINTS.getBookingsByGuest, { guestId })),
    updateStatus: (id, status) => apiPut(replaceUrlParams(API_ENDPOINTS.updateBookingStatus, { id }), { status })
};

// دوال المرافق
const AmenitiesAPI = {
    getAll: () => apiGet(API_ENDPOINTS.getAmenities),
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getAmenity, { id })),
    create: (amenityData) => apiPost(API_ENDPOINTS.createAmenity, amenityData),
    update: (id, amenityData) => apiPut(replaceUrlParams(API_ENDPOINTS.updateAmenity, { id }), amenityData),
    delete: (id) => apiDelete(replaceUrlParams(API_ENDPOINTS.deleteAmenity, { id }))
};

// دوال النزلاء
const GuestsAPI = {
    register: (guestData) => apiPost(API_ENDPOINTS.registerGuest, guestData),
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getGuest, { id }))
};
