// السلايدر الأوتوماتيكي للهيدر
let currentSlideIndex = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

// تشغيل السلايدر تلقائياً
function autoSlide() {
    currentSlideIndex++;
    if (currentSlideIndex >= slides.length) {
        currentSlideIndex = 0;
    }
    showSlide(currentSlideIndex);
}

// عرض سلايد معين
function showSlide(index) {
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
    dots[index].classList.add('active');
}

// الانتقال لسلايد معين عند الضغط على النقطة
function currentSlide(n) {
    currentSlideIndex = n - 1;
    showSlide(currentSlideIndex);
}

// تشغيل السلايدر كل ثانيتين
let slideInterval = setInterval(autoSlide, 2000);

// إيقاف التشغيل التلقائي عند التمرير فوق السلايدر
document.querySelector('.hero-slider').addEventListener('mouseenter', () => {
    clearInterval(slideInterval);
});

// استئناف التشغيل التلقائي عند مغادرة السلايدر
document.querySelector('.hero-slider').addEventListener('mouseleave', () => {
    slideInterval = setInterval(autoSlide, 2000);
});

// تفعيل زر "ابدأ رحلتك"
document.querySelectorAll('.hero-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        // التمرير إلى قسم الفنادق
        document.querySelector('.hotels-section').scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// تفعيل روابط القائمة للتمرير السلس
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        const href = link.getAttribute('href');

        // إذا كان الرابط يشير إلى قسم في الصفحة
        if (href.startsWith('#') && href !== '#logout') {
            e.preventDefault();

            // إزالة الكلاس active من جميع الروابط
            document.querySelectorAll('.nav-link').forEach(l => {
                l.classList.remove('active');
            });

            // إضافة الكلاس active للرابط الحالي
            link.classList.add('active');

            // التمرير للقسم المطلوب
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
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });

    // إذا كنا في أعلى الصفحة، فعّل رابط الرئيسية
    if (window.pageYOffset < 300) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector('.nav-link[href="#"]').classList.add('active');
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
    // Load top rated hotels if on the index page
    const topHotelsContainer = document.getElementById('top-rated-hotels-list');
    if (topHotelsContainer) {
        loadTopHotels();
    }

    document.querySelectorAll('.feature').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
});

async function loadTopHotels() {
    const container = document.getElementById('top-rated-hotels-list');
    if (!container) return;

    try {
        // نرسل الطلب لجلب البيانات
        const places = await PlacesAPI.getAll({ _sort: 'rating', _limit: 3 });

        // --- الخطوة الأهم: مسح علامة التحميل فور وصول الرد ---
        container.innerHTML = ''; 

        if (!places || places.length === 0) {
            container.innerHTML = '<p style="text-align:center; width:100%;">لا توجد وجهات متاحة حالياً</p>';
            return;
        }

        places.forEach(place => {
            const card = document.createElement('div');
            card.className = 'hotel-card';

            // حساب التقييم (Rating)
            let rating = 0;
            if (place.reviews && place.reviews.length > 0) {
                const sum = place.reviews.reduce((acc, r) => acc + r.rating, 0);
                rating = Math.round(sum / place.reviews.length);
            }

            let ratingHtml = '';
            for (let i = 0; i < 5; i++) {
                ratingHtml += i < rating ? '<i class="fas fa-star"></i>' : '<i class="far fa-star"></i>';
            }

            // معالجة الصور (Image Handling)
            let imageUrl = 'images/hotel1.jpg'; 
            if (place.images && place.images.length > 0) {
                imageUrl = place.images[0];
            }

            const price = (place.price !== null && place.price !== undefined) ? place.price.toLocaleString() : 'N/A';

            card.innerHTML = `
                <div class="hotel-image">
                    <img src="${imageUrl}" alt="${place.title}">
                    <div class="hotel-rating">${ratingHtml}</div>
                </div>
                <div class="hotel-info">
                    <h3 class="hotel-name">${place.title}</h3>
                    <div class="hotel-price">
                        <span class="price-amount">${price}</span>
                        <span class="price-currency"> ر.س</span>
                        <span class="price-per">/الليلة</span>
                    </div>
                    <button class="details-btn" onclick="window.location.href='hotel-details.html?hotel=${place.id}'">عرض التفاصيل</button>
                </div>
            `;

            // إعدادات الأنيميشن الابتدائية
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease-out';

            container.appendChild(card);
            observer.observe(card); // الآن ستعمل لأننا عرفنا الـ observer في الأعلى
        });

    } catch (error) {
        console.error('Error loading hotels:', error);
        container.innerHTML = '<p style="text-align:center; width:100%; color:red;">حدث خطأ أثناء تحميل الفنادق. تأكد من تشغيل السيرفر.</p>';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const isAdmin = localStorage.getItem('is_admin') === 'true';
    const adminLink = document.querySelector('a[href="admindash.html"]');
    if (adminLink) {
        adminLink.style.display = isAdmin ? 'inline-block' : 'none';
    }
});


function updateNavbar() {
    const token = localStorage.getItem('access_token');
    // إذا لم يوجد توكن، نعتبره ليس أدمن تلقائياً لتجنب القيم القديمة
    const isAdmin = token ? (localStorage.getItem('is_admin') === 'true') : false;

    // جلب العناصر مع التحقق من وجودها في الصفحة
    const adminLink = document.getElementById('adminLink');
    const nuzulLink = document.getElementById('nuzulLink');
    const loginLink = document.getElementById('loginLink');
    const logoutLink = document.getElementById('logoutLink');
    const profileContainer = document.getElementById('profileContainer');

    if (token) {
        // --- حالة تسجيل الدخول ---
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'inline-block';
        if (profileContainer) profileContainer.style.display = 'flex';
        
        // إظهار روابط الإدارة فقط للأدمن
        const adminDisplay = isAdmin ? 'inline-block' : 'none';
        if (adminLink) adminLink.style.display = adminDisplay;
    } else {
        // --- حالة تسجيل الخروج (إخفاء كل شيء حساس) ---
        if (loginLink) loginLink.style.display = 'inline-block';
        if (logoutLink) logoutLink.style.display = 'none';
        if (adminLink) adminLink.style.display = 'none';
        if (nuzulLink) nuzulLink.style.display = 'none';
        if (profileContainer) profileContainer.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', updateNavbar);