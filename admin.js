/**
 * ملف: admin.js
 * الوصف: إدارة صفحة إضافة وتعديل الفنادق
 * الوظائف: إضافة/حذف أقسام النموذج، حفظ البيانات في localStorage، عرض الفنادق المضافة
 */

let currentEditId = null; // متغير لتتبع حالة التعديل
const DEFAULT_FORM_TITLE = 'إضافة فندق جديد';
const EDIT_FORM_TITLE = 'تعديل الفندق';
const DEFAULT_SUBMIT_HTML = '<i class="fas fa-save"></i> حفظ الفندق';
const EDIT_SUBMIT_HTML = '<i class="fas fa-save"></i> تحديث الفندق';

function clearEditMode() {
    currentEditId = null;

    const submitBtn = document.querySelector('#addHotelForm button[type="submit"]');
    if (submitBtn) {
        submitBtn.innerHTML = DEFAULT_SUBMIT_HTML;
    }

    const formTitle = document.querySelector('.admin-form-container .form-title');
    if (formTitle) {
        formTitle.textContent = DEFAULT_FORM_TITLE;
    }

    const imageInput = document.getElementById('hotelImages');
    if (imageInput) {
        imageInput.required = true;
    }

    const locationInput = document.getElementById('hotelLocation');
    if (locationInput) {
        locationInput.required = true;
    }

    const regionInput = document.getElementById('hotelRegion');
    if (regionInput) {
        regionInput.required = true;
    }
}

