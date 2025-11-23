-- ========================================
-- 01_MYSQL_CREATE_DIMENSION_TABLES.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 1
-- Creates all dimension tables

USE ProductDW;

-- 1. DIM_Brand
DROP TABLE IF EXISTS DIM_Brand;
CREATE TABLE DIM_Brand (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    brand_type ENUM('Official', 'Other') DEFAULT 'Other',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_brand_name (brand_name)
);

-- 2. DIM_Seller
DROP TABLE IF EXISTS DIM_Seller;
CREATE TABLE DIM_Seller (
    seller_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_name VARCHAR(255) NOT NULL,
    seller_type ENUM('Tiki Trading', 'Other') DEFAULT 'Other',
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_seller_name (seller_name)
);

-- 3. DIM_Category
DROP TABLE IF EXISTS DIM_Category;
CREATE TABLE DIM_Category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    category_level INT DEFAULT 1,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_category_name (category_name)
);

-- 4. DIM_Fulfillment_Type
DROP TABLE IF EXISTS DIM_Fulfillment_Type;
CREATE TABLE DIM_Fulfillment_Type (
    fulfillment_id INT AUTO_INCREMENT PRIMARY KEY,
    fulfillment_type VARCHAR(100) NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_fulfillment_type (fulfillment_type)
);

-- 5. DIM_Time
DROP TABLE IF EXISTS DIM_Time;
CREATE TABLE DIM_Time (
    time_id INT AUTO_INCREMENT PRIMARY KEY,
    date_key DATE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    day INT,
    week_of_year INT,
    day_of_week INT,
    month_name VARCHAR(20),
    quarter_name VARCHAR(10),
    is_weekend BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_date_key (date_key)
);

-- 6. DIM_Product
DROP TABLE IF EXISTS DIM_Product;
CREATE TABLE DIM_Product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    tiki_product_id BIGINT,
    product_name TEXT NOT NULL,
    short_description TEXT,
    description TEXT,
    product_url TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_tiki_product_id (tiki_product_id)
);

SELECT 'All Dimension Tables created successfully!' as Status;
SHOW TABLES LIKE 'DIM_%';