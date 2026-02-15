/**
 * ملف: hotel-details.js
 * الوصف: إدارة صفحة تفاصيل الفنادق
 * الوظائف: عرض تفاصيل الفندق، المراجعات، السلايدر، دعم الفنادق المضافة من المستخدمين
 */

// ==================== مصفوفة أيقونات المرافق ====================
const amenityIcons = {
    // English Keys
    "Wifi": "fas fa-wifi",
    "WiFi": "fas fa-wifi",
    "Pool": "fas fa-swimming-pool",
    "Air conditioning": "fas fa-wind",
    "Kitchen": "fas fa-utensils",
    "Parking": "fas fa-parking",
    "Gym": "fas fa-dumbbell",
    "Breakfast": "fas fa-coffee",
    "Spa": "fas fa-spa",
    "Pet friendly": "fas fa-paw",
    "Heating": "fas fa-fire",
    "TV": "fas fa-tv",
    "Iron": "fas fa-tshirt",
    "Hair dryer": "fas fa-wind",
    "Linen": "fas fa-bed",
    "Towels": "fas fa-bath",

    // Arabic Keys (matching admin.js labels)
    "واي فاي": "fas fa-wifi",
    "موقف سيارات": "fas fa-parking",
    "مسبح": "fas fa-swimming-pool",
    "صالة رياضة": "fas fa-dumbbell",
    "مطعم": "fas fa-utensils",
    "سبا": "fas fa-spa",
    "تكييف": "fas fa-wind",
    "تلفاز": "fas fa-tv",
    "غسيل ملابس": "fas fa-tshirt",
    "بار": "fas fa-cocktail",
    "إفطار": "fas fa-coffee",
    "نقل للمطار": "fas fa-shuttle-van",
    "حيوانات أليفة": "fas fa-paw",
    "خدمة غرف": "fas fa-concierge-bell",
    "مركز أعمال": "fas fa-briefcase",
    "دخول للكراسي المتحركة": "fas fa-wheelchair",

    "default": "fas fa-check-circle"
};

// جلب بيانات الفندق من الـ backend
async function fetchPlaceFromBackend(placeId) {
    try {
        const data = await PlacesAPI.getById(placeId);
        if (data && data.id) {

            // تحويل المرافق لإضافة الأيقونات
            const amenitiesWithIcons = (data.amenities || []).map(amenity => ({
                text: amenity.amenity_name || amenity.name, // Handle different field names
                // Use icon from backend if available, otherwise fallback to map
                icon: amenity.icon || amenityIcons[amenity.amenity_name] || amenityIcons[amenity.name] || amenityIcons['default']
            }));

            // معالجة الصور
            let images = [];
            if (Array.isArray(data.images) && data.images.length > 0) {
                images = data.images;
            } else {
                images = ['images/hotel1.jpg']; // صورة افتراضية
            }

            return {
                id: data.id,
                name: data.title || 'مكان',
                nameAr: data.title || '',
                location: data.location || `${data.latitude || ''}, ${data.longitude || ''}`,
                rating: 5, // افتراضي
                startPrice: data.price || 0,
                images: images,
                tagline: data.description ? data.description.substring(0, 100) + '...' : '',
                description: data.description || '',
                amenities: amenitiesWithIcons,
                reviews: data.reviews || [],
                owner: data.owner,
                status: data.status
            };
        }
    } catch (err) {
        console.warn('تعذر جلب المكان من الـ backend:', err);
    }
    return null;
}

