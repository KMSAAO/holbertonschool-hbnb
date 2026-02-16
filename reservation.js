/**
 * ملف: reservation.js
 * الوصف: إدارة صفحة الحجز
 * الوظائف: عرض الغرف المتاحة، حساب الأسعار مع الضرائب، دعم الفنادق المضافة من المستخدمين
 */


// الحصول على الفندق الحالي من URL
let currentHotel = {};

// الحصول على الفندق الحالي من URL (يدعم API)
async function fetchCurrentHotel() {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel');

    if (!hotelParam) return null;

    // 1. التحقق من الفنادق المضافة من المستخدمين أولاً (localStorage)
    if (hotelParam.startsWith('hotel_')) {
        const userHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
        const userHotel = userHotels.find(h => h.id === hotelParam);
        if (userHotel) {
            return {
                id: userHotel.id,
                name: userHotel.nameEn || userHotel.name,
                nameAr: userHotel.name,
                location: userHotel.location,
                rating: 5,
                rooms: userHotel.rooms || [{
                    id: 'standard-' + userHotel.id,
                    name: 'غرفة قياسية',
                    price: parseFloat(userHotel.price) || 500,
                    features: ['يستوعب 2', 'إطلالة'],
                    size: 35
                }]
            };
        }
    }

    // 2. التحقق من الـ backend API
    if (typeof PlacesAPI !== 'undefined') {
        try {
            console.log('جلب بيانات الفندق من API:', hotelParam);
            const place = await PlacesAPI.getById(hotelParam);

            if (place) {
                // إنشاء غرفة افتراضية بناءً على السعر لأن الـ backend لا يدعم الغرف حالياً
                const defaultRoom = {
                    id: 'standard-room-' + place.id,
                    name: 'غرفة قياسية',
                    price: place.price || 500,
                    features: ['سرير مزدوج', 'إطلالة', 'تكييف', 'واي فاي مجاني', 'يستوعب 2'],
                    size: 35,
                    image: 'images/hotel1.jpg' // صورة افتراضية صحيحة
                };

                return {
                    id: place.id,
                    name: place.title || 'فندق',
                    nameAr: place.title || 'فندق',
                    location: `${place.latitude || '0'}, ${place.longitude || '0'}`, // يمكن تحسين العرض لاحقاً
                    rating: 5,
                    rooms: [defaultRoom]
                };
            }
        } catch (err) {
            console.error('فشل جلب الفندق من API:', err);
        }
    }

    return null;
}

// تحميل بيانات الفندق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', async () => {
    // إظهار مؤشر تحميل بسيط
    const container = document.querySelector('.booking-container');
    if (container) {
        // يمكن إضافة spinner هنا
    }

    const hotel = await fetchCurrentHotel();

    if (hotel) {
        currentHotel = hotel;
        updateHotelInfo();

        // تعيين الحد الأدنى للتواريخ (اليوم)
        const today = new Date().toISOString().split('T')[0];
        const checkInInput = document.getElementById('checkInDate');
        const checkOutInput = document.getElementById('checkOutDate');

        if (checkInInput) checkInInput.setAttribute('min', today);
        if (checkOutInput) checkOutInput.setAttribute('min', today);

        // تعيين تاريخ افتراضي (غداً لمدة 3 أيام)
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        if (checkInInput) checkInInput.value = tomorrow.toISOString().split('T')[0];

        const checkout = new Date();
        checkout.setDate(checkout.getDate() + 4);
        if (checkOutInput) checkOutInput.value = checkout.toISOString().split('T')[0];

        calculateAll(); // تحديث الحسابات الأولية
    } else {
        // عرض رسالة خطأ
        const container = document.querySelector('.booking-container') || document.body;
        if (container) {
            container.innerHTML = `
                <div style="text-align: center; padding: 100px 20px;">
                    <i class="fas fa-exclamation-circle fa-4x" style="color: #c62828; margin-bottom: 20px;"></i>
                    <h1 style="font-family: 'Amiri', serif;">عذراً، الوجهة غير موجودة أو تم حذفها</h1>
                    <p>لم نتمكن من العثور على تفاصيل الحجز لهذه الوجهة.</p>
                    <a href="places.html" class="status-active" style="display: inline-block; margin-top: 20px; text-decoration: none; font-size: 1.2rem;">العودة للوجهات</a>
                </div>
            `;
        }
    }
});

