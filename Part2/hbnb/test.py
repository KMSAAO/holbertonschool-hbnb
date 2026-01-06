from app.models.place import Place
from app.models.user import User
from app.enums.place_status import PlaceStatus
import uuid
from app.services.facade import HBnBFacade



amenity_1 = {"amenity_name": "wifi", "description": "wifi in the room", "status": "removed"}

# --- بداية التطبيق ---

# 1. تشغيل النظام (Facade Initialization)
facade = HBnBFacade()

print("--- Test 1: Creating a valid user ---")
try:
    # الـ API ينادي دالة واحدة فقط!
    amenity_1 = facade.create_amenity(amenity_1)
    print(f"✅ Success: Created {str(amenity_1)}")
except Exception as e:
    print(f"❌ Error: {e}")
