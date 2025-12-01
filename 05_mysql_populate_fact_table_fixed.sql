-- ========================================
-- 05_mysql_populate_fact_table.sql
-- ========================================
-- Populate fact table with proper joins

USE ProductDW;

-- Populate Fact_product_stats - theo schema diagram
INSERT INTO Fact_product_stats (
    product_id, brand_id, seller_id, fulfillment_id, time_id,
    price, quantity_sold, rating_average, review_count
)
SELECT 
    sp.id as product_id,
    db.brand_id,
    ds.seller_id,
    df.fulfillment_id,
    dt.time_id,
    IFNULL(sp.price, 0) as price,
    IFNULL(sp.quantity_sold, 0) as quantity_sold,
    IFNULL(sp.rating_average, 0.0) as rating_average,
    IFNULL(sp.review_count, 0) as review_count
FROM STAGING_Products sp
INNER JOIN DIM_Brand db ON db.brand_name = CASE 
    WHEN sp.brand IS NULL OR TRIM(sp.brand) = '' THEN 'Unknown'
    ELSE TRIM(sp.brand)
END
INNER JOIN DIM_Seller ds ON ds.seller_name = CASE 
    WHEN sp.current_seller IS NULL OR TRIM(sp.current_seller) = '' THEN 'Unknown Seller'
    ELSE TRIM(sp.current_seller)
END
INNER JOIN DIM_Fulfillment_Type df ON df.fulfillment_type = CASE 
    WHEN sp.fulfillment_type = 'dropship' THEN 'dropship'
    WHEN sp.fulfillment_type = 'tiki_delivery' THEN 'tiki_delivery'
    WHEN sp.fulfillment_type = 'seller_delivery' THEN 'seller_delivery'
    ELSE 'unknown'
END
INNER JOIN DIM_Time dt ON dt.date_key = CURDATE()
WHERE sp.id IS NOT NULL;

SELECT CONCAT('Fact_product_stats populated: ', COUNT(*), ' records') as Status FROM Fact_product_stats;

-- Summary report - chỉ 4 dimension tables + 1 fact table
SELECT 'ETL Process Completed!' as Status;
SELECT 
    'STAGING_Products' as Table_Name, COUNT(*) as Records FROM STAGING_Products
UNION ALL SELECT 'Dim_brand', COUNT(*) FROM DIM_Brand
UNION ALL SELECT 'Dim_seller', COUNT(*) FROM DIM_Seller  
UNION ALL SELECT 'Dim_Fulfillment_Type', COUNT(*) FROM DIM_Fulfillment_Type
UNION ALL SELECT 'Dim_Time', COUNT(*) FROM DIM_Time
UNION ALL SELECT 'Fact_product_stats', COUNT(*) FROM Fact_product_stats
ORDER BY Records DESC;