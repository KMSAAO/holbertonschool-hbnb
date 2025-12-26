
# HBnB Evolution: Technical Blueprint <img src="https://github.com/user-attachments/assets/9027300d-16db-4118-9710-888e93619ce0" align="right" width="200" />

### Introduction
HBnB Evolution is a simplified version of a vacation rental platform. This document provides a comprehensive technical guide to the system architecture and design, serving as a foundation for the upcoming implementation phases.

---

## Problem Description
The HBnB project aims to solve the challenge of building a scalable and modular property management system. The primary goal is to ensure:
- Decoupling: Separation of presentation, logic, and data storage layers to improve maintainability.
- Consistency: Maintaining clear and logical relationships between users, places, and reviews.
- Scalability: Creating a robust design that allows for future enhancements with minimal refactoring.

---

## Project Tasks
This technical documentation is the result of completing the following foundational design tasks:
1. Task 0: Designing the High-Level Package Diagram to outline the layered architecture.
2. Task 1: Developing a Detailed Class Diagram for the Business Logic layer.
3. Task 2: Constructing Sequence Diagrams for key API interaction flows.
4. Task 3: Compiling all design elements into this comprehensive technical document.

---

## Design Diagrams

### 1. High-Level Package Diagram 
<img width="1200" height="1920" alt="image" src="https://github.com/user-attachments/assets/2ba8dda2-ab43-4742-9e75-6325023f6a85" />

Explanatory Notes:
- Presentation Layer: The entry point for the system via API calls.
- Business Logic Layer: Contains core models and validation rules.
- Persistence Layer: Responsible for all database interactions.

### 2. Detailed Class Diagram 
![Class Diagram](./path-to-your-image/Class_Diagram.png)

Explanatory Notes:
- Core Entities: Defines User, Place, Review, and Amenity.
- BaseModel: Common parent class providing universal attributes like id and timestamps.

---

### 3.Sequence Diagrams for API Calls
#### User Registration
<img width="2184" height="1494" alt="image" src="https://github.com/user-attachments/assets/c5ff2de9-9eef-4ec5-af52-e39153217b30" />

#### Place Creation
<img width="2044" height="1490" alt="image" src="https://github.com/user-attachments/assets/47bf3fa9-acd1-4c69-aca1-018029a9e3a7" />

#### Review Submission
<img width="2148" height="1494" alt="image" src="https://github.com/user-attachments/assets/7b517fb7-38e4-46c0-88fe-be262db15e75" />

#### Fetching a List of Places
<img width="2608" height="1488" alt="image" src="https://github.com/user-attachments/assets/37084465-ee07-4365-a909-d36aaaeeba45" />

### Explanatory Note for Sequence Diagrams:
These diagrams illustrate the dynamic interaction between the system layers. 
They demonstrate how the Presentation Layer communicates with the Business Logic via a Facade, and how data is validated before being committed to the Persistence Layer.
Each flow ensures robust error handling and clear response status codes for all key API endpoints.

---

### 🛠 Tools Used

- draw.io – For creating UML diagrams.

- Mermaid.js – For code-based diagram generation.

- GitHub – For version control and documentation hosting.

---

### 📝 Notes

- All diagrams follow UML notation standards.

- The design is based on the given business rules and requirements.

---

### ✍️ Authors
