
-- Create Data base
CREATE DATABASE IF NOT EXISTS hbnb_db;

USE hbnb_db;
-- Create User table
CREATE TABLE if not exists users (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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


SET @admin_id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SET @place_id = UUID();
SET @amenity_id = UUID();


INSERT INTO users (id, first_name, last_name, email, password, is_admin, is_active)
VALUES (@admin_id, 'Nawaf', 'Saleh', 'NA@gmail.com', '$2b$12$ywfMB7Srq3o7T0nJVQ5i6ez2eTn5oI1jq/75FKHCQYCYqfldrxuLa', TRUE, TRUE);

INSERT INTO places (id, user_id, title, description, price, status, latitude, longitude)
VALUES (@place_id, @admin_id, 'Cozy Cottage', 'A cozy cottage in the countryside.', 120.00, 'available', 34.0522, -118.2437);

INSERT INTO reviews (id, user_id, place_id, rating, comment)
VALUES (UUID(), @admin_id, @place_id, 5, 'Amazing place! Had a wonderful time.');

INSERT INTO amenities (id, amenity_name, description, status)
VALUES (@amenity_id, 'WiFi', 'High-speed wireless internet access.', 'active');

INSERT INTO place_amenity (place_id, amenity_id)
VALUES (@place_id, @amenity_id);

-- Query to verify data insertion
SELECT * FROM users;
SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM amenities;
SELECT * FROM place_amenity;

-- update statements
UPDATE users
SET first_name = 'Khalid'
WHERE id = @admin_id;

UPDATE places
SET price = 150.00, status = 'booked'
WHERE id = @place_id;

--delete statements

-- DELETE FROM reviews WHERE place_id = @place_id;
-- DELETE FROM place_amenity WHERE place_id = @place_id;
-- DELETE FROM places WHERE id = @place_id;
-- DELETE FROM users WHERE id = @admin_id;
-- DELETE FROM amenities WHERE id = @amenity_id;



-- Drop tables if they exist (for cleanup)


-- DROP TABLE IF EXISTS place_amenity;
-- DROP TABLE IF EXISTS amenities;
-- DROP TABLE IF EXISTS reviews;
-- DROP TABLE IF EXISTS places;
-- DROP TABLE IF EXISTS users;
