// login.js - النسخة النهائية (شاملة التحقق والربط الصحيح)

// ==========================================
// 1. دوال الواجهة (UI Functions)
// ==========================================

// التبديل بين تسجيل الدخول وإنشاء الحساب
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });

    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    const targetContent = document.getElementById(tabName);
    const targetBtn = document.querySelector(`[data-tab="${tabName}"]`);

    if (targetContent) targetContent.classList.add('active');
    if (targetBtn) targetBtn.classList.add('active');
}

// إظهار/إخفاء كلمة المرور
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    const icon = input.nextElementSibling.querySelector('i');

    if (input.type === 'password') {
        input.type = 'text';
        if (icon) {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        }
    } else {
        input.type = 'password';
        if (icon) {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }
}

function toggleAdminCodeField() {
    const isAdminCheckbox = document.getElementById('signupIsAdmin');
    const adminCodeGroup = document.getElementById('adminCodeGroup');
    const adminCodeInput = document.getElementById('signupAdminCode');

    if (!isAdminCheckbox || !adminCodeGroup || !adminCodeInput) return;

    if (isAdminCheckbox.checked) {
        adminCodeGroup.style.display = 'block';
        adminCodeInput.required = true;
    } else {
        adminCodeGroup.style.display = 'none';
        adminCodeInput.required = false;
        adminCodeInput.value = '';
    }
}

// دالة عرض الإشعارات
function showNotification(message, type = 'error') {
    // إزالة أي إشعار قديم إن وجد
    const oldNotification = document.querySelector('.notification');
    if (oldNotification) oldNotification.remove();

    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.style.cssText = `
        position: fixed; top: 20px; right: 20px;
        background: ${type === 'success' ? '#4CAF50' : '#f44336'};
        color: white; padding: 15px 20px; border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 10000;
        font-family: 'Amiri', serif; font-size: 1.1rem;
        transition: opacity 0.5s ease;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// ==========================================
// 2. دوال الاتصال بالسيرفر (API Logic)
// ==========================================

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    if (!email || !password) {
        showNotification('الرجاء ملء جميع الحقول', 'error');
        return;
    }

    try {
        // 1. تسجيل الدخول والحصول على التوكن
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // 2. حفظ التوكن
            localStorage.setItem('access_token', data.access_token);

            // 3. فك تشفير JWT للحصول على user_id
            let userId = '';
            try {
                const tokenParts = data.access_token.split('.');
                const payload = JSON.parse(atob(tokenParts[1]));
                userId = payload.sub || payload.identity || '';
            } catch (e) {
                console.warn('تعذر فك تشفير JWT:', e);
            }

            // 4. جلب بيانات المستخدم من الـ backend
            if (userId) {
                localStorage.setItem('userId', userId);
                try {
                    const userResponse = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${data.access_token}`
                        }
                    });
                    if (userResponse.ok) {
                        const userData = await userResponse.json();
                        // 5. حفظ جلسة المستخدم (يربط مع auth.js)
                        saveUserSession({
                            firstName: userData.first_name || '',
                            lastName: userData.last_name || '',
                            email: userData.email || email,
                            gender: userData.gender || 'female'
                        });
                    } else {
                        // حفظ بيانات أساسية إذا فشل جلب المستخدم
                        saveUserSession({
                            firstName: '',
                            lastName: '',
                            email: email,
                            gender: 'female'
                        });
                    }
                } catch (fetchErr) {
                    console.warn('تعذر جلب بيانات المستخدم:', fetchErr);
                    saveUserSession({ firstName: '', lastName: '', email: email, gender: 'female' });
                }
            } else {
                // حفظ جلسة بدون userId
                saveUserSession({ firstName: '', lastName: '', email: email, gender: 'female' });
            }

            showNotification('تم تسجيل الدخول بنجاح', 'success');
            setTimeout(() => { window.location.href = 'index.html'; }, 800);
        } else {
            const errorMessage = data.message || data.error || 'بيانات الدخول غير صحيحة';
            showNotification(errorMessage, 'error');
        }
    } catch (error) {
        console.error(error);
        showNotification('تعذر الاتصال بالسيرفر. تأكد من تشغيل run.py', 'error');
    }
}

async function handleSignup(event) {
    event.preventDefault();

    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    const isAdmin = !!document.getElementById('signupIsAdmin')?.checked;
    const adminCode = document.getElementById('signupAdminCode')?.value || '';

    // --- التحقق من الشروط (Validations) ---

    // 1. الاسم الأول
    if (!firstName || firstName.length > 50) {
        showNotification('الاسم الأول مطلوب ويجب أن لا يتجاوز 50 حرفاً', 'error');
        return;
    }

    // 2. الاسم الأخير
    if (!lastName || lastName.length > 50) {
        showNotification('الاسم الأخير مطلوب ويجب أن لا يتجاوز 50 حرفاً', 'error');
        return;
    }

    // 3. البريد الإلكتروني (Regex)
    const emailPattern = /^[\w\.-]+@[\w\.-]+\.\w+$/;
    if (!email || !emailPattern.test(email)) {
        showNotification('صيغة البريد الإلكتروني غير صحيحة', 'error');
        return;
    }

    // 4. كلمة المرور (الطول)
    if (!password || password.length < 6) {
        showNotification('كلمة المرور يجب أن تكون 6 خانات على الأقل', 'error');
        return;
    }

    // 5. تطابق كلمة المرور
    if (password !== confirmPassword) {
        showNotification('كلمتا المرور غير متطابقتين', 'error');
        return;
    }

    if (isAdmin && !adminCode.trim()) {
        showNotification('الرجاء إدخال كود المسؤول', 'error');
        return;
    }

    try {
        // لاحظ: الرابط بدون شرطة في النهاية لتجنب مشاكل CORS
        const response = await fetch('http://127.0.0.1:5000/api/v1/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                first_name: firstName,
                last_name: lastName,
                email: email,
                password: password,
                is_admin: isAdmin,
                admin_code: adminCode.trim()
            })
        });

        const data = await response.json();

        if (response.ok) {
            showNotification('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول', 'success');
            setTimeout(() => { switchTab('login'); }, 1500);
        } else {
            const errorMsg = data.message || data.error || 'فشل إنشاء الحساب';
            showNotification(errorMsg, 'error');
        }
    } catch (error) {
        console.error(error);
        showNotification('حدث خطأ أثناء الاتصال بالخادم', 'error');
    }
}

// ==========================================
// 3. تهيئة الصفحة والربط (Initialization)
// ==========================================

document.addEventListener('DOMContentLoaded', () => {

    // ربط أزرار التبويبات
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // ربط فورم تسجيل الدخول
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.removeEventListener('submit', handleLogin);
        loginForm.addEventListener('submit', handleLogin);
    }

    // ربط فورم إنشاء الحساب
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.removeEventListener('submit', handleSignup);
        signupForm.addEventListener('submit', handleSignup);
    }

    const isAdminCheckbox = document.getElementById('signupIsAdmin');
    if (isAdminCheckbox) {
        isAdminCheckbox.addEventListener('change', toggleAdminCodeField);
        toggleAdminCodeField();
    }
});
