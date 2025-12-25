sequenceDiagram
    participant User
    participant API as Presentation(API)
    participant Facade
    participant UserService as BusinessLogic(User)
    participant DB as Persistence(Database)

    %% Note: User sends registration data to API
    User ->> API: POST /users (registration data)
    
    %% Note: API forwards data to Facade
    API ->> Facade: createUser(data)
    
    %% Note: Facade calls UserService to validate data
    Facade ->> UserService: validateUser(data)
    
    %% Note: UserService saves user in Database
    UserService ->> DB: saveUser(user)
    DB -->> UserService: user saved
    
    %% Note: UserService confirms creation to Facade
    UserService -->> Facade: user created
    
    %% Note: Facade sends success response to API
    Facade -->> API: success response
    
    %% Note: API responds 201 Created to User
    API -->> User: 201 Created
