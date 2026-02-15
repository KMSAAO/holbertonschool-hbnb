/**
 * ملف: login.js
 * الوصف: إدارة عمليات تسجيل الدخول، إنشاء الحساب، والتحقق من صحة البيانات.
 */

// ==================== 1. وظائف الواجهة (UI Functions) ====================

function switchTab(tabName) {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => btn.classList.remove('active'));

    document.getElementById(tabName).classList.add('active');
    const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeBtn) activeBtn.classList.add('active');
}

function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.toggle-password-btn i');
    
    if (input.type === 'password') {
        input.type = 'text';
        button.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        button.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i> <span>${message}</span>`;
    
    // الأنماط البرمجية للإشعار
    notification.style.cssText = `position: fixed; top: 20px; right: 20px; background: ${type === 'success' ? '#4CAF50' : '#f44336'}; color: white; padding: 1rem 1.5rem; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.3); display: flex; align-items: center; gap: 0.8rem; font-family: 'Amiri', serif; font-size: 1.1rem; z-index: 10000; animation: slideInRight 0.3s ease;`;
    
    document.body.appendChild(notification);
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => { if (document.body.contains(notification)) document.body.removeChild(notification); }, 300);
    }, 2000);
}

// ==================== 2. معالجة البيانات (Auth Processing) ====================

// معالجة تسجيل الدخول (Login)
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!email || !password) {
        showNotification('الرجاء ملء جميع الحقول', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // 1. حفظ التوكن
            if (data.access_token) {
                document.cookie = `token=${data.access_token}; path=/`;
            }

            // 2. التقاط الـ ID (أهم خطوة!)
            // نتأكد من التقاطه سواء جاء باسم id أو user_id
            const userId = data.id || data.user_id;

            console.log("🔥 تم التقاط المعرف:", userId); // للتأكد في الكونسول

            // 3. حفظ كائن currentUser (هذا ما يبحث عنه admin.js)
            const userObj = {
                id: userId,
                first_name: data.first_name || 'مستخدم',
                last_name: data.last_name || '',
                email: email
            };
            localStorage.setItem('currentUser', JSON.stringify(userObj));

            // 4. حفظ القيم المنفصلة (عشان النافبار والملفات القديمة ما تزعل)
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('userFirstName', data.first_name || 'مستخدم');
            localStorage.setItem('userEmail', email);

            showNotification('تم تسجيل الدخول بنجاح', 'success');
            setTimeout(() => { window.location.href = '/'; }, 1000);

        } else {
            showNotification(data.message || 'فشل تسجيل الدخول', 'error');
        }
    } catch (error) {
        console.error('Login Error:', error);
        showNotification('حدث خطأ في الاتصال بالسيرفر', 'error');
    }
}

// معالجة إنشاء الحساب (Signup)
async function handleSignup(event) {
    event.preventDefault();
    
    // جلب القيم أولاً لتجنب خطأ التعريف
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();

    // فحص الأحرف العربية في كلمة المرور (ASCII Only)
    const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+$/;

    if (!passwordRegex.test(password)) {
        showNotification('كلمة المرور يجب أن تحتوي على أحرف إنجليزية وأرقام ورموز فقط', 'error');
        return;
    }

    const userData = { email, password, first_name: firstName, last_name: lastName };

    try {
        const response = await fetch('/api/v1/users/create_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });

        if (response.ok) {
            showNotification('تم إنشاء الحساب بنجاح! سجل دخولك الآن', 'success');
            switchTab('login');
        } else {
            const data = await response.json();
            showNotification(data.message || 'فشل إنشاء الحساب', 'error');
        }
    } catch (error) {
        showNotification('حدث خطأ في الاتصال', 'error');
    }
}

// ==================== 3. التحقق اللحظي (Live Validation) ====================

function validateSignupPassword() {
    const password = document.getElementById('signupPassword').value;
    const strengthIndicator = document.getElementById('signupPasswordStrength');
    const passwordRegex = /^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+$/;
    
    if (!password) {
        strengthIndicator.className = 'password-strength';
        return false;
    }

    // التحقق من اللغة (فحص فوري)
    if (!passwordRegex.test(password)) {
        strengthIndicator.className = 'password-strength weak';
        // يمكنك إضافة نص تنبيهي هنا
        return false;
    }
    
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
    
    if (strength <= 2) strengthIndicator.className = 'password-strength weak';
    else if (strength <= 4) strengthIndicator.className = 'password-strength medium';
    else strengthIndicator.className = 'password-strength strong';
    
    return strength === 5;
}

// ==================== 4. تهيئة الصفحة (Initialization) ====================

document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => switchTab(btn.getAttribute('data-tab')));
    });

    const loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.addEventListener('submit', handleLogin);

    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
        const signupPasswordInput = document.getElementById('signupPassword');
        if (signupPasswordInput) signupPasswordInput.addEventListener('input', validateSignupPassword);
    }
});