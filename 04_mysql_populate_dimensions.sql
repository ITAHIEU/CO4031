-- ========================================
-- 04_MYSQL_POPULATE_DIMENSIONS.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 4
-- Populates all dimension tables from staging data

USE ProductDW;

-- Check if staging data exists first
SELECT COUNT(*) as Staging_Records FROM STAGING_Products;

-- Skip sample data insertion - rely on CSV import only
-- Sample data only if CSV import completely failed
SELECT 'Using data from CSV import' as Status;

-- 1. Populate DIM_Time (current date)
INSERT IGNORE INTO DIM_Time (date_key, year, quarter, month, day, week_of_year, day_of_week, month_name, quarter_name, is_weekend)
SELECT 
    CURDATE() as date_key,
    YEAR(CURDATE()) as year,
    QUARTER(CURDATE()) as quarter,
    MONTH(CURDATE()) as month,
    DAY(CURDATE()) as day,
    WEEK(CURDATE()) as week_of_year,
    DAYOFWEEK(CURDATE()) as day_of_week,
    MONTHNAME(CURDATE()) as month_name,
    CONCAT('Q', QUARTER(CURDATE())) as quarter_name,
    CASE WHEN DAYOFWEEK(CURDATE()) IN (1,7) THEN TRUE ELSE FALSE END as is_weekend;

-- 2. Populate DIM_Brand
INSERT IGNORE INTO DIM_Brand (brand_name)
SELECT DISTINCT
    COALESCE(NULLIF(TRIM(brand_name), ''), 'Unknown') as brand_name
FROM STAGING_Products
WHERE brand_name IS NOT NULL;

-- 3. Populate DIM_Seller  
INSERT IGNORE INTO DIM_Seller (seller_name)
SELECT DISTINCT
    COALESCE(NULLIF(TRIM(seller_name), ''), 'Unknown') as seller_name
FROM STAGING_Products
WHERE seller_name IS NOT NULL;

-- 4. Populate DIM_Category
INSERT IGNORE INTO DIM_Category (category_name, category_level)
SELECT DISTINCT
    COALESCE(NULLIF(TRIM(category_names), ''), 'Uncategorized') as category_name,
    1 as category_level
FROM STAGING_Products
WHERE category_names IS NOT NULL;

-- 5. Populate DIM_Fulfillment_Type (default values)
INSERT IGNORE INTO DIM_Fulfillment_Type (fulfillment_type, description)
VALUES 
    ('Tiki Fulfillment', 'Fulfilled by Tiki'),
    ('Seller Fulfillment', 'Fulfilled by Seller'),
    ('Unknown', 'Unknown fulfillment type');

-- 6. Populate DIM_Product
INSERT IGNORE INTO DIM_Product (tiki_product_id, product_name, short_description, description, product_url)
SELECT DISTINCT
    id as tiki_product_id,
    COALESCE(NULLIF(TRIM(name), ''), 'Unnamed Product') as product_name,
    COALESCE(NULLIF(TRIM(short_description), ''), '') as short_description,
    COALESCE(NULLIF(TRIM(description), ''), '') as description,
    COALESCE(NULLIF(TRIM(product_url), ''), '') as product_url
FROM STAGING_Products
WHERE id IS NOT NULL;

-- Show population results
SELECT 'Dimension tables populated successfully!' as Status;
SELECT 'DIM_Brand' as Table_Name, COUNT(*) as Record_Count FROM DIM_Brand
UNION ALL
SELECT 'DIM_Seller', COUNT(*) FROM DIM_Seller  
UNION ALL
SELECT 'DIM_Category', COUNT(*) FROM DIM_Category
UNION ALL
SELECT 'DIM_Fulfillment_Type', COUNT(*) FROM DIM_Fulfillment_Type
UNION ALL
SELECT 'DIM_Time', COUNT(*) FROM DIM_Time
UNION ALL
SELECT 'DIM_Product', COUNT(*) FROM DIM_Product;