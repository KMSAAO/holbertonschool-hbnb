/**
 * ملف: api-config.js
 * الوصف: إعدادات الاتصال بالـ API
 * 
 * ⚠️ ملاحظة مهمة:
 * - هذا الملف يحتوي على إعدادات الاتصال بقاعدة البيانات
 * - يجب تغيير API_BASE_URL إلى عنوان السيرفر الخاص بك
 * - تأكد من أن السيرفر Backend يعمل قبل استخدام الموقع
 */

// ==================== إعدادات الـ API ====================

// عنوان API الأساسي (غيّر هذا إلى عنوان سيرفرك)
const API_BASE_URL = 'http://localhost:3000/api'; // أو 'https://your-domain.com/api'

// نقاط النهاية للـ API
const API_ENDPOINTS = {
    // المستخدمين
    login: '/users/login',
    register: '/users/register',
    getUser: '/users/:id',
    updateUser: '/users/:id',
    
    // الفنادق
    getHotels: '/hotels',
    getHotel: '/hotels/:id',
    createHotel: '/hotels',
    updateHotel: '/hotels/:id',
    deleteHotel: '/hotels/:id',
    
    // الغرف
    getRooms: '/hotels/:hotelId/rooms',
    
    // المراجعات
    getReviews: '/hotels/:hotelId/reviews',
    createReview: '/hotels/:hotelId/reviews',
    
    // الحجوزات
    getBookings: '/bookings',
    createBooking: '/bookings',
    getUserBookings: '/users/:userId/bookings',
    
    // الدفع
    processPayment: '/payments',
    
    // الصور
    uploadImage: '/upload'
};

// ==================== دوال مساعدة للـ API ====================

/**
 * دالة لإرسال طلب GET
 * @param {string} endpoint - نقطة النهاية
 * @param {object} params - المعاملات (اختياري)
 */
async function apiGet(endpoint, params = {}) {
    try {
        const url = new URL(`${API_BASE_URL}${endpoint}`);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API GET Error:', error);
        throw error;
    }
}

/**
 * دالة لإرسال طلب POST
 * @param {string} endpoint - نقطة النهاية
 * @param {object} data - البيانات المراد إرسالها
 */
async function apiPost(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API POST Error:', error);
        throw error;
    }
}

/**
 * دالة لإرسال طلب PUT (للتحديث)
 * @param {string} endpoint - نقطة النهاية
 * @param {object} data - البيانات المراد تحديثها
 */
async function apiPut(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API PUT Error:', error);
        throw error;
    }
}

/**
 * دالة لإرسال طلب DELETE
 * @param {string} endpoint - نقطة النهاية
 */
async function apiDelete(endpoint) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API DELETE Error:', error);
        throw error;
    }
}

/**
 * دالة لرفع الصور
 * @param {File} file - ملف الصورة
 */
async function apiUploadImage(file) {
    try {
        const formData = new FormData();
        formData.append('image', file);
        
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.uploadImage}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getAuthToken()}`
            },
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Upload Error:', error);
        throw error;
    }
}

/**
 * الحصول على التوكن من localStorage
 */
function getAuthToken() {
    const user = JSON.parse(localStorage.getItem('currentUser') || '{}');
    return user.token || '';
}

/**
 * استبدال المعاملات في الـ URL
 * مثال: replaceUrlParams('/hotels/:id', { id: 123 }) => '/hotels/123'
 */
function replaceUrlParams(endpoint, params) {
    let url = endpoint;
    Object.keys(params).forEach(key => {
        url = url.replace(`:${key}`, params[key]);
    });
    return url;
}

// ==================== دوال خاصة بكل نوع بيانات ====================

// دوال الفنادق
const HotelsAPI = {
    // الحصول على جميع الفنادق
    getAll: () => apiGet(API_ENDPOINTS.getHotels),
    
    // الحصول على فندق محدد
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getHotel, { id })),
    
    // إضافة فندق جديد
    create: (hotelData) => apiPost(API_ENDPOINTS.createHotel, hotelData),
    
    // تحديث فندق
    update: (id, hotelData) => apiPut(replaceUrlParams(API_ENDPOINTS.updateHotel, { id }), hotelData),
    
    // حذف فندق
    delete: (id) => apiDelete(replaceUrlParams(API_ENDPOINTS.deleteHotel, { id }))
};

// دوال المستخدمين
const UsersAPI = {
    // تسجيل دخول
    login: (username, password) => apiPost(API_ENDPOINTS.login, { username, password }),
    
    // تسجيل جديد
    register: (userData) => apiPost(API_ENDPOINTS.register, userData),
    
    // الحصول على بيانات مستخدم
    getById: (id) => apiGet(replaceUrlParams(API_ENDPOINTS.getUser, { id })),
    
    // تحديث بيانات مستخدم
    update: (id, userData) => apiPut(replaceUrlParams(API_ENDPOINTS.updateUser, { id }), userData)
};

// دوال المراجعات
const ReviewsAPI = {
    // الحصول على مراجعات فندق
    getByHotelId: (hotelId) => apiGet(replaceUrlParams(API_ENDPOINTS.getReviews, { hotelId })),
    
    // إضافة مراجعة
    create: (hotelId, reviewData) => apiPost(replaceUrlParams(API_ENDPOINTS.createReview, { hotelId }), reviewData)
};

// دوال الحجوزات
const BookingsAPI = {
    // الحصول على جميع حجوزات المستخدم
    getUserBookings: (userId) => apiGet(replaceUrlParams(API_ENDPOINTS.getUserBookings, { userId })),
    
    // إنشاء حجز جديد
    create: (bookingData) => apiPost(API_ENDPOINTS.createBooking, bookingData)
};

// دوال الدفع
const PaymentsAPI = {
    // معالجة الدفع
    process: (paymentData) => apiPost(API_ENDPOINTS.processPayment, paymentData)
};
