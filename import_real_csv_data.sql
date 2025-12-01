
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
(row_index, id, name, description, original_price, price, fulfillment_type, brand, 
 review_count, rating_average, favourite_count, pay_later, current_seller, 
 date_created, number_of_images, vnd_cashback, has_video, category, quantity_sold);

-- Kiểm tra import
SELECT 'CSV Import completed!' as Status;
SELECT COUNT(*) as Total_Records_Imported FROM STAGING_Products;
SELECT 'Sample imported data:' as Info;
SELECT id, name, brand, current_seller, price FROM STAGING_Products LIMIT 5;