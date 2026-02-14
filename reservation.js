/**
 * ملف: reservation.js
 * الوصف: إدارة صفحة الحجز
 * الوظائف: عرض الغرف المتاحة، حساب الأسعار مع الضرائب، دعم الفنادق المضافة من المستخدمين
 */

// ==================== قاعدة بيانات الفنادق ====================

const hotelsData = {
    shebara: {
        name: 'Shebara Resort',
        nameAr: 'منتجع شيبارا',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'beach-villa',
                name: 'فيلا شاطئية من غرفة نوم واحدة',
                price: 10300,
                features: ['مسبح لامتناهي', 'إطلالة على البحر', 'يستوعب 2'],
                size: 104
            },
            {
                id: 'overwater-villa',
                name: 'فيلا من غرفة نوم واحدة فوق المياه',
                price: 14000,
                features: ['مسبح لامتناهي', 'إطلالة على البحر', 'يستوعب 2'],
                size: 104
            },
            {
                id: 'overwater-villa-2bed',
                name: 'فيلا فوق الماء بغرفتي نوم',
                price: 19200,
                features: ['مسبح لامتناهي', 'إطلالة على البحر', 'يستوعب 4'],
                size: 189
            }
        ]
    },
    desertrock: {
        name: 'Desert Rock Resort',
        nameAr: 'منتجع ديزرت روك',
        location: 'حانك، العلا، المملكة العربية السعودية',
        rating: 5,
        description: 'استمتع بخدمة ذات مستوى عالمي في Desert Rock Resort. يوفر مكان الإقامة مطعماً ومسبحاً خارجياً، بالإضافة إلى ساونا وحوض استحمام ساخن. يوفر مكان الإقامة للضيوف خدمة الغرف، ومكتب استقبال يعمل على مدار الساعة.',
        rooms: [
            {
                id: 'wadi-villa',
                name: 'فيلا الوادي من غرفة نوم واحدة',
                price: 8500,
                features: ['شرفة خاصة', 'إطلالة على الجبل', 'يستوعب 2'],
                size: 171,
                image: 'images/desertrock-wadi.jpg'
            },
            {
                id: 'cliff-villa',
                name: 'فيلا معلقة على المنحدر من غرفة واحدة',
                price: 10200,
                features: ['مدخل خاص', 'إطلالة على الجبل', 'يستوعب 2'],
                size: 183,
                image: 'images/desertrock-cliff.jpg'
            },
            {
                id: 'wadi-villa-2bed',
                name: 'فيلا الوادي من غرفتي نوم',
                price: 17000,
                features: ['صالة معيشة', 'إطلالة على الجبل', 'يستوعب 4'],
                size: 259,
                image: 'images/desertrock-wadi2.jpg'
            }
        ]
    },
    shaden: {
        name: 'Shaden Resort',
        nameAr: 'منتجع شادن',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'deluxe-room',
                name: 'غرفة ديلوكس مزدوجة',
                price: 4120,
                features: ['مسبح خاص', 'إطلالة على الجبل', 'يستوعب 2'],
                size: 40
            },
            {
                id: 'premium-suite',
                name: 'جناح بريميوم عائلي',
                price: 5850,
                features: ['مسبح خاص', 'إطلالة على الحديقة', 'يستوعب 3'],
                size: 60
            },
            {
                id: 'executive-villa',
                name: 'فيلا تنفيذية من غرفتين',
                price: 8200,
                features: ['مسبح لامتناهي', 'إطلالة بانورامية', 'يستوعب 4'],
                size: 95
            }
        ]
    },
    chedi: {
        name: 'The Chedi Hegra',
        nameAr: 'ذا تشيدي حجرا',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'desert-view',
                name: 'غرفة مطلة على الصحراء',
                price: 5336,
                features: ['شرفة خاصة', 'إطلالة على الصحراء', 'يستوعب 2'],
                size: 48
            },
            {
                id: 'heritage-suite',
                name: 'جناح التراث الفاخر',
                price: 7200,
                features: ['صالة واسعة', 'إطلالة على الحجر', 'يستوعب 3'],
                size: 72
            },
            {
                id: 'royal-pavilion',
                name: 'جناح رويال بافيليون',
                price: 10500,
                features: ['حديقة خاصة', 'إطلالة بانورامية', 'يستوعب 4'],
                size: 120
            }
        ]
    },
    fairmont: {
        name: 'Fairmont Riyadh',
        nameAr: 'فيرمونت الرياض',
        location: 'الرياض، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'superior-room',
                name: 'غرفة سوبريور كينج',
                price: 950,
                features: ['مكتب عمل', 'إطلالة على المدينة', 'يستوعب 2'],
                size: 38
            },
            {
                id: 'executive-suite',
                name: 'جناح تنفيذي بغرفة نوم واحدة',
                price: 1800,
                features: ['صالة معيشة', 'إطلالة بانورامية', 'يستوعب 3'],
                size: 65
            },
            {
                id: 'presidential-suite',
                name: 'الجناح الرئاسي',
                price: 3000,
                features: ['غرفتين نوم', 'صالة طعام خاصة', 'يستوعب 5'],
                size: 150
            }
        ]
    },
    ashar: {
        name: 'Ashar Tented Resort',
        nameAr: 'منتجع آشار الخيمي',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'deluxe-tent',
                name: 'خيمة ديلوكس',
                price: 2800,
                features: ['شرفة خاصة', 'إطلالة على الجبال', 'يستوعب 2'],
                size: 45
            },
            {
                id: 'premium-tent',
                name: 'خيمة بريميوم',
                price: 3500,
                features: ['حمام خاص فاخر', 'منطقة جلوس', 'يستوعب 2'],
                size: 55
            },
            {
                id: 'royal-tent',
                name: 'الخيمة الملكية',
                price: 5200,
                features: ['مدخل خاص', 'جاكوزي خاص', 'يستوعب 4'],
                size: 75
            }
        ]
    },
    caravan: {
        name: 'Caravan AlUla by Our Habitas',
        nameAr: 'قافلة العلا',
        location: 'العلا، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'standard-cabin',
                name: 'كابينة قياسية',
                price: 2831,
                features: ['إطلالة جبلية', 'ميني بار', 'أثاث خارجي', 'دش مطري', 'تكييف', 'واي فاي مجاني', 'يستوعب 2'],
                size: 35
            },
            {
                id: 'deluxe-cabin',
                name: 'كابينة ديلوكس',
                price: 3400,
                features: ['شرفة واسعة', 'منطقة جلوس', 'ميكروويف', 'إطلالة بانورامية', 'حمام فاخر', 'مستلزمات استحمام فاخرة', 'يستوعب 2'],
                size: 45
            },
            {
                id: 'premium-suite',
                name: 'جناح بريميوم',
                price: 4000,
                features: ['غرفة معيشة منفصلة', 'شرفة خاصة كبيرة', 'ميني بار مجاني', 'إطلالة 360 درجة', 'حمام مزدوج', 'أثاث خارجي فاخر', 'يستوعب 3'],
                size: 65
            }
        ]
    },
    mandarin: {
        name: 'Mandarin Oriental Al Faisaliah',
        nameAr: 'ماندارين أورينتال الفيصلية',
        location: 'الرياض، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'deluxe-room',
                name: 'غرفة ديلوكس',
                price: 1530,
                features: ['تلفزيون شاشة مسطحة', 'تحكم لمسي للإضاءة', 'قنوات فضائية', 'خادم شخصي 24 ساعة', 'تكييف ذكي', 'واي فاي مجاني', 'يستوعب 2'],
                size: 45
            },
            {
                id: 'executive-suite',
                name: 'جناح تنفيذي',
                price: 3000,
                features: ['صالة معيشة منفصلة', 'تفاصيل أرابيسك معمارية', 'ميني بار', 'حمام رخامي فاخر', 'شرفة خاصة', 'تكنولوجيا حديثة', 'خدمة خادم شخصي', 'يستوعب 3'],
                size: 75
            },
            {
                id: 'royal-suite',
                name: 'الجناح الملكي',
                price: 5000,
                features: ['غرفتي نوم فاخرتين', 'صالة طعام خاصة', 'مكتب رئاسي', 'حمامين فاخرين', 'شرفة بانورامية', 'تصميم سكني راقٍ', 'خدمة بتلر حصرية', 'يستوعب 5'],
                size: 150
            }
        ]
    },
    movenpick: {
        name: 'Movenpick Hotel and Residences Riyadh',
        nameAr: 'فندق وريزيدنس موفنبيك الرياض',
        location: 'الرياض، المملكة العربية السعودية',
        rating: 5,
        rooms: [
            {
                id: 'superior-room',
                name: 'غرفة سوبريور',
                price: 1300,
                features: ['إطلالة على المسبح', 'مكتب عمل', 'تلفزيون حديث', 'حمام خاص فاخر', 'واي فاي مجاني', 'يستوعب 2'],
                size: 40
            },
            {
                id: 'deluxe-suite',
                name: 'جناح ديلوكس',
                price: 2400,
                features: ['غرفة معيشة منفصلة', 'شرفة خاصة', 'إطلالة بانورامية', 'حمام رخامي', 'مطبخ صغير', 'خدمة غرف 24 ساعة', 'يستوعب 3'],
                size: 70
            },
            {
                id: 'presidential-suite',
                name: 'الجناح الرئاسي',
                price: 3500,
                features: ['غرفتي نوم فاخرتين', 'صالة طعام خاصة', 'شرفة واسعة مع إطلالة', 'حمامين فاخرين', 'مطبخ كامل', 'خدمات كونسيرج حصرية', 'يستوعب 5'],
                size: 120
            }
        ]
    }
};

