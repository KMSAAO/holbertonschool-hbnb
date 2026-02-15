// السلايدر الأوتوماتيكي للهيدر
let currentSlideIndex = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

// تشغيل السلايدر تلقائياً
function autoSlide() {
    // ✅ إضافة تحقق: إذا لم تكن هناك سلايدات، توقف فوراً
    if (slides.length === 0) return; 

    currentSlideIndex++;
    if (currentSlideIndex >= slides.length) {
        currentSlideIndex = 0;
    }
    showSlide(currentSlideIndex);
}

// عرض سلايد معين
function showSlide(index) {
    // ✅ تحقق إضافي لضمان وجود السلايدات قبل الوصول لخصائصها
    if (slides.length === 0 || !slides[index]) return; //

    // إخفاء جميع السلايدات
    slides.forEach(slide => {
        slide.classList.remove('active');
    });
    
    // إزالة التفعيل من جميع النقاط
    dots.forEach(dot => {
        dot.classList.remove('active');
    });
    
    // عرض السلايد المطلوب
    slides[index].classList.add('active');
    if (dots[index]) dots[index].classList.add('active');
}

// الانتقال لسلايد معين عند الضغط على النقطة
function currentSlide(n) {
    currentSlideIndex = n - 1;
    showSlide(currentSlideIndex);
}

// ✅ تشغيل السلايدر فقط إذا كانت العناصر موجودة فعلياً في الصفحة
let slideInterval;
if (slides.length > 0) {
    slideInterval = setInterval(autoSlide, 2000);
}

// إيقاف التشغيل التلقائي عند التمرير فوق السلايدر (مع التحقق من وجوده)
const heroSlider = document.querySelector('.hero-slider');
if (heroSlider) { // ✅ هذا السطر يمنع خطأ null (reading 'addEventListener')
    heroSlider.addEventListener('mouseenter', () => {
        if (slideInterval) clearInterval(slideInterval);
    });

    heroSlider.addEventListener('mouseleave', () => {
        if (slides.length > 0) {
            slideInterval = setInterval(autoSlide, 2000);
        }
    });
}

// تفعيل زر "ابدأ رحلتك"
document.querySelectorAll('.hero-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const hotelSection = document.querySelector('.hotels-section');
        if (hotelSection) { // ✅ تحقق من وجود القسم قبل التمرير
            hotelSection.scrollIntoView({ 
                behavior: 'smooth' 
            });
        }
    });
});

// تفعيل روابط القائمة للتمرير السلس
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');
        
        if (href && href.startsWith('#') && href !== '#logout') {
            e.preventDefault();
            
            document.querySelectorAll('.nav-link').forEach(l => {
                l.classList.remove('active');
            });
            
            link.classList.add('active');
            
            const section = document.querySelector(href);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// تغيير الرابط النشط حسب موضع التمرير
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (current && link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
    
    // إذا كنا في أعلى الصفحة، فعّل رابط الرئيسية (مع التحقق من وجوده)
    if (window.pageYOffset < 300) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        const homeLink = document.querySelector('.nav-link[href="#"]');
        if (homeLink) homeLink.classList.add('active');
    }
});

// تأثير ظهور العناصر عند التمرير
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// تطبيق التأثير على الكروت والميزات
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.hotel-card, .feature').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
});