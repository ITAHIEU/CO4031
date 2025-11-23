# Kho Dữ Liệu Sản Phẩm (Product Data Warehouse)

## Tổng quan
Kho dữ liệu này được thiết kế để phân tích hiệu suất sản phẩm từ dữ liệu Tiki, bao gồm thông tin về sản phẩm, thương hiệu, người bán, và các chỉ số bán hàng.

## Kiến trúc Data Warehouse

### Star Schema Design
```
                    DIM_Time
                        |
    DIM_Brand -----> FACT_Product_Sales <----- DIM_Seller
                        |
    DIM_Category -------|
                        |
                DIM_Fulfillment_Type
                        |
                   DIM_Product
```

## Bảng Dimension (Dimension Tables)

### 1. DIM_Brand
- **Mục đích**: Lưu trữ thông tin thương hiệu
- **Khóa chính**: `brand_id`
- **Thuộc tính chính**:
  - `brand_name`: Tên thương hiệu
  - `brand_type`: Loại thương hiệu (OEM, Branded, Generic)

### 2. DIM_Seller  
- **Mục đích**: Lưu trữ thông tin người bán
- **Khóa chính**: `seller_id`
- **Thuộc tính chính**:
  - `seller_name`: Tên người bán
  - `seller_status`: Trạng thái (Active, Inactive)

### 3. DIM_Fulfillment_Type
- **Mục đích**: Lưu trữ thông tin phương thức giao hàng
- **Khóa chính**: `fulfillment_id`
- **Thuộc tính chính**:
  - `fulfillment_type`: Loại giao hàng (dropship, seller_delivery, tiki_delivery)
  - `delivery_speed`: Tốc độ giao hàng (Fast, Medium, Slow)

### 4. DIM_Time
- **Mục đích**: Dimension thời gian cho phân tích theo thời gian
- **Khóa chính**: `time_id`
- **Thuộc tính chính**:
  - `date_key`: Khóa ngày (YYYYMMDD)
  - `full_date`, `year`, `month`, `quarter`
  - `is_weekend`, `is_holiday`
  - `fiscal_year`, `fiscal_quarter`

### 5. DIM_Category
- **Mục đích**: Lưu trữ phân loại sản phẩm
- **Khóa chính**: `category_id`
- **Thuộc tính chính**:
  - `category_name`: Tên danh mục
  - `category_level`: Cấp độ phân loại
  - `parent_category_id`: Danh mục cha (hỗ trợ hierarchy)

### 6. DIM_Product
- **Mục đích**: Thông tin chi tiết sản phẩm
- **Khóa chính**: `product_id`
- **Thuộc tính chính**:
  - `tiki_product_id`: ID gốc từ Tiki
  - `product_name`: Tên sản phẩm
  - `product_description`: Mô tả sản phẩm
  - `has_video`, `number_of_images`: Thông tin media

## Bảng Fact (Fact Table)

### FACT_Product_Sales
- **Mục đích**: Lưu trữ dữ liệu bán hàng và hiệu suất sản phẩm
- **Khóa chính**: `sales_fact_id`
- **Foreign Keys**: Liên kết đến tất cả dimension tables
- **Measures chính**:
  - `original_price`, `current_price`: Giá gốc và giá hiện tại
  - `discount_amount`, `discount_percentage`: Thông tin giảm giá (tính toán)
  - `quantity_sold`: Số lượng đã bán
  - `review_count`, `rating_average`: Đánh giá của khách hàng
  - `favourite_count`: Số lượt yêu thích
  - `vnd_cashback`: Cashback

## Bảng Tổng hợp (Summary Tables)

### 1. FACT_Product_Monthly_Summary
- Tổng hợp hiệu suất sản phẩm theo tháng
- Bao gồm: doanh thu, đánh giá, số người bán

### 2. FACT_Brand_Performance_Summary  
- Tổng hợp hiệu suất thương hiệu theo tháng
- Bao gồm: số sản phẩm, doanh thu, giá trung bình

## Cấu trúc File

