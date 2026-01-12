import unittest
from app import create_app

class TestPlaceAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        
        import uuid  # <-- استدعاء المكتبة
        
        # نولد إيميل عشوائي عشان ما يقول لنا "الإيميل مستخدم من قبل"
        unique_email = f"owner_{uuid.uuid4()}@test.com"

        self.user_data = {
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email,  # <-- نستخدم الإيميل العشوائي هنا
            "password": "password123"
        }
        
        # ننشئ المستخدم
        user_response = self.client.post('/api/v1/users/register', json=self.user_data)
        
        # (خطوة تصحيح) لو فشل الإنشاء، اطبع السبب عشان نعرف المشكلة
        if user_response.status_code != 201:
            raise ValueError(f"Setup failed: Could not create user. Status: {user_response.status_code}, Response: {user_response.json}")

        self.owner_id = user_response.json['id']

        # تجهيز بيانات المكان
        self.place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 34.05,
            "longitude": -118.25,
            "owner_id": self.owner_id,
            "status": "available" 
        }

    def test_create_place_success(self):
        """Test creating a place with valid data"""
        response = self.client.post('/api/v1/places/', json=self.place_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], self.place_data['title'])
        self.assertEqual(response.json['owner_id'], self.owner_id)
        # نحفظ الـ ID لاستخدامه لاحقاً إذا احتجنا
        self.place_id = response.json['id']

    def test_create_place_invalid_data(self):
        """Test creating a place with invalid data (e.g. negative price)"""
        invalid_data = self.place_data.copy()
        invalid_data['price'] = -50.0  # سعر بالسالب (خطأ)

        response = self.client.post('/api/v1/places/', json=invalid_data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('Price must be a non-negative number', response.json['message'])

    def test_create_place_invalid_owner(self):
        """Test creating a place with non-existent owner_id"""
        invalid_data = self.place_data.copy()
        invalid_data['owner_id'] = "fake-uuid-123"

        response = self.client.post('/api/v1/places/', json=invalid_data)
        
        # حسب كودك في Service، هذا يرفع ValueError ويتحول لـ 400
        self.assertEqual(response.status_code, 400)
        self.assertIn('Owner not found', response.json['message'])

    def test_get_place(self):
        """Test retrieving a place by ID"""
        # أولاً ننشئ المكان
        create_response = self.client.post('/api/v1/places/', json=self.place_data)
        place_id = create_response.json['id']

        # ثانياً نحاول جلبه
        response = self.client.get(f'/api/v1/places/{place_id}')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], place_id)
        self.assertEqual(response.json['title'], self.place_data['title'])

    def test_update_place(self):
        """Test updating place details"""
        # ننشئ المكان
        create_response = self.client.post('/api/v1/places/', json=self.place_data)
        place_id = create_response.json['id']

        # بيانات التحديث
        update_data = {
            "title": "Updated Luxury Apartment",
            "price": 250.0
        }

        # نرسل طلب التعديل
        response = self.client.put(f'/api/v1/places/{place_id}', json=update_data)
        
        self.assertEqual(response.status_code, 200)
        
        # التحقق من أن البيانات تغيرت فعلاً
        self.assertEqual(response.json['title'], "Updated Luxury Apartment")
        self.assertEqual(response.json['price'], 250.0)
        # التأكد أن البيانات الأخرى لم تتغير
        self.assertEqual(response.json['description'], self.place_data['description'])

    def test_delete_place(self):
        """Test deleting a place"""
        # ننشئ المكان
        create_response = self.client.post('/api/v1/places/', json=self.place_data)
        place_id = create_response.json['id']

        # نحذفه
        response = self.client.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 204)

        # نتأكد أنه اختفى (نتوقع 404 عند البحث عنه)
        get_response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)
