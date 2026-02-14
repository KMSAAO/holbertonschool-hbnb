/**
 * ملف: reservation.js
 * الوصف: إدارة الحجوزات مع التحقق من وجود العناصر لتجنب الأخطاء.
 */

let currentHotel = null;

function getAuthToken() {
    return document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
}

// ==================== 1. جلب البيانات (مع التحقق) ====================

async function fetchHotelForReservation() {
    // تحقق أمان: إذا لم نكن في صفحة تحتوي على حقول تواريخ، لا تكمل العمل
    if (!document.getElementById('checkInDate')) return;

    const urlParams = new URLSearchParams(window.location.search);
    const hotelId = urlParams.get('id');

    if (!hotelId) return;

    try {
        const response = await fetch(`/api/v1/places/${hotelId}`);
        if (!response.ok) throw new Error('Hotel not found');
        
        currentHotel = await response.json();
        
        updateHotelUI();
        calculateAll(); // لن تسبب خطأ الآن لأننا تحققنا في البداية
    } catch (error) {
        console.error('Error fetching hotel:', error);
    }
}

function updateHotelUI() {
    if (!currentHotel) return;

    const nameElem = document.querySelector('.hotel-name');
    const locElem = document.querySelector('.hotel-location');
    const summaryName = document.querySelector('.summary-card .summary-value');

    // استخدام Optional Chaining (?.) لتجنب الأخطاء إذا لم توجد العناصر
    if (nameElem) nameElem.textContent = currentHotel.title;
    if (summaryName) summaryName.textContent = currentHotel.title;
    if (locElem) locElem.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${currentHotel.latitude}, ${currentHotel.longitude}`;

    // توليد خيار الغرفة
    const roomsSection = document.getElementById('roomsListContainer');
    if (roomsSection) {
        roomsSection.innerHTML = `
            <div class="room-option selected" data-price="${currentHotel.price}">
                <div class="room-option-header">
                    <div class="room-option-info">
                        <h3>جناح نُزل المتميز</h3>
                        <p class="room-size">إقامة فاخرة</p>
                    </div>
                    <div class="room-option-price">
                        <span class="price-value">${currentHotel.price} ر.س</span>
                        <span class="price-label">/ ليلة</span>
                    </div>
                </div>
                </div>
        `;
    }
}

// ==================== 2. الحسابات (مع منع الانهيار) ====================

function calculateAll() {
    // أهم إصلاح: التأكد من وجود العناصر قبل قراءة .value
    const checkInInput = document.getElementById('checkInDate');
    const checkOutInput = document.getElementById('checkOutDate');

    if (!checkInInput || !checkOutInput || !currentHotel) return;

    const checkIn = checkInInput.value;
    const checkOut = checkOutInput.value;
    
    let nights = 0;
    if (checkIn && checkOut) {
        const d1 = new Date(checkIn);
        const d2 = new Date(checkOut);
        nights = Math.max(0, Math.ceil((d2 - d1) / (1000 * 60 * 60 * 24)));
    }

    // تحديث العناصر في الصفحة (فقط إذا كانت موجودة)
    const nightsElem = document.getElementById('summaryNights');
    if (nightsElem) nightsElem.textContent = nights;
    
    // ... باقي الحسابات
}

// ==================== 3. التهيئة ====================

document.addEventListener('DOMContentLoaded', () => {
    // التأكد من وجود العناصر قبل إضافة المستمعين
    const checkInInput = document.getElementById('checkInDate');
    const checkOutInput = document.getElementById('checkOutDate');

    if (checkInInput && checkOutInput) {
        const today = new Date().toISOString().split('T')[0];
        checkInInput.min = today;
        checkOutInput.min = today;
        
        checkInInput.addEventListener('change', calculateAll);
        checkOutInput.addEventListener('change', calculateAll);
        
        // تشغيل الجلب فقط إذا كنا في صفحة الحجز
        fetchHotelForReservation();
    }
});