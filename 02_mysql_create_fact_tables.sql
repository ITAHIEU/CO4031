-- ========================================
-- 02_MYSQL_CREATE_FACT_TABLES.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 2
-- Creates fact table and staging table

USE ProductDW;

-- Staging Table
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

-- Main Fact Table - theo schema diagram  
DROP TABLE IF EXISTS Fact_product_stats;
CREATE TABLE Fact_product_stats (
    UniqueID BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    brand_id INT NOT NULL, 
    seller_id INT NOT NULL,
    fulfillment_id INT NOT NULL,
    price DECIMAL(15,2) NOT NULL DEFAULT 0.00,
    quantity_sold INT DEFAULT 0,
    rating_average DECIMAL(3,2) DEFAULT 0.00,
    review_count INT DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Key Constraints
    FOREIGN KEY (brand_id) REFERENCES DIM_Brand(brand_id),
    FOREIGN KEY (seller_id) REFERENCES DIM_Seller(seller_id),
    FOREIGN KEY (fulfillment_id) REFERENCES DIM_Fulfillment_Type(fulfillment_id),
    
    -- Indexes for better performance
    INDEX idx_product_id (product_id),
    INDEX idx_brand_id (brand_id),
    INDEX idx_seller_id (seller_id),
    INDEX idx_fulfillment_id (fulfillment_id)
);

SELECT 'Fact Table and Staging Table created successfully!' as Status;
SHOW TABLES LIKE '%Product%';