function setEditMode(placeId) {
    currentEditId = placeId;

    const submitBtn = document.querySelector('#addHotelForm button[type="submit"]');
    if (submitBtn) {
        submitBtn.innerHTML = EDIT_SUBMIT_HTML;
    }

    const formTitle = document.querySelector('.admin-form-container .form-title');
    if (formTitle) {
        formTitle.textContent = EDIT_FORM_TITLE;
    }

    const imageInput = document.getElementById('hotelImages');
    if (imageInput) {
        imageInput.required = false;
    }

    // Location/region are not fully represented in backend place schema yet.
    // Keep edit flow usable by relaxing these required flags while editing.
    const locationInput = document.getElementById('hotelLocation');
    if (locationInput) {
        locationInput.required = false;
    }

    const regionInput = document.getElementById('hotelRegion');
    if (regionInput) {
        regionInput.required = false;
    }
}

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

    clearEditMode();

    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // التحقق من وضع التعديل مقابل الإضافة
            const isEditMode = !!currentEditId;

            // جمع البيانات
            const hotelData = {
                id: 'hotel_' + Date.now(),
                name: document.getElementById('hotelName').value,
                nameEn: document.getElementById('hotelNameEn').value,
                location: document.getElementById('hotelLocation').value,
                tagline: document.getElementById('hotelTagline').value,
                region: document.getElementById('hotelRegion').value,
                latitude: parseFloat(document.getElementById('hotelLatitude').value) || 0,
                longitude: parseFloat(document.getElementById('hotelLongitude').value) || 0,
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
            if (!isEditMode && imageFiles.length === 0) {
                alert('يرجى رفع صورة واحدة على الأقل');
                return;
            }

            if (imageFiles.length > 5) {
                alert('يمكنك رفع 5 صور كحد أقصى');
                return;
            }

            // const previousHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
            // const nextHotels = JSON.parse(JSON.stringify(previousHotels));

            // let targetIndex = -1;
            /*
            if (isEditMode) {
                targetIndex = nextHotels.findIndex(h => h.id === currentEditId);
                // ...
            } else {
                // ...
            }
            */

            // أيضاً حفظ/تحديث في الـ backend
            const userId = localStorage.getItem('userId');

            if (userId && typeof PlacesAPI !== 'undefined') {
                try {
                    let apiPlace;

                    if (isEditMode) {
                        // Resolve amenities to IDs for update
                        const allAmenities = await AmenitiesAPI.getAll();
                        const resolvedAmenityIds = [];
                        const createdAmenityIds = [];
                        // Deduplicate by text (normalized) to avoid sending duplicates
                        const processedTexts = new Set();
                        const normalizeAmenityName = (value) => {
                            return (value || '')
                                .toString()
                                .trim()
                                .toLowerCase()
                                .replace(/[\u064b-\u0652]/g, '')
                                .replace(/[\u0623\u0625\u0622]/g, '\u0627')
                                .replace(/\u0629/g, '\u0647')
                                .replace(/\u0649/g, '\u064a')
                                .replace(/[^\p{L}\p{N}\s]/gu, ' ')
                                .replace(/\s+/g, ' ')
                                .replace(/^(?:\u0627\u0644)\s*/, '')
                                .trim();
                        };
                        const aliasMap = {
                            wifi: ['wifi', 'wi fi', 'wi-fi', 'internet', 'wireless', 'واي فاي', 'وايفاي', 'انترنت', 'الانترنت'],
                            parking: ['parking', 'car park', 'garage', 'موقف سيارات', 'مواقف سيارات', 'باركينج', 'موقف'],
                            'swimming pool': ['swimming pool', 'pool', 'حمام سباحه', 'حمام سباحة', 'مسبح', 'المسبح'],
                            gym: ['gym', 'fitness', 'fitness center', 'جيم', 'نادي رياضي', 'صالة رياضة', 'الصالة الرياضية'],
                            restaurant: ['restaurant', 'dining', 'مطعم', 'المطعم', 'مطاعم'],
                            spa: ['spa', 'سبا', 'السبا'],
                            'air conditioning': ['air conditioning', 'ac', 'a c', 'a/c', 'تكييف', 'التكييف', 'مكيف'],
                            tv: ['tv', 'television', 'تلفاز', 'تلفزيون', 'التلفاز', 'التلفزيون'],
                            laundry: ['laundry', 'washing', 'غسيل ملابس', 'غسيل', 'مغسلة', 'مغسله'],
                            bar: ['bar', 'cocktail', 'بار', 'البار'],
                            breakfast: ['breakfast', 'افطار', 'إفطار', 'فطور', 'الفطور', 'بوفيه'],
                            'airport shuttle': ['airport shuttle', 'shuttle', 'airport transfer', 'نقل للمطار', 'توصيل للمطار', 'مواصلات المطار'],
                            'pets allowed': ['pets allowed', 'pet friendly', 'pets', 'حيوانات أليفة', 'حيوانات اليفة', 'مسموح بالحيوانات'],
                            'room service': ['room service', 'خدمة غرف', 'خدمة الغرف'],
                            'business center': ['business center', 'مركز أعمال', 'مركز اعمال'],
                            'wheelchair accessible': ['wheelchair accessible', 'accessible', 'دخول للكراسي المتحركة', 'مناسب لذوي الإعاقة', 'مناسب لذوي الاعاقة']
                        };
                        const decodeJwtPayload = (token) => {
                            try {
                                const payloadPart = (token || '').split('.')[1];
                                if (!payloadPart) return null;
                                const base64 = payloadPart.replace(/-/g, '+').replace(/_/g, '/');
                                const padded = base64 + '='.repeat((4 - (base64.length % 4)) % 4);
                                return JSON.parse(atob(padded));
                            } catch (_) {
                                return null;
                            }
                        };

                        // Decode JWT claims to know if this user can create amenities
                        let canCreateAmenities = false;
                        const claims = decodeJwtPayload(localStorage.getItem('access_token') || '');
                        canCreateAmenities = !!(claims && claims.is_admin);

                        for (const item of hotelData.amenities) {
                            const rawText = (item.text || '').trim();
                            if (!rawText) {
                                alert('يوجد مرفق بدون اسم. يرجى إدخال اسم صالح قبل التحديث.');
                                return;
                            }
                            const normalizedText = normalizeAmenityName(rawText);

                            if (processedTexts.has(normalizedText)) {
                                continue;
                            }
                            processedTexts.add(normalizedText);

                            // Try matching by exact text + option aliases (Arabic/English + tokens)
                            const option = amenityOptions.find(opt => {
                                return opt.icon === item.icon
                                    || normalizeAmenityName(opt.label) === normalizedText
                                    || normalizeAmenityName(opt.labelEn) === normalizedText;
                            });
                            const candidateNames = new Set([
                                normalizedText,
                                normalizeAmenityName(rawText)
                            ]);
                            if (option) {
                                candidateNames.add(normalizeAmenityName(option.label));
                                candidateNames.add(normalizeAmenityName(option.labelEn));
                                candidateNames.add((option.label || '').trim().toLowerCase());
                                candidateNames.add((option.labelEn || '').trim().toLowerCase());
                                (option.labelEn || '')
                                    .split(/\s+/)
                                    .map(s => normalizeAmenityName(s.trim().toLowerCase()))
                                    .filter(Boolean)
                                    .forEach(token => candidateNames.add(token));
                                const optionKey = normalizeAmenityName(option.labelEn);
                                (aliasMap[optionKey] || [])
                                    .map(alias => normalizeAmenityName(alias))
                                    .filter(Boolean)
                                    .forEach(alias => candidateNames.add(alias));
                            }

                            const match = allAmenities.find(a =>
                                candidateNames.has(((a.amenity_name || '').trim().toLowerCase()))
                                || candidateNames.has(normalizeAmenityName(a.amenity_name))
                            );

                            if (match) {
                                resolvedAmenityIds.push(match.id);
                                continue;
                            }

                            if (!canCreateAmenities) {
                                alert(`المرفق "${rawText}" غير موجود في النظام، ولا تملك صلاحية إنشاء مرافق جديدة.\n\nتم إلغاء التحديث لضمان عدم فقدان البيانات.`);
                                return;
                            }

                            // Explicit creation of missing amenity
                            try {
                                const newAmenity = await AmenitiesAPI.create({
                                    amenity_name: rawText,
                                    status: 'Active' // Default
                                });
                                if (newAmenity && newAmenity.id) {
                                    resolvedAmenityIds.push(newAmenity.id);
                                    createdAmenityIds.push(newAmenity.id);
                                } else {
                                    throw new Error('Created amenity has no ID');
                                }
                            } catch (createErr) {
                                console.error('Failed to create amenity:', rawText, createErr);

                                // Best-effort rollback to avoid partially-created amenities
                                if (createdAmenityIds.length > 0 && typeof AmenitiesAPI !== 'undefined' && typeof AmenitiesAPI.delete === 'function') {
                                    for (const createdId of createdAmenityIds) {
                                        try {
                                            await AmenitiesAPI.delete(createdId);
                                        } catch (rollbackErr) {
                                            console.warn('Rollback delete failed for amenity:', createdId, rollbackErr);
                                        }
                                    }
                                }

                                // Stop update to prevent data loss (silent removal of amenity)
                                alert(`عذراً، تعذر إنشاء المرفق "${rawText}".\n\nالسبب: ${createErr.message || 'خطأ غير معروف'}.\n\nتم إلغاء التحديث لضمان عدم فقدان البيانات.`);
                                return; // Abort submission
                            }
                        }

                        // Deduplicate IDs as a final safeguard
                        const uniqueAmenityIds = [...new Set(resolvedAmenityIds)];

                        // تحديث
                        apiPlace = await PlacesAPI.update(currentEditId, {
                            title: hotelData.name || hotelData.nameEn,
                            description: hotelData.about?.[0]?.text || hotelData.tagline || '',
                            price: parseFloat(hotelData.startPrice) || 0,
                            latitude: hotelData.latitude,
                            longitude: hotelData.longitude,
                            location: hotelData.location,
                            status: 'available',
                            number_of_rooms: hotelData.rooms.length,
                            max_guests: 0, // Placeholder
                            tagline: hotelData.tagline,
                            rules: '', // Placeholder
                            details: hotelData.about,
                            rooms: hotelData.rooms,
                            amenities: uniqueAmenityIds // Send IDs
                        });
                        console.log('تم تحديث المكان في الـ backend:', apiPlace);
                    } else {
                        // إنشاء
                        apiPlace = await PlacesAPI.create({
                            title: hotelData.name || hotelData.nameEn,
                            description: hotelData.about?.[0]?.text || hotelData.tagline || '',
                            price: parseFloat(hotelData.startPrice) || 0,
                            // Create flow still accepts naive list of objects/strings as per previous service logic
                            amenities: hotelData.amenities,
                            location: hotelData.location,
                            user_id: userId,
                            latitude: hotelData.latitude,
                            longitude: hotelData.longitude,
                            status: 'available',
                            number_of_rooms: hotelData.rooms.length,
                            max_guests: 0,
                            tagline: hotelData.tagline,
                            rules: '',
                            details: hotelData.about,
                            rooms: hotelData.rooms
                        });
                        console.log('تم حفظ المكان في الـ backend:', apiPlace);
                    }

                    // رفع الصور إلى السيرفر (إذا وجدت صور جديدة)
                    if (apiPlace && apiPlace.id && imageFiles.length > 0) {
                        try {
                            const uploadResult = await PlacesAPI.uploadImages(apiPlace.id, imageFiles);
                            console.log('تم رفع الصور بنجاح');
                        } catch (uploadErr) {
                            console.warn('تعذر رفع الصور:', uploadErr);
                        }
                    }

                    clearEditMode();
                    alert(isEditMode ? 'تم تحديث الفندق بنجاح!' : 'تم إضافة الفندق بنجاح!');
                    // Reload list instead of page reload
                    displayUserHotels();
                    // window.location.reload(); 

                } catch (err) {
                    console.error('تعذر حفظ/تحديث المكان في الـ backend:', err);
                    alert('عذراً، حدث خطأ أثناء الاتصال بالخادم.\n\n' + err.message);
                }
            } else {
                alert('يجب تسجيل الدخول لإضافة فندق.');
            }
        });

        form.addEventListener('reset', () => {
            setTimeout(() => {
                clearEditMode();
                const previewContainer = document.getElementById('imagesPreview');
                if (previewContainer) {
                    previewContainer.innerHTML = '';
                }
            }, 0);
        });
    }

    // عرض الفنادق المضافة
    displayUserHotels();
});

