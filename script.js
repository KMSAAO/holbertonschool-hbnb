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

    try {
        // Use PlacesAPI wrapper from api-config.js to handle full URL and auth if needed
        const places = await PlacesAPI.getAll({ _sort: 'rating', _limit: 3 });

        container.innerHTML = ''; // Clear loading spinner

        if (places.length === 0) {
            container.innerHTML = '<p style="text-align:center; width:100%;">لا توجد وكهات متاحة حالياً</p>';
            return;
        }

        places.forEach(place => {
            const card = document.createElement('div');
            card.className = 'hotel-card';

            // Calculate rating stars
            let ratingHtml = '';
            // Determine rating: use average from reviews if available on the object, 
            // or we might need to calculate it if the API returns raw reviews.
            // Our backend get_top_places logic sorts by rating but returns Place objects.
            // Validating: Place objects usually have a 'reviews' list.

            let rating = 0;
            if (place.reviews && place.reviews.length > 0) {
                const sum = place.reviews.reduce((acc, r) => acc + r.rating, 0);
                rating = Math.round(sum / place.reviews.length);
            }

            for (let i = 0; i < 5; i++) {
                if (i < rating) {
                    ratingHtml += '<i class="fas fa-star"></i>';
                } else {
                    ratingHtml += '<i class="far fa-star"></i>';
                }
            }

            // Handle image - use first image or placeholder
            let imageUrl = 'images/hotel1.jpg'; // specific placeholder
            if (place.images && place.images.length > 0) {
                // Check if it's a string needing parse (API handles this usually)
                // If it's a list, take first.
                imageUrl = place.images[0];
            } else {
                // Random default for variety if no image, or just cyclic
                const defaults = ['images/hotel1.jpg', 'images/hotel2.jpg', 'images/hotel3.jpg'];
                // distinct based on id char?
                const idx = place.id.charCodeAt(0) % 3;
                imageUrl = defaults[idx];
            }

            // Safe access for price
            const price = (place.price !== null && place.price !== undefined)
                ? place.price.toLocaleString()
                : 'N/A';

            card.innerHTML = `
                <div class="hotel-image">
                    <img src="${imageUrl}" alt="${place.title}">
                    <div class="hotel-rating">
                        ${ratingHtml}
                    </div>
                </div>
                <div class="hotel-info">
                    <h3 class="hotel-name">${place.title}</h3>
                    <div class="hotel-price">
                        <span class="price-amount">${price}</span>
                        <span class="price-currency">ر.س</span>
                        <span class="price-per">/الليلة</span>
                    </div>
                    <button class="details-btn" onclick="showLoadingScreen('hotel-details.html?hotel=${place.id}')">عرض التفاصيل</button>
                </div>
            `;

            // Initial style for animation
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease-out';

            container.appendChild(card);

            // Observe for animation
            observer.observe(card);
        });

    } catch (error) {
        console.error('Error loading hotels:', error);
        container.innerHTML = '<p style="text-align:center; width:100%; color:red;">حدث خطأ أثناء تحميل الفنادق. يرجى المحاولة لاحقاً.</p>';
    }
}
