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
    UserService ->> DB: saveUser(user)
    DB -->> UserService: user saved
    UserService -->> Facade: user created
    Facade -->> API: success response
    API -->> User: 201 Created

## Note:
In this scenario, the user sends registration data through the API.
The API forwards the data to the Facade, which calls the UserService to validate the data.
After validation, the user information is saved in the database.
Once the user is stored, the Facade returns a success confirmation to the API, and the API sends a "201 Created" response back to the user.