// الحصول على الفندق الحالي من URL
let currentHotel = {};

// الحصول على الفندق الحالي من URL (يدعم API)
async function fetchCurrentHotel() {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel');

    // 1. التحقق من الفنادق المضافة من المستخدمين أولاً (localStorage)
    if (hotelParam && hotelParam.startsWith('hotel_')) {
        const userHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
        const userHotel = userHotels.find(h => h.id === hotelParam);
        if (userHotel) {
            return {
                name: userHotel.nameEn || userHotel.name,
                nameAr: userHotel.name,
                location: userHotel.location,
                rating: 5,
                rooms: userHotel.rooms || []
            };
        }
    }

    // 2. التحقق من الفنادق الأساسية (hardcoded)
    if (hotelsData[hotelParam]) {
        return hotelsData[hotelParam];
    }

    // 3. التحقق من الـ backend API (للأماكن الجديدة)
    if (hotelParam && hotelParam.length > 20 && typeof PlacesAPI !== 'undefined') {
        try {
            console.log('جلب بيانات الفندق من API:', hotelParam);
            const place = await PlacesAPI.getById(hotelParam);
            if (place) {
                // إنشاء غرفة افتراضية بناءً على السعر
                const defaultRoom = {
                    id: 'standard-room-' + place.id,
                    name: 'غرفة قياسية',
                    price: place.price || 500,
                    features: ['سرير مزدوج', 'إطلالة', 'تكييف', 'واي فاي مجاني', 'يستوعب 2'],
                    size: 35,
                    image: 'images/default-hotel.jpg'
                };

                return {
                    name: place.title || 'فندق غير معروف',
                    nameAr: place.title || 'فندق غير معروف',
                    location: `${place.latitude || '0'}, ${place.longitude || '0'}`,
                    rating: 5,
                    rooms: [defaultRoom]
                };
            }
        } catch (err) {
            console.error('فشل جلب الفندق من API:', err);
        }
    }

    return null; // لا يوجد fallback لـ Shebara
}

