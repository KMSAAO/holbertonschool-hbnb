// إظهار شاشة التحميل عند الانتقال للملف الشخصي
function showLoadingScreen(targetUrl) {
    // إنشاء شاشة التحميل
    const loadingScreen = document.createElement('div');
    loadingScreen.className = 'loading-screen';
    loadingScreen.innerHTML = `
        <div class="loading-dots">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
        <div class="loading-text">جاري التحميل...</div>
    `;
    
    document.body.appendChild(loadingScreen);
    
    // بعد ثانية، إخفاء الشاشة والانتقال
    setTimeout(() => {
        loadingScreen.classList.add('fade-out');
        setTimeout(() => {
            window.location.href = targetUrl;
        }, 200);
    }, 1000);
}

// إضافة حدث للأيقونة في الصفحات
document.addEventListener('DOMContentLoaded', () => {
    const profileLinks = document.querySelectorAll('a[href="profile.html"]');
    
    profileLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            // منع الانتقال المباشر
            e.preventDefault();
            
            // إظهار شاشة التحميل
            showLoadingScreen('profile.html');
        });
    });
});
