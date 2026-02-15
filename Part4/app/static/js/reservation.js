/**
 * ملف: reservation.js
 * الوصف: إدارة الحجوزات، الحسابات المالية، وتبديل طرق الدفع.
 */

let currentHotel = null;

document.addEventListener('DOMContentLoaded', () => {
    // تشغيل الجلب والتهيئة عند تحميل الصفحة
    const urlParams = new URLSearchParams(window.location.search);
    const hotelId = urlParams.get('id');

    if (hotelId) {
        fetchHotelForReservation(hotelId);
    }

    // إعداد مستمعي الأحداث للعناصر (Events)
    setupEventListeners();
});

// ==================== 1. جلب البيانات وتحديث الواجهة ====================

async function fetchHotelForReservation(hotelId) {
    try {
        const response = await fetch(`/api/v1/places/${hotelId}`);
        if (!response.ok) throw new Error('Hotel not found');
        
        currentHotel = await response.json();
        
        updateHotelUI();
        calculateAll(); 
    } catch (error) {
        console.error('Error fetching hotel:', error);
    }
}

function updateHotelUI() {
    if (!currentHotel) return;

    // تحديث الأسماء (Header + Summary)
    document.querySelectorAll('.hotel-name, .summary-value').forEach(el => {
        if (el.textContent.trim() === 'Shebara Resort' || el.id === 'summaryHotelName') {
            el.textContent = currentHotel.title;
        }
    });

    // تحديث الموقع
    const locElem = document.querySelector('.hotel-location');
    if (locElem) locElem.innerHTML = `<i class="fas fa-map-marker-alt"></i> ${currentHotel.latitude}, ${currentHotel.longitude}`;

    // تعيين الحد الأدنى للتواريخ
    const today = new Date().toISOString().split('T')[0];
    const checkInInput = document.getElementById('checkInDate');
    const checkOutInput = document.getElementById('checkOutDate');
    if (checkInInput) checkInInput.min = today;
    if (checkOutInput) checkOutInput.min = today;
}

// ==================== 2. الحسابات المالية ====================

function calculateAll() {
    const checkInInput = document.getElementById('checkInDate');
    const checkOutInput = document.getElementById('checkOutDate');

    if (!checkInInput || !checkOutInput || !currentHotel) return;

    const d1 = new Date(checkInInput.value);
    const d2 = new Date(checkOutInput.value);
    
    let nights = 0;
    if (checkInInput.value && checkOutInput.value) {
        nights = Math.max(0, Math.ceil((d2 - d1) / (1000 * 60 * 60 * 24)));
    }

    // تحديث عدد الليالي في الواجهة
    const nightsDisplay = document.getElementById('nightsCount');
    const summaryNights = document.getElementById('summaryNights');
    if (nightsDisplay) nightsDisplay.textContent = nights;
    if (summaryNights) summaryNights.textContent = nights;

    if (nights > 0) {
        const subtotal = currentHotel.price * nights;
        const tax = subtotal * 0.2075; // نسبة الضريبة 20.75%
        const total = subtotal + tax;

        // تحديث المبالغ
        document.getElementById('summarySubtotal').textContent = `${subtotal.toLocaleString()} ر.س`;
        document.getElementById('summaryTax').textContent = `${tax.toLocaleString(undefined, {minimumFractionDigits: 2})} ر.س`;
        document.getElementById('summaryTotal').textContent = `${total.toLocaleString(undefined, {minimumFractionDigits: 2})} ر.س`;
        document.getElementById('payBtnAmount').textContent = `${total.toLocaleString(undefined, {minimumFractionDigits: 2})} ر.س`;
        
        // تحديث التواريخ في الملخص
        document.getElementById('summaryCheckIn').textContent = checkInInput.value;
        document.getElementById('summaryCheckOut').textContent = checkOutInput.value;
    }
}

// ==================== 3. منطق الدفع والتبديل ====================