// تحميل بيانات الفندق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', async () => {
    const hotel = await fetchCurrentHotel();

    if (hotel) {
        currentHotel = hotel;
        updateHotelInfo();
        calculateAll(); // تحديث الحسابات الأولية
    } else {
        // عرض رسالة خطأ
        const container = document.querySelector('.booking-container') || document.body;
        container.innerHTML = `
            <div style="text-align: center; padding: 100px 20px;">
                <i class="fas fa-exclamation-circle fa-4x" style="color: #c62828; margin-bottom: 20px;"></i>
                <h1 style="font-family: 'Amiri', serif;">عذراً، الوجهة غير موجودة</h1>
                <p>لم نتمكن من العثور على تفاصيل الحجز لهذه الوجهة.</p>
                <a href="places.html" class="status-active" style="display: inline-block; margin-top: 20px; text-decoration: none; font-size: 1.2rem;">العودة للوجهات</a>
            </div>
        `;
    }
});

// حساب تفاصيل الحجز

// تحديث التواريخ
document.getElementById('checkInDate').addEventListener('change', calculateAll);
document.getElementById('checkOutDate').addEventListener('change', calculateAll);

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
    const currentValue = parseInt(input.value);
    const min = type === 'adults' ? 1 : 0;
    const max = type === 'adults' ? 20 : 10;
    const newValue = Math.max(min, Math.min(max, currentValue + change));
    input.value = newValue;

    // تحديث الملخص
    document.getElementById(type === 'adults' ? 'summaryAdults' : 'summaryChildren').textContent = newValue;
}

