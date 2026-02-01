from app import create_app
from app.sqlalchemy import db
from app.models.user import User
from app.models.place import Place
import uuid
from datetime import datetime

app = create_app()

# with app.app_context():
#     new_user = User(
#         first_name='Khalid',
#         last_name='Alomari',
#         email='khalid.alomari@example.com',
#         password='$2b$12$ABCDEFHashedPasswordHere',
#         is_admin=False,
#         is_active=True,
#     )
    
#     db.session.add(new_user)
#     db.session.commit()
#     print("added successfully...")

with app.app_context():
    user = User.query.filter_by(email='khalid.alomari@example.com').first()

    if not user:
        print("User not found!")
    else:
        new_place = Place(
            user_id=user.id,
            title='Luxury Apartment',
            description='A spacious apartment with sea view.',
            price=250.00,
            status='available',
            latitude=24.774265,
            longitude=46.738586
        )

        db.session.add(new_place)
        db.session.commit()
        print("Place added successfully...")
