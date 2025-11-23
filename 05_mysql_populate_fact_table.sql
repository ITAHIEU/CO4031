-- ========================================
-- 05_MYSQL_POPULATE_FACT_TABLE.sql
-- ========================================
-- MySQL Data Warehouse Creation Pipeline - Step 5
-- Populates fact table with transformed data

USE ProductDW;

-- Clear existing fact data
TRUNCATE TABLE FACT_Product_Sales;

-- Populate FACT_Product_Sales
INSERT INTO FACT_Product_Sales (
    product_id, brand_id, seller_id, category_id, fulfillment_id, time_id,
    tiki_product_id, original_price, current_price, quantity_sold, 
    review_count, rating_average, favourite_count, all_time_quantity_sold
)
SELECT 
    dp.product_id,
    db.brand_id,
    ds.seller_id,
    dc.category_id,
    df.fulfillment_id,
    dt.time_id,
    sp.id as tiki_product_id,
    COALESCE(sp.original_price, 0) as original_price,
    COALESCE(sp.current_price, 0) as current_price,
    COALESCE(sp.quantity_sold, 0) as quantity_sold,
    COALESCE(sp.review_count, 0) as review_count,
    COALESCE(sp.rating_average, 0) as rating_average,
    COALESCE(sp.favourite_count, 0) as favourite_count,
    COALESCE(sp.all_time_quantity_sold, 0) as all_time_quantity_sold
FROM STAGING_Products sp
INNER JOIN DIM_Product dp ON sp.id = dp.tiki_product_id
INNER JOIN DIM_Brand db ON COALESCE(NULLIF(TRIM(sp.brand_name), ''), 'Unknown') = db.brand_name
INNER JOIN DIM_Seller ds ON COALESCE(NULLIF(TRIM(sp.seller_name), ''), 'Unknown') = ds.seller_name  
INNER JOIN DIM_Category dc ON COALESCE(NULLIF(TRIM(sp.category_names), ''), 'Uncategorized') = dc.category_name
INNER JOIN DIM_Fulfillment_Type df ON df.fulfillment_type = 'Tiki Fulfillment'
INNER JOIN DIM_Time dt ON dt.date_key = CURDATE()
WHERE sp.id IS NOT NULL;

-- Show ETL results
SELECT 'Fact table populated successfully!' as Status;
SELECT COUNT(*) as Total_Fact_Records FROM FACT_Product_Sales;

-- Validation queries
SELECT 'Data validation:' as Info;
SELECT 
    'Total Records' as Metric,
    COUNT(*) as Value
FROM FACT_Product_Sales
UNION ALL
SELECT 
    'Records with Valid Prices',
    COUNT(*)
FROM FACT_Product_Sales
WHERE current_price > 0
UNION ALL
SELECT 
    'Records with Reviews',
    COUNT(*)
FROM FACT_Product_Sales  
WHERE review_count > 0;