// ==================== عرض وإدارة الفنادق المضافة ====================

// ==================== عرض وإدارة الفنادق المضافة ====================

let currentUserHotels = []; // لتخزين القائمة المحملة من الـ API

// عرض الفنادق المضافة من المستخدم
async function displayUserHotels() {
    const container = document.getElementById('userHotelsList');
    if (!container) return;

    const userId = localStorage.getItem('userId');
    if (!userId) {
        container.innerHTML = '<p class="empty-message">يجب تسجيل الدخول لعرض الفنادق.</p>';
        return;
    }

    container.innerHTML = '<p class="loading-message">جاري تحميل الفنادق...</p>';

    try {
        // Fetch from API
        // We use 'ME' if we have a token, but here we might rely on the token being in headers
        // PlacesAPI.getAll uses apiGet which should attach token.
        // We can pass user_id='ME' to leverage the backend filter we just verified.
        const places = await PlacesAPI.getAll({ user_id: 'ME' });
        currentUserHotels = places;

        if (!places || places.length === 0) {
            container.innerHTML = '<p class="empty-message">لم تقم بإضافة أي فنادق بعد</p>';
            return;
        }

        container.innerHTML = '';
        places.forEach((hotel) => {
            const imageUrl = (hotel.images && hotel.images.length > 0)
                ? hotel.images[0]
                : 'images/default-hotel.jpg';

            // API returns 'title', frontend used 'name'.
            // API returns 'tagline' or 'description'.

            const card = document.createElement('div');
            card.className = 'user-hotel-card';
            card.innerHTML = `
                <img src="${imageUrl}" alt="${hotel.title}" class="user-hotel-image">
                <div class="user-hotel-info">
                    <h3 class="user-hotel-name">${hotel.title}</h3>
                    <p class="user-hotel-location">
                        <i class="fas fa-map-marker-alt"></i>
                        ${hotel.location || hotel.tagline || 'لا يوجد وصف مختصر'}
                    </p>
                    <div class="user-hotel-actions">
                        <button class="edit-hotel-btn" onclick="editHotel('${hotel.id}')">
                            <i class="fas fa-edit"></i> تعديل
                        </button>
                        <button class="delete-hotel-btn" onclick="deleteHotel('${hotel.id}')">
                            <i class="fas fa-trash"></i> حذف
                        </button>
                    </div>
                </div>
            `;
            container.appendChild(card);
        });

    } catch (error) {
        console.error('Error fetching hotels:', error);
        container.innerHTML = '<p class="error-message">تعذر تحميل الفنادق.</p>';
    }
}

