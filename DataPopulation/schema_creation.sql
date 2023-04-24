CREATE DATABASE IF NOT EXISTS FloRide;
USE FloRide;

DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS user (
    user_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    phone_number VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (user_id)
);

DROP TABLE IF EXISTS car;
CREATE TABLE IF NOT EXISTS car (
    car_id INT NOT NULL AUTO_INCREMENT,
    car_type VARCHAR(50) NOT NULL,
    vin_number VARCHAR(50) NOT NULL UNIQUE,
    PRIMARY KEY (car_id)
);

DROP TABLE IF EXISTS review;
CREATE TABLE IF NOT EXISTS review (
    review_id INT NOT NULL AUTO_INCREMENT,
    star_review INT NOT NULL CHECK (star_review BETWEEN 1 AND 5),
    feedback TEXT,
    PRIMARY KEY (review_id)
);

DROP TABLE IF EXISTS location_coords;
CREATE TABLE IF NOT EXISTS location_coords (
    location_id INT NOT NULL AUTO_INCREMENT,
    latitude DECIMAL(18, 15) NOT NULL,
    longitude DECIMAL(18, 15) NOT NULL,
    PRIMARY KEY (location_id)
);

DROP TABLE IF EXISTS payment;
CREATE TABLE IF NOT EXISTS payment (
    payment_id INT NOT NULL AUTO_INCREMENT,
    payment_datetime DATE NOT NULL,
    payment_method VARCHAR(10) NOT NULL,
    payment_amount INT NOT NULL,
    PRIMARY KEY (payment_id)
);

DROP TABLE IF EXISTS driver;
CREATE TABLE IF NOT EXISTS driver (
    driver_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    phone_number VARCHAR(12) NOT NULL,
    gender CHAR(1) NOT NULL,
    license_number VARCHAR(18) NOT NULL UNIQUE,
    rating DECIMAL(3,2) NOT NULL,
    date_of_birth DATE NOT NULL,
    car_id INT NOT NULL,
    location_id INT NOT NULL,
    PRIMARY KEY (driver_id),
    FOREIGN KEY (car_id) REFERENCES car(car_id),
    FOREIGN KEY (location_id) REFERENCES location_coords(location_id)
); --phone_number ko unique kyu nhi kiya tharv gaandu

DROP TABLE IF EXISTS booking_status;
CREATE TABLE IF NOT EXISTS booking_status (
	status_id INT UNIQUE NOT NULL AUTO_INCREMENT,
	status_name VARCHAR(16) NOT NULL UNIQUE CHECK (status_name IN ('pending', 'completed', 'cancelled')),
    PRIMARY KEY (status_id)
);

DROP TABLE IF EXISTS booking;
CREATE TABLE IF NOT EXISTS booking (
    booking_id INT UNIQUE NOT NULL AUTO_INCREMENT,
    passenger_id INT NOT NULL,
    driver_id INT NOT NULL,
    pickup_location_id INT NOT NULL,
    dropoff_location_id INT NOT NULL,
    booking_datetime DATETIME NOT NULL,
    completion_datetime DATETIME NOT NULL,
    payment_id INT NULL,
    fare DECIMAL(10,2) NOT NULL,
    distance DECIMAL(4,1) NOT NULL,
    status_id INT NOT NULL,
    review_id INT,
    PRIMARY KEY (booking_id),
    FOREIGN KEY (passenger_id) REFERENCES user(user_id),
    FOREIGN KEY (driver_id) REFERENCES driver(driver_id),
    FOREIGN KEY (pickup_location_id) REFERENCES location_coords(location_id),
    FOREIGN KEY (dropoff_location_id) REFERENCES location_coords(location_id),
    FOREIGN KEY (payment_id) REFERENCES payment(payment_id),
    FOREIGN KEY (status_id) REFERENCES booking_status(status_id),
    FOREIGN KEY (review_id) REFERENCES review(review_id)
); -- why is payment id possibly null?







