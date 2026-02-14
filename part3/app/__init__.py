from flask import Flask, jsonify
from flask_restx import Api
from flask_cors import CORS  # استيراد المكتبة

# استيراد الـ Namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as review_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.guests import api as guests_ns
from app.api.v1.bookings import api as bookings_ns

# استيراد الامتدادات (Extensions)
from app.bcrypt import bcrypt
from app.JWTManger import jwt   
from app.db import db
import app.services.facade as facade

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    # 🔥 التعديل السحري هنا 🔥
    # هذا يمنع Flask من تحويل الرابط (Redirect) إذا كانت الشرطة المائلة ناقصة أو زائدة
    # ويحل مشكلة CORS Error + 308 Permanent Redirect
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    # تفعيل CORS والسماح لجميع المصادر (*) بالوصول
    CORS(app, resources={r"/*": {"origins": "*"}})

    # تهيئة المكتبات
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # إنشاء الجداول تلقائياً عند بدء التشغيل
    with app.app_context():
        db.create_all()

    # إعدادات الـ API والتوثيق (Swagger)
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/docs',
        authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': "Bearer <JWT>"
            }
        },
        security='Bearer Auth'
    )

    # إضافة الـ Namespaces (المسارات)
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(review_ns, path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(guests_ns, path='/api/v1/guests')
    api.add_namespace(bookings_ns, path='/api/v1/bookings')

    # مسار للتأكد أن السيرفر يعمل
    @app.route("/")
    def index():
        return jsonify({"message": "HBnB API is running", "status": "success"})

    return app

# دالة استرجاع بيانات المستخدم للـ JWT (مهمة للتوثيق)
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """
    Optional: used by flask-jwt-extended if you want current_user auto loading.
    We keep it safe: return None if user not found.
    """
    identity = jwt_data.get("sub")
    if not identity:
        return None

    try:
        user = facade.get_user(identity)
        return user  
    except Exception:
        return None