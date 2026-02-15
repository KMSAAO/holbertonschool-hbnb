/**
 * ملف: bookings.js
 * الوصف: إدارة صفحة الحجوزات - تم التعديل لربط البيانات مع الحفاظ على الكود الأصلي.
 */

document.addEventListener('DOMContentLoaded', () => {
    // التحقق من تسجيل الدخول (إذا كانت الدالة موجودة في auth.js)
    if (typeof checkProtectedPage === 'function') {
        checkProtectedPage();
    }
    
    // تحميل الحجوزات فور فتح الصفحة
    loadBookings();
});

// ✅ 1. تحديث دالة التحميل لتقرأ من المفتاح الموحد
function loadBookings() {
    const bookingsList = document.getElementById('bookingsList');
    const emptyState = document.getElementById('emptyState');
    
    // جلب الحجوزات من المفتاح الذي استخدمناه في صفحة الدفع (myBookings)
    const bookings = JSON.parse(localStorage.getItem('myBookings') || '[]');
    
    console.log("الحجوزات التي تم العثور عليها:", bookings); // للتأكد في الكونسول

    if (bookings.length === 0) {
        if (bookingsList) bookingsList.style.display = 'none';
        if (emptyState) emptyState.style.display = 'block';
        return;
    }
    
    if (bookingsList) bookingsList.style.display = 'flex';
    if (emptyState) emptyState.style.display = 'none';
    
    // استدعاء دالة العرض (التي أضفناها بالأسفل لتشغيل كودك الأصلي)
    displayBookings(bookings);
}

// ✅ 2. إضافة الدالة التي تربط البيانات بالقالب (Template) الخاص بك
function displayBookings(bookings) {
    const bookingsList = document.getElementById('bookingsList');
    if (!bookingsList) return;
    bookingsList.innerHTML = ''; // مسح القائمة الحالية

    bookings.reverse().forEach((booking, index) => {
        // نستخدم دالتك الأصلية لبناء البطاقة
        const card = createBookingCard(booking, index);
        bookingsList.appendChild(card);
    });
}

// ✅ 3. دالتك الأصلية (أضفنا قيم افتراضية فقط لضمان عدم ظهور undefined)
function createBookingCard(booking, index) {
    const card = document.createElement('div');
    card.className = 'booking-card';
    
    const statusInfo = getStatusInfo(booking.status || 'confirmed');
    
    // حساب عدد الليالي (أو استخدامه إذا كان جاهزاً)
    const nights = booking.nights || 0;
    
    card.innerHTML = `
        <img src="${booking.hotelImage || '/static/images/shebara1.jpg'}" alt="${booking.hotelName}" class="booking-image">
        
        <div class="booking-details">
            <h2 class="booking-hotel-name">${booking.hotelName}</h2>
            <div class="booking-info">
                <div class="info-item">
                    <i class="fas fa-bed"></i>
                    <span>${booking.roomName || 'جناح متميز'}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-calendar-check"></i>
                    <span>تسجيل الدخول: ${booking.checkIn}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-calendar-times"></i>
                    <span>تسجيل الخروج: ${booking.checkOut}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-moon"></i>
                    <span>${nights} ليالي</span>
                </div>
                <div class="info-item">
                    <i class="${statusInfo.icon}"></i>
                    <span>الحالة: ${statusInfo.text}</span>
                </div>
            </div>
        </div>
        
        <div class="booking-actions">
            <div class="booking-total">${booking.totalPrice}</div>
            <button class="booking-btn btn-details" onclick="viewBookingDetails(${index})">
                <i class="fas fa-eye"></i> عرض التفاصيل
            </button>
            ${!booking.status.includes('cancelled') && !booking.status.includes('ملغي') ? `
                <button class="booking-btn btn-cancel" onclick="cancelBooking(${index})">
                    <i class="fas fa-times"></i> إلغاء الحجز
                </button>
            ` : ''}
        </div>
    `;
    
    return card;
}

// ✅ 4. باقي دوالك الأصلية اتركها كما هي تماماً

function getStatusInfo(status) {
    const statusMap = {
        'confirmed': { icon: 'fas fa-check-circle', text: 'مؤكد' },
        'pending': { icon: 'fas fa-clock', text: 'قيد الانتظار' },
        'cancelled': { icon: 'fas fa-times-circle', text: 'ملغي' }
    };
    return statusMap[status] || statusMap['confirmed'];
}

function formatDate(dateString) {
    if (!dateString) return "-";
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ar-SA', options);
}

function viewBookingDetails(index) {
    const bookings = JSON.parse(localStorage.getItem('myBookings') || '[]');
    const booking = bookings[index];
    if (!booking) return;
    
    alert("تفاصيل الحجز لـ: " + booking.hotelName + "\nالمبلغ الإجمالي: " + booking.totalPrice);
}

function cancelBooking(index) {
    if (!confirm('هل أنت متأكد من إلغاء هذا الحجز؟')) return;
    
    let bookings = JSON.parse(localStorage.getItem('myBookings') || '[]');
    
    if (bookings[index]) {
        bookings[index].status = 'cancelled';
        localStorage.setItem('myBookings', JSON.stringify(bookings));
        loadBookings();
        alert('تم إلغاء الحجز بنجاح');
    }
}