function selectPaymentMethod(method) {
    // تحديث شكل الأزرار
    document.querySelectorAll('.payment-method').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');

    const cardFields = document.getElementById('cardFields');
    const applePayMsg = document.getElementById('applePayMessage');
    const payBtnText = document.getElementById('payBtnText');
    const payBtnIcon = document.getElementById('payBtnIcon');

    if (method === 'applepay') {
        cardFields.style.display = 'none';
        applePayMsg.style.display = 'block';
        payBtnText.textContent = 'ادفع بـ Apple Pay';
        payBtnIcon.className = 'fab fa-apple-pay';
    } else {
        cardFields.style.display = 'block';
        applePayMsg.style.display = 'none';
        payBtnIcon.className = 'fas fa-lock';
        payBtnText.textContent = (method === 'mada') ? 'تأكيد الدفع بمدى' : 'تأكيد الدفع';
    }
}

// دالة الحفظ النهائية (Local Storage) لكي تظهر في صفحة الحجوزات
function processPayment(event) {
    event.preventDefault();

    // 1. جلب بيانات المستخدم (ضروري جداً لربط الحجز بالحساب)
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser || !currentUser.email) {
        alert("يرجى تسجيل الدخول أولاً لإتمام الحجز");
        return;
    }

    // 2. تجميع بيانات الحجز (تأكد من وجود roomName و hotelImage)
    const bookingData = {
        bookingId: 'BK-' + Math.floor(Math.random() * 100000),
        hotelName: document.querySelector('.hotel-name').textContent,
        hotelImage: '/static/images/shebara1.jpg', // صورة افتراضية
        roomName: 'جناح نُزل المتميز',
        checkIn: document.getElementById('checkInDate').value,
        checkOut: document.getElementById('checkOutDate').value,
        nights: document.getElementById('nightsCount').textContent,
        totalPrice: document.getElementById('summaryTotal').textContent,
        status: 'confirmed', //
        bookingDate: new Date().toISOString(),
        guests: 2
    };

    // 3. الحفظ باستخدام المفتاح الذي يتوقعه ملف bookings.js الأصلي
    const storageKey = `bookings_${currentUser.email}`; //
    let userBookings = JSON.parse(localStorage.getItem(storageKey) || '[]');
    userBookings.push(bookingData);
    localStorage.setItem(storageKey, JSON.stringify(userBookings));

    alert('✓ تم تأكيد حجزك بنجاح! سيظهر الآن في قائمة حجوزاتك.');
    window.location.href = '/bookings';
}

// ==================== 4. وظائف المساعدة والتحكم ====================

function setupEventListeners() {
    const checkInInput = document.getElementById('checkInDate');
    const checkOutInput = document.getElementById('checkOutDate');
    if (checkInInput) checkInInput.addEventListener('change', calculateAll);
    if (checkOutInput) checkOutInput.addEventListener('change', calculateAll);

    // تنسيق رقم البطاقة
    const cardInput = document.getElementById('cardNumber');
    if (cardInput) {
        cardInput.addEventListener('input', (e) => {
            e.target.value = e.target.value.replace(/\D/g, '').replace(/(.{4})/g, '$1 ').trim();
        });
    }
}

function completeBooking() {
    if (document.getElementById('nightsCount').textContent === '0') return alert('اختر تواريخ إقامة صحيحة');
    
    // نقل البيانات لقسم ملخص الطلب
    document.getElementById('paymentSummary').innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;"><span>الفندق:</span> <strong>${currentHotel.title}</strong></div>
        <div style="display:flex; justify-content:space-between; border-top:1px solid #eee; padding-top:10px;"><span>الإجمالي:</span> <strong>${document.getElementById('summaryTotal').textContent}</strong></div>
    `;

    document.getElementById('bookingSection').style.display = 'none';
    document.getElementById('paymentSection').style.display = 'block';
    window.scrollTo(0,0);
}

function backToBooking() {
    document.getElementById('bookingSection').style.display = 'block';
    document.getElementById('paymentSection').style.display = 'none';
}