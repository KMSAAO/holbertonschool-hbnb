// الفلترة حسب المنطقة
const filterButtons = document.querySelectorAll('.filter-btn');
const destinationCards = document.querySelectorAll('.destination-card');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        // إزالة active من جميع الأزرار
        filterButtons.forEach(btn => btn.classList.remove('active'));
        
        // إضافة active للزر المضغوط
        button.classList.add('active');
        
        const filterValue = button.getAttribute('data-filter');
        
        // فلترة البطاقات
        destinationCards.forEach(card => {
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

// تأثير الظهور التدريجي للبطاقات
destinationCards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all 0.5s ease';
});

// تفعيل تأثير الظهور عند التحميل
window.addEventListener('load', () => {
    destinationCards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// زر عرض المزيد
const loadMoreBtn = document.querySelector('.load-more-btn');
if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
        alert('سيتم تحميل المزيد من الوجهات قريباً!');
    });
}

// زر الترتيب
const sortBtn = document.querySelector('.sort-btn');
if (sortBtn) {
    sortBtn.addEventListener('click', () => {
        alert('خيارات الترتيب:\n1. الأعلى تقييماً\n2. الأقل سعراً\n3. الأعلى سعراً\n4. الأحدث');
    });
}

// زر احجز الآن
const bookButtons = document.querySelectorAll('.card-btn');
bookButtons.forEach(btn => {
    // تحقق إذا الزر ما عنده onclick مخصص
    if (!btn.hasAttribute('onclick')) {
        btn.addEventListener('click', function() {
            const cardTitle = this.closest('.destination-card').querySelector('.card-title').textContent;
            alert(`سيتم توجيهك لصفحة الحجز لـ ${cardTitle}`);
        });
    }
});

// زر ابدأ رحلتك في الهيرو
const heroCta = document.querySelector('.hero-cta-btn');
if (heroCta) {
    heroCta.addEventListener('click', () => {
        // التمرير إلى قسم البطاقات
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
