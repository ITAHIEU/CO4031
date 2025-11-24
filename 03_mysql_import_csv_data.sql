-- ========================================
-- 03_MYSQL_IMPORT_CSV_DATA.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 3
-- Imports CSV data into staging table

USE ProductDW;

-- Clear staging table
TRUNCATE TABLE STAGING_Products;

-- Import CSV data using LOAD DATA LOCAL INFILE with correct column mapping
LOAD DATA LOCAL INFILE 'vietnamese_tiki_products_backpacks_suitcases.csv'
INTO TABLE STAGING_Products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(row_index, id, name, description, original_price, price, fulfillment_type, brand, 
 review_count, rating_average, favourite_count, pay_later, current_seller, 
 date_created, number_of_images, vnd_cashback, has_video, category, quantity_sold);

-- Check import results
SET @record_count = (SELECT COUNT(*) FROM STAGING_Products);
SELECT CONCAT('Successfully imported ', @record_count, ' records!') as Import_Status;

-- Check import results
SELECT 'CSV Import completed!' as Status;
SELECT COUNT(*) as Total_Records_Imported FROM STAGING_Products;
SELECT 'Sample data:' as Info;
SELECT * FROM STAGING_Products LIMIT 5;