// حذف فندق
async function deleteHotel(id) {
    if (confirm('هل أنت متأكد من حذف هذا الفندق؟')) {
        try {
            await PlacesAPI.delete(id);
            alert('تم حذف الفندق بنجاح');
            displayUserHotels(); // Refresh list
        } catch (error) {
            console.error('Error deleting hotel:', error);
            alert('تعذر حذف الفندق: ' + error.message);
        }
    }
}

// تعديل فندق
function editHotel(id) {
    const hotel = currentUserHotels.find(h => h.id === id);

    if (!hotel) return;

    // تعيين وضع التعديل
    setEditMode(hotel.id);

    // 1. ملء الحقول الأساسية
    // API uses 'title', 'price', etc.
    document.getElementById('hotelName').value = hotel.title || '';
    // hotelNameEn might not exist in API model? We assume title is enough for now or use same.
    document.getElementById('hotelNameEn').value = hotel.title || '';

    // API doesn't have 'location' as string, it has lat/long. 
    // Maybe 'tagline' stores location text if we abuse it? 
    // Or we assume location is part of description?
    // Current backend has 'tagline'. Admin form has 'location' field.
    // If we want to persist 'location' text, we should have added it to backend.
    // For now, let's map 'location' to 'tagline' or leave empty?
    // Wait, Place model has 'tagline'.
    document.getElementById('hotelLocation').value = hotel.location || '';
    document.getElementById('hotelTagline').value = hotel.tagline || '';
    document.getElementById('hotelRegion').value = ''; // Not in API

    document.getElementById('hotelLatitude').value = hotel.latitude ?? '';
    document.getElementById('hotelLongitude').value = hotel.longitude ?? '';

    // 2. ملء أقسام الوصف
    const aboutContainer = document.getElementById('aboutSections');
    aboutContainer.innerHTML = ''; // مسح القديم

    // hotel.details is JSON/List from API (Phase 3)
    let aboutData = hotel.details;
    if (typeof aboutData === 'string') {
        try { aboutData = JSON.parse(aboutData); } catch (e) { }
    }

    if (aboutData && Array.isArray(aboutData) && aboutData.length > 0) {
        aboutData.forEach(item => {
            addAboutSection();
            const sections = document.querySelectorAll('.about-item');
            const lastSection = sections[sections.length - 1];

            lastSection.querySelector('.about-title').value = item.title;
            lastSection.querySelector('.about-content').value = item.text;
            lastSection.querySelector('.about-icon').value = item.icon;
        });
    } else {
        // Fallback or empty
        addAboutSection();
        // If we have description but no details, maybe put description in first section?
        if (hotel.description) {
            const sections = document.querySelectorAll('.about-item');
            const lastSection = sections[sections.length - 1];
            lastSection.querySelector('.about-title').value = 'الوصف';
            lastSection.querySelector('.about-content').value = hotel.description;
        }
    }

    // 3. ملء المرافق
    const amenitiesContainer = document.getElementById('amenitiesList');
    amenitiesContainer.innerHTML = '';

    // hotel.amenities is list of Amenity objects {id, amenity_name, ...} or similar from API
    // Frontend expects {icon, text}
    // We need to map if possible. But backend Amenity model doesn't store icon!
    // This is a disconnect.
    // Frontend Admin stores amenities as rich objects. Backend stores Amenity entities.
    // If we want to persist Icons, we need to store them in Amenity table OR uses a fixed mapping.
    // admin.js line 91 has `amenityOptions`.
    // We can try to match amenity_name to label/labelEn to find icon.

    if (hotel.amenities && hotel.amenities.length > 0) {
        hotel.amenities.forEach(item => {
            addAmenity();
            const amenities = document.querySelectorAll('.amenity-item');
            const lastAmenity = amenities[amenities.length - 1];

            const iconInput = lastAmenity.querySelector('.amenity-icon-value');
            const textInput = lastAmenity.querySelector('.amenity-text');
            const triggerSpan = lastAmenity.querySelector('.dropdown-trigger span');

            // Try to find icon from name
            const foundOpt = amenityOptions.find(opt => opt.label === item.amenity_name || opt.labelEn === item.amenity_name) || amenityOptions[0];
            const iconClass = item.icon || foundOpt.icon;

            iconInput.value = iconClass;
            textInput.value = item.amenity_name; // Use backend name

            const labelEn = foundOpt.labelEn;
            triggerSpan.innerHTML = `<i class="${iconClass}"></i> ${labelEn}`;
        });
    } else {
        addAmenity();
    }

    // 4. ملء الغرف
    const roomsContainer = document.getElementById('roomsList');
    roomsContainer.innerHTML = '';

    const roomsData = Array.isArray(hotel.rooms) ? hotel.rooms : [];
    if (roomsData.length > 0) {
        roomsData.forEach(item => {
            addRoom();
            const rooms = document.querySelectorAll('.room-item');
            const lastRoom = rooms[rooms.length - 1];

            lastRoom.querySelector('.room-name').value = item.name || '';
            lastRoom.querySelector('.room-price').value = item.price ?? '';
            lastRoom.querySelector('.room-size').value = item.size ?? '';

            const features = Array.isArray(item.features)
                ? item.features.join(', ')
                : (item.features || '');
            lastRoom.querySelector('.room-features').value = features;
        });
    } else {
        addRoom();
    }

    // مسح الصور من العرض
    document.getElementById('imagesPreview').innerHTML = '';

    // التمرير للأعلى
    document.getElementById('addHotelForm').scrollIntoView({ behavior: 'smooth' });
}
