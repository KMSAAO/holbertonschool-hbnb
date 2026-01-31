from app import create_app
from app.sqlalchemy import db
from app.models.user import User  # تأكد من مسار الموديل الصحيح
import uuid
from datetime import datetime

app = create_app()

with app.app_context():
    new_user = User(
        first_name='Ali',
        last_name='Alzahrani',
        email='alمi@example.com',
        password='$2b$12$ABCDEFHashedPasswordHere',
        is_admin=False,
        is_active=True,
    )
    
    db.session.add(new_user)
    db.session.commit()
    print("added successfully...")