### SQL Scripts
1. **01_create_dimension_tables.sql** - Tạo các bảng dimension
2. **02_create_fact_tables.sql** - Tạo bảng fact và summary
3. **03_populate_dimensions.sql** - Nạp dữ liệu cơ bản vào dimension
4. **04_etl_process.sql** - Quy trình ETL hoàn chỉnh
5. **05_analytical_queries.sql** - Các câu truy vấn phân tích mẫu
6. **06_data_import.sql** - Hướng dẫn import dữ liệu CSV

## Quy trình Triển khai

### Bước 1: Tạo Database và Tables
```sql
-- Chạy theo thứ tự:
-- 1. Tạo database mới
-- 2. Chạy 01_create_dimension_tables.sql
-- 3. Chạy 02_create_fact_tables.sql
```

### Bước 2: Import Dữ liệu
```sql
-- 1. Chạy 03_populate_dimensions.sql (tạo staging table)
-- 2. Sử dụng 06_data_import.sql để import CSV
-- 3. Kiểm tra dữ liệu staging
```

### Bước 3: ETL Process
```sql
-- Chạy 04_etl_process.sql để:
-- 1. Nạp dữ liệu vào dimension tables
-- 2. Nạp dữ liệu vào fact table
-- 3. Cập nhật summary tables
-- 4. Kiểm tra chất lượng dữ liệu
```

### Bước 4: Phân tích Dữ liệu
```sql
-- Chạy 05_analytical_queries.sql để:
-- 1. Phân tích hiệu suất thương hiệu
-- 2. Phân tích danh mục sản phẩm
-- 3. Phân tích người bán
-- 4. Báo cáo tổng hợp
```

## Các Chỉ số Phân tích Chính

### 1. Hiệu suất Thương hiệu
- Doanh thu theo thương hiệu
- Số sản phẩm theo thương hiệu
- Đánh giá trung bình
- Thị phần

### 2. Phân tích Danh mục
- Doanh thu theo danh mục
- Giá trung bình theo danh mục
- Số lượng sản phẩm bán chạy

### 3. Hiệu suất Người bán
- Top người bán theo doanh thu
- Số thương hiệu được bán
- Đánh giá khách hàng

### 4. Phân tích Giá cả
- Phân bố giá theo danh mục
- Tỷ lệ giảm giá
- Phân tích pricing tiers

### 5. Engagement Khách hàng
- Phân tích theo rating
- Số lượt đánh giá
- Số lượt yêu thích

## Tối ưu hóa Performance

### Indexing Strategy
- Clustered index trên fact table
- Non-clustered indexes cho các foreign keys
- Covering indexes cho các truy vấn phổ biến
- Columnstore index cho analytical workloads

### Partitioning (Khuyến nghị)
- Partition fact table theo time_id
- Archive dữ liệu cũ khi cần thiết

## Bảo trì và Monitoring

### ETL Monitoring
- Batch ID tracking
- Data quality checks
- Error handling và logging

### Regular Tasks
- Update time dimension
- Refresh summary tables
- Monitor query performance
- Archive old data

## Mở rộng Tương lai

### Potential Enhancements
1. **Real-time streaming**: Thêm real-time data processing
2. **Machine Learning**: Tích hợp predictive analytics
3. **Advanced Analytics**: Thêm customer segmentation
4. **Mobile Analytics**: Thêm mobile app metrics
5. **Social Media**: Tích hợp social media sentiment

### Additional Dimensions
- DIM_Customer (nếu có dữ liệu khách hàng)
- DIM_Geography (nếu có dữ liệu địa lý)
- DIM_Promotion (nếu có dữ liệu khuyến mãi)

## Troubleshooting

### Common Issues
1. **CSV Import Errors**: Kiểm tra encoding và format
2. **Performance Issues**: Review indexing strategy
3. **Data Quality**: Implement data validation rules
4. **ETL Failures**: Check foreign key constraints

### Support
- Kiểm tra log files trong ETL process
- Sử dụng data profiling tools
- Monitor system resources during ETL

---
**Phiên bản**: 1.0  
**Ngày tạo**: November 2025  
**Tác giả**: Data Warehouse Team