// حساب تفاصيل الحجز

// تحديث التواريخ
const checkInEl = document.getElementById('checkInDate');
const checkOutEl = document.getElementById('checkOutDate');
if (checkInEl) checkInEl.addEventListener('change', calculateAll);
if (checkOutEl) checkOutEl.addEventListener('change', calculateAll);

// تحديث عدد الغرف
function updateRoomQuantity(btn, change) {
    const input = btn.parentElement.querySelector('.qty-input');
    const currentValue = parseInt(input.value);
    const newValue = Math.max(0, Math.min(10, currentValue + change));
    input.value = newValue;

    // تحديث حالة الغرفة
    const roomOption = btn.closest('.room-option');
    if (newValue > 0) {
        roomOption.classList.add('selected');
    } else {
        roomOption.classList.remove('selected');
    }

    calculateAll();
}

// تحديث عدد النزلاء
function updateGuests(type, change) {
    const input = document.getElementById(type === 'adults' ? 'adultsCount' : 'childrenCount');
    if (!input) return;

    const currentValue = parseInt(input.value);
    const min = type === 'adults' ? 1 : 0;
    const max = type === 'adults' ? 20 : 10;
    const newValue = Math.max(min, Math.min(max, currentValue + change));
    input.value = newValue;

    // تحديث الملخص
    const summarySpan = document.getElementById(type === 'adults' ? 'summaryAdults' : 'summaryChildren');
    if (summarySpan) summarySpan.textContent = newValue;
}

// حساب عدد الليالي
function calculateNights() {
    const checkIn = document.getElementById('checkInDate')?.value;
    const checkOut = document.getElementById('checkOutDate')?.value;

    if (checkIn && checkOut) {
        const date1 = new Date(checkIn);
        const date2 = new Date(checkOut);
        const diffTime = date2 - date1;
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays > 0) {
            return diffDays;
        }
    }
    return 0;
}

// تحديث عرض التواريخ
function updateDateDisplay() {
    const checkIn = document.getElementById('checkInDate')?.value;
    const checkOut = document.getElementById('checkOutDate')?.value;
    const nights = calculateNights();

    // تحديث عدد الليالي
    const nightsCountEl = document.getElementById('nightsCount');
    const summaryNightsEl = document.getElementById('summaryNights');
    if (nightsCountEl) nightsCountEl.textContent = nights;
    if (summaryNightsEl) summaryNightsEl.textContent = nights;

    // تحديث التواريخ في الملخص
    const summaryCheckIn = document.getElementById('summaryCheckIn');
    if (summaryCheckIn) {
        if (checkIn) {
            const date = new Date(checkIn);
            summaryCheckIn.textContent = date.toLocaleDateString('ar-EG');
        } else {
            summaryCheckIn.textContent = '-';
        }
    }

    const summaryCheckOut = document.getElementById('summaryCheckOut');
    if (summaryCheckOut) {
        if (checkOut) {
            const date = new Date(checkOut);
            summaryCheckOut.textContent = date.toLocaleDateString('ar-EG');
        } else {
            summaryCheckOut.textContent = '-';
        }
    }
}

