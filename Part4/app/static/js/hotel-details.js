/**
 * ملف: hotel-details.js
 * الوصف: إدارة عرض تفاصيل الفندق، السعر، المرافق، والتقييمات.
 */

// دالة مساعدة لجلب التوكن (ضرورية لنشر التقييم)
function getAuthToken() {
    return document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
}

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelId = urlParams.get('id');

    if (!hotelId) {
        window.location.href = '/places';
        return;
    }

    // استدعاء جميع الدالات
    fetchHotelDetails(hotelId);
    fetchHotelAmenities(hotelId);
    fetchHotelReviews(hotelId);
    setupReviewForm(hotelId);
});

// ==================== 1. جلب تفاصيل الفندق والسعر ====================
async function fetchHotelDetails(id) {
    try {
        const response = await fetch(`/api/v1/places/${id}`);
        const place = await response.json();

        // عرض البيانات الأساسية
        document.querySelector('.hotel-name').textContent = place.title;
        document.querySelector('.hotel-location').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${place.latitude}, ${place.longitude}`;
        
        const descDiv = document.getElementById('hotelFullDescription');
        if (descDiv) descDiv.textContent = place.description || "لا يوجد وصف.";

        // 🔥 إصلاح السعر 🔥
        // نحاول العثور على العنصر بالـ ID أو الكلاس
        const priceElement = document.getElementById('hotelPrice') || document.querySelector('.hotel-price');
        if (priceElement) {
            priceElement.textContent = place.price; // وضع السعر
        }
        const bookingName = document.querySelector('.booking-hotel-name');
        const bookingPrice = document.querySelector('.booking-price');
        
        if (bookingName) bookingName.textContent = place.title;
        if (bookingPrice) bookingPrice.textContent = `${place.price} ر.س / ليلة`;
        // منطق المالك (إخفاء زر التقييم إذا كان المستخدم هو المالك)
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const currentUserId = currentUser ? currentUser.id : null;
        const placeOwnerId = place.owner_id || place.user_id;
        const reviewSection = document.querySelector('.add-review-section');

        if (currentUserId && String(currentUserId).trim() === String(placeOwnerId).trim()) {
            if (reviewSection) {
                reviewSection.style.display = 'none';
                if (!document.querySelector('.owner-msg')) {
                    const msg = document.createElement('p');
                    msg.className = 'owner-msg';
                    msg.style.cssText = "color: #815B2F; background: #fdf5e6; padding: 15px; border-radius: 8px; font-weight: bold; margin-top: 15px;";
                    msg.innerHTML = '<i class="fas fa-info-circle"></i> أنت صاحب هذا العقار.';
                    reviewSection.parentNode.insertBefore(msg, reviewSection);
                }
            }
        }

    } catch (error) {
        console.error('Error fetching details:', error);
    }
}

// ==================== 2. جلب المرافق (مع حل مشكلة الأيقونات) ====================
async function fetchHotelAmenities(placeId) {
    const grid = document.getElementById('amenitiesGrid');
    if (!grid) return;

    try {
        const response = await fetch(`/api/v1/places/${placeId}/amenities`);
        
        // التحقق من الاستجابة قبل التحويل لـ JSON
        let amenities = [];
        if (response.ok) {
            amenities = await response.json();
        }

        grid.innerHTML = '';

        if (!amenities || amenities.length === 0) {
            // عرض رسالة بدلاً من إخفاء القسم بالكامل ليعرف المستخدم أن الكود يعمل
            grid.innerHTML = '<p class="text-muted" style="grid-column: 1/-1;">لا توجد مرافق مسجلة لهذا العقار.</p>';
            return;
        }

        amenities.forEach(amenity => {
            const item = document.createElement('div');
            item.className = 'amenity-item';
            
            // استخدام أيقونة افتراضية إذا كانت الأيقونة غير موجودة أو فارغة
            // ندعم amenity.icon أو amenity.name للأيقونات
            const iconClass = amenity.icon ? amenity.icon : 'fas fa-check-circle';
            const amenityName = amenity.name || amenity.amenity_name || 'مرفق';

            item.innerHTML = `
                <i class="${iconClass}"></i>
                <span>${amenityName}</span>`;
            grid.appendChild(item);
        });
    } catch (error) {
        console.error('Amenities Error:', error);
    }
}

// ==================== 3. جلب التقييمات (مع الفلترة) ====================
async function fetchHotelReviews(placeId) {
    const reviewsList = document.getElementById('reviewsList');
    
    try {
        // نطلب كل المراجعات
        const response = await fetch('/api/v1/reviews/');

        if (!response.ok) {
            if (reviewsList) reviewsList.innerHTML = '<p class="text-muted">تعذر تحميل التقييمات.</p>';
            return;
        }

        const allReviews = await response.json();

        // فلترة المراجعات الخاصة بهذا الفندق فقط
        const placeReviews = allReviews.filter(review => review.place_id === placeId);

        if (reviewsList) {
            reviewsList.innerHTML = '';

            if (placeReviews.length === 0) {
                reviewsList.innerHTML = '<div class="alert alert-info">لا توجد تقييمات بعد. كن أول من يقيّم! ⭐</div>';
                return;
            }

            // ترتيب الأحدث أولاً
            placeReviews.reverse();

            placeReviews.forEach(review => {
                const userName = review.user_name || "نزيل";
                
                let starsHtml = '';
                for (let i = 1; i <= 5; i++) {
                    starsHtml += i <= review.rating 
                        ? '<i class="fas fa-star text-warning"></i>' 
                        : '<i class="far fa-star text-secondary"></i>';
                }

                const reviewCard = document.createElement('div');
                reviewCard.className = 'review-card mb-3 p-3 border rounded';
                reviewCard.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center mb-2">
                        <h6 class="mb-0 fw-bold">${userName}</h6>
                        <div class="stars">${starsHtml}</div>
                    </div>
                    <p class="mb-0 text-muted">${review.comment}</p>
                `;
                reviewsList.appendChild(reviewCard);
            });
        }
    } catch (error) {
        console.error("Error fetching reviews:", error);
        if (reviewsList) reviewsList.innerHTML = '<p>حدث خطأ في الاتصال.</p>';
    }
}

