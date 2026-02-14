/**
 * ملف: places.js
 * الوصف: تحميل وعرض الأماكن ديناميكياً من الـ API
 * التحديث: تم إزالة البيانات الثابتة واستبدالها بجلب من /api/v1/places
 */

// ==================== تحميل الأماكن من الـ API ====================

/**
 * جلب جميع الأماكن من الـ API وعرضها كبطاقات
 */
async function fetchAndRenderPlaces() {
    const grid = document.getElementById('placesGrid');
    const loadingEl = document.getElementById('placesLoading');
    const noPlacesEl = document.getElementById('noPlacesMessage');
    const errorEl = document.getElementById('placesError');

    if (!grid) return;

    // إظهار التحميل وإخفاء البقية
    if (loadingEl) loadingEl.style.display = 'flex';
    if (noPlacesEl) noPlacesEl.style.display = 'none';
    if (errorEl) errorEl.style.display = 'none';

    // إزالة البطاقات القديمة (لو كانت موجودة)
    grid.querySelectorAll('.destination-card').forEach(card => card.remove());

    try {
        // جلب من الـ API
        const places = await PlacesAPI.getAll();

        // إخفاء التحميل
        if (loadingEl) loadingEl.style.display = 'none';

        if (!Array.isArray(places) || places.length === 0) {
            // لا توجد وجهات
            if (noPlacesEl) noPlacesEl.style.display = 'flex';
            return;
        }

        // عرض كل مكان كبطاقة
        places.forEach((place, index) => {
            const card = createPlaceCard(place, index);
            grid.appendChild(card);
        });

        // تطبيق تأثير الظهور التدريجي
        applyFadeInAnimation();

        // تحديث الفلاتر لتعمل مع البطاقات الجديدة
        setupFilters();

    } catch (error) {
        console.error('خطأ في تحميل الأماكن:', error);
        if (loadingEl) loadingEl.style.display = 'none';
        if (errorEl) errorEl.style.display = 'flex';
    }
}

/**
 * إنشاء بطاقة مكان/فندق من بيانات الـ API
 */
function createPlaceCard(place, index) {
    const card = document.createElement('div');
    card.className = 'destination-card';
    // استخدام data-place-id لتخزين معرف المكان
    card.setAttribute('data-place-id', place.id);

    // تحديد الصورة — استخدام صورة افتراضية بناءً على الترتيب
    const imageIndex = (index % 9) + 1;
    const imageSrc = `images/hotel${imageIndex}.jpg`;

    // تنسيق السعر
    const price = place.price ? Number(place.price).toLocaleString('en-US') : '0';

    // تقصير الوصف
    const description = place.description
        ? (place.description.length > 60 ? place.description.substring(0, 60) + '...' : place.description)
        : '';

    // تحديد حالة المكان
    const statusBadge = (place.status === 'available' || place.status === 'active')
        ? '<span class="status-active">متاح</span>'
        : '<span class="status-inactive">غير متاح</span>';

    card.innerHTML = `
        <div class="card-image-wrapper">
            <img src="${imageSrc}" alt="${place.title}" class="card-image"
                 onerror="this.src='images/hotel1.jpg'">
            <div class="card-badge">
                <i class="fas fa-star"></i>
                <span>5.0</span>
            </div>
        </div>
        <div class="card-content">
            <h3 class="card-title">${place.title}</h3>
            <div class="card-location">
                <i class="fas fa-map-marker-alt"></i>
                <span>${description || 'المملكة العربية السعودية'}</span>
            </div>
            <div class="card-rating">
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
                <i class="fas fa-star"></i>
            </div>
            <div class="card-price">
                <span class="price-amount">${price}</span>
                <span class="price-currency">ر.س</span>
                <span class="price-per">/ لليلة الواحدة</span>
            </div>
            <button class="card-btn" onclick="showLoadingScreen('hotel-details.html?hotel=${place.id}')">احجز الآن</button>
        </div>
    `;

    return card;
}

// ==================== الفلاتر ====================

/**
 * إعداد أزرار الفلاتر لتعمل مع البطاقات الديناميكية
 */
function setupFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const destinationCards = document.querySelectorAll('.destination-card');

    filterButtons.forEach(button => {
        // إزالة أي مستمع حدث قديم (لمنع التكرار)
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);

        newButton.addEventListener('click', () => {
            // إزالة active من جميع الأزرار
            document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));

            // إضافة active للزر المضغوط
            newButton.classList.add('active');

            const filterValue = newButton.getAttribute('data-filter');

            // فلترة البطاقات — لأن الأماكن من الـ API لا تحتوي على region
            // نعرض الكل عند الضغط على أي فلتر
            const cards = document.querySelectorAll('.destination-card');
            cards.forEach(card => {
                if (filterValue === 'all') {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'scale(1)';
                    }, 10);
                } else {
                    const cardRegion = card.getAttribute('data-region');
                    if (cardRegion === filterValue) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'scale(1)';
                        }, 10);
                    } else if (!cardRegion) {
                        // البطاقات من الـ API ليس لها region — نعرضها دائماً
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'scale(1)';
                        }, 10);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.8)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                }
            });
        });
    });
}

// ==================== تأثيرات بصرية ====================

/**
 * تأثير الظهور التدريجي للبطاقات
 */
function applyFadeInAnimation() {
    const cards = document.querySelectorAll('.destination-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.5s ease';
    });

    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// ==================== أحداث الصفحة ====================

// زر الترتيب
const sortBtn = document.querySelector('.sort-btn');
if (sortBtn) {
    sortBtn.addEventListener('click', () => {
        alert('خيارات الترتيب:\n1. الأعلى تقييماً\n2. الأقل سعراً\n3. الأعلى سعراً\n4. الأحدث');
    });
}

// زر ابدأ رحلتك في الهيرو
const heroCta = document.querySelector('.hero-cta-btn');
if (heroCta) {
    heroCta.addEventListener('click', () => {
        document.querySelector('.destinations-grid-section').scrollIntoView({
            behavior: 'smooth'
        });
    });
}

// تأثير التمرير - تغيير شفافية الهيرو
window.addEventListener('scroll', () => {
    const heroSection = document.querySelector('.destinations-hero');
    if (heroSection) {
        const scrolled = window.pageYOffset;
        const heroHeight = heroSection.offsetHeight;

        if (scrolled < heroHeight) {
            const opacity = 1 - (scrolled / heroHeight) * 0.5;
            heroSection.style.opacity = opacity;
        }
    }
});

// ==================== التحميل عند فتح الصفحة ====================

document.addEventListener('DOMContentLoaded', () => {
    fetchAndRenderPlaces();
});
