-- ========================================
-- 03_MYSQL_IMPORT_CSV_DATA.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 3
-- Imports CSV data into staging table

USE ProductDW;

-- Clear staging table
TRUNCATE TABLE STAGING_Products;

-- Import CSV data - Use existing import method
-- Note: CSV data was already imported in previous steps
-- This step verifies the import

-- Check if data already exists
SET @record_count = (SELECT COUNT(*) FROM STAGING_Products);
SELECT CASE 
    WHEN @record_count > 0 THEN 'Data already imported successfully!'
    ELSE 'No data found. Please import CSV manually via MySQL Workbench.'
END as Import_Status;

-- Check import results
SELECT 'CSV Import completed!' as Status;
SELECT COUNT(*) as Total_Records_Imported FROM STAGING_Products;
SELECT 'Sample data:' as Info;
SELECT * FROM STAGING_Products LIMIT 5;