# 🚀 HƯỚNG DẪN CHẠY DATA WAREHOUSE VỚI MYSQL

## CÁCH 1: TỰ ĐỘNG (KHUYẾN NGHỊ)

### Bước 1: Chạy script tự động
```cmd
MySQL_Deploy.bat
```

### Bước 2: Nhập thông tin kết nối
- **Host**: localhost (hoặc địa chỉ MySQL server)
- **Port**: 3306 (mặc định)
- **Username**: root (hoặc user của bạn)
- **Password**: [nhập password MySQL]
- **Database**: ProductDW (mặc định)

## CÁCH 2: THỦ CÔNG VỚI MYSQL WORKBENCH

### Bước 1: Mở MySQL Workbench
1. Kết nối đến MySQL server
2. Tạo connection mới nếu chưa có

### Bước 2: Tạo Database Structure
```sql
-- Mở file MySQL_create_dwh.sql trong Workbench
-- Hoặc copy nội dung và chạy
```

### Bước 3: Import CSV Data
```sql
-- Trong MySQL Workbench:
USE ProductDW;

-- Bật local_infile
SET GLOBAL local_infile = 1;

-- Import CSV (thay đổi đường dẫn cho phù hợp)
LOAD DATA LOCAL INFILE 'e:/Tai lieu/Data Warehouse/DWH project/vietnamese_tiki_products_backpacks_suitcases.csv'
INTO TABLE STAGING_Products
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(row_number, id, name, description, original_price, price, fulfillment_type,
 brand, review_count, rating_average, favourite_count, pay_later, current_seller,
 date_created, number_of_images, vnd_cashback, has_video, category, quantity_sold);

-- Kiểm tra import
SELECT COUNT(*) as Records_Imported FROM STAGING_Products;
```

### Bước 4: Chạy ETL Process
```sql
-- Mở file MySQL_etl_process.sql trong Workbench
-- Hoặc copy nội dung và chạy
```

## CÁCH 3: COMMAND LINE

### Bước 1: Tạo Database
```cmd
mysql -u root -p -e "source MySQL_create_dwh.sql"
```

### Bước 2: Import CSV
```cmd
mysql -u root -p ProductDW --local-infile=1 -e "
LOAD DATA LOCAL INFILE 'vietnamese_tiki_products_backpacks_suitcases.csv'
INTO TABLE STAGING_Products
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;"
```

### Bước 3: Run ETL
```cmd
mysql -u root -p -e "source MySQL_etl_process.sql"
```

## KIỂM TRA KẾT QUẢ

### Kiểm tra Tables đã tạo
```sql
USE ProductDW;
SHOW TABLES;
```

### Kiểm tra dữ liệu
```sql
-- Kiểm tra staging data
SELECT COUNT(*) as Staging_Records FROM STAGING_Products;

-- Kiểm tra dimension tables
SELECT 'DIM_Brand' as TableName, COUNT(*) as Records FROM DIM_Brand
UNION ALL SELECT 'DIM_Seller', COUNT(*) FROM DIM_Seller
UNION ALL SELECT 'DIM_Category', COUNT(*) FROM DIM_Category  
UNION ALL SELECT 'DIM_Product', COUNT(*) FROM DIM_Product
UNION ALL SELECT 'FACT_Product_Sales', COUNT(*) FROM FACT_Product_Sales;
```

### Test Views
```sql
-- Test product sales view
SELECT * FROM VW_Product_Sales LIMIT 10;

-- Test brand performance view  
SELECT * FROM VW_Brand_Performance LIMIT 10;
```

## CÁC TRUY VẤN PHÂN TÍCH MẪU

### 1. Top 10 Brands theo doanh thu
```sql
SELECT 
    brand_name,
    brand_type,
    total_products,
    total_quantity_sold,
    ROUND(total_revenue, 2) as total_revenue,
    ROUND(avg_price, 2) as avg_price,
    ROUND(avg_rating, 2) as avg_rating
FROM VW_Brand_Performance 
ORDER BY total_revenue DESC 
LIMIT 10;
```

### 2. Phân tích Category
```sql
SELECT 
    dc.category_name,
    COUNT(DISTINCT fps.product_id) as total_products,
    SUM(fps.quantity_sold) as total_quantity_sold,
    ROUND(SUM(fps.current_price * fps.quantity_sold), 2) as total_revenue,
    ROUND(AVG(fps.current_price), 2) as avg_price,
    ROUND(AVG(fps.rating_average), 2) as avg_rating
FROM FACT_Product_Sales fps
INNER JOIN DIM_Category dc ON fps.category_id = dc.category_id
WHERE fps.is_active = TRUE
GROUP BY dc.category_name
ORDER BY total_revenue DESC;
```

### 3. Top Sellers
```sql
SELECT 
    ds.seller_name,
    COUNT(DISTINCT fps.product_id) as total_products,
    COUNT(DISTINCT fps.brand_id) as brands_sold,
    SUM(fps.quantity_sold) as total_quantity_sold,
    ROUND(SUM(fps.current_price * fps.quantity_sold), 2) as total_revenue,
    ROUND(AVG(fps.rating_average), 2) as avg_rating
FROM FACT_Product_Sales fps
INNER JOIN DIM_Seller ds ON fps.seller_id = ds.seller_id
WHERE fps.is_active = TRUE
GROUP BY ds.seller_name
HAVING COUNT(DISTINCT fps.product_id) >= 5
ORDER BY total_revenue DESC
LIMIT 15;
```

### 4. Phân tích giá theo danh mục
```sql
SELECT 
    dc.category_name,
    COUNT(*) as total_products,
    MIN(fps.current_price) as min_price,
    MAX(fps.current_price) as max_price,
    ROUND(AVG(fps.current_price), 2) as avg_price,
    ROUND(AVG(fps.discount_percentage), 2) as avg_discount_percentage
FROM FACT_Product_Sales fps
INNER JOIN DIM_Category dc ON fps.category_id = dc.category_id
WHERE fps.is_active = TRUE AND fps.current_price > 0
GROUP BY dc.category_name
ORDER BY avg_price DESC;
```

## XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: local_infile disabled
```sql
-- Giải pháp: Bật local_infile
SET GLOBAL local_infile = 1;
```

### Lỗi: Access denied
- Kiểm tra username/password
- Đảm bảo user có quyền CREATE DATABASE, INSERT, SELECT

### Lỗi: CSV import failed
- Kiểm tra đường dẫn file CSV
- Đảm bảo file CSV có định dạng UTF-8
- Thử import thủ công qua MySQL Workbench Table Data Import Wizard

### Lỗi: Foreign key constraint
- Đảm bảo chạy scripts theo thúc tự:
  1. MySQL_create_dwh.sql
  2. Import CSV
  3. MySQL_etl_process.sql

## KẾT QUẢ MONG ĐỢI

Sau khi hoàn thành, bạn sẽ có:
- ✅ Database ProductDW với 8 tables
- ✅ ~5,367 records trong STAGING_Products  
- ✅ Dimension tables đầy đủ dữ liệu
- ✅ FACT_Product_Sales với đầy đủ metrics
- ✅ 2 Views để truy vấn nhanh
- ✅ Time dimension từ 2020-2025
- ✅ Summary tables cho reporting

## 🎯 NEXT STEPS

1. **Kết nối Power BI/Tableau** để tạo dashboard
2. **Thiết lập backup schedule** cho database
3. **Tạo additional views** cho specific analysis
4. **Implement incremental loading** cho dữ liệu mới
5. **Monitor performance** và tối ưu hóa indexes