// تحديث معلومات الصفحة
function updatePageContent(hotel) {
    if (!hotel) return;

    // تحديث العنوان
    document.title = `${hotel.name} - نُزل`;

    // تحديث اسم الفندق
    const hotelNameElement = document.querySelector('.hotel-name');
    if (hotelNameElement) hotelNameElement.textContent = hotel.name;

    // تحديث الموقع
    const hotelLocationElement = document.querySelector('.hotel-location span');
    if (hotelLocationElement) hotelLocationElement.textContent = `الموقع: ${hotel.location}`;

    // تحديث السعر
    const priceAmountElement = document.querySelector('.price-amount');
    if (priceAmountElement) priceAmountElement.textContent = `${hotel.startPrice.toLocaleString('en-US')} ر.س`;

    // تحديث tagline
    const taglineElement = document.querySelector('.hotel-tagline p');
    if (taglineElement) taglineElement.textContent = hotel.tagline;

    // تحديث قسم "عن الثمان" (الوصف)
    const descriptionElement = document.querySelector('.hotel-description');
    if (descriptionElement) {
        descriptionElement.innerHTML = `
            <h2 class="section-title">عن المكان</h2>
            <p>${hotel.description}</p>
        `;
    }

    // تحديث المرافق
    const amenitiesSection = document.querySelector('.hotel-amenities');
    const amenitiesGrid = document.querySelector('.amenities-grid');

    if (amenitiesSection && amenitiesGrid) {
        if (hotel.amenities && hotel.amenities.length > 0) {
            amenitiesSection.style.display = 'block';
            let amenitiesHTML = '';
            hotel.amenities.forEach(amenity => {
                amenitiesHTML += `
                    <div class="amenity-item">
                        <i class="${amenity.icon}"></i>
                        <span>${amenity.text}</span>
                    </div>
                `;
            });
            amenitiesGrid.innerHTML = amenitiesHTML;
        } else {
            // إخفاء القسم بالكامل إذا لم توجد مرافق
            amenitiesSection.style.display = 'none';
        }
    }

    // تحديث الصور في السلايدر
    const sliderWrapper = document.querySelector('.slider-wrapper');
    if (sliderWrapper) {
        let slidesHTML = '';
        let dotsHTML = '';

        hotel.images.forEach((img, index) => {
            slidesHTML += `<div class="hotel-slide ${index === 0 ? 'active' : ''}"><img src="${img}" alt="${hotel.name} ${index + 1}" onerror="this.src='images/hotel1.jpg'"></div>`;
            dotsHTML += `<span class="dot ${index === 0 ? 'active' : ''}" onclick="goToSlide(${index})"></span>`;
        });

        sliderWrapper.innerHTML = `
            ${slidesHTML}
            <button class="slider-arrow prev" onclick="changeSlide(-1)">
                <i class="fas fa-chevron-right"></i>
            </button>
            <button class="slider-arrow next" onclick="changeSlide(1)">
                <i class="fas fa-chevron-left"></i>
            </button>
            <div class="slider-dots">${dotsHTML}</div>
        `;
    }

    // تحديث الشريط الثابت للحجز
    const bookingBarName = document.querySelector('.booking-hotel-name');
    const bookingBarPrice = document.querySelector('.booking-price');
    const bookingBtn = document.querySelector('.booking-btn');

    if (bookingBarName) bookingBarName.textContent = hotel.name;
    if (bookingBarPrice) bookingBarPrice.textContent = `يبدأ من ${hotel.startPrice.toLocaleString('ar-EG')} ر.س / ليلة`;

    if (bookingBtn) {
        bookingBtn.setAttribute('onclick', `handleBooking()`);
    }

    // تحديث رابط الحجز القديم (إن وجد)
    const bookButton = document.querySelector('.book-button');
    if (bookButton) {
        const hotelParam = new URLSearchParams(window.location.search).get('hotel');
        bookButton.setAttribute('onclick', `window.location.href='reservation.html?hotel=${hotelParam}'`);
    }

    // إخفاء قسم "الغرف" كلياً لأنه غير مدعوم في الـ backend حالياً
    const roomsSection = document.querySelector('.hotel-rooms');
    if (roomsSection) {
        roomsSection.style.display = 'none';
    }

    // إخفاء مفصل لقسم الموقع لأنه hardcoded
    const locationSection = document.getElementById('locationSection');
    if (locationSection) {
        locationSection.style.display = 'none';
    }

    // تحديث إحصائيات التقييم (Dynamic)
    const avgElement = document.getElementById('averageRating');
    const countElement = document.getElementById('reviewsCount');
    const ratingStarsContainer = document.querySelector('.rating-score .rating-stars');
    const ratingLabel = document.querySelector('.rating-score .rating-label');

    if (hotel.reviews && hotel.reviews.length > 0) {
        const totalRating = hotel.reviews.reduce((acc, r) => acc + (r.rating || 0), 0);
        const avgRating = (totalRating / hotel.reviews.length).toFixed(1);

        if (avgElement) avgElement.textContent = avgRating;
        if (countElement) countElement.textContent = `${hotel.reviews.length} تقييمات`;

        // Update Stars
        if (ratingStarsContainer) {
            let starsHTML = '';
            for (let i = 1; i <= 5; i++) {
                if (i <= Math.round(avgRating)) {
                    starsHTML += '<i class="fas fa-star"></i>';
                } else {
                    starsHTML += '<i class="far fa-star"></i>';
                }
            }
            ratingStarsContainer.innerHTML = starsHTML;
        }

        // Update Label
        if (ratingLabel) {
            let label = '';
            if (avgRating >= 4.5) label = 'ممتاز';
            else if (avgRating >= 3.5) label = 'جيد جداً';
            else if (avgRating >= 2.5) label = 'جيد';
            else if (avgRating >= 1.5) label = 'مقبول';
            else label = 'ضعيف';
            ratingLabel.textContent = label;
        }

    } else {
        if (avgElement) avgElement.textContent = '-';
        if (countElement) countElement.textContent = '0 تقييمات';

        if (ratingStarsContainer) {
            ratingStarsContainer.innerHTML = `
                <i class="far fa-star"></i>
                <i class="far fa-star"></i>
                <i class="far fa-star"></i>
                <i class="far fa-star"></i>
                <i class="far fa-star"></i>
             `;
        }
        if (ratingLabel) ratingLabel.textContent = '';
    }
}

