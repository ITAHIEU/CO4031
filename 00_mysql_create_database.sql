-- ========================================
-- 00_MYSQL_CREATE_DATABASE.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 0
-- Creates database and sets up initial configuration

-- Drop and recreate database
DROP DATABASE IF EXISTS ProductDW;
CREATE DATABASE ProductDW 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE ProductDW;

SELECT 'Database ProductDW created successfully!' as Status;
SELECT DATABASE() as Current_Database;