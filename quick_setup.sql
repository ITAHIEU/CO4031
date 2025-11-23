-- MySQL Data Warehouse Quick Setup
CREATE DATABASE IF NOT EXISTS ProductDW;
USE ProductDW;

-- Drop existing tables
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS FACT_Product_Sales;
DROP TABLE IF EXISTS DIM_Product;
DROP TABLE IF EXISTS DIM_Category;
DROP TABLE IF EXISTS DIM_Time;
DROP TABLE IF EXISTS DIM_Fulfillment_Type;
DROP TABLE IF EXISTS DIM_Seller;
DROP TABLE IF EXISTS DIM_Brand;
DROP TABLE IF EXISTS STAGING_Products;
SET FOREIGN_KEY_CHECKS = 1;

-- Create tables
CREATE TABLE DIM_Brand (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL UNIQUE,
    brand_type VARCHAR(50) DEFAULT 'Unknown'
);

CREATE TABLE DIM_Seller (
    seller_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_name VARCHAR(200) NOT NULL UNIQUE,
    seller_status VARCHAR(50) DEFAULT 'Active'
);

CREATE TABLE DIM_Fulfillment_Type (
    fulfillment_id INT AUTO_INCREMENT PRIMARY KEY,
    fulfillment_type VARCHAR(50) NOT NULL UNIQUE,
    fulfillment_description VARCHAR(200),
    delivery_speed VARCHAR(50)
);

CREATE TABLE DIM_Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    category_level INT DEFAULT 1
);

CREATE TABLE DIM_Time (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    date_key INT NOT NULL UNIQUE,
    full_date DATE NOT NULL,
    year INT,
    month_number INT,
    month_name VARCHAR(20),
    quarter INT
);

CREATE TABLE DIM_Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    tiki_product_id BIGINT NOT NULL UNIQUE,
    product_name VARCHAR(500),
    brand_id INT,
    category_id INT,
    has_video BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (brand_id) REFERENCES DIM_Brand(brand_id),
    FOREIGN KEY (category_id) REFERENCES DIM_Category(category_id)
);

CREATE TABLE FACT_Product_Sales (
    sales_fact_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    brand_id INT NOT NULL,
    seller_id INT NOT NULL,
    fulfillment_id INT NOT NULL,
    time_id INT,
    category_id INT NOT NULL,
    tiki_product_id BIGINT NOT NULL,
    original_price DECIMAL(18,2),
    current_price DECIMAL(18,2),
    quantity_sold INT DEFAULT 0,
    review_count INT DEFAULT 0,
    rating_average DECIMAL(3,2) DEFAULT 0.00,
    favourite_count INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (product_id) REFERENCES DIM_Product(product_id),
    FOREIGN KEY (brand_id) REFERENCES DIM_Brand(brand_id),
    FOREIGN KEY (seller_id) REFERENCES DIM_Seller(seller_id),
    FOREIGN KEY (fulfillment_id) REFERENCES DIM_Fulfillment_Type(fulfillment_id),
    FOREIGN KEY (category_id) REFERENCES DIM_Category(category_id)
);

CREATE TABLE STAGING_Products (
    row_num INT,
    id BIGINT,
    name VARCHAR(1000),
    description TEXT,
    original_price DECIMAL(18,2),
    price DECIMAL(18,2),
    fulfillment_type VARCHAR(50),
    brand VARCHAR(200),
    review_count INT,
    rating_average DECIMAL(3,2),
    favourite_count INT,
    pay_later VARCHAR(10),
    current_seller VARCHAR(200),
    date_created INT,
    number_of_images INT,
    vnd_cashback DECIMAL(18,2),
    has_video VARCHAR(10),
    category VARCHAR(200),
    quantity_sold INT
);

-- Insert default data
INSERT INTO DIM_Fulfillment_Type (fulfillment_type, fulfillment_description, delivery_speed) VALUES 
('dropship', 'Dropshipping', 'Medium'),
('seller_delivery', 'Seller Delivery', 'Medium'), 
('tiki_delivery', 'Tiki Delivery', 'Fast');

-- Insert some time data
INSERT INTO DIM_Time (date_key, full_date, year, month_number, month_name, quarter) VALUES
(20241119, '2024-11-19', 2024, 11, 'November', 4),
(20250101, '2025-01-01', 2025, 1, 'January', 1);

SELECT 'Database structure created successfully!' as Status;
SHOW TABLES;