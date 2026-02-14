/**
 * ملف: admin.js
 * الوصف: إدارة عمليات الإضافة، الحذف، والعرض الديناميكي للفنادق عبر الـ API.
 */

// دالة جلب التوكن من الكوكيز للتوثيق
function getAuthToken() {
    return document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
}

// ==================== 1. إدارة أقسام الواجهة (UI Management) ====================

// إضافة قسم وصف جديد
function addAboutSection() {
    const container = document.getElementById('aboutSections');
    const newSection = document.createElement('div');
    newSection.className = 'about-item';
    newSection.innerHTML = `
        <div class="form-group">
            <label>عنوان القسم <span class="required">*</span></label>
            <input type="text" class="about-title" placeholder="مثال: المرافق" required>
        </div>
        <div class="form-group">
            <label>الوصف <span class="required">*</span></label>
            <textarea class="about-content" rows="4" placeholder="اكتب وصف تفصيلي..." required></textarea>
        </div>
        <button type="button" class="remove-btn" onclick="removeElement(this, '.about-item')">
            <i class="fas fa-trash"></i> حذف القسم
        </button>
    `;
    container.appendChild(newSection);
}

// إضافة مرفق جديد
function addAmenity() {
    const container = document.getElementById('amenitiesList');
    const newAmenity = document.createElement('div');
    newAmenity.className = 'amenity-item';
    newAmenity.innerHTML = `
        <input type="text" class="amenity-icon" placeholder="مثال: fas fa-wifi" value="fas fa-star">
        <input type="text" class="amenity-text" placeholder="مثال: واي فاي مجاني" required>
        <button type="button" class="remove-btn" onclick="removeElement(this, '.amenity-item')">
            <i class="fas fa-trash"></i>
        </button>
    `;
    container.appendChild(newAmenity);
}

// دالة عامة لحذف العناصر من الواجهة
function removeElement(btn, selector) {
    const items = document.querySelectorAll(selector);
    if (items.length > 1) {
        btn.parentElement.remove();
    } else {
        alert('يجب أن يكون هناك عنصر واحد على الأقل');
    }
}

// ==================== 2. معاينة الصور (Image Preview) ====================

document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('hotelImages');
    const previewContainer = document.getElementById('imagesPreview');
    
    if (imageInput) {
        imageInput.addEventListener('change', (e) => {
            previewContainer.innerHTML = '';
            const files = Array.from(e.target.files);
            
            if (files.length > 5) {
                alert('يمكنك رفع 5 صور كحد أقصى');
                imageInput.value = '';
                return;
            }
            
            files.forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const div = document.createElement('div');
                    div.className = 'preview-image';
                    div.innerHTML = `
                        <img src="${event.target.result}" alt="صورة ${index + 1}">
                        <button type="button" class="remove-image" onclick="this.parentElement.remove()">
                            <i class="fas fa-times"></i>
                        </button>
                    `;
                    previewContainer.appendChild(div);
                };
                reader.readAsDataURL(file);
            });
        });
    }
});

// ==================== 3. العمليات البرمجية (API Operations) ====================

// حفظ الفندق في قاعدة البيانات (POST)
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addHotelForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const token = getAuthToken();

            if (!token) {
                alert('يجب تسجيل الدخول أولاً');
                return;
            }

            // تجميع البيانات المتوافقة مع الـ Backend Schema
            const hotelData = {
                title: document.getElementById('hotelName').value,
                description: document.getElementById('hotelTagline').value,
                price: parseFloat(document.getElementById('hotelBasePrice').value),
                latitude: parseFloat(document.getElementById('hotelLat').value),
                longitude: parseFloat(document.getElementById('hotelLng').value),
                status: 'available'
            };

            try {
                const response = await fetch('/api/v1/places/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(hotelData)
                });

                if (response.ok) {
                    alert('تم إضافة الفندق بنجاح! 🎉');
                    window.location.reload();
                } else {
                    const err = await response.json();
                    alert('فشل الحفظ: ' + (err.message || 'خطأ غير معروف'));
                }
            } catch (error) {
                alert('حدث خطأ في الاتصال بالسيرفر');
                console.error('Error:', error);
            }
        });
    }
    
    // تحميل قائمة الفنادق المضافة عند تشغيل الصفحة
    displayUserHotels();
});

// جلب وعرض الفنادق من السيرفر (GET)
async function displayUserHotels() {
    const container = document.getElementById('userHotelsList');
    if (!container) return;

    // 1. جلب بيانات المستخدم الحالي من المتصفح
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    if (!currentUser || !currentUser.id) return;

    try {
        const response = await fetch('/api/v1/places/');
        const places = await response.json();

        // 2. الفلترة: عرض الفنادق التي تملكها أنت فقط
        const myPlaces = places.filter(place => place.user_id === currentUser.id);

        if (myPlaces.length === 0) {
            container.innerHTML = '<p class="empty-message">لم تقم بإضافة أي فنادق بهذا الحساب بعد.</p>';
            return;
        }

        container.innerHTML = '';
        myPlaces.forEach(place => {
            container.innerHTML += `
                <div class="user-hotel-card">
                    <img src="/static/images/hotel1.jpg" class="user-hotel-image">
                    <div class="user-hotel-info">
                        <h3 class="user-hotel-name">${place.title}</h3>
                        <p class="user-hotel-location"><i class="fas fa-map-marker-alt"></i> ${place.price} ر.س / ليلة</p>
                        <div class="user-hotel-actions">
                            <button class="delete-hotel-btn" onclick="deleteHotel('${place.id}')">حذف</button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// حذف فندق نهائياً (DELETE)
async function deleteHotel(placeId) {
    if (!confirm('هل أنت متأكد من حذف هذا الفندق؟')) return;

    const token = getAuthToken();
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            alert('تم حذف الفندق بنجاح');
            displayUserHotels(); // تحديث القائمة بعد الحذف
        } else {
            alert('ليس لديك صلاحية لحذف هذا الفندق أو حدث خطأ');
        }
    } catch (error) {
        alert('حدث خطأ في الاتصال بالسيرفر');
        console.error('Error deleting hotel:', error);
    }
}