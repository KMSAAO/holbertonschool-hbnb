// إدارة حالة تسجيل الدخول

// التحقق من حالة تسجيل الدخول
function isLoggedIn() {
    return localStorage.getItem('isLoggedIn') === 'true';
}

// الحصول على معلومات المستخدم
function getUserInfo() {
    return {
        firstName: localStorage.getItem('userFirstName') || '',
        lastName: localStorage.getItem('userLastName') || '',
        email: localStorage.getItem('userEmail') || '',
        gender: localStorage.getItem('userGender') || 'female'
    };
}

// حفظ معلومات المستخدم عند تسجيل الدخول
function saveUserSession(userData) {
    localStorage.setItem('isLoggedIn', 'true');
    localStorage.setItem('userFirstName', userData.firstName || '');
    localStorage.setItem('userLastName', userData.lastName || '');
    localStorage.setItem('userEmail', userData.email || '');
    localStorage.setItem('userGender', userData.gender || 'female');
}

// تسجيل الخروج
function logout() {
    // تسجيل الخروج مباشرة بدون تأكيد
    performLogout();
}

// عرض مربع تأكيد تسجيل الخروج
function showLogoutConfirmation() {
    // إنشاء overlay
    const overlay = document.createElement('div');
    overlay.className = 'logout-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease;
    `;
    
    // إنشاء مربع التأكيد
    const confirmBox = document.createElement('div');
    confirmBox.className = 'logout-confirm-box';
    confirmBox.style.cssText = `
        background: #EFE2CF;
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 450px;
        width: 90%;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: slideUp 0.3s ease;
        font-family: 'Amiri', serif;
    `;
    
    confirmBox.innerHTML = `
        <div style="font-size: 4rem; margin-bottom: 1rem;">😢</div>
        <h2 style="color: #815B2F; font-size: 1.8rem; margin-bottom: 1rem; font-weight: 700;">
            هل أنت متأكد؟
        </h2>
        <p style="color: #815B2F; font-size: 1.3rem; margin-bottom: 2rem; line-height: 1.8;">
            نحن حزينون لأنك سوف تغادرنا 😔💔
        </p>
        <div style="display: flex; gap: 1rem; justify-content: center;">
            <button id="confirmLogoutBtn" style="
                padding: 1rem 2rem;
                background: #815B2F;
                color: #EFE2CF;
                border: none;
                border-radius: 12px;
                font-family: 'Amiri', serif;
                font-size: 1.2rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s ease;
                flex: 1;
            ">
                نعم، تسجيل الخروج
            </button>
            <button id="cancelLogoutBtn" style="
                padding: 1rem 2rem;
                background: transparent;
                color: #815B2F;
                border: 2px solid #815B2F;
                border-radius: 12px;
                font-family: 'Amiri', serif;
                font-size: 1.2rem;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.3s ease;
                flex: 1;
            ">
                إلغاء
            </button>
        </div>
    `;
    
    overlay.appendChild(confirmBox);
    document.body.appendChild(overlay);
    
    // إضافة تأثيرات hover للأزرار
    const confirmBtn = document.getElementById('confirmLogoutBtn');
    const cancelBtn = document.getElementById('cancelLogoutBtn');
    
    confirmBtn.onmouseover = () => {
        confirmBtn.style.background = '#6B4A26';
        confirmBtn.style.transform = 'translateY(-2px)';
        confirmBtn.style.boxShadow = '0 5px 15px rgba(129, 91, 47, 0.3)';
    };
    confirmBtn.onmouseout = () => {
        confirmBtn.style.background = '#815B2F';
        confirmBtn.style.transform = 'translateY(0)';
        confirmBtn.style.boxShadow = 'none';
    };
    
    cancelBtn.onmouseover = () => {
        cancelBtn.style.background = '#815B2F';
        cancelBtn.style.color = '#EFE2CF';
        cancelBtn.style.transform = 'translateY(-2px)';
        cancelBtn.style.boxShadow = '0 5px 15px rgba(129, 91, 47, 0.2)';
    };
    cancelBtn.onmouseout = () => {
        cancelBtn.style.background = 'transparent';
        cancelBtn.style.color = '#815B2F';
        cancelBtn.style.transform = 'translateY(0)';
        cancelBtn.style.boxShadow = 'none';
    };
    
    // معالجة النقر على نعم
    confirmBtn.onclick = () => {
        overlay.remove();
        performLogout();
    };
    
    // معالجة النقر على إلغاء
    cancelBtn.onclick = () => {
        overlay.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            overlay.remove();
        }, 300);
    };
    
    // إغلاق عند النقر على الخلفية
    overlay.onclick = (e) => {
        if (e.target === overlay) {
            overlay.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    };
}

// تنفيذ تسجيل الخروج الفعلي
function performLogout() {
    // حذف جميع بيانات المستخدم
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('userFirstName');
    localStorage.removeItem('userLastName');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('userGender');
    
    // حفظ علامة للإشعار
    localStorage.setItem('showLogoutMessage', 'true');
    
    // إظهار شاشة التحميل
    if (typeof showLoadingScreen === 'function') {
        showLoadingScreen('index.html');
    } else {
        window.location.href = 'index.html';
    }
}

// تحديث navbar حسب حالة تسجيل الدخول
function updateNavbar() {
    const loggedIn = isLoggedIn();
    console.log('تحديث Navbar - هل مسجل دخول؟', loggedIn);
    console.log('بيانات المستخدم:', getUserInfo());
    
    // العناصر التي تظهر فقط للمسجلين
    const bookingsLink = document.getElementById('bookingsLink');
    const logoutLink = document.getElementById('logoutLink');
    const profileCircle = document.querySelector('.profile-circle');
    const adminLink = document.querySelector('a[href="/admin"]');
    
    // العناصر التي تظهر فقط لغير المسجلين
    const loginLink = document.getElementById('loginLink');
    
    console.log('العناصر:', {
        bookingsLink: bookingsLink,
        logoutLink: logoutLink,
        profileCircle: profileCircle,
        adminLink: adminLink,
        loginLink: loginLink
    });
    
    if (loggedIn) {
        // المستخدم مسجل دخول
        console.log('المستخدم مسجل - تحديث العناصر');
        if (bookingsLink) bookingsLink.style.display = 'inline-block';
        if (logoutLink) logoutLink.style.display = 'inline-block';
        if (adminLink) adminLink.style.display = 'inline-block';
        if (profileCircle) {
            profileCircle.style.display = 'flex';
            profileCircle.style.pointerEvents = 'auto';
            profileCircle.style.cursor = 'pointer';
        }
        if (loginLink) loginLink.style.display = 'none';
    } else {
        // المستخدم غير مسجل
        console.log('المستخدم غير مسجل - إخفاء العناصر');
        if (bookingsLink) bookingsLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'none';
        if (adminLink) adminLink.style.display = 'none';
        if (profileCircle) {
            profileCircle.style.display = 'none';
        }
        if (loginLink) loginLink.style.display = 'inline-block';
    }
}

// التحقق من الصفحات المحمية
function checkProtectedPage() {
    const currentPage = window.location.pathname.split('/').pop();
    const protectedPages = ['profile.html', 'bookings.html'];
    
    if (protectedPages.includes(currentPage) && !isLoggedIn()) {
        // إذا كان في صفحة محمية وغير مسجل، يوجهه لتسجيل الدخول
        showNotification('يجب تسجيل الدخول أولاً', 'error');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
        return false;
    }
    return true;
}

// منع الوصول لرابط الحجوزات
function handleBookingsClick(event) {
    if (!isLoggedIn()) {
        event.preventDefault();
        showNotification('يجب تسجيل الدخول لعرض الحجوزات', 'error');
        setTimeout(() => {
            window.location.href = 'login.html';
        }, 1500);
    }
}

// عرض إشعار
function showNotification(message, type) {
    // التحقق من وجود إشعار سابق
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : '#f44336'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font-family: 'Amiri', serif;
        font-size: 1.1rem;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// إضافة أنماط الرسوم المتحركة
const authStyle = document.createElement('style');
authStyle.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(-100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeOut {
        from {
            opacity: 1;
        }
        to {
            opacity: 0;
        }
    }
    
    @keyframes slideUp {
        from {
            transform: translateY(50px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(authStyle);

// تشغيل updateNavbar فوراً
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAuth);
} else {
    initAuth();
}

function initAuth() {
    // تحديث navbar
    updateNavbar();
    
    // التحقق من الصفحات المحمية
    checkProtectedPage();
    
    // إضافة مستمع لرابط الحجوزات
    const bookingsLink = document.getElementById('bookingsLink');
    if (bookingsLink) {
        bookingsLink.addEventListener('click', handleBookingsClick);
    }
    
    // عرض رسالة الخروج إذا كانت موجودة
    if (localStorage.getItem('showLogoutMessage') === 'true') {
        localStorage.removeItem('showLogoutMessage');
        setTimeout(() => {
            showNotification('نراك قريباً! 👋', 'success');
        }, 300);
    }
}
