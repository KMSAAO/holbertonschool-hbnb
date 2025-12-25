```mermaid
sequenceDiagram
participant User
participant API as Presentation(API)
participant Facade
participant UserService as BusinessLogic(Review)
participant DB as Persistence(Database)

User->>API: POST /review (review data)
API->>Facade: createReview(data)
Facade->>UserService: validateReview(data)
alt data valid
    UserService->>DB: saveReview(data)
    DB-->>UserService: review saved
    UserService-->>Facade: review created
    Facade-->>API: success response
    API-->>User: 201 Created

else data invalid
    UserService-->>Facade: validation error
    Facade-->>API: error response
    API-->>User: 400 Bad Request
end
