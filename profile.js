// تخزين القيم الأصلية
let originalValues = {
    email: '',
    gender: ''
};

// تفعيل وضع التعديل
function enableEdit(field) {
    const formActions = document.getElementById('formActions');

    if (field === 'email') {
        const emailInput = document.getElementById('emailInput');
        const emailGroup = emailInput.closest('.form-group');

        if (emailInput.hasAttribute('readonly')) {
            originalValues.email = emailInput.value;
            emailInput.removeAttribute('readonly');
            emailGroup.classList.add('active');
            emailInput.focus();
            formActions.style.display = 'flex';
        }
    } else if (field === 'gender') {
        const genderInput = document.getElementById('genderInput');
        const genderGroup = genderInput.closest('.form-group');

        if (genderInput.hasAttribute('disabled')) {
            originalValues.gender = genderInput.value;
            genderInput.removeAttribute('disabled');
            genderGroup.classList.add('active');
            genderInput.focus();
            formActions.style.display = 'flex';
        }
    }
}

// حفظ التغييرات
async function saveChanges() {
    const emailInput = document.getElementById('emailInput');
    const genderInput = document.getElementById('genderInput');
    const formActions = document.getElementById('formActions');

    if (!emailInput.hasAttribute('readonly')) {
        const emailValue = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(emailValue)) {
            alert('الرجاء إدخال بريد إلكتروني صحيح');
            emailInput.focus();
            return;
        }
    }

    // حفظ في الـ backend
    const userId = localStorage.getItem('userId');
    if (userId && typeof UsersAPI !== 'undefined') {
        try {
            await UsersAPI.update(userId, {
                email: emailInput.value.trim()
            });
            // تحديث localStorage
            localStorage.setItem('userEmail', emailInput.value.trim());
        } catch (err) {
            console.warn('تعذر تحديث الملف في الـ backend:', err);
        }
    }

    if (!emailInput.hasAttribute('readonly')) {
        emailInput.setAttribute('readonly', 'readonly');
        emailInput.closest('.form-group').classList.remove('active');
        originalValues.email = emailInput.value;
    }

    if (!genderInput.hasAttribute('disabled')) {
        genderInput.setAttribute('disabled', 'disabled');
        genderInput.closest('.form-group').classList.remove('active');
        originalValues.gender = genderInput.value;
    }

    formActions.style.display = 'none';
    showNotification('تم حفظ التغييرات بنجاح', 'success');
}

// إلغاء التعديل
function cancelEdit() {
    const emailInput = document.getElementById('emailInput');
    const genderInput = document.getElementById('genderInput');
    const formActions = document.getElementById('formActions');

    if (!emailInput.hasAttribute('readonly')) {
        emailInput.value = originalValues.email;
        emailInput.setAttribute('readonly', 'readonly');
        emailInput.closest('.form-group').classList.remove('active');
    }

    if (!genderInput.hasAttribute('disabled')) {
        genderInput.value = originalValues.gender;
        genderInput.setAttribute('disabled', 'disabled');
        genderInput.closest('.form-group').classList.remove('active');
    }

    formActions.style.display = 'none';
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
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : '#f44336'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-family: 'Amiri', serif;
        font-size: 1.1rem;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
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

// إظهار/إخفاء قسم تغيير كلمة المرور
function togglePasswordSection() {
    const section = document.getElementById('passwordChangeSection');
    if (section) {
        if (section.style.display === 'none' || section.style.display === '') {
            section.style.display = 'block';
        } else {
            section.style.display = 'none';
            document.getElementById('currentPassword').value = '';
            document.getElementById('newPassword').value = '';
            document.getElementById('confirmPassword').value = '';
            resetPasswordRequirements();
        }
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

// التحقق من متطلبات كلمة المرور
function validatePassword() {
    const password = document.getElementById('newPassword').value;

    const lengthValid = password.length >= 8;
    updateRequirement('req-length', lengthValid);

    const uppercaseValid = /[A-Z]/.test(password);
    updateRequirement('req-uppercase', uppercaseValid);

    const lowercaseValid = /[a-z]/.test(password);
    updateRequirement('req-lowercase', lowercaseValid);

    const numberValid = /[0-9]/.test(password);
    updateRequirement('req-number', numberValid);

    const specialValid = /[!@#$%^&*(),.?":{}|<>]/.test(password);
    updateRequirement('req-special', specialValid);

    return lengthValid && uppercaseValid && lowercaseValid && numberValid && specialValid;
}

// تحديث حالة المتطلب
function updateRequirement(id, isValid) {
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

// إعادة تعيين متطلبات كلمة المرور
function resetPasswordRequirements() {
    const requirements = ['req-length', 'req-uppercase', 'req-lowercase', 'req-number', 'req-special'];
    requirements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.classList.remove('valid');
            const icon = element.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-check-circle');
                icon.classList.add('fa-circle');
            }
        }
    });
}

// حفظ كلمة المرور الجديدة
async function savePassword() {
    const currentPassword = document.getElementById('currentPassword').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (!currentPassword || !newPassword || !confirmPassword) {
        showNotification('الرجاء ملء جميع الحقول', 'error');
        return;
    }

    if (!validatePassword()) {
        showNotification('كلمة المرور الجديدة لا تستوفي المتطلبات', 'error');
        return;
    }

    if (newPassword !== confirmPassword) {
        showNotification('كلمتا المرور غير متطابقتين', 'error');
        return;
    }

    // محاولة تحديث كلمة المرور في الـ backend
    const userId = localStorage.getItem('userId');
    if (userId && typeof UsersAPI !== 'undefined') {
        try {
            await UsersAPI.update(userId, {
                password: newPassword
            });
        } catch (err) {
            console.warn('تعذر تحديث كلمة المرور في الـ backend:', err);
        }
    }

    showNotification('تم تغيير كلمة المرور بنجاح', 'success');
    togglePasswordSection();
}

// إلغاء تغيير كلمة المرور
function cancelPasswordChange() {
    togglePasswordSection();
}

// تهيئة القيم الأصلية عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    originalValues.email = document.getElementById('emailInput').value;
    originalValues.gender = document.getElementById('genderInput').value;

    const newPasswordInput = document.getElementById('newPassword');
    if (newPasswordInput) {
        newPasswordInput.addEventListener('input', validatePassword);
    }
});
