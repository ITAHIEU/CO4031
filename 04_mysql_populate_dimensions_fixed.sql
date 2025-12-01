-- ========================================
-- 04_mysql_populate_dimensions.sql
-- ========================================
-- GitHub Actions compatible ETL process

USE ProductDW;

-- Populate DIM_Brand
INSERT IGNORE INTO DIM_Brand (brand_name)
SELECT DISTINCT 
    CASE 
        WHEN brand IS NULL OR TRIM(brand) = '' THEN 'Unknown'
        ELSE TRIM(brand)
    END as brand_name
FROM STAGING_Products;

SELECT CONCAT('DIM_Brand populated: ', COUNT(*), ' records') as Status FROM DIM_Brand;

-- Populate DIM_Seller  
INSERT IGNORE INTO DIM_Seller (seller_name)
SELECT DISTINCT
    CASE 
        WHEN current_seller IS NULL OR TRIM(current_seller) = '' THEN 'Unknown Seller'
        ELSE TRIM(current_seller)
    END as seller_name
FROM STAGING_Products;

SELECT CONCAT('DIM_Seller populated: ', COUNT(*), ' records') as Status FROM DIM_Seller;

-- Populate DIM_Fulfillment_Type
INSERT IGNORE INTO DIM_Fulfillment_Type (fulfillment_type, description)
VALUES 
    ('dropship', 'Dropshipping fulfillment'),
    ('tiki_delivery', 'Tiki delivery'),
    ('seller_delivery', 'Seller delivery'),
    ('unknown', 'Unknown fulfillment');

SELECT CONCAT('DIM_Fulfillment_Type populated: ', COUNT(*), ' records') as Status FROM DIM_Fulfillment_Type;