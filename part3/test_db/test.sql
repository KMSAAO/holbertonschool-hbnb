
-- Create User table
CREATE TABLE if not exists users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    Create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Place table
CREATE TABLE if not exists places (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    status VARCHAR(50),
    latitude FLOAT,
    longitude FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create Review table
CREATE TABLE if not exists reviews (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36),
    place_id CHAR(36),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE(user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id)
);

-- Create Amenity table
CREATE TABLE if not exists amenities (
    id CHAR(36) PRIMARY KEY,
    amenity_name VARCHAR(255) UNIQUE,
    description TEXT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Place_Amenity join table
CREATE TABLE if not exists place_amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

insert into users (id, first_name, last_name, email, password, is_admin, is_active)
values
(id, 'Nawaf', 'Saleh', 'NA@gmail.com', '$2b$12$PK6MXIU39Sw2LAyS8VNnlOg8YiKbtOkbWJhIufaek2v9xVzv9yRum', TRUE, TRUE);

insert into places (id, user_id, title, description, price, status, latitude, longitude)
values
(id, "830e5844-d44f-4f3b-8c2d-b347ef70fec4", 'Cozy Cottage', 'A cozy cottage in the countryside.', 120.00, 'available', 34.0522, -118.2437);

insert into reviews (id, "830e5844-d44f-4f3b-8c2d-b347ef70fec4", "830e5844-d44f-4f3b-8c2d-b347ef70fec4", 5, "Nice")
values
(id, user_id, place_id, 5, 'Amazing place! Had a wonderful time.');

insert into amenities (id, 'WIFI', 'Speed WIFI', 'active');
values
(id, 'WiFi', 'High-speed wireless internet access.', 'active');

insert into place_amenity (place_id, amenity_id)
values
(place_id, amenity_id);

-- Query to verify data insertion
SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM amenities;
SELECT * FROM place_amenity;

--update statements
UPDATE users
SET first_name = 'Khalid', last_name = 'Mohammed', email = 'KO@gmail.com'
WHERE id = id;

UPDATE places
SET title = 'Modern Apartment', description = 'A modern apartment in the city center.', price = 150.00, status = 'booked'
WHERE id = id;

UPDATE reviews
SET rating = 4, comment = 'Great place, but could be cleaner.'

WHERE id = id;

UPDATE amenities
SET amenity_name = 'Pool', description = 'Outdoor swimming pool.', status = 'active'
WHERE id = id;

update place_amenity
SET place_id = place_id, amenity_id = amenity_id
WHERE place_id = place_id AND amenity_id = amenity_id;

--delete statements
DELETE FROM users WHERE id = id;
DELETE FROM places WHERE id = id;
DELETE FROM reviews WHERE id = id;
DELETE FROM amenities WHERE id = id;
DELETE FROM place_amenity WHERE place_id = place_id AND amenity_id = amenity_id;


-- Drop tables if they exist (for cleanup)
DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS users;