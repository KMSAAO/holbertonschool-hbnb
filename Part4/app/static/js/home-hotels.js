// ==================== تحميل الفنادق في الصفحة الرئيسية ====================

// دالة لإنشاء كارت الفندق
function createHotelCard(hotel) {
    const card = document.createElement('div');
    card.className = 'hotel-card';
    
    // حساب عدد النجوم
    const stars = '★'.repeat(hotel.rating || 5);
    
    // الحصول على أقل سعر من الغرف
    let minPrice = Infinity;
    if (hotel.rooms && hotel.rooms.length > 0) {
        hotel.rooms.forEach(room => {
            if (room.price < minPrice) {
                minPrice = room.price;
            }
        });
    }
    
    // إذا لم يكن هناك غرف، استخدم السعر الأساسي
    if (minPrice === Infinity) {
        minPrice = hotel.basePrice || 0;
    }
    
    card.innerHTML = `
        <div class="hotel-image">
            <img src="${hotel.mainImage || hotel.images[0]}" alt="${hotel.nameAr}">
            <div class="hotel-rating">
                ${Array(hotel.rating || 5).fill('<i class="fas fa-star"></i>').join('')}
            </div>
        </div>
        <div class="hotel-info">
            <h3 class="hotel-name">${hotel.nameAr}</h3>
            <div class="hotel-price">
                <span class="price-amount">${minPrice.toLocaleString('ar-SA')}</span>
                <span class="price-currency">ر.س</span>
                <span class="price-per">/الليلة</span>
            </div>
            <button class="details-btn" onclick="showLoadingScreen('hotel-details.html?hotel=${hotel.id}')">عرض التفاصيل</button>
        </div>
    `;
    
    return card;
}

// دالة لتحميل الفنادق
function loadHomeHotels() {
    const container = document.getElementById('hotelsContainer');
    
    if (!container) {
        console.error('لم يتم العثور على حاوية الفنادق');
        return;
    }
    
    // مسح المحتوى الحالي
    container.innerHTML = '';
    
    // جلب الفنادق من hotels-data.js
    if (typeof hotelsDetailsData === 'undefined') {
        console.error('لم يتم تحميل بيانات الفنادق');
        container.innerHTML = '<p style="text-align: center; padding: 40px;">لا توجد فنادق متاحة حالياً</p>';
        return;
    }
    
    // عرض أول 3 فنادق فقط في الصفحة الرئيسية
    const featuredHotels = Object.values(hotelsDetailsData).slice(0, 3);
    
    featuredHotels.forEach(hotel => {
        const card = createHotelCard(hotel);
        container.appendChild(card);
    });
}

// تحميل الفنادق عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', loadHomeHotels);
