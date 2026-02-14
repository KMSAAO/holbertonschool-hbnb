/**
 * ملف: places.js
 * الوظيفة: إدارة التفاعلات البصرية وجلب بيانات الفنادق من MySQL
 */

// ==================== 1. جلب وعرض البيانات ديناميكياً ====================

async function fetchAllPlaces() {
    const container = document.getElementById('hotelsContainer');
    if (!container) return;

    try {
        // طلب البيانات من السيرفر
        const response = await fetch('/api/v1/places/');
        const places = await response.json();

        // تفريغ الحاوية من أي كروت ثابتة قديمة
        container.innerHTML = '';

        if (places.length === 0) {
            container.innerHTML = '<p class="empty-message">لا توجد وجهات متاحة حالياً في قاعدة البيانات.</p>';
            return;
        }

        places.forEach(place => {
            // ملاحظة تقنية: نستخدم الأعمدة title و price و id كما في ملف SQL
            const cardHTML = `
                <div class="hotel-card" data-region="${place.region || 'all'}" style="opacity: 0; transform: translateY(20px); transition: all 0.5s ease;">
                    <div class="hotel-image">
                        <img src="/static/images/${place.image_url || 'hotel1.jpg'}" alt="${place.title}">
                        <div class="hotel-rating">
                            <i class="fas fa-star"></i> 4.8
                        </div>
                    </div>
                    <div class="hotel-info">
                        <h3 class="hotel-name">${place.title}</h3>
                        <p class="hotel-price">
                            <span class="price-amount">${place.price}</span> ر.س / ليلة
                        </p>
                        <button class="details-btn" onclick="showLoadingScreen('/hotel-details?id=${place.id}')">
                            عرض التفاصيل
                        </button>
                    </div>
                </div>`;
            container.insertAdjacentHTML('beforeend', cardHTML);
        });

        // تشغيل تأثير الظهور التدريجي بعد إضافة الكروت
        triggerFadeIn();

    } catch (error) {
        console.error('Error fetching places:', error);
        container.innerHTML = '<p class="error-message">حدث خطأ أثناء تحميل البيانات.</p>';
    }
}

// ==================== 2. التأثيرات البصرية والانتقالات ====================

// دالة لجعل الكروت تظهر تدريجياً
function triggerFadeIn() {
    const cards = document.querySelectorAll('.hotel-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// التمرير السلس عند الضغط على "ابدأ رحلتك"
function setupHeroScroll() {
    const heroBtn = document.querySelector('.hero-btn');
    const target = document.querySelector('.intro-section');
    if (heroBtn && target) {
        heroBtn.addEventListener('click', () => {
            target.scrollIntoView({ behavior: 'smooth' });
        });
    }
}

// ==================== 3. تهيئة الصفحة عند التحميل ====================

document.addEventListener('DOMContentLoaded', () => {
    // تشغيل جلب البيانات من السيرفر فوراً
    fetchAllPlaces();
    
    // إعداد التمرير السلس
    setupHeroScroll();
    
    // مراقبة التمرير لتغيير شفافية الهيدر (اختياري)
    window.addEventListener('scroll', () => {
        const hero = document.querySelector('.hero-slider');
        if (hero) {
            let opacity = 1 - (window.pageYOffset / 600);
            hero.style.opacity = opacity < 0 ? 0 : opacity;
        }
    });
});