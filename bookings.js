/**
 * ملف: bookings.js
 * الوصف: إدارة صفحة الحجوزات - عرض وفلترة الحجوزات
 */

// ==================== تحميل الحجوزات ====================

document.addEventListener('DOMContentLoaded', () => {
    // التحقق من تسجيل الدخول
    checkProtectedPage();
    
    // تحميل الحجوزات
    loadBookings();
});

// تحميل وعرض الحجوزات
function loadBookings() {
    const bookingsList = document.getElementById('bookingsList');
    const emptyState = document.getElementById('emptyState');
    
    // جلب الحجوزات من localStorage
    const bookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    
    // التحقق من وجود حجوزات
    if (bookings.length === 0) {
        bookingsList.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    bookingsList.style.display = 'flex';
    emptyState.style.display = 'none';
    
    // عرض الحجوزات
    displayBookings(bookings);
}

// إنشاء بطاقة حجز
function createBookingCard(booking, index) {
    const card = document.createElement('div');
    card.className = 'booking-card';
    
    // تحديد الأيقونة والنص حسب الحالة
    const statusInfo = getStatusInfo(booking.status || 'confirmed');
    
    // حساب عدد الليالي
    const checkIn = new Date(booking.checkIn);
    const checkOut = new Date(booking.checkOut);
    const nights = Math.ceil((checkOut - checkIn) / (1000 * 60 * 60 * 24));
    
    card.innerHTML = `
        <img src="${booking.hotelImage || 'images/hotel1.jpg'}" alt="${booking.hotelName}" class="booking-image">
        
        <div class="booking-details">
            <h2 class="booking-hotel-name">${booking.hotelName}</h2>
            <div class="booking-info">
                <div class="info-item">
                    <i class="fas fa-bed"></i>
                    <span>${booking.roomName}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-calendar-check"></i>
                    <span>تسجيل الدخول: ${formatDate(booking.checkIn)}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-calendar-times"></i>
                    <span>تسجيل الخروج: ${formatDate(booking.checkOut)}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-moon"></i>
                    <span>${nights} ${nights > 10 ? 'ليلة' : 'ليالي'}</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-users"></i>
                    <span>${booking.guests || 2} ضيف</span>
                </div>
                <div class="info-item">
                    <i class="fas fa-clock"></i>
                    <span>تاريخ الحجز: ${formatDate(booking.bookingDate)}</span>
                </div>
                <div class="info-item">
                    <i class="${statusInfo.icon}"></i>
                    <span>الحالة: ${statusInfo.text}</span>
                </div>
            </div>
        </div>
        
        <div class="booking-actions">
            <div class="booking-total">${booking.totalPrice.toLocaleString('ar-EG')} ر.س</div>
            <button class="booking-btn btn-details" onclick="viewBookingDetails(${index})">
                <i class="fas fa-eye"></i> عرض التفاصيل
            </button>
            ${booking.status !== 'cancelled' ? `
                <button class="booking-btn btn-cancel" onclick="cancelBooking(${index})">
                    <i class="fas fa-times"></i> إلغاء الحجز
                </button>
            ` : ''}
        </div>
    `;
    
    return card;
}

// معلومات الحالة
function getStatusInfo(status) {
    const statusMap = {
        'confirmed': {
            icon: 'fas fa-check-circle',
            text: 'مؤكد'
        },
        'pending': {
            icon: 'fas fa-clock',
            text: 'قيد الانتظار'
        },
        'cancelled': {
            icon: 'fas fa-times-circle',
            text: 'ملغي'
        }
    };
    
    return statusMap[status] || statusMap['confirmed'];
}

// تنسيق التاريخ
function formatDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('ar-SA', options);
}

// ==================== عرض تفاصيل الحجز ====================

function viewBookingDetails(index) {
    const bookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    const booking = bookings[index];
    
    if (!booking) return;
    
    // عرض نافذة منبثقة بالتفاصيل
    const modal = document.createElement('div');
    modal.className = 'booking-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        padding: 20px;
    `;
    
    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: white;
        border-radius: 15px;
        padding: 40px;
        max-width: 600px;
        width: 100%;
        max-height: 80vh;
        overflow-y: auto;
        font-family: 'Amiri', serif;
    `;
    
    modalContent.innerHTML = `
        <h2 style="color: #815B2F; margin-bottom: 20px; font-size: 2rem;">تفاصيل الحجز</h2>
        <div style="line-height: 2;">
            <p><strong>رقم الحجز:</strong> ${booking.bookingId || 'BK-' + index}</p>
            <p><strong>الفندق:</strong> ${booking.hotelName}</p>
            <p><strong>الغرفة:</strong> ${booking.roomName}</p>
            <p><strong>تسجيل الدخول:</strong> ${formatDate(booking.checkIn)}</p>
            <p><strong>تسجيل الخروج:</strong> ${formatDate(booking.checkOut)}</p>
            <p><strong>عدد الضيوف:</strong> ${booking.guests || 2}</p>
            <p><strong>السعر الكلي:</strong> ${booking.totalPrice.toLocaleString('ar-EG')} ر.س</p>
            <p><strong>الحالة:</strong> ${getStatusInfo(booking.status || 'confirmed').text}</p>
        </div>
        <button onclick="this.closest('.booking-modal').remove()" style="
            margin-top: 30px;
            padding: 15px 40px;
            background: #815B2F;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1rem;
            width: 100%;
            font-family: 'Amiri', serif;
        ">إغلاق</button>
    `;
    
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
    
    // إغلاق عند النقر خارج المحتوى
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// ==================== إلغاء الحجز ====================

function cancelBooking(index) {
    if (!confirm('هل أنت متأكد من إلغاء هذا الحجز؟')) {
        return;
    }
    
    const bookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    
    if (bookings[index]) {
        bookings[index].status = 'cancelled';
        localStorage.setItem('bookings', JSON.stringify(bookings));
        
        // إعادة تحميل الصفحة
        loadBookings();
        
        alert('تم إلغاء الحجز بنجاح');
    }
}
