import os
from flask import Flask, jsonify, send_from_directory, abort, current_app
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


from app.bcrypt import bcrypt
from app.JWTManger import jwt   
from app.db import db
import app.services.facade as facade

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    
    app.url_map.strict_slashes = False

    app.config.from_object(config_class)

    CORS(app, resources={r"/*": {"origins": "*"}})

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)


    with app.app_context():
        db.create_all()

        place_columns = [
            ("images", "TEXT DEFAULT '[]'"),
            ("number_of_rooms", "INTEGER DEFAULT 0"),
            ("max_guests", "INTEGER DEFAULT 0"),
            ("tagline", "VARCHAR(255)"),
            ("rules", "TEXT"),
            ("details", "TEXT"),
            ("rooms", "TEXT DEFAULT '[]'"),
            ("location", "VARCHAR(255)"),
        ]

        for column_name, column_type in place_columns:
            try:
                db.session.execute(db.text(
                    f"ALTER TABLE places ADD COLUMN {column_name} {column_type}"
                ))
                db.session.commit()
                print(f"✅ Migration: '{column_name}' column added to places table")
            except Exception:
                db.session.rollback()

        amenity_columns = [
            ("icon", "VARCHAR(50)"),
        ]

        for column_name, column_type in amenity_columns:
            try:
                db.session.execute(db.text(
                    f"ALTER TABLE amenities ADD COLUMN {column_name} {column_type}"
                ))
                db.session.commit()
                print(f"Migration: '{column_name}' column added to amenities table")
            except Exception:
                db.session.rollback()
        try:
            from app.models.amenity import Amenity
            from app.enums.place_amenity_status import PlaceAmenityStatus

            default_amenities = [
                ("واي فاي", "fas fa-wifi"),
                ("موقف سيارات", "fas fa-parking"),
                ("مسبح", "fas fa-swimming-pool"),
                ("صالة رياضة", "fas fa-dumbbell"),
                ("مطعم", "fas fa-utensils"),
                ("سبا", "fas fa-spa"),
                ("تكييف", "fas fa-wind"),
                ("تلفاز", "fas fa-tv"),
                ("غسيل ملابس", "fas fa-tshirt"),
                ("بار", "fas fa-cocktail"),
                ("إفطار", "fas fa-coffee"),
                ("نقل للمطار", "fas fa-shuttle-van"),
                ("حيوانات أليفة", "fas fa-paw"),
                ("خدمة غرف", "fas fa-concierge-bell"),
                ("مركز أعمال", "fas fa-briefcase"),
                ("دخول للكراسي المتحركة", "fas fa-wheelchair"),
            ]

            existing_names = {
                (a.amenity_name or "").strip().lower()
                for a in Amenity.query.all()
                if a.amenity_name
            }

            created_count = 0
            for amenity_name, icon in default_amenities:
                key = amenity_name.strip().lower()
                if key in existing_names:
                    continue

                db.session.add(Amenity(
                    amenity_name=amenity_name,
                    description=None,
                    status=PlaceAmenityStatus.ACTIVE,
                    icon=icon
                ))
                existing_names.add(key)
                created_count += 1

            if created_count > 0:
                db.session.commit()
                print(f"Seeded {created_count} default amenities")
        except Exception:
            db.session.rollback()

        # Create uploads directory
        upload_folder = app.config.get('UPLOAD_FOLDER', os.path.join(os.path.dirname(__file__), '..', 'uploads'))
        os.makedirs(os.path.join(upload_folder, 'places'), exist_ok=True)

    # ==================== خدمة الملفات المرفوعة ====================

    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            return send_from_directory(upload_folder, filename)
        abort(404)

    # ==================== مسارات الواجهة الأمامية ====================

    # الصفحة الرئيسية — تقدم index.html من مجلد الـ Frontend
    @app.route("/")
    def index():
        return send_from_directory(FRONTEND_DIR, 'index.html')

    # مسار للتحقق من حالة الـ API
    @app.route("/api/health")
    def health_check():
        return jsonify({"message": "HBnB API is running", "status": "success"})

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

    # ==================== خدمة ملفات الواجهة الأمامية ====================
    # هذا المسار يقدم جميع ملفات HTML, CSS, JS, والصور من مجلد الـ Frontend
    # مسارات API أعلاه لها أولوية أعلى لأنها أكثر تحديداً
    @app.route('/<path:filename>')
    def serve_frontend(filename):
        file_path = os.path.join(FRONTEND_DIR, filename)
        if os.path.isfile(file_path):
            return send_from_directory(FRONTEND_DIR, filename)
        abort(404)

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

