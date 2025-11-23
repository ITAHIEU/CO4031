-- ========================================
-- IMPORT_REAL_CSV_DATA.sql
-- ========================================
-- Import dữ liệu thật từ CSV file

USE ProductDW;

-- Xóa dữ liệu sample cũ
TRUNCATE TABLE STAGING_Products;
TRUNCATE TABLE FACT_Product_Sales;
DELETE FROM DIM_Product WHERE product_id > 0;
DELETE FROM DIM_Brand WHERE brand_id > 0;
DELETE FROM DIM_Seller WHERE seller_id > 0;
DELETE FROM DIM_Category WHERE category_id > 0;

-- Reset AUTO_INCREMENT
ALTER TABLE DIM_Product AUTO_INCREMENT = 1;
ALTER TABLE DIM_Brand AUTO_INCREMENT = 1;
ALTER TABLE DIM_Seller AUTO_INCREMENT = 1;
ALTER TABLE DIM_Category AUTO_INCREMENT = 1;

-- Import CSV data vào staging
LOAD DATA LOCAL INFILE 'E:\\Tai lieu\\Data Warehouse\\DWH project\\vietnamese_tiki_products_backpacks_suitcases.csv'
INTO TABLE STAGING_Products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(id, name, short_description, description, brand_name, seller_name, 
 original_price, current_price, quantity_sold, review_count, rating_average, 
 favourite_count, all_time_quantity_sold, category_names, thumbnail_url, product_url);

-- Kiểm tra import
SELECT 'CSV Import completed!' as Status;
SELECT COUNT(*) as Total_Records_Imported FROM STAGING_Products;
SELECT 'Sample imported data:' as Info;
SELECT id, name, brand_name, seller_name, current_price FROM STAGING_Products LIMIT 5;