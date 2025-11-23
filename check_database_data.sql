-- ========================================
-- CHECK_DATABASE_DATA.sql
-- ========================================
-- Kiểm tra dữ liệu trong database ProductDW

USE ProductDW;

-- Kiểm tra tất cả tables
SELECT 'Database tables:' as Info;
SHOW TABLES;

-- Kiểm tra số lượng record từng table
SELECT 'Record counts:' as Info;
SELECT 'STAGING_Products' as Table_Name, COUNT(*) as Record_Count FROM STAGING_Products
UNION ALL
SELECT 'DIM_Brand', COUNT(*) FROM DIM_Brand
UNION ALL
SELECT 'DIM_Seller', COUNT(*) FROM DIM_Seller  
UNION ALL
SELECT 'DIM_Category', COUNT(*) FROM DIM_Category
UNION ALL
SELECT 'DIM_Fulfillment_Type', COUNT(*) FROM DIM_Fulfillment_Type
UNION ALL
SELECT 'DIM_Time', COUNT(*) FROM DIM_Time
UNION ALL
SELECT 'DIM_Product', COUNT(*) FROM DIM_Product
UNION ALL
SELECT 'FACT_Product_Sales', COUNT(*) FROM FACT_Product_Sales;

-- Sample data từ staging
SELECT 'Sample from STAGING_Products:' as Info;
SELECT * FROM STAGING_Products LIMIT 5;

-- Sample data từ fact table
SELECT 'Sample from FACT_Product_Sales:' as Info;
SELECT * FROM FACT_Product_Sales LIMIT 5;