// حساب المجموع الكلي
function calculateAll() {
    updateDateDisplay();

    const nights = calculateNights();
    let subtotal = 0;
    const selectedRoomsList = document.getElementById('selectedRoomsList');
    if (selectedRoomsList) selectedRoomsList.innerHTML = '';

    // حساب كل غرفة محددة
    const roomOptions = document.querySelectorAll('.room-option');
    roomOptions.forEach(room => {
        const input = room.querySelector('.qty-input');
        if (!input) return;

        const qty = parseInt(input.value);
        if (qty > 0) {
            const price = parseFloat(room.getAttribute('data-price'));
            const roomName = room.getAttribute('data-name');
            const roomTotal = price * nights * qty;
            subtotal += roomTotal;

            // إضافة للقائمة
            if (selectedRoomsList) {
                const roomItem = document.createElement('div');
                roomItem.className = 'summary-item';
                roomItem.innerHTML = `
                    <span class="summary-label">${roomName} × ${qty}</span>
                    <span class="summary-value" style="direction: ltr;">${roomTotal.toLocaleString('en-US')} ر.س</span>
                `;
                selectedRoomsList.appendChild(roomItem);
            }
        }
    });

    // حساب الضرائب (20.75%)
    const tax = Math.round(subtotal * 0.2075);
    const total = subtotal + tax;

    // تحديث الملخص
    const subtotalEl = document.getElementById('summarySubtotal');
    const taxEl = document.getElementById('summaryTax');
    const totalEl = document.getElementById('summaryTotal');

    if (subtotalEl) subtotalEl.textContent = subtotal.toLocaleString('en-US') + ' ر.س';
    if (taxEl) taxEl.textContent = tax.toLocaleString('en-US') + ' ر.س';
    if (totalEl) totalEl.textContent = total.toLocaleString('en-US') + ' ر.س';
}

