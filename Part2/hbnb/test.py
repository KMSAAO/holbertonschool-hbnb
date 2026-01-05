from app.models.place import Place
from app.models.user import User
from app.enums.place_status import PlaceStatus

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
