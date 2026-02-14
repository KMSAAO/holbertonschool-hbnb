/**
 * ملف: admin.js
 * الوصف: إدارة صفحة إضافة وتعديل الفنادق
 * الوظائف: إضافة/حذف أقسام النموذج، حفظ البيانات في localStorage، عرض الفنادق المضافة
 */

// ==================== إدارة أقسام الوصف ====================

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
        <div class="form-group">
            <label>أيقونة (FontAwesome)</label>
            <input type="text" class="about-icon" placeholder="مثال: fas fa-spa" value="fas fa-hotel">
        </div>
        <button type="button" class="remove-btn" onclick="removeAboutSection(this)">
            <i class="fas fa-trash"></i> حذف القسم
        </button>
    `;
    container.appendChild(newSection);
}

// حذف قسم وصف
function removeAboutSection(btn) {
    const sections = document.querySelectorAll('.about-item');
    if (sections.length > 1) {
        btn.parentElement.remove();
    } else {
        alert('يجب أن يكون هناك قسم واحد على الأقل');
    }
}

// ==================== إدارة المرافق ====================

// قائمة المرافق القياسية
const amenityOptions = [
    { icon: 'fas fa-wifi', label: 'واي فاي', labelEn: 'WiFi' },
    { icon: 'fas fa-parking', label: 'موقف سيارات', labelEn: 'Parking' },
    { icon: 'fas fa-swimming-pool', label: 'مسبح', labelEn: 'Swimming Pool' },
    { icon: 'fas fa-dumbbell', label: 'صالة رياضة', labelEn: 'Gym' },
    { icon: 'fas fa-utensils', label: 'مطعم', labelEn: 'Restaurant' },
    { icon: 'fas fa-spa', label: 'سبا', labelEn: 'Spa' },
    { icon: 'fas fa-wind', label: 'تكييف', labelEn: 'Air Conditioning' },
    { icon: 'fas fa-tv', label: 'تلفاز', labelEn: 'TV' },
    { icon: 'fas fa-tshirt', label: 'غسيل ملابس', labelEn: 'Laundry' },
    { icon: 'fas fa-cocktail', label: 'بار', labelEn: 'Bar' },
    { icon: 'fas fa-coffee', label: 'إفطار', labelEn: 'Breakfast' },
    { icon: 'fas fa-shuttle-van', label: 'نقل للمطار', labelEn: 'Airport Shuttle' },
    { icon: 'fas fa-paw', label: 'حيوانات أليفة', labelEn: 'Pets Allowed' },
    { icon: 'fas fa-concierge-bell', label: 'خدمة غرف', labelEn: 'Room Service' },
    { icon: 'fas fa-briefcase', label: 'مركز أعمال', labelEn: 'Business Center' },
    { icon: 'fas fa-wheelchair', label: 'دخول للكراسي المتحركة', labelEn: 'Wheelchair Accessible' }
];

// إنشاء خيارات القائمة المنسدلة
function getDropdownOptionsHTML() {
    return amenityOptions.map(opt => `
        <div class="dropdown-item" data-value="${opt.icon}" data-label="${opt.label}">
            <i class="${opt.icon}"></i> ${opt.labelEn}
        </div>
    `).join('');
}

// إضافة مرفق جديد
function addAmenity() {
    const container = document.getElementById('amenitiesList');
    const newAmenity = document.createElement('div');
    newAmenity.className = 'amenity-item';

    newAmenity.innerHTML = `
        <div class="custom-dropdown" tabindex="0">
            <div class="dropdown-trigger">
                <span>اختر أيقونة</span>
                <i class="fas fa-chevron-down"></i>
            </div>
            <input type="hidden" class="amenity-icon-value">
            <div class="dropdown-menu">
                ${getDropdownOptionsHTML()}
            </div>
        </div>
        <input type="text" class="amenity-text" placeholder="مثال: واي فاي مجاني" required>
        <button type="button" class="remove-btn" onclick="removeAmenity(this)">
            <i class="fas fa-trash"></i>
        </button>
    `;
    container.appendChild(newAmenity);
}

// Event Delegation for Dropdowns
document.addEventListener('click', function (e) {
    // Toggle Dropdown
    const trigger = e.target.closest('.dropdown-trigger');
    if (trigger) {
        const dropdown = trigger.parentElement;
        const allDropdowns = document.querySelectorAll('.custom-dropdown.active');

        // Close other dropdowns
        allDropdowns.forEach(d => {
            if (d !== dropdown) d.classList.remove('active');
        });

        dropdown.classList.toggle('active');
        e.stopPropagation();
        return;
    }

    // Select Option
    const item = e.target.closest('.dropdown-item');
    if (item) {
        const dropdown = item.closest('.custom-dropdown');
        const triggerSpan = dropdown.querySelector('.dropdown-trigger span');
        const hiddenInput = dropdown.querySelector('.amenity-icon-value');
        const amenityItem = dropdown.closest('.amenity-item');
        const textInput = amenityItem.querySelector('.amenity-text');

        const iconClass = item.dataset.value;
        const label = item.dataset.label;

        // Update UI
        triggerSpan.innerHTML = `<i class="${iconClass}"></i> ${item.textContent.trim()}`;
        hiddenInput.value = iconClass;

        // Auto-fill text if empty
        if (!textInput.value) {
            textInput.value = label;
        }

        dropdown.classList.remove('active');
        e.stopPropagation();
        return;
    }

    // Close when clicking outside
    if (!e.target.closest('.custom-dropdown')) {
        document.querySelectorAll('.custom-dropdown.active').forEach(d => {
            d.classList.remove('active');
        });
    }
});

// تهيئة القوائم الموجودة عند التحميل (إن وجدت)
document.addEventListener('DOMContentLoaded', () => {
    const initialDropdowns = document.querySelectorAll('.dropdown-menu');
    initialDropdowns.forEach(menu => {
        if (!menu.children.length) {
            menu.innerHTML = getDropdownOptionsHTML();
        }
    });
});

// حذف مرفق
function removeAmenity(btn) {
    const amenities = document.querySelectorAll('.amenity-item');
    if (amenities.length > 1) {
        btn.parentElement.remove();
    } else {
        alert('يجب أن يكون هناك مرفق واحد على الأقل');
    }
}

// ==================== إدارة الغرف ====================

// إضافة غرفة جديدة
function addRoom() {
    const container = document.getElementById('roomsList');
    const newRoom = document.createElement('div');
    newRoom.className = 'room-item';
    newRoom.innerHTML = `
        <div class="form-row">
            <div class="form-group">
                <label>اسم الغرفة <span class="required">*</span></label>
                <input type="text" class="room-name" placeholder="مثال: غرفة عائلية" required>
            </div>
            <div class="form-group">
                <label>السعر (ر.س) <span class="required">*</span></label>
                <input type="number" class="room-price" placeholder="2500" required min="0">
            </div>
            <div class="form-group">
                <label>المساحة (م²) <span class="required">*</span></label>
                <input type="number" class="room-size" placeholder="60" required min="1">
            </div>
        </div>
        <div class="form-group">
            <label>المميزات (افصل بفاصلة) <span class="required">*</span></label>
            <input type="text" class="room-features" placeholder="مثال: شرفة خاصة, تكييف, منطقة جلوس" required>
        </div>
        <button type="button" class="remove-btn" onclick="removeRoom(this)">
            <i class="fas fa-trash"></i> حذف الغرفة
        </button>
    `;
    container.appendChild(newRoom);
}

// حذف غرفة
function removeRoom(btn) {
    const rooms = document.querySelectorAll('.room-item');
    if (rooms.length > 1) {
        btn.parentElement.remove();
    } else {
        alert('يجب أن يكون هناك غرفة واحدة على الأقل');
    }
}

// ==================== معاينة الصور ====================

// معاينة الصور قبل الرفع
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
                        <button type="button" class="remove-image" onclick="removeImage(this, ${index})">
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

// حذف صورة من المعاينة
function removeImage(btn, index) {
    btn.parentElement.remove();
}

// ==================== حفظ الفندق ====================

// حفظ بيانات الفندق في localStorage
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('addHotelForm');

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // جمع البيانات
            const hotelData = {
                id: 'hotel_' + Date.now(),
                name: document.getElementById('hotelName').value,
                nameEn: document.getElementById('hotelNameEn').value,
                location: document.getElementById('hotelLocation').value,
                tagline: document.getElementById('hotelTagline').value,
                region: document.getElementById('hotelRegion').value,
                startPrice: 0,
                images: [],
                about: [],
                amenities: [],
                rooms: []
            };

            // جمع أقسام الوصف
            document.querySelectorAll('.about-item').forEach(item => {
                const title = item.querySelector('.about-title').value;
                const content = item.querySelector('.about-content').value;
                const icon = item.querySelector('.about-icon').value || 'fas fa-info-circle';

                if (title && content) {
                    hotelData.about.push({
                        title: title,
                        icon: icon,
                        text: content
                    });
                }
            });

            // جمع المرافق
            document.querySelectorAll('.amenity-item').forEach(item => {
                const iconInput = item.querySelector('.amenity-icon-value');
                // Fallback for older items or if just text input was used previously, but now we use hidden input
                const icon = iconInput ? iconInput.value : '';
                const text = item.querySelector('.amenity-text').value;

                if (icon && text) {
                    hotelData.amenities.push({
                        icon: icon,
                        text: text
                    });
                }
            });

            // جمع الغرف
            document.querySelectorAll('.room-item').forEach((item, index) => {
                const name = item.querySelector('.room-name').value;
                const price = parseInt(item.querySelector('.room-price').value);
                const size = parseInt(item.querySelector('.room-size').value);
                const features = item.querySelector('.room-features').value.split(',').map(f => f.trim());

                if (name && price && size) {
                    hotelData.rooms.push({
                        id: 'room_' + index,
                        name: name,
                        price: price,
                        size: size,
                        features: features
                    });

                    // تحديث أقل سعر
                    if (index === 0 || price < hotelData.startPrice) {
                        hotelData.startPrice = price;
                    }
                }
            });

            // معالجة الصور
            const imageFiles = document.getElementById('hotelImages').files;
            if (imageFiles.length === 0) {
                alert('يرجى رفع صور الفندق');
                return;
            }

            if (imageFiles.length === 0) {
                alert('يرجى رفع صورة واحدة على الأقل');
                return;
            }

            if (imageFiles.length > 5) {
                alert('يمكنك رفع 5 صور كحد أقصى');
                return;
            }

            // حفظ أسماء الصور مؤقتاً (سيتم تحديثها بعد الرفع الفعلي)
            hotelData.images = [];

            // حفظ البيانات في localStorage
            let userHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
            userHotels.push(hotelData);
            localStorage.setItem('userHotels', JSON.stringify(userHotels));

            // أيضاً حفظ في الـ backend
            const userId = localStorage.getItem('userId');

            if (userId && typeof PlacesAPI !== 'undefined') {
                try {
                    const apiPlace = await PlacesAPI.create({
                        title: hotelData.name || hotelData.nameEn,
                        description: hotelData.about?.[0]?.text || hotelData.tagline || '',
                        price: parseFloat(hotelData.startPrice) || 0,
                        amenities: hotelData.amenities, // Send amenities array ({icon, text})
                        user_id: userId,
                        latitude: 0,
                        longitude: 0,
                        status: 'available' // تصحيح الحالة لتطابق الـ enum في backend
                    });

                    console.log('تم حفظ المكان في الـ backend:', apiPlace);

                    // رفع الصور إلى السيرفر
                    let uploadedImages = [];
                    if (apiPlace && apiPlace.id && imageFiles.length > 0) {
                        try {
                            const uploadResult = await PlacesAPI.uploadImages(apiPlace.id, imageFiles);
                            uploadedImages = uploadResult.images || [];
                            console.log('تم رفع الصور بنجاح:', uploadedImages);
                        } catch (uploadErr) {
                            console.warn('تعذر رفع الصور:', uploadErr);
                            // المكان تم حفظه بنجاح لكن الصور لم ترفع
                        }
                    }

                    // تحديث الـ ID والصور في localStorage ليطابق الـ backend
                    if (apiPlace && apiPlace.id) {
                        let currentHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
                        // تحديث آخر فندق تمت إضافته
                        if (currentHotels.length > 0) {
                            currentHotels[currentHotels.length - 1].id = apiPlace.id;
                            currentHotels[currentHotels.length - 1].images = uploadedImages;
                            localStorage.setItem('userHotels', JSON.stringify(currentHotels));
                        }
                    }

                    // عرض رسالة نجاح فقط إذا نجح الحفظ في الـ API
                    alert('تم إضافة الفندق بنجاح! سيظهر في صفحة الوجهات.');
                    window.location.reload();

                } catch (err) {
                    console.error('تعذر حفظ المكان في الـ backend:', err);

                    // حذف الفندق من localStorage لأنه فشل في الـ API
                    let currentHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
                    currentHotels.pop();
                    localStorage.setItem('userHotels', JSON.stringify(currentHotels));

                    alert('عذراً، حدث خطأ أثناء حفظ الفندق في الخادم. يرجى التأكد من البيانات والمحاولة مرة أخرى.\n\n' + err.message);
                }
            } else {
                // في حال عدم وجود اتصال بالـ API (نادر الحدوث)
                alert('تم إضافة الفندق محلياً فقط.');
                window.location.reload();
            }
        });
    }

    // عرض الفنادق المضافة
    displayUserHotels();
});

// ==================== عرض وإدارة الفنادق المضافة ====================

// عرض الفنادق المضافة من المستخدم
function displayUserHotels() {
    const container = document.getElementById('userHotelsList');
    if (!container) return;

    const userHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');

    if (userHotels.length === 0) {
        container.innerHTML = '<p class="empty-message">لم تقم بإضافة أي فنادق بعد</p>';
        return;
    }

    container.innerHTML = '';
    userHotels.forEach((hotel, index) => {
        const card = document.createElement('div');
        card.className = 'user-hotel-card';
        card.innerHTML = `
            <img src="${hotel.images[0] || 'images/default-hotel.jpg'}" alt="${hotel.name}" class="user-hotel-image">
            <div class="user-hotel-info">
                <h3 class="user-hotel-name">${hotel.name}</h3>
                <p class="user-hotel-location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${hotel.location}
                </p>
                <div class="user-hotel-actions">
                    <button class="edit-hotel-btn" onclick="editHotel(${index})">
                        <i class="fas fa-edit"></i> تعديل
                    </button>
                    <button class="delete-hotel-btn" onclick="deleteHotel(${index})">
                        <i class="fas fa-trash"></i> حذف
                    </button>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}

// حذف فندق
function deleteHotel(index) {
    if (confirm('هل أنت متأكد من حذف هذا الفندق؟')) {
        let userHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
        userHotels.splice(index, 1);
        localStorage.setItem('userHotels', JSON.stringify(userHotels));
        displayUserHotels();
        alert('تم حذف الفندق بنجاح');
    }
}

// تعديل فندق (للمستقبل)
function editHotel(index) {
    alert('ميزة التعديل ستكون متاحة قريباً');
}
