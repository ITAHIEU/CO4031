-- ========================================
-- 01_MYSQL_CREATE_DIMENSION_TABLES.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 1
-- Creates all dimension tables

USE ProductDW;

-- Tắt foreign key checks để có thể drop tables
SET FOREIGN_KEY_CHECKS = 0;

-- 1. DIM_Brand
DROP TABLE IF EXISTS DIM_Brand;
CREATE TABLE DIM_Brand (
    brand_id INT AUTO_INCREMENT PRIMARY KEY,
    brand_name VARCHAR(255) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_brand_name (brand_name)
);

-- 2. DIM_Seller
DROP TABLE IF EXISTS DIM_Seller;
CREATE TABLE DIM_Seller (
    seller_id INT AUTO_INCREMENT PRIMARY KEY,
    seller_name VARCHAR(255) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_seller_name (seller_name)
);

-- 3. DIM_Fulfillment_Type
DROP TABLE IF EXISTS DIM_Fulfillment_Type;
CREATE TABLE DIM_Fulfillment_Type (
    fulfillment_id INT AUTO_INCREMENT PRIMARY KEY,
    fulfillment_type VARCHAR(100) NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_fulfillment_type (fulfillment_type)
);

-- Bật lại foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

SELECT 'All Dimension Tables created successfully!' as Status;
SHOW TABLES LIKE 'DIM_%';