// التبديل بين تسجيل الدخول وإنشاء الحساب
function switchTab(tabName) {
    // إخفاء جميع المحتويات
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });

    // إلغاء تفعيل جميع الأزرار
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.classList.remove('active');
    });

    // تفعيل التبويب المطلوب
    document.getElementById(tabName).classList.add('active');
    const activeBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
}

// إظهار/إخفاء كلمة المرور
function togglePasswordVisibility(inputId) {
    const input = document.getElementById(inputId);
    const button = input.parentElement.querySelector('.toggle-password-btn i');
    
    if (input.type === 'password') {
        input.type = 'text';
        button.classList.remove('fa-eye');
        button.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        button.classList.remove('fa-eye-slash');
        button.classList.add('fa-eye');
    }
}

// عرض إشعار
function showNotification(message, type) {
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
    }, 1500);
}

// التحقق من صحة البريد الإلكتروني
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// التحقق من صحة كلمة المرور
function validatePassword(password) {
    // 8 أحرف على الأقل، حرف كبير، حرف صغير، رقم، رمز خاص
    const lengthValid = password.length >= 8;
    const uppercaseValid = /[A-Z]/.test(password);
    const lowercaseValid = /[a-z]/.test(password);
    const numberValid = /[0-9]/.test(password);
    const specialValid = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    
    return lengthValid && uppercaseValid && lowercaseValid && numberValid && specialValid;
}

// معالجة تسجيل الدخول
function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;
    
    if (!email || !password) {
        showNotification('الرجاء ملء جميع الحقول', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showNotification('الرجاء إدخال بريد إلكتروني صحيح', 'error');
        return;
    }
    
    // هنا سيتم التحقق من البيانات مع قاعدة البيانات
    // مثال: إذا كانت البيانات صحيحة
    
    // حفظ بيانات المستخدم في localStorage
    if (typeof saveUserSession === 'function') {
        saveUserSession({
            firstName: 'أميرة', // سيتم استبدالها ببيانات من قاعدة البيانات
            lastName: 'السلطان',
            email: email,
            gender: 'female'
        });
    }
    
    showNotification('تم تسجيل الدخول بنجاح', 'success');
    
    // إظهار شاشة التحميل والتوجيه للصفحة الرئيسية
    setTimeout(() => {
        if (typeof showLoadingScreen === 'function') {
            showLoadingScreen('index.html');
        } else {
            window.location.href = 'index.html';
        }
    }, 800);
}

// معالجة إنشاء الحساب
function handleSignup(event) {
    event.preventDefault();
    
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    const termsAccepted = document.getElementById('termsCheckbox').checked;
    
    if (!firstName || !lastName || !email || !password || !confirmPassword) {
        showNotification('الرجاء ملء جميع الحقول', 'error');
        return;
    }
    
    if (!validateEmail(email)) {
        showNotification('الرجاء إدخال بريد إلكتروني صحيح', 'error');
        return;
    }
    
    if (!validateSignupPassword()) {
        showNotification('كلمة المرور لا تستوفي المتطلبات', 'error');
        return;
    }
    
    if (password !== confirmPassword) {
        showNotification('كلمتا المرور غير متطابقتين', 'error');
        return;
    }
    
    if (!termsAccepted) {
        showNotification('يجب الموافقة على شروط الاستخدام', 'error');
        return;
    }
    
    // هنا سيتم حفظ البيانات في قاعدة البيانات
    
    // حفظ بيانات المستخدم في localStorage
    if (typeof saveUserSession === 'function') {
        saveUserSession({
            firstName: firstName,
            lastName: lastName,
            email: email,
            gender: 'female' // افتراضي
        });
    }
    
    showNotification('تم إنشاء الحساب بنجاح', 'success');
    
    // إظهار شاشة التحميل والتوجيه للصفحة الرئيسية
    setTimeout(() => {
        if (typeof showLoadingScreen === 'function') {
            showLoadingScreen('index.html');
        } else {
            window.location.href = 'index.html';
        }
    }, 800);
}

// التحقق من متطلبات كلمة المرور في صفحة إنشاء الحساب
function validateSignupPassword() {
    const password = document.getElementById('signupPassword').value;
    const strengthIndicator = document.getElementById('signupPasswordStrength');
    
    if (!password) {
        strengthIndicator.className = 'password-strength';
        return false;
    }
    
    let strength = 0;
    
    // التحقق من الطول
    if (password.length >= 8) strength++;
    
    // التحقق من الأحرف الكبيرة
    if (/[A-Z]/.test(password)) strength++;
    
    // التحقق من الأحرف الصغيرة
    if (/[a-z]/.test(password)) strength++;
    
    // التحقق من الأرقام
    if (/[0-9]/.test(password)) strength++;
    
    // التحقق من الرموز الخاصة
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++;
    
    // تحديث مؤشر القوة
    if (strength <= 2) {
        strengthIndicator.className = 'password-strength weak';
    } else if (strength <= 4) {
        strengthIndicator.className = 'password-strength medium';
    } else {
        strengthIndicator.className = 'password-strength strong';
    }
    
    // كلمة المرور قوية إذا استوفت جميع الشروط
    return strength === 5;
}

// تحديث حالة المتطلب في صفحة إنشاء الحساب
function updateSignupRequirement(id, isValid) {
    const element = document.getElementById(id);
    if (element) {
        if (isValid) {
            element.classList.add('valid');
            element.querySelector('i').classList.remove('fa-circle');
            element.querySelector('i').classList.add('fa-check-circle');
        } else {
            element.classList.remove('valid');
            element.querySelector('i').classList.remove('fa-check-circle');
            element.querySelector('i').classList.add('fa-circle');
        }
    }
}

// إضافة أنماط الرسوم المتحركة
const style = document.createElement('style');
style.textContent = `
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
`;
document.head.appendChild(style);

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', () => {
    // إضافة مستمعي الأحداث للتبويبات
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // إضافة مستمعي الأحداث للنماذج
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
        
        // إضافة مستمع للتحقق من كلمة المرور في صفحة إنشاء الحساب
        const signupPasswordInput = document.getElementById('signupPassword');
        if (signupPasswordInput) {
            signupPasswordInput.addEventListener('input', validateSignupPassword);
        }
    }
});