// حساب عدد الليالي
function calculateNights() {
    const checkIn = document.getElementById('checkInDate').value;
    const checkOut = document.getElementById('checkOutDate').value;

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
    const checkIn = document.getElementById('checkInDate').value;
    const checkOut = document.getElementById('checkOutDate').value;
    const nights = calculateNights();

    // تحديث عدد الليالي
    document.getElementById('nightsCount').textContent = nights;
    document.getElementById('summaryNights').textContent = nights;

    // تحديث التواريخ في الملخص
    if (checkIn) {
        const date = new Date(checkIn);
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        document.getElementById('summaryCheckIn').textContent = `${year}/${month}/${day}`;
    } else {
        document.getElementById('summaryCheckIn').textContent = '-';
    }

    if (checkOut) {
        const date = new Date(checkOut);
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        document.getElementById('summaryCheckOut').textContent = `${year}/${month}/${day}`;
    } else {
        document.getElementById('summaryCheckOut').textContent = '-';
    }
}

// حساب المجموع الكلي
function calculateAll() {
    updateDateDisplay();

    const nights = calculateNights();
    let subtotal = 0;
    const selectedRoomsList = document.getElementById('selectedRoomsList');
    selectedRoomsList.innerHTML = '';

    // حساب كل غرفة محددة
    const roomOptions = document.querySelectorAll('.room-option');
    roomOptions.forEach(room => {
        const qty = parseInt(room.querySelector('.qty-input').value);
        if (qty > 0) {
            const price = parseInt(room.getAttribute('data-price'));
            const roomName = room.getAttribute('data-name');
            const roomTotal = price * nights * qty;
            subtotal += roomTotal;

            // إضافة للقائمة
            const roomItem = document.createElement('div');
            roomItem.className = 'summary-item';
            roomItem.innerHTML = `
                <span class="summary-label">${roomName} × ${qty}</span>
                <span class="summary-value" style="direction: ltr;">${roomTotal.toLocaleString('en-US')} ر.س</span>
            `;
            selectedRoomsList.appendChild(roomItem);
        }
    });

    // حساب الضرائب (20.75%)
    const tax = Math.round(subtotal * 0.2075);
    const total = subtotal + tax;

    // تحديث الملخص
    document.getElementById('summarySubtotal').textContent = subtotal.toLocaleString('en-US') + ' ر.س';
    document.getElementById('summaryTax').textContent = tax.toLocaleString('en-US') + ' ر.س';
    document.getElementById('summaryTotal').textContent = total.toLocaleString('en-US') + ' ر.س';
}

