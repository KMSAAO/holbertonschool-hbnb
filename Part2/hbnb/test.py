from app.models.place import Place
from app.models.user import User
from app.enums.place_status import PlaceStatus
import uuid

user = User("Ali", "Saleh", "ali@mail.com","AaZz123456")

place = Place(
    user= user,
    title="Luxury Villa",
    description="Amazing view, private pool",
    price=1200,
    status=PlaceStatus.AVAILABLE,
    latitude=24.7136,
    longitude=46.6753
)

print(str(place.user.id))
print(place.title)
print(place.description)
print(place.price)
print(place.status.value)
print(place.latitude)
print(place.longitude)




# 1. تعريف كلاس بسيط يمثل المستخدم (Model)
class User:
    def __init__(self, first_name, email):
        self.id = str(uuid.uuid4())  # توليد ID فريد تلقائياً
        self.first_name = first_name
        self.email = email

    # هذه الدالة فقط لتحسين شكل الطباعة
    def __repr__(self):
        return f"<User: {self.first_name} (ID: {self.id})>"

# 2. تعريف المخزن (Repository)
class InMemoryRepository:
    def __init__(self):
        self.storage = {}  # هنا القاموس الذي يحفظ البيانات (قاعدة البيانات الوهمية)

    def add(self, entity):
        # التخزين: المفتاح هو الـ ID والقيمة هي الكائن كامل
        self.storage[entity.id] = entity
        print(f"✅ Saved: {entity.first_name}")

    def get(self, entity_id):
        # الاسترجاع: البحث باستخدام الـ ID
        return self.storage.get(entity_id)

    def get_by_email(self, email):
        # بحث مخصص: ندور على كل المستخدمين لنبحث عن الإيميل
        for item in self.storage.values():
            if item.email == email:
                return item
        return None

# ==========================================
# 3. التجربة العملية (Simulation)
# ==========================================

print("--- 1. تهيئة النظام ---")
user_repo = InMemoryRepository()

print("\n--- 2. إنشاء بيانات (Create) ---")
user1 = User("Ahmed", "ahmed@example.com")
user2 = User("Sarah", "sarah@example.com")
user3 = User("khalid", "khalid@example.com")

print(f"User 1 Created with ID: {user1.id}")
print(f"User 2 Created with ID: {user2.id}")
user3.id

print("\n--- 3. التخزين في الـ Repo (Add) ---")
user_repo.add(user1)
user_repo.add(user2)
user_repo.add(user3)


print("\n--- 4. استدعاء البيانات (Get by ID) ---")
# تخيل أنك الآن في صفحة البروفايل ومعك الـ ID فقط
fetched_user = user_repo.get(user3.id)
print(f"Found user by ID: {fetched_user}")
