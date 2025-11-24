-- ========================================
-- 02_MYSQL_CREATE_FACT_TABLES.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 2
-- Creates fact table and staging table

USE ProductDW;

-- Staging Table (matching CSV structure)
DROP TABLE IF EXISTS STAGING_Products;
CREATE TABLE STAGING_Products (
    row_index INT,
    id BIGINT,
    name TEXT,
    description TEXT,
    original_price DECIMAL(15,2),
    price DECIMAL(15,2),
    fulfillment_type VARCHAR(50),
    brand VARCHAR(255),
    review_count INT DEFAULT 0,
    rating_average DECIMAL(3,2) DEFAULT 0.00,
    favourite_count INT DEFAULT 0,
    pay_later BOOLEAN DEFAULT FALSE,
    current_seller TEXT,
    date_created INT,
    number_of_images INT DEFAULT 0,
    vnd_cashback INT DEFAULT 0,
    has_video BOOLEAN DEFAULT FALSE,
    category TEXT,
    quantity_sold INT DEFAULT 0
);

-- Main Fact Table
DROP TABLE IF EXISTS FACT_Product_Sales;
CREATE TABLE FACT_Product_Sales (
    fact_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    brand_id INT NOT NULL,
    seller_id INT NOT NULL,
    category_id INT NOT NULL,
    fulfillment_id INT NOT NULL,
    time_id INT NOT NULL,
    tiki_product_id BIGINT,
    original_price DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    current_price DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    quantity_sold INT DEFAULT 0,
    review_count INT DEFAULT 0,
    rating_average DECIMAL(3,2) DEFAULT 0.00,
    favourite_count INT DEFAULT 0,
    all_time_quantity_sold INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (product_id) REFERENCES DIM_Product(product_id),
    FOREIGN KEY (brand_id) REFERENCES DIM_Brand(brand_id),
    FOREIGN KEY (seller_id) REFERENCES DIM_Seller(seller_id),
    FOREIGN KEY (category_id) REFERENCES DIM_Category(category_id),
    FOREIGN KEY (fulfillment_id) REFERENCES DIM_Fulfillment_Type(fulfillment_id),
    FOREIGN KEY (time_id) REFERENCES DIM_Time(time_id),
    
    -- Indexes for better performance
    INDEX idx_product_id (product_id),
    INDEX idx_brand_id (brand_id),
    INDEX idx_seller_id (seller_id),
    INDEX idx_category_id (category_id),
    INDEX idx_tiki_product_id (tiki_product_id),
    INDEX idx_created_date (created_date)
);

SELECT 'Fact Table and Staging Table created successfully!' as Status;
SHOW TABLES LIKE '%Product%';