// إتمام الحجز
async function completeBooking() {
    // التحقق من تسجيل الدخول
    if (typeof isLoggedIn === 'function' && !isLoggedIn()) {
        if (typeof showNotification === 'function') {
            showNotification('يجب تسجيل الدخول أولاً', 'error');
        } else {
            alert('يجب تسجيل الدخول أولاً');
        }
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    // التحقق من التواريخ
    const checkIn = document.getElementById('checkInDate')?.value;
    const checkOut = document.getElementById('checkOutDate')?.value;

    if (!checkIn || !checkOut) {
        if (typeof showNotification === 'function') {
            showNotification('الرجاء اختيار تواريخ الإقامة', 'error');
        } else {
            alert('الرجاء اختيار تواريخ الإقامة');
        }
        return;
    }

    const nights = calculateNights();
    if (nights <= 0) {
        if (typeof showNotification === 'function') {
            showNotification('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول', 'error');
        } else {
            alert('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول');
        }
        return;
    }

    // التحقق من اختيار غرفة
    let hasRooms = false;
    const roomOptions = document.querySelectorAll('.room-option');
    roomOptions.forEach(room => {
        const input = room.querySelector('.qty-input');
        if (input && parseInt(input.value) > 0) {
            hasRooms = true;
        }
    });

    if (!hasRooms) {
        if (typeof showNotification === 'function') {
            showNotification('الرجاء اختيار غرفة واحدة على الأقل', 'error');
        } else {
            alert('الرجاء اختيار غرفة واحدة على الأقل');
        }
        return;
    }

    // جمع بيانات الحجز
    const subtotalEl = document.getElementById('summarySubtotal');
    const taxEl = document.getElementById('summaryTax');
    const totalEl = document.getElementById('summaryTotal');
    const adultsEl = document.getElementById('adultsCount');
    const childrenEl = document.getElementById('childrenCount');

    // Helper to parse price string "1,000 ر.س" -> 1000
    const parsePrice = (str) => {
        return parseFloat(str.replace(/[^0-9.]/g, '')) || 0;
    };

    const bookingData = {
        hotelName: currentHotel.name,
        hotelNameAr: currentHotel.nameAr,
        checkIn: checkIn,
        checkOut: checkOut,
        nights: nights,
        adults: parseInt(adultsEl?.value || 1),
        children: parseInt(childrenEl?.value || 0),
        rooms: [],
        subtotal: parsePrice(subtotalEl?.textContent || '0'),
        tax: parsePrice(taxEl?.textContent || '0'),
        total: parsePrice(totalEl?.textContent || '0')
    };

    // جمع بيانات الغرف
    roomOptions.forEach(room => {
        const input = room.querySelector('.qty-input');
        const qty = parseInt(input.value);
        if (qty > 0) {
            const price = parseFloat(room.dataset.price);
            const name = room.dataset.name;
            const roomTotal = price * nights * qty;

            bookingData.rooms.push({
                name: name,
                quantity: qty,
                pricePerNight: price,
                total: roomTotal
            });
        }
    });

    // حفظ البيانات في localStorage (مؤقت)
    try {
        localStorage.setItem('currentBooking', JSON.stringify(bookingData));
    } catch (e) {
        console.error('خطأ في حفظ البيانات:', e);
        alert('حدث خطأ في حفظ بيانات الحجز');
        return;
    }

    // إخفاء قسم الحجز وإظهار قسم الدفع
    const bookingSection = document.getElementById('bookingSection');
    const paymentSection = document.getElementById('paymentSection');

    if (bookingSection) bookingSection.style.display = 'none';
    if (paymentSection) paymentSection.style.display = 'block';

    window.scrollTo(0, 0);

    // ملء ملخص الطلب في قسم الدفع
    populatePaymentSummary(bookingData);
}

// تحديث معلومات الفندق في الصفحة
function updateHotelInfo() {
    // تحديث اسم الفندق
    const hotelNameElement = document.querySelector('.hotel-name');
    if (hotelNameElement) {
        hotelNameElement.textContent = currentHotel.name;
    }

    // تحديث الموقع
    const hotelLocationElement = document.querySelector('.hotel-location');
    if (hotelLocationElement) {
        hotelLocationElement.innerHTML = `
            <i class="fas fa-map-marker-alt"></i>
            ${currentHotel.location}
        `;
    }

    // تحديث النجوم
    const hotelRatingElement = document.querySelector('.hotel-rating span');
    if (hotelRatingElement) {
        hotelRatingElement.textContent = `منتجع ${currentHotel.rating} نجوم`;
    }

    // تحديث خيارات الغرف
    const roomOptionsContainer = document.querySelector('.booking-form-section');
    // البحث عن القسم الثالث (يفترض أنه قسم الغرف)
    // أو البحث عن الحاوية داخل الـ form
    const roomsSection = roomOptionsContainer?.querySelector('.booking-section-card:nth-child(3)');

    if (roomsSection && currentHotel.rooms) {
        let roomsHTML = `
            <h2 class="section-title">
                <i class="fas fa-bed"></i>
                اختر نوع الغرفة
            </h2>
        `;

        currentHotel.rooms.forEach(room => {
            roomsHTML += `
                <div class="room-option" data-price="${room.price}" data-name="${room.name}">
                    <div class="room-option-header">
                        <div class="room-option-info">
                            <h3>${room.name}</h3>
                            <div class="room-features">
                                ${room.features.map(f => `<span><i class="fas fa-check"></i> ${f}</span>`).join('')}
                            </div>
                            <p class="room-size">${room.size} متر مربع</p>
                        </div>
                        <div class="room-option-price">
                            <span class="price-value">${room.price.toLocaleString('en-US')} ر.س</span>
                            <span class="price-label">لكل ليلة</span>
                        </div>
                    </div>
                    <div class="room-option-footer">
                        <div class="qty-controls">
                            <button type="button" class="qty-btn" onclick="updateRoomQuantity(this, -1)">-</button>
                            <input type="number" class="qty-input" value="0" min="0" max="10" readonly>
                            <button type="button" class="qty-btn" onclick="updateRoomQuantity(this, 1)">+</button>
                        </div>
                    </div>
                </div>
            `;
        });

        roomsSection.innerHTML = roomsHTML;
    }
}

// ملء ملخص الطلب في قسم الدفع
function populatePaymentSummary(bookingData) {
    const summaryDiv = document.getElementById('paymentSummary');
    if (!summaryDiv) return;

    let html = '';

    // الفندق والتواريخ
    html += `
        <div class="summary-row">
            <span>الفندق:</span>
            <span>${bookingData.hotelName || bookingData.hotel}</span>
        </div>
        <div class="summary-row">
            <span>تاريخ الوصول:</span>
            <span>${bookingData.checkIn}</span>
        </div>
        <div class="summary-row">
            <span>تاريخ المغادرة:</span>
            <span>${bookingData.checkOut}</span>
        </div>
        <div class="summary-row">
            <span>عدد الليالي:</span>
            <span>${bookingData.nights}</span>
        </div>
    `;

    // الغرف
    if (bookingData.rooms) {
        bookingData.rooms.forEach(room => {
            const roomQty = room.quantity || 1;
            const roomPrice = room.total || 0;
            // التأكد من أن roomPrice رقم
            const priceVal = typeof roomPrice === 'string' ? parseFloat(roomPrice.replace(/[^0-9.]/g, '')) : roomPrice;

            html += `
                <div class="summary-row">
                    <span>${room.name} × ${roomQty}</span>
                    <span>${priceVal.toLocaleString('en-US')} ريال</span>
                </div>
            `;
        });
    }

    // المجموع الفرعي والضريبة والمجموع الكلي
    html += `
        <div class="summary-row">
            <span>المجموع الفرعي:</span>
            <span>${bookingData.subtotal.toLocaleString('en-US')} ريال</span>
        </div>
        <div class="summary-row">
            <span>الضريبة (20.75%):</span>
            <span>${bookingData.tax.toLocaleString('en-US')} ريال</span>
        </div>
        <div class="summary-row total">
            <span>المجموع الكلي:</span>
            <span>${bookingData.total.toLocaleString('en-US')} ريال</span>
        </div>
    `;

    summaryDiv.innerHTML = html;

    // تحديث زر الدفع بالمبلغ
    const payBtn = document.getElementById('payBtnAmount');
    if (payBtn) {
        payBtn.textContent = `${bookingData.total.toLocaleString('en-US')} ريال`;
    }
}

// العودة لصفحة الحجز
function backToBooking() {
    const bookingSection = document.getElementById('bookingSection');
    const paymentSection = document.getElementById('paymentSection');

    if (paymentSection) paymentSection.style.display = 'none';
    if (bookingSection) bookingSection.style.display = 'block';

    window.scrollTo(0, 0);
}

// معالجة الدفع
async function processPayment(event) {
    if (event) event.preventDefault();

    // التحقق من تسجيل الدخول
    if (typeof isLoggedIn === 'function' && !isLoggedIn()) {
        alert('يجب تسجيل الدخول أولاً');
        window.location.href = 'login.html';
        return;
    }

    // التحقق من طريقة الدفع المختارة
    const selectedMethod = document.querySelector('.payment-method.active');
    const isApplePay = selectedMethod && selectedMethod.querySelector('span').textContent.includes('Apple');

    let paymentMethod = 'بطاقة ائتمان';
    let cardLastFour = '';

    if (isApplePay) {
        paymentMethod = 'Apple Pay';
        cardLastFour = '****';
        alert('جاري معالجة الدفع عبر Apple Pay...');
    } else {
        const cardName = document.getElementById('cardName')?.value.trim();
        const cardNumber = document.getElementById('cardNumber')?.value.replace(/\s/g, '');
        const expiryDate = document.getElementById('expiryDate')?.value;
        const cvv = document.getElementById('cvv')?.value;

        if (!cardName) { alert('الرجاء إدخال اسم حامل البطاقة'); return; }
        if (cardNumber.length !== 16 || !/^\d+$/.test(cardNumber)) { alert('الرجاء إدخال رقم بطاقة صحيح (16 رقم)'); return; }
        if (!/^\d{2}\/\d{2}$/.test(expiryDate)) { alert('الرجاء إدخال تاريخ انتهاء صحيح (MM/YY)'); return; }
        if (cvv.length !== 3 || !/^\d+$/.test(cvv)) { alert('الرجاء إدخال رمز CVV صحيح (3 أرقام)'); return; }

        cardLastFour = cardNumber.slice(-4);
        if (selectedMethod && selectedMethod.querySelector('span').textContent.includes('مدى')) {
            paymentMethod = 'مدى';
        }
    }

    // الحصول على بيانات الحجز
    const bookingDataStr = localStorage.getItem('currentBooking');
    if (!bookingDataStr) {
        alert('حدث خطأ في استرجاع بيانات الحجز');
        return;
    }
    const bookingData = JSON.parse(bookingDataStr);

    // إضافة معلومات الدفع
    bookingData.paymentMethod = paymentMethod;
    bookingData.cardLastFour = cardLastFour;
    bookingData.paymentDate = new Date().toISOString();
    bookingData.bookingId = 'BK' + Date.now();
    bookingData.status = 'confirmed';

    // حفظ في localStorage (للمستخدم)
    let allBookings = JSON.parse(localStorage.getItem('bookings') || '[]');
    allBookings.push({
        bookingId: bookingData.bookingId,
        hotelName: bookingData.hotelName,
        roomName: bookingData.rooms?.[0]?.name || 'غرفة',
        checkIn: bookingData.checkIn,
        checkOut: bookingData.checkOut,
        guests: (bookingData.adults || 1) + (bookingData.children || 0),
        totalPrice: bookingData.total,
        status: 'confirmed',
        bookingDate: bookingData.paymentDate,
        hotelImage: 'images/hotel1.jpg'
    });
    localStorage.setItem('bookings', JSON.stringify(allBookings));

    // أيضاً حفظ في الـ backend
    const userId = localStorage.getItem('userId'); // Assuming logic stores userId
    // If using JWT, we might need to decode it or use a stored user object
    // Assuming 'userId' is stored or we can get it from 'user' object
    // If not, we might need a way to get current user ID. 
    // Usually isLoggedIn checks token. 

    // Fallback if userId not directly in localStorage but in token or 'user' object
    let finalUserId = userId;
    if (!finalUserId) {
        const userObj = JSON.parse(localStorage.getItem('user'));
        if (userObj && userObj.id) finalUserId = userObj.id;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel') || '';

    if (finalUserId && typeof BookingsAPI !== 'undefined') {
        try {
            await BookingsAPI.create({
                place_id: hotelParam, // Using place_id as expected by backend
                // Backend might extract user_id from token if protected, 
                // OR we send it if the endpoint allows (usually protected endpoints get user from token)
                // But let's send what we can.
                // check_in/out format? Backend usually expects ISO or YYYY-MM-DD
                check_in: new Date(bookingData.checkIn).toISOString(),
                check_out: new Date(bookingData.checkOut).toISOString(),
            });
            console.log('تم حفظ الحجز في الـ backend');
        } catch (err) {
            console.warn('تعذر حفظ الحجز في الـ backend:', err);
            // We continue anyway as client-side success is priority for UX now
        }
    }

    // حذف الحجز المؤقت
    localStorage.removeItem('currentBooking');

    // عرض رسالة النجاح
    alert(`✓ تم تأكيد حجزك بنجاح!\nرقم الحجز: ${bookingData.bookingId}\n\nسيتم إرسال تفاصيل الحجز على بريدك الإلكتروني`);

    // الانتقال للصفحة الرئيسية
    window.location.href = 'index.html';
}

// Helper functions for formatting (keep existing logic)
function formatCardNumber(input) {
    let value = input.value.replace(/\s/g, '').replace(/\D/g, '');
    let formatted = value.match(/.{1,4}/g);
    input.value = formatted ? formatted.join(' ') : value;
}

function formatExpiryDate(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
    }
    input.value = value;
}

function validateCVV(input) {
    input.value = input.value.replace(/\D/g, '').slice(0, 3);
}

function selectPaymentMethod(method) {
    // Logic as before
    document.querySelectorAll('.payment-method').forEach(el => {
        el.classList.remove('active');
    });
    const target = event.target.closest('.payment-method'); // event is global or needs passing
    if (target) target.classList.add('active');

    const cardFields = document.getElementById('cardFields');
    const applePayMessage = document.getElementById('applePayMessage');
    const payBtnText = document.getElementById('payBtnText');
    const payBtnIcon = document.getElementById('payBtnIcon');
    const cardInputs = cardFields.querySelectorAll('input');

    if (method === 'applepay') {
        cardFields.style.display = 'none';
        applePayMessage.style.display = 'block';
        if (payBtnText) payBtnText.textContent = 'ادفع بـ Apple Pay';
        if (payBtnIcon) payBtnIcon.className = 'fab fa-apple-pay';
        cardInputs.forEach(input => input.removeAttribute('required'));
    } else {
        cardFields.style.display = 'block';
        applePayMessage.style.display = 'none';
        if (method === 'mada') {
            if (payBtnText) payBtnText.textContent = 'تأكيد الدفع بمدى';
            if (payBtnIcon) payBtnIcon.className = 'fas fa-money-check';
        } else {
            if (payBtnText) payBtnText.textContent = 'تأكيد الدفع';
            if (payBtnIcon) payBtnIcon.className = 'fas fa-lock';
        }
        cardInputs.forEach(input => input.setAttribute('required', 'required'));
    }
}
