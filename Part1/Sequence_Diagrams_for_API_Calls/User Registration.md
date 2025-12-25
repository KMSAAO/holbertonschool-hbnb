## User Registration

```mermaid
sequenceDiagram
    participant User
    participant API as Presentation(API)
    participant Facade
    participant UserService as BusinessLogic(User)
    participant DB as Persistence(Database)

    User ->> API: POST /users (registration data)
    API ->> Facade: createUser(data)
    Facade ->> UserService: validateUser(data)
    alt data valid
        UserService ->> DB: saveUser(user)
        DB -->> UserService: user saved
        UserService -->> Facade: user created
        Facade -->> API: success response
        API -->> User: 201 Created
    else data invalid
        UserService -->> Facade: validation error
        Facade -->> API: error response
        API -->> User: 400 Bad Request
    end
