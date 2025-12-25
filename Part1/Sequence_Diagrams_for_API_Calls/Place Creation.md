```mermaid
sequenceDiagram
    participant User
    participant API as Presentation(API)
    participant Facade
    participant PlaceService as BusinessLogic(Place)
    participant DB as Persistence(Database)

    User ->> API: POST /places (place data)
    API ->> Facade: createPlace(data)
    Facade ->> PlaceService: validatePlace(data)
    alt data valid
        PlaceService ->> DB: savePlace(place)
        DB -->> PlaceService: place saved
        PlaceService -->> Facade: place created
        Facade -->> API: success response
        API -->> User: 201 Created
    else data invalid
        PlaceService -->> Facade: validation error
        Facade -->> API: error response
        API -->> User: 400 Bad Request
    end
