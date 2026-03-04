CREATE TABLE IF NOT EXISTS bookings (
    id SERIAL PRIMARY KEY,
    booking_id INT UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    destination VARCHAR(255),
    booking_date DATE,
    price DECIMAL(10, 2),
    rating INT,
    status VARCHAR(50),
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);