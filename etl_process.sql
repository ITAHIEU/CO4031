-- ETL Process for MySQL Data Warehouse
USE ProductDW;

-- Step 1: Populate DIM_Brand
INSERT INTO DIM_Brand (brand_name, brand_type)
SELECT DISTINCT 
    IFNULL(NULLIF(TRIM(brand), ''), 'Unknown') as brand_name,
    CASE 
        WHEN UPPER(TRIM(brand)) = 'OEM' THEN 'OEM'
        WHEN UPPER(TRIM(brand)) IN ('NO BRAND', 'UNKNOWN', '') THEN 'Generic'
        WHEN brand IS NULL THEN 'Generic'
        ELSE 'Branded'
    END as brand_type
FROM STAGING_Products sp
WHERE NOT EXISTS (
    SELECT 1 FROM DIM_Brand db 
    WHERE db.brand_name = IFNULL(NULLIF(TRIM(sp.brand), ''), 'Unknown')
);

SELECT CONCAT('DIM_Brand populated. Total records: ', COUNT(*)) as Status FROM DIM_Brand;

-- Step 2: Populate DIM_Seller
INSERT INTO DIM_Seller (seller_name)
SELECT DISTINCT 
    IFNULL(NULLIF(TRIM(current_seller), ''), 'Unknown Seller') as seller_name
FROM STAGING_Products sp
WHERE NOT EXISTS (
    SELECT 1 FROM DIM_Seller ds 
    WHERE ds.seller_name = IFNULL(NULLIF(TRIM(sp.current_seller), ''), 'Unknown Seller')
);

SELECT CONCAT('DIM_Seller populated. Total records: ', COUNT(*)) as Status FROM DIM_Seller;

-- Step 3: Populate DIM_Category
INSERT INTO DIM_Category (category_name)
SELECT DISTINCT 
    IFNULL(NULLIF(TRIM(category), ''), 'Uncategorized') as category_name
FROM STAGING_Products sp
WHERE NOT EXISTS (
    SELECT 1 FROM DIM_Category dc 
    WHERE dc.category_name = IFNULL(NULLIF(TRIM(sp.category), ''), 'Uncategorized')
);

SELECT CONCAT('DIM_Category populated. Total records: ', COUNT(*)) as Status FROM DIM_Category;

-- Step 4: Populate DIM_Product
INSERT INTO DIM_Product (tiki_product_id, product_name, brand_id, category_id, has_video)
SELECT DISTINCT
    sp.id as tiki_product_id,
    LEFT(IFNULL(NULLIF(TRIM(sp.name), ''), 'Unnamed Product'), 500) as product_name,
    db.brand_id,
    dc.category_id,
    CASE WHEN UPPER(TRIM(sp.has_video)) = 'TRUE' THEN TRUE ELSE FALSE END as has_video
FROM STAGING_Products sp
INNER JOIN DIM_Brand db ON db.brand_name = IFNULL(NULLIF(TRIM(sp.brand), ''), 'Unknown')
INNER JOIN DIM_Category dc ON dc.category_name = IFNULL(NULLIF(TRIM(sp.category), ''), 'Uncategorized')
WHERE sp.id IS NOT NULL
    AND NOT EXISTS (
        SELECT 1 FROM DIM_Product dp 
        WHERE dp.tiki_product_id = sp.id
    );

SELECT CONCAT('DIM_Product populated. Total records: ', COUNT(*)) as Status FROM DIM_Product;

-- Step 5: Populate FACT_Product_Sales
INSERT INTO FACT_Product_Sales (
    product_id, brand_id, seller_id, fulfillment_id, category_id,
    tiki_product_id, original_price, current_price, quantity_sold,
    review_count, rating_average, favourite_count
)
SELECT 
    dp.product_id,
    db.brand_id,
    ds.seller_id,
    df.fulfillment_id,
    dc.category_id,
    sp.id as tiki_product_id,
    IFNULL(sp.original_price, 0) as original_price,
    IFNULL(sp.price, 0) as current_price,
    IFNULL(sp.quantity_sold, 0) as quantity_sold,
    IFNULL(sp.review_count, 0) as review_count,
    IFNULL(sp.rating_average, 0) as rating_average,
    IFNULL(sp.favourite_count, 0) as favourite_count
FROM STAGING_Products sp
INNER JOIN DIM_Product dp ON dp.tiki_product_id = sp.id
INNER JOIN DIM_Brand db ON db.brand_name = IFNULL(NULLIF(TRIM(sp.brand), ''), 'Unknown')
INNER JOIN DIM_Seller ds ON ds.seller_name = IFNULL(NULLIF(TRIM(sp.current_seller), ''), 'Unknown Seller')
INNER JOIN DIM_Fulfillment_Type df ON df.fulfillment_type = IFNULL(sp.fulfillment_type, 'dropship')
INNER JOIN DIM_Category dc ON dc.category_name = IFNULL(NULLIF(TRIM(sp.category), ''), 'Uncategorized')
WHERE sp.id IS NOT NULL;

SELECT CONCAT('FACT_Product_Sales populated. Total records: ', COUNT(*)) as Status FROM FACT_Product_Sales;

-- Final Summary
SELECT 'ETL PROCESS COMPLETED!' as Status;
SELECT 'Data Summary:' as Info;
SELECT 'DIM_Brand' as TableName, COUNT(*) as Records FROM DIM_Brand
UNION ALL SELECT 'DIM_Seller', COUNT(*) FROM DIM_Seller
UNION ALL SELECT 'DIM_Category', COUNT(*) FROM DIM_Category  
UNION ALL SELECT 'DIM_Product', COUNT(*) FROM DIM_Product
UNION ALL SELECT 'FACT_Product_Sales', COUNT(*) FROM FACT_Product_Sales
UNION ALL SELECT 'STAGING_Products', COUNT(*) FROM STAGING_Products;