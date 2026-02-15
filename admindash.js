// admindash.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('access_token');
    let isAdmin = localStorage.getItem('is_admin'); 

    const isAdminString = String(isAdmin).toLowerCase();

    console.log("Checking Admin Access...");
    console.log("Token exists:", !!token);
    console.log("Is Admin Value:", isAdminString);

    if (!token || isAdminString !== 'true') {
        alert('هذه المنطقة مخصصة للمديرين فقط!');
        window.location.href = 'index.html';
        return;
    }
    fetchData('users'); 
});

async function fetchData(type) {
    const tableBody = document.getElementById('admin-data-rows');
    const tableHeader = document.getElementById('admin-header');
    const loader = document.getElementById('admin-loader');

    loader.style.display = 'block';
    tableBody.innerHTML = '';

    try {
        const response = await fetch(`/api/v1/${type}/`, {
            // تم التأكد من استخدام access_token هنا أيضاً
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });
        const data = await response.json();

        // إعداد عناوين الجدول
        if (type === 'users') {
            tableHeader.innerHTML = '<th>الاسم الكامل</th><th>البريد الإلكتروني</th><th>الصلاحية</th><th>الإجراء</th>';
        } else if (type === 'places') {
            tableHeader.innerHTML = '<th>اسم المكان</th><th>السعر</th><th>الموقع</th><th>الإجراء</th>';
        } else if (type === 'reviews') {
            tableHeader.innerHTML = '<th>التعليق</th><th>التقييم</th><th>الإجراء</th>';
        }

        // بناء الصفوف
        data.forEach(item => {
            const tr = document.createElement('tr');
            let info = '';

            if (type === 'users') {
                info = `<td>${item.first_name} ${item.last_name}</td><td>${item.email}</td><td>${item.is_admin ? 'مدير' : 'عضو'}</td>`;
            } else if (type === 'places') {
                info = `<td>${item.title}</td><td>${item.price} ر.س</td><td>${item.location || 'غير محدد'}</td>`;
            } else if (type === 'reviews') {
                info = `<td>${item.comment}</td><td>${item.rating} نجوم</td>`;
            }

            tr.innerHTML = `${info}<td><button class="btn-delete" onclick="handleDelete('${type}', '${item.id}')">حذف</button></td>`;
            tableBody.appendChild(tr);
        });
    } catch (err) {
        console.error('خطأ في جلب البيانات:', err);
    } finally {
        loader.style.display = 'none';
    }
}

async function handleDelete(type, id) {
    if (!confirm('هل أنت متأكد من حذف هذا السجل؟ لا يمكن التراجع عن هذا الإجراء.')) return;

    try {
        const response = await fetch(`/api/v1/${type}/${id}`, {
            method: 'DELETE',
            // --- التصحيح هنا: غيرنا 'token' إلى 'access_token' لكي يعمل الحذف ---
            headers: { 'Authorization': `Bearer ${localStorage.getItem('access_token')}` }
        });

        if (response.ok) {
            alert('تم الحذف بنجاح');
            fetchData(type); // تحديث الجدول
        } else {
            alert('عذراً، لا تملك الصلاحية الكافية للحذف');
        }
    } catch (err) {
        alert('خطأ في الاتصال بالسيرفر');
    }
}

function switchTab(type, event) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    fetchData(type);
}