// ==================== 4. إعداد نموذج التقييم ====================
function setupReviewForm(id) {
    const form = document.getElementById('reviewForm');
    const stars = document.querySelectorAll('.star-rating i');
    const ratingInput = document.getElementById('selectedRating');

    // تفاعل النجوم
    stars.forEach(star => {
        star.style.cursor = 'pointer';
        star.addEventListener('click', function() {
            const val = parseInt(this.getAttribute('data-rating'));
            if (ratingInput) ratingInput.value = val;
            
            stars.forEach(s => {
                const r = parseInt(s.getAttribute('data-rating'));
                if (r <= val) {
                    s.classList.remove('far'); s.classList.add('fas'); s.style.color = '#FFD700';
                } else {
                    s.classList.remove('fas'); s.classList.add('far'); s.style.color = '#ccc';
                }
            });
        });
    });

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const token = getAuthToken(); 
            if (!token) return alert('يرجى تسجيل الدخول');

            const reviewText = document.getElementById('reviewText').value;
            const ratingValue = parseInt(ratingInput.value);

            if (!reviewText || !ratingValue) {
                return alert('يرجى كتابة تعليق واختيار تقييم');
            }

            const payload = {
                place_id: id,
                rating: ratingValue,
                comment: reviewText
            };

            try {
                const response = await fetch('/api/v1/reviews/', { 
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}` 
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    alert('تم النشر بنجاح! 🎉');
                    window.location.reload();
                } else {
                    const err = await response.json();
                    alert('فشل النشر: ' + (err.message || 'خطأ في البيانات'));
                }
            } catch (error) {
                console.error(error);
                alert('خطأ في الاتصال بالسيرفر');
            }
        });
    }
}