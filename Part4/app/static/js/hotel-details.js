/**
 * ملف: hotel-details.js
 * الوصف: نسخة نهائية موحدة لجلب البيانات، التقييمات، والمرافق ديناميكياً.
 */

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const hotelId = urlParams.get('id');

    if (!hotelId) {
        window.location.href = '/places';
        return;
    }

    // استدعاء جميع الدالات عند تحميل الصفحة
    fetchHotelDetails(hotelId);
    fetchHotelAmenities(hotelId);
    fetchHotelReviews(hotelId);
    setupReviewForm(hotelId);
});

// ==================== 1. جلب بيانات الفندق (نسخة مدمجة) ====================
async function fetchHotelDetails(id) {
    try {
        const response = await fetch(`/api/v1/places/${id}`);
        const place = await response.json();

        // 1. استخراج معرف المالك (مع دعم الاسمين لتجنب الأخطاء)
        // إذا كان الباك اند يرسل owner_id نستخدمه، وإلا نستخدم user_id
        const placeOwnerId = place.owner_id || place.user_id;

        // 2. استخراج معرف المستخدم الحالي
        const currentUser = JSON.parse(localStorage.getItem('currentUser'));
        const currentUserId = currentUser ? currentUser.id : null;

        console.log("🔍 تصحيح المعرفات:");
        console.log("👤 المستخدم الحالي:", currentUserId);
        console.log("🏠 صاحب الفندق:", placeOwnerId);

        // 3. منطق إظهار/إخفاء الفورم
        const reviewSection = document.querySelector('.add-review-section');
        
        if (!currentUserId) {
            // الحالة 1: غير مسجل دخول -> إخفاء
            if (reviewSection) reviewSection.style.display = 'none';
        } 
        // مقارنة القيم كنصوص لضمان الدقة
        else if (String(currentUserId).trim() === String(placeOwnerId).trim()) {
            // الحالة 2: المستخدم هو المالك -> إخفاء + رسالة
            if (reviewSection) {
                reviewSection.style.display = 'none';
                // التأكد من عدم تكرار الرسالة
                if (!document.querySelector('.owner-msg')) {
                    const msg = document.createElement('p');
                    msg.className = 'owner-msg';
                    msg.style.cssText = "color: #815B2F; background: #fdf5e6; padding: 15px; border-radius: 8px; margin-top: 15px; font-weight: bold;";
                    msg.innerHTML = '<i class="fas fa-info-circle"></i> أنت صاحب هذا العقار؛ التقييمات متاحة للنزلاء فقط.';
                    reviewSection.parentNode.insertBefore(msg, reviewSection);
                }
            }
        } 
        else {
            // الحالة 3: مستخدم عادي (ليس المالك) -> إظهار الفورم
            if (reviewSection) reviewSection.style.display = 'block';
        }

        // تحديث باقي البيانات في الصفحة
        document.querySelector('.hotel-name').textContent = place.title;
        document.querySelector('.hotel-location').innerHTML = `<i class="fas fa-map-marker-alt"></i> ${place.latitude}, ${place.longitude}`;
        const descDiv = document.getElementById('hotelFullDescription');
        if (descDiv) descDiv.textContent = place.description || "لا يوجد وصف.";

    } catch (error) {
        console.error('Error fetching details:', error);
    }
}

// ==================== 2. جلب المرافق (Dynamic) ====================
async function fetchHotelAmenities(placeId) {
    const grid = document.getElementById('amenitiesGrid');
    if (!grid) return;

    try {
        const response = await fetch(`/api/v1/places/${placeId}/amenities`);
        const amenities = await response.json();

        grid.innerHTML = '';

        if (!amenities || amenities.length === 0) {
            const section = document.querySelector('.hotel-amenities');
            if (section) section.style.display = 'none';
            return;
        }

        amenities.forEach(amenity => {
            const item = document.createElement('div');
            item.className = 'amenity-item';
            item.innerHTML = `
                <i class="${amenity.icon || 'fas fa-check'}"></i>
                <span>${amenity.name || amenity.amenity_name}</span>`;
            grid.appendChild(item);
        });
    } catch (error) {
        console.error('Amenities Error:', error);
    }
}

// ==================== 3. التقييمات والتعليقات ====================
async function fetchHotelReviews(id) {
    const reviewsList = document.getElementById('reviewsList');
    try {
        const response = await fetch(`/api/v1/reviews/places/${id}`);
        // إذا لم يجد تقييمات (404) أو حدث خطأ، توقف بهدوء
        if (!response.ok) {
            if (reviewsList) reviewsList.innerHTML = '<p>لا توجد تقييمات حالياً.</p>';
            return;
        }
        const reviews = await response.json();
        // ... كود عرض التقييمات
    } catch (error) {
        console.log("No reviews found or API error.");
    }
}

// ==================== 4. إعداد نموذج التقييم ====================
function setupReviewForm(id) {
    const form = document.getElementById('reviewForm');
    const stars = document.querySelectorAll('.star-rating i');
    let selectedRating = 0;

    stars.forEach(star => {
        star.addEventListener('click', () => {
            selectedRating = star.getAttribute('data-rating');
            document.getElementById('selectedRating').value = selectedRating;
            stars.forEach(s => {
                const r = s.getAttribute('data-rating');
                s.classList.toggle('fas', r <= selectedRating);
                s.classList.toggle('far', r > selectedRating);
            });
        });
    });

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];

            if (!token) return alert('يرجى تسجيل الدخول');

            try {
                const response = await fetch(`/api/v1/reviews/places/${id}`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({ rating: parseInt(selectedRating), comment: document.getElementById('reviewText').value })
                });

                if (response.ok) {
                    alert('تم النشر بنجاح!');
                    window.location.reload();
                }
            } catch (error) {
                alert('خطأ في الاتصال');
            }
        });
    }
}