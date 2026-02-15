/**
 * ملف: admin.js
 * الوصف: إدارة الفنادق عبر API وربطها بقاعدة البيانات مباشرة.
 */

// الحصول على التوكن من الكوكيز
function getAuthToken() {
    return document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
}

// ==================== 1. عرض الفنادق (من قاعدة البيانات) ====================

async function displayUserHotels() {
    console.log("جاري جلب الفنادق من السيرفر...");
    
    const container = document.getElementById('userHotelsList');
    if (!container) return; // الخروج إذا لم تكن القائمة موجودة في الصفحة

    // 1. التحقق من هوية المستخدم
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser || !currentUser.id) {
        container.innerHTML = '<p class="empty-message">يرجى تسجيل الدخول لعرض عقاراتك.</p>';
        return;
    }

    try {
        // 2. طلب البيانات من الـ API
        const response = await fetch('/api/v1/places/');
        if (!response.ok) throw new Error('فشل الاتصال بالسيرفر');
        
        const allPlaces = await response.json();

        // 3. الفلترة: عرض ما يملكه المستخدم الحالي فقط
        const myPlaces = allPlaces.filter(place => {
            // دعم التسميتين المحتملتين من الباك إند
            const placeOwner = place.owner_id || place.user_id;
            // مقارنة آمنة (String vs String)
            return String(placeOwner).trim() === String(currentUser.id).trim();
        });

        console.log(`تم العثور على ${myPlaces.length} فندق للمستخدم الحالي.`);

        if (myPlaces.length === 0) {
            container.innerHTML = '<p class="empty-message">لم تقم بإضافة أي فنادق حتى الآن.</p>';
            return;
        }

        // 4. رسم الكروت
        container.innerHTML = '';
        myPlaces.forEach(place => {
            // صورة افتراضية إذا لم توجد صور
            const placeImg = (place.images && place.images.length > 0) ? place.images[0] : '/static/images/default-hotel.jpg';

            const card = document.createElement('div');
            card.className = 'user-hotel-card';
            card.innerHTML = `
                <img src="${placeImg}" alt="${place.title}" class="user-hotel-image" onerror="this.src='/static/images/logo.png'">
                <div class="user-hotel-info">
                    <h3 class="user-hotel-name">${place.title}</h3>
                    <p class="user-hotel-location">
                        <i class="fas fa-map-marker-alt"></i> ${place.price} ر.س / ليلة
                    </p>
                    <div class="user-hotel-actions">
                        <button class="delete-hotel-btn" onclick="deleteHotel('${place.id}')">
                            <i class="fas fa-trash"></i> حذف
                        </button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = '<p class="empty-message">حدث خطأ في تحميل البيانات.</p>';
    }
}

// ==================== 2. إضافة فندق جديد (POST) ====================

document.addEventListener('DOMContentLoaded', () => {
    // محاولة عرض الفنادق فور تحميل الصفحة
    displayUserHotels();

    const form = document.getElementById('addHotelForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const token = getAuthToken();
            if (!token) {
                alert('عذراً، انتهت جلستك. يرجى تسجيل الدخول مجدداً.');
                window.location.href = '/login';
                return;
            }

            // جمع البيانات من النموذج
            const currentUser = JSON.parse(localStorage.getItem('currentUser'));
            const placeData = {
                title: document.getElementById('hotelName').value,
                description: document.getElementById('hotelDescription')?.value || document.getElementById('hotelTagline')?.value || "وصف افتراضي",
                price: parseInt(document.getElementById('hotelPrice')?.value || document.getElementById('hotelBasePrice')?.value || 0),
                latitude: parseFloat(document.getElementById('hotelLat')?.value || 0),
                longitude: parseFloat(document.getElementById('hotelLng')?.value || 0),
                owner_id: currentUser.id // ربط الفندق بصاحبه
            };

            try {
                const response = await fetch('/api/v1/places/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(placeData)
                });

                if (response.ok) {
                    alert('تم إضافة الفندق بنجاح! 🎉');
                    form.reset();
                    // تحديث القائمة فوراً دون الحاجة لتحديث الصفحة
                    displayUserHotels();
                } else {
                    const err = await response.json();
                    alert('فشل الإضافة: ' + (err.message || 'خطأ غير معروف'));
                }
            } catch (error) {
                console.error(error);
                alert('حدث خطأ في الاتصال بالسيرفر');
            }
        });
    }
});

// ==================== 3. حذف فندق (DELETE) ====================

async function deleteHotel(placeId) {
    if (!confirm('هل أنت متأكد من حذف هذا العقار نهائياً؟')) return;

    const token = getAuthToken();
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            alert('تم الحذف بنجاح');
            // إزالة الكارت من الشاشة فوراً
            displayUserHotels(); 
        } else {
            alert('فشل الحذف. تأكد أنك تملك الصلاحية.');
        }
    } catch (error) {
        console.error(error);
        alert('حدث خطأ أثناء الحذف');
    }
}

// ==================== 4. وظائف الواجهة الإضافية (إدارة الأقسام) ====================

function addAboutSection() {
    const container = document.getElementById('aboutSections');
    if (!container) return;
    const div = document.createElement('div');
    div.className = 'about-item';
    div.innerHTML = `
        <div class="form-group"><label>العنوان</label><input type="text" class="about-title" required></div>
        <div class="form-group"><label>الوصف</label><textarea class="about-content" rows="2" required></textarea></div>
        <button type="button" class="remove-btn" onclick="this.parentElement.remove()"><i class="fas fa-trash"></i></button>
    `;
    container.appendChild(div);
}

function addAmenity() {
    const container = document.getElementById('amenitiesList');
    if (!container) return;
    const div = document.createElement('div');
    div.className = 'amenity-item';
    div.innerHTML = `
        <input type="text" class="amenity-text" placeholder="مثال: مسبح" required>
        <button type="button" class="remove-btn" onclick="this.parentElement.remove()"><i class="fas fa-trash"></i></button>
    `;
    container.appendChild(div);
}