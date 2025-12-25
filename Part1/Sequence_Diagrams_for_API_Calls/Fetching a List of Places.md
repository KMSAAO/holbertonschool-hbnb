```mermaid
sequenceDiagram
    participant User
    participant API as Presentation(API)
    participant Facade
    participant Service as BusinessLogic(Amenity)
    participant DB as Persistence(Database)

    User->>API: GET /places?amenity=WIFI
    API->>Facade: getPlaces(amenity="WIFI")

  
  
    Facade->>Service: validateAmenityName("WIFI")
    
    alt Amenity Name Not Found
        Service-->>Facade: Error: Amenity name does not exist
        
        Facade-->>API: throw validationException
        
        API-->>User: HTTP 400 Bad Request ({msg: "Invalid Amenity"})
        
    else Amenity Name is Valid
        Facade->>Service: findPlacesByAmenity("WIFI")
        Service->>DB: SQL Query (Select * where amenity=...)
        activate DB
        DB-->>Service: Return [List of Places] OR []
        deactivate DB
        Service-->>Facade: Return List
        Facade-->>API: Return Response
        API-->>User: HTTP 200 OK (Data)
    end