// عرض المراجعات
// دالة لتأمين النصوص من XSS
function escapeHtml(text) {
    if (!text) return '';
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// عرض المراجعات
async function displayReviews(hotel) {
    const reviewsContainer = document.getElementById('reviewsList');
    if (!reviewsContainer) return;

    // استخدام المراجعات من الـ backend
    const reviews = hotel.reviews || [];

    if (reviews.length === 0) {
        reviewsContainer.innerHTML = '<p class="no-reviews">لا توجد تقييمات بعد لهذا المكان.</p>';
        return;
    }

    let reviewsHTML = '';
    reviews.forEach(review => {
        // افتراض أن التقييم نجمي
        let stars = '';
        const rating = review.rating || 5;
        for (let i = 0; i < 5; i++) {
            if (i < rating) stars += '<i class="fas fa-star"></i>';
            else stars += '<i class="far fa-star"></i>';
        }

        reviewsHTML += `
            <div class="review-card">
                <div class="review-header">
                    <span class="reviewer-name">${review.user ? escapeHtml(`${review.user.first_name} ${review.user.last_name}`.trim()) : 'مستخدم'}</span>
                    <span class="review-date">${new Date(review.created_at || Date.now()).toLocaleDateString('ar-EG')}</span>
                </div>
                <div class="review-rating">${stars}</div>
                <p class="review-text">${escapeHtml(review.comment)}</p>
            </div>
        `;
    });

    reviewsContainer.innerHTML = reviewsHTML;
}

// تحديد التقييم (النجوم)
function setRating(rating) {
    const ratingInput = document.getElementById('selectedRating');
    if (ratingInput) ratingInput.value = rating;

    const stars = document.querySelectorAll('.star-rating i');
    stars.forEach(star => {
        const starRating = parseInt(star.getAttribute('data-rating'));
        if (starRating <= rating) {
            star.classList.remove('far');
            star.classList.add('fas');
        } else {
            star.classList.remove('fas');
            star.classList.add('far');
        }
    });
}

// إرسال المراجعة
async function submitReview(event) {
    event.preventDefault();

    // التحقق من تسجيل الدخول
    if (typeof isLoggedIn === 'function' && !isLoggedIn()) {
        alert('يجب تسجيل الدخول لإضافة تقييم');
        window.location.href = 'login.html';
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('hotel');
    const ratingElement = document.getElementById('selectedRating');
    const commentElement = document.getElementById('reviewText');

    const rating = ratingElement ? ratingElement.value : 0;
    const comment = commentElement ? commentElement.value : '';

    if (rating == 0) {
        alert('الرجاء اختيار التقييم (عدد النجوم)');
        return;
    }

    try {
        const reviewData = {
            place_id: placeId,
            rating: parseInt(rating),
            comment: comment
        };

        await ReviewsAPI.create(reviewData);
        alert('تم إضافة تقييمك بنجاح');

        // تحديث البيانات
        const hotel = await fetchPlaceFromBackend(placeId);
        if (hotel) {
            displayReviews(hotel);
            updatePageContent(hotel);
        }

        // إعادة تعيين النموذج
        document.getElementById('reviewForm').reset();
        setRating(0);

    } catch (error) {
        console.error('Error submitting review:', error);
        alert('حدث خطأ أثناء إضافة التقييم: ' + error.message);
    }
}


// سلايدر صور الفندق
let currentSlide = 0;
let slideInterval;

function startSlider() {
    slideInterval = setInterval(() => {
        changeSlide(1);
    }, 3000);
}

function stopSlider() {
    clearInterval(slideInterval);
}

function changeSlide(direction) {
    const slides = document.querySelectorAll('.hotel-slide');
    const dots = document.querySelectorAll('.dot');

    if (slides.length === 0) return;

    slides[currentSlide].classList.remove('active');
    if (dots[currentSlide]) dots[currentSlide].classList.remove('active');

    currentSlide = currentSlide + direction;

    if (currentSlide >= slides.length) {
        currentSlide = 0;
    } else if (currentSlide < 0) {
        currentSlide = slides.length - 1;
    }

    slides[currentSlide].classList.add('active');
    if (dots[currentSlide]) dots[currentSlide].classList.add('active');
}

function goToSlide(slideIndex) {
    const slides = document.querySelectorAll('.hotel-slide');
    const dots = document.querySelectorAll('.dot');

    if (slides.length === 0) return;

    slides[currentSlide].classList.remove('active');
    if (dots[currentSlide]) dots[currentSlide].classList.remove('active');

    currentSlide = slideIndex;

    slides[currentSlide].classList.add('active');
    if (dots[currentSlide]) dots[currentSlide].classList.add('active');

    stopSlider();
    startSlider();
}

// معالجة الحجز
function handleBooking() {
    // التحقق من تسجيل الدخول
    if (typeof isLoggedIn === 'function' && !isLoggedIn()) {
        if (typeof showNotification === 'function') {
            showNotification('يجب تسجيل الدخول أولاً للحجز', 'error');
        } else {
            alert('يجب تسجيل الدخول أولاً للحجز');
        }
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel');

    if (typeof showLoadingScreen === 'function') {
        showLoadingScreen(`reservation.html?hotel=${hotelParam}`);
    } else {
        window.location.href = `reservation.html?hotel=${hotelParam}`;
    }
}

// Initialization
document.addEventListener('DOMContentLoaded', async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelParam = urlParams.get('hotel');

    if (!hotelParam) {
        // عرض رسالة خطأ
        displayError();
        return;
    }

    // إظهار تحميل
    const mainContent = document.querySelector('main');
    // يمكن إضافة spinner هنا

    const hotel = await fetchPlaceFromBackend(hotelParam);

    if (hotel) {
        updatePageContent(hotel);
        displayReviews(hotel);

        // إعداد السلايدر
        const sliderWrapper = document.querySelector('.slider-wrapper');
        if (sliderWrapper) {
            sliderWrapper.addEventListener('mouseenter', stopSlider);
            sliderWrapper.addEventListener('mouseleave', startSlider);
            startSlider();
        }
    } else {
        displayError();
    }
});

function displayError() {
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.innerHTML = `
            <div class="places-error" style="height: 50vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
                <i class="fas fa-exclamation-circle fa-4x" style="color: #c62828; margin-bottom: 20px;"></i>
                <h2 style="font-family: 'Amiri', serif; margin-bottom: 10px;">عذراً، الوجهة غير موجودة</h2>
                <p style="margin-bottom: 20px;">لم نتمكن من العثور على تفاصيل هذه الوجهة.</p>
                <a href="places.html" class="card-btn" style="text-decoration: none; display: inline-block; width: auto;">العودة للوجهات</a>
            </div>
        `;
    }
}

// إيقاف السلايدر عند مغادرة الصفحة
window.addEventListener('beforeunload', stopSlider);
