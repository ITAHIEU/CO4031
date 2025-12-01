-- ========================================
-- 05_mysql_populate_fact_table.sql
-- ========================================
-- Populate fact table with proper joins

USE ProductDW;

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
    IFNULL(sp.original_price, 0) as original_price,
    IFNULL(sp.price, 0) as current_price,
    IFNULL(sp.quantity_sold, 0) as quantity_sold,
    IFNULL(sp.review_count, 0) as review_count,
    IFNULL(sp.rating_average, 0.0) as rating_average,
    IFNULL(sp.favourite_count, 0) as favourite_count,
    IFNULL(sp.quantity_sold, 0) as all_time_quantity_sold
FROM STAGING_Products sp
INNER JOIN DIM_Product dp ON dp.tiki_product_id = sp.id
INNER JOIN DIM_Brand db ON db.brand_name = CASE 
    WHEN sp.brand IS NULL OR TRIM(sp.brand) = '' THEN 'Unknown'
    ELSE TRIM(sp.brand)
END
INNER JOIN DIM_Seller ds ON ds.seller_name = CASE 
    WHEN sp.current_seller IS NULL OR TRIM(sp.current_seller) = '' THEN 'Unknown Seller'
    ELSE TRIM(sp.current_seller)
END
INNER JOIN DIM_Category dc ON dc.category_name = CASE 
    WHEN sp.category IS NULL OR TRIM(sp.category) = '' THEN 'Uncategorized'
    ELSE TRIM(sp.category)
END
INNER JOIN DIM_Fulfillment_Type df ON df.fulfillment_type = CASE 
    WHEN sp.fulfillment_type = 'dropship' THEN 'dropship'
    WHEN sp.fulfillment_type = 'tiki_delivery' THEN 'tiki_delivery'
    WHEN sp.fulfillment_type = 'seller_delivery' THEN 'seller_delivery'
    ELSE 'unknown'
END
INNER JOIN DIM_Time dt ON dt.date_key = CURDATE()
WHERE sp.id IS NOT NULL;

SELECT CONCAT('FACT_Product_Sales populated: ', COUNT(*), ' records') as Status FROM FACT_Product_Sales;

-- Summary report
SELECT 'ETL Process Completed!' as Status;
SELECT 
    'STAGING_Products' as Table_Name, COUNT(*) as Records FROM STAGING_Products
UNION ALL SELECT 'DIM_Brand', COUNT(*) FROM DIM_Brand
UNION ALL SELECT 'DIM_Seller', COUNT(*) FROM DIM_Seller
UNION ALL SELECT 'DIM_Category', COUNT(*) FROM DIM_Category
UNION ALL SELECT 'DIM_Product', COUNT(*) FROM DIM_Product
UNION ALL SELECT 'DIM_Fulfillment_Type', COUNT(*) FROM DIM_Fulfillment_Type
UNION ALL SELECT 'DIM_Time', COUNT(*) FROM DIM_Time
UNION ALL SELECT 'FACT_Product_Sales', COUNT(*) FROM FACT_Product_Sales
ORDER BY Records DESC;