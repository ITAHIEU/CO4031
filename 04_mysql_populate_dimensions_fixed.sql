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

-- Populate DIM_Category
INSERT IGNORE INTO DIM_Category (category_name, category_level)  
SELECT DISTINCT
    CASE 
        WHEN category IS NULL OR TRIM(category) = '' THEN 'Uncategorized'
        ELSE TRIM(category)
    END as category_name,
    1 as category_level
FROM STAGING_Products;

SELECT CONCAT('DIM_Category populated: ', COUNT(*), ' records') as Status FROM DIM_Category;

-- Populate DIM_Fulfillment_Type
INSERT IGNORE INTO DIM_Fulfillment_Type (fulfillment_type, description)
VALUES 
    ('dropship', 'Dropshipping fulfillment'),
    ('tiki_delivery', 'Tiki delivery'),
    ('seller_delivery', 'Seller delivery'),
    ('unknown', 'Unknown fulfillment');

SELECT CONCAT('DIM_Fulfillment_Type populated: ', COUNT(*), ' records') as Status FROM DIM_Fulfillment_Type;

-- Populate DIM_Time
INSERT IGNORE INTO DIM_Time (
    date_key, year, quarter, month, day, week_of_year, day_of_week,
    month_name, quarter_name, is_weekend
)
VALUES (
    CURDATE(),
    YEAR(CURDATE()),
    QUARTER(CURDATE()),
    MONTH(CURDATE()),
    DAY(CURDATE()),
    WEEK(CURDATE()),
    DAYOFWEEK(CURDATE()),
    MONTHNAME(CURDATE()),
    CONCAT('Q', QUARTER(CURDATE())),
    CASE WHEN DAYOFWEEK(CURDATE()) IN (1, 7) THEN TRUE ELSE FALSE END
);

SELECT CONCAT('DIM_Time populated: ', COUNT(*), ' records') as Status FROM DIM_Time;

-- Populate DIM_Product
INSERT IGNORE INTO DIM_Product (tiki_product_id, product_name, short_description, description, product_url)
SELECT DISTINCT
    sp.id as tiki_product_id,
    CASE 
        WHEN sp.name IS NULL OR TRIM(sp.name) = '' THEN 'Unnamed Product'
        ELSE LEFT(TRIM(sp.name), 1000)
    END as product_name,
    CASE 
        WHEN sp.name IS NULL OR TRIM(sp.name) = '' THEN 'No description'
        ELSE LEFT(TRIM(sp.name), 500)
    END as short_description,
    CASE 
        WHEN sp.description IS NULL OR TRIM(sp.description) = '' THEN 'No detailed description'
        ELSE LEFT(TRIM(sp.description), 2000)
    END as description,
    CONCAT('https://tiki.vn/product/', sp.id) as product_url
FROM STAGING_Products sp
WHERE sp.id IS NOT NULL;

SELECT CONCAT('DIM_Product populated: ', COUNT(*), ' records') as Status FROM DIM_Product;