-- Create Views for Easy Analysis
USE ProductDW;

-- Product Sales View
DROP VIEW IF EXISTS VW_Product_Sales;
CREATE VIEW VW_Product_Sales AS
SELECT 
    dp.product_name,
    dp.tiki_product_id,
    db.brand_name,
    db.brand_type,
    dc.category_name,
    ds.seller_name,
    df.fulfillment_type,
    fps.original_price,
    fps.current_price,
    ROUND((fps.original_price - fps.current_price), 2) as discount_amount,
    CASE 
        WHEN fps.original_price > 0 THEN 
            ROUND(((fps.original_price - fps.current_price) / fps.original_price) * 100, 2)
        ELSE 0 
    END as discount_percentage,
    fps.quantity_sold,
    fps.review_count,
    fps.rating_average,
    fps.favourite_count,
    ROUND((fps.current_price * fps.quantity_sold), 2) as total_revenue
FROM FACT_Product_Sales fps
INNER JOIN DIM_Product dp ON fps.product_id = dp.product_id
INNER JOIN DIM_Brand db ON fps.brand_id = db.brand_id
INNER JOIN DIM_Category dc ON fps.category_id = dc.category_id
INNER JOIN DIM_Seller ds ON fps.seller_id = ds.seller_id
INNER JOIN DIM_Fulfillment_Type df ON fps.fulfillment_id = df.fulfillment_id
WHERE fps.is_active = TRUE;

-- Brand Performance View
DROP VIEW IF EXISTS VW_Brand_Performance;
CREATE VIEW VW_Brand_Performance AS
SELECT 
    db.brand_name,
    db.brand_type,
    COUNT(DISTINCT fps.product_id) as total_products,
    COUNT(DISTINCT fps.seller_id) as total_sellers,
    SUM(fps.quantity_sold) as total_quantity_sold,
    ROUND(SUM(fps.current_price * fps.quantity_sold), 2) as total_revenue,
    ROUND(AVG(fps.current_price), 2) as avg_price,
    ROUND(AVG(fps.rating_average), 2) as avg_rating,
    SUM(fps.review_count) as total_reviews
FROM FACT_Product_Sales fps
INNER JOIN DIM_Brand db ON fps.brand_id = db.brand_id
WHERE fps.is_active = TRUE
GROUP BY db.brand_name, db.brand_type;

-- Category Performance View
DROP VIEW IF EXISTS VW_Category_Performance;
CREATE VIEW VW_Category_Performance AS
SELECT 
    dc.category_name,
    COUNT(DISTINCT fps.product_id) as total_products,
    SUM(fps.quantity_sold) as total_quantity_sold,
    ROUND(SUM(fps.current_price * fps.quantity_sold), 2) as total_revenue,
    ROUND(AVG(fps.current_price), 2) as avg_price,
    ROUND(AVG(fps.rating_average), 2) as avg_rating,
    MIN(fps.current_price) as min_price,
    MAX(fps.current_price) as max_price
FROM FACT_Product_Sales fps
INNER JOIN DIM_Category dc ON fps.category_id = dc.category_id
WHERE fps.is_active = TRUE
GROUP BY dc.category_name;

SELECT 'Views created successfully!' as Status;
SELECT 'Available Views:' as Info;
SHOW TABLES LIKE 'VW_%';

-- Test Views
SELECT 'Testing VW_Product_Sales:' as Test;
SELECT * FROM VW_Product_Sales LIMIT 5;

SELECT 'Testing VW_Brand_Performance:' as Test;
SELECT * FROM VW_Brand_Performance ORDER BY total_revenue DESC LIMIT 10;

SELECT 'Testing VW_Category_Performance:' as Test;
SELECT * FROM VW_Category_Performance ORDER BY total_revenue DESC LIMIT 10;