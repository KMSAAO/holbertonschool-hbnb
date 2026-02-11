/**
 * ملف: user-hotels.js
 * الوصف: عرض الفنادق المضافة من المستخدمين في صفحة الوجهات
 * الوظيفة: قراءة البيانات من localStorage وإضافتها ديناميكياً للصفحة
 */

// عرض الفنادق المضافة من المستخدمين في صفحة الوجهات
document.addEventListener('DOMContentLoaded', () => {
    const destinationsGrid = document.querySelector('.destinations-grid');
    if (!destinationsGrid) return;
    
    const userHotels = JSON.parse(localStorage.getItem('userHotels') || '[]');
    
    userHotels.forEach(hotel => {
        const card = document.createElement('div');
        card.className = 'destination-card';
        card.innerHTML = `
            <div class="destination-image-container">
                <img src="${hotel.images[0] || 'images/default-hotel.jpg'}" alt="${hotel.name}">
                <div class="rating-badge">
                    <i class="fas fa-star"></i>
                    <span>جديد</span>
                </div>
            </div>
            <div class="destination-info">
                <h3 class="destination-title">${hotel.name}</h3>
                <p class="destination-location">
                    <i class="fas fa-map-marker-alt"></i>
                    ${hotel.location}
                </p>
                <div class="destination-price">
                    <span class="price-label">يبدأ من</span>
                    <span class="price-amount">${hotel.startPrice.toLocaleString('ar-EG')} ر.س</span>
                    <span class="price-period">لليلة</span>
                </div>
                <button class="book-btn" onclick="showLoadingScreen('hotel-details.html?hotel=${hotel.id}')">
                    <i class="fas fa-calendar-check"></i>
                    احجز الآن
                </button>
            </div>
        `;
        destinationsGrid.appendChild(card);
    });
});