// إتمام الحجز
function completeBooking() {
    // التحقق من تسجيل الدخول
    if (typeof isLoggedIn === 'function' && !isLoggedIn()) {
        if (typeof showNotification === 'function') {
            showNotification('يجب تسجيل الدخول أولاً', 'error');
        }
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    // التحقق من التواريخ
    const checkIn = document.getElementById('checkInDate').value;
    const checkOut = document.getElementById('checkOutDate').value;

    if (!checkIn || !checkOut) {
        if (typeof showNotification === 'function') {
            showNotification('الرجاء اختيار تواريخ الإقامة', 'error');
        }
        return;
    }

    const nights = calculateNights();
    if (nights <= 0) {
        if (typeof showNotification === 'function') {
            showNotification('تاريخ المغادرة يجب أن يكون بعد تاريخ الوصول', 'error');
        }
        return;
    }

    // التحقق من اختيار غرفة
    let hasRooms = false;
    const roomOptions = document.querySelectorAll('.room-option');
    roomOptions.forEach(room => {
        const qty = parseInt(room.querySelector('.qty-input').value);
        if (qty > 0) {
            hasRooms = true;
        }
    });

    if (!hasRooms) {
        if (typeof showNotification === 'function') {
            showNotification('الرجاء اختيار غرفة واحدة على الأقل', 'error');
        }
        return;
    }

    // جمع بيانات الحجز
    const bookingData = {
        hotelName: currentHotel.name,
        hotelNameAr: currentHotel.nameAr,
        checkIn: checkIn,
        checkOut: checkOut,
        nights: nights,
        adults: parseInt(document.getElementById('adultsCount').value),
        children: parseInt(document.getElementById('childrenCount').value),
        rooms: [],
        subtotal: 0,
        tax: 0,
        total: 0
    };

    // جمع بيانات الغرف
    roomOptions.forEach(room => {
        const qty = parseInt(room.querySelector('.qty-input').value);
        if (qty > 0) {
            const price = parseInt(room.dataset.price);
            const name = room.dataset.name;
            const roomTotal = price * nights * qty;

            bookingData.rooms.push({
                name: name,
                quantity: qty,
                pricePerNight: price,
                total: roomTotal
            });

            bookingData.subtotal += roomTotal;
        }
    });

    // حساب الضرائب والمجموع
    bookingData.tax = Math.round(bookingData.subtotal * 0.2075);
    bookingData.total = bookingData.subtotal + bookingData.tax;

    // حفظ البيانات في localStorage
    try {
        localStorage.setItem('currentBooking', JSON.stringify(bookingData));
        console.log('تم حفظ بيانات الحجز:', bookingData);
    } catch (e) {
        console.error('خطأ في حفظ البيانات:', e);
        alert('حدث خطأ في حفظ بيانات الحجز');
        return;
    }

    // إخفاء قسم الحجز وإظهار قسم الدفع
    document.getElementById('bookingSection').style.display = 'none';
    document.getElementById('paymentSection').style.display = 'block';
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
    const roomsSection = roomOptionsContainer.querySelector('.booking-section-card:nth-child(3)');

    if (roomsSection) {
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

// تعيين الحد الأدنى للتواريخ (اليوم)
document.addEventListener('DOMContentLoaded', () => {
    // تحديث معلومات الفندق في الصفحة
    updateHotelInfo();

    // تحديث اسم الفندق في الملخص
    const summaryHotelName = document.querySelector('.summary-card .summary-value');
    if (summaryHotelName) {
        summaryHotelName.textContent = currentHotel.name;
    }

    const today = new Date().toISOString().split('T')[0];
    document.getElementById('checkInDate').setAttribute('min', today);
    document.getElementById('checkOutDate').setAttribute('min', today);

    // تعيين تاريخ افتراضي (غداً لمدة 3 أيام)
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.getElementById('checkInDate').value = tomorrow.toISOString().split('T')[0];

    const checkout = new Date();
    checkout.setDate(checkout.getDate() + 4);
    document.getElementById('checkOutDate').value = checkout.toISOString().split('T')[0];

    calculateAll();
});

// ملء ملخص الطلب في قسم الدفع
function populatePaymentSummary(bookingData) {
    const summaryDiv = document.getElementById('paymentSummary');
    if (!summaryDiv) {
        console.error('لم يتم العثور على عنصر paymentSummary');
        return;
    }

    console.log('ملء ملخص الطلب:', bookingData);

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
    bookingData.rooms.forEach(room => {
        const roomQty = room.quantity || room.count || 1;
        const roomPrice = room.total || room.totalPrice || 0;
        html += `
            <div class="summary-row">
                <span>${room.name} × ${roomQty}</span>
                <span>${roomPrice.toLocaleString('en-US')} ريال</span>
            </div>
        `;
    });

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

    console.log('تم ملء ملخص الطلب بنجاح');
}

// العودة لصفحة الحجز
function backToBooking() {
    document.getElementById('paymentSection').style.display = 'none';
    document.getElementById('bookingSection').style.display = 'block';
    window.scrollTo(0, 0);
}

// معالجة الدفع
async function processPayment(event) {
    event.preventDefault();

    // التحقق من تسجيل الدخول
    if (!isLoggedIn()) {
        alert('يجب تسجيل الدخول أولاً');
        window.location.href = 'login.html';
        return;
    }

    // التحقق من طريقة الدفع المختارة
    const selectedMethod = document.querySelector('.payment-method.active');
    const isApplePay = selectedMethod && selectedMethod.querySelector('span').textContent === 'Apple Pay';

    let paymentMethod = 'بطاقة ائتمان';
    let cardLastFour = '';

    if (isApplePay) {
        paymentMethod = 'Apple Pay';
        cardLastFour = '****';
        alert('جاري معالجة الدفع عبر Apple Pay...');
    } else {
        const cardName = document.getElementById('cardName').value.trim();
        const cardNumber = document.getElementById('cardNumber').value.replace(/\s/g, '');
        const expiryDate = document.getElementById('expiryDate').value;
        const cvv = document.getElementById('cvv').value;

        if (!cardName) { alert('الرجاء إدخال اسم حامل البطاقة'); return; }
        if (cardNumber.length !== 16 || !/^\d+$/.test(cardNumber)) { alert('الرجاء إدخال رقم بطاقة صحيح (16 رقم)'); return; }
        if (!/^\d{2}\/\d{2}$/.test(expiryDate)) { alert('الرجاء إدخال تاريخ انتهاء صحيح (MM/YY)'); return; }
        if (cvv.length !== 3 || !/^\d+$/.test(cvv)) { alert('الرجاء إدخال رمز CVV صحيح (3 أرقام)'); return; }

        cardLastFour = cardNumber.slice(-4);
        if (selectedMethod && selectedMethod.querySelector('span').textContent === 'مدى') {
            paymentMethod = 'مدى';
        }
    }

    // الحصول على بيانات الحجز
    const bookingData = JSON.parse(localStorage.getItem('currentBooking'));
    if (!bookingData) {
        alert('حدث خطأ في استرجاع بيانات الحجز');
        return;
    }

    // إضافة معلومات الدفع
    bookingData.paymentMethod = paymentMethod;
    bookingData.cardLastFour = cardLastFour;
    bookingData.paymentDate = new Date().toISOString();
    bookingData.bookingId = 'BK' + Date.now();
    bookingData.status = 'confirmed';

    // حفظ في localStorage
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
    const userId = localStorage.getItem('userId');
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel') || '';

    if (userId && typeof BookingsAPI !== 'undefined') {
        try {
            await BookingsAPI.create({
                guest_id: userId,
                place_id: hotelParam,
                check_in: bookingData.checkIn,
                check_out: bookingData.checkOut,
                status: 'confirmed'
            });
            console.log('تم حفظ الحجز في الـ backend');
        } catch (err) {
            console.warn('تعذر حفظ الحجز في الـ backend:', err);
        }
    }

    // حذف الحجز المؤقت
    localStorage.removeItem('currentBooking');

    // عرض رسالة النجاح
    alert(`✓ تم تأكيد حجزك بنجاح!\nرقم الحجز: ${bookingData.bookingId}\n\nسيتم إرسال تفاصيل الحجز على بريدك الإلكتروني`);

    // الانتقال للصفحة الرئيسية
    window.location.href = 'index.html';
}

// تنسيق رقم البطاقة (إضافة مسافات كل 4 أرقام)
function formatCardNumber(input) {
    let value = input.value.replace(/\s/g, '').replace(/\D/g, '');
    let formatted = value.match(/.{1,4}/g);
    input.value = formatted ? formatted.join(' ') : value;
}

// تنسيق تاريخ الانتهاء (MM/YY)
function formatExpiryDate(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 2) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
    }
    input.value = value;
}

// التحقق من الأرقام فقط لـ CVV
function validateCVV(input) {
    input.value = input.value.replace(/\D/g, '').slice(0, 3);
}

// اختيار طريقة الدفع
function selectPaymentMethod(method) {
    document.querySelectorAll('.payment-method').forEach(el => {
        el.classList.remove('active');
    });
    event.target.closest('.payment-method').classList.add('active');

    const cardFields = document.getElementById('cardFields');
    const applePayMessage = document.getElementById('applePayMessage');
    const payBtnText = document.getElementById('payBtnText');
    const payBtnIcon = document.getElementById('payBtnIcon');
    const cardInputs = cardFields.querySelectorAll('input');

    if (method === 'applepay') {
        // إخفاء حقول البطاقة وإظهار رسالة Apple Pay
        cardFields.style.display = 'none';
        applePayMessage.style.display = 'block';

        // تغيير نص الزر
        payBtnText.textContent = 'ادفع بـ Apple Pay';
        payBtnIcon.className = 'fab fa-apple-pay';

        // إزالة required من حقول البطاقة
        cardInputs.forEach(input => input.removeAttribute('required'));
    } else {
        // إظهار حقول البطاقة وإخفاء رسالة Apple Pay
        cardFields.style.display = 'block';
        applePayMessage.style.display = 'none';

        // إرجاع نص الزر
        if (method === 'mada') {
            payBtnText.textContent = 'تأكيد الدفع بمدى';
            payBtnIcon.className = 'fas fa-money-check';
        } else {
            payBtnText.textContent = 'تأكيد الدفع';
            payBtnIcon.className = 'fas fa-lock';
        }

        // إضافة required لحقول البطاقة
        cardInputs.forEach(input => input.setAttribute('required', 'required'));
    }
}
