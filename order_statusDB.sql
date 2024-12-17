CREATE DATABASE order_status;
USE order_status;

-- Create the orders table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    status VARCHAR(255),
    details VARCHAR(255)
);

-- Insert records into orders
INSERT INTO orders (order_id, status, details)
VALUES
(1001, 'Shipped', 'Expected delivery: 2024-12-20'),
(1002, 'Processing', 'Your order is being prepared.'),
(1003, 'Delivered', 'Delivered on: 2024-12-15');

-- Select records from orders
SELECT * FROM orders;

-- Create the locations table with a foreign key referencing orders
CREATE TABLE locations (
    location_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    latitude DOUBLE NOT NULL,
    longitude DOUBLE NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- Describe the locations table
DESCRIBE locations;

-- Insert records into locations
INSERT INTO locations (order_id, latitude, longitude, updated_at)
VALUES (1001, 14.58915910627848, 120.98233726106778, NOW());

-- Select records from locations
SELECT * FROM locations;
UPDATE locations
SET latitude = 14.58915910627848, 
    longitude = 120.98233726106778, 
    updated_at = NOW()  -- You can set this to a specific datetime if necessary
WHERE order_id = 1001;

