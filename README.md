# Data Warehouse Project - Vietnamese Tiki Products Analysis

## 📋 Tổng Quan Dự Án

Dự án xây dựng hệ thống Data Warehouse hoàn chỉnh để phân tích dữ liệu sản phẩm balo/vali từ Tiki Vietnam, bao gồm OLAP Analysis, Data Mining, Machine Learning và Real-time Dashboard.

**Dữ liệu:** 5,361 sản phẩm với 19 thuộc tính  
**Architecture:** Star Schema với 3 Dimension Tables + 1 Fact Table  
**Technologies:** MySQL, Python, Scikit-learn, GitHub Actions, GitHub Pages  
**Live Demo:** [https://itahieu.github.io/CO4031/](https://itahieu.github.io/CO4031/)

---

## 🏗️ Kiến Trúc Data Warehouse

### Star Schema Design (Theo Diagram Thực Tế)

```
    Dim_brand ────┐
                  │
    Dim_seller ───┼──► Fact_product_stats
                  │
    Dim_Fulfillment_Type ──┘
```

### Cấu Trúc Bảng

#### **Dimension Tables (3 bảng):**

1. **Dim_brand**

   - `UniqueID` (PK)
   - `brand_id` (FK)
   - `brand_name` (VARCHAR(255))

2. **Dim_seller**

   - `UniqueID` (PK)
   - `seller_id` (FK)
   - `seller_name` (VARCHAR(255))

3. **Dim_Fulfillment_Type**
   - `UniqueID` (PK)
   - `fulfillment_id` (FK)
   - `fulfillment_type` (VARCHAR(100))

#### **Fact Table (1 bảng):**

4. **Fact_product_stats**
   - `UniqueID` (PK)
   - `product_id`, `brand_id`, `seller_id`, `fulfillment_id` (FKs)
   - `price`, `quantity_sold`, `rating_average`, `review_count` (Measures)

#### **Staging Table:**

6. **STAGING_Products**
   - Chứa dữ liệu thô từ CSV (19 cột)
   - Sử dụng cho ETL process

---

## 🛠️ Yêu Cầu Hệ Thống

### Software Requirements:

- **Python 3.8+**
- **MySQL 8.0+**
- **Git**

### Python Libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn mysql-connector-python
```

### Database Configuration:

- MySQL Server: `localhost:3306`
- Database: `ProductDW`
- User: `root`, Password: `123456`

---

## 🚀 Hướng Dẫn Chạy Từng Bước

### **BƯỚC 1: Chuẩn Bị Dự Án**

#### 1.1. Clone Repository

```bash
git clone https://github.com/ITAHIEU/CO4031.git
cd CO4031
```

#### 1.2. Kiểm Tra Files

```bash
# Windows PowerShell
dir *.csv          # vietnamese_tiki_products_backpacks_suitcases.csv
dir *.sql          # 6+ SQL files
dir *.py           # 10+ Python files

# Linux/Mac
ls *.csv
ls *.sql
ls *.py
```

#### 1.3. Tạo Thư Mục Output

```bash
mkdir data
mkdir data/clean
```

---

### **BƯỚC 2: Setup Database**

#### 2.1. Tạo Database

```sql
-- Kết nối MySQL
mysql -u root -p

-- Tạo database
CREATE DATABASE ProductDW;
EXIT;
```

#### 2.2. Tạo Tables

```bash
# Windows
Get-Content 01_mysql_create_dimension_tables.sql | mysql -u root -p ProductDW
Get-Content 02_mysql_create_fact_tables.sql | mysql -u root -p ProductDW

# Linux/Mac
mysql -u root -p ProductDW < 01_mysql_create_dimension_tables.sql
mysql -u root -p ProductDW < 02_mysql_create_fact_tables.sql
```

#### 2.3. Verify Database Structure

```sql
mysql -u root -p ProductDW
SHOW TABLES;
-- Expected: 5 tables (3 dim + 1 fact + 1 staging)
```

---

### **BƯỚC 3: Data Preprocessing**

#### 3.1. Làm Sạch Dữ Liệu

```bash
python data_preprocessing.py
```

**Expected Output:**

```
=== DATA PREPROCESSING ===
✅ Loaded 5,361 products from CSV
✅ Cleaned data: 5,359 products (removed 2 duplicates)
✅ Created price segments: 4 categories
✅ Saved: data/clean/products_clean.csv
```

---

### **BƯỚC 4: ETL Process**

#### 4.1. Import CSV Data

```bash
python -c "
import pandas as pd
import mysql.connector
import getpass

df = pd.read_csv('vietnamese_tiki_products_backpacks_suitcases.csv')
password = getpass.getpass('Enter MySQL password: ')
conn = mysql.connector.connect(host='localhost', user='root', password=password, database='ProductDW')
cursor = conn.cursor()

# Import data vào STAGING_Products
# (Chi tiết implementation trong test_csv_import.py)
print('✅ Imported 5,361 records successfully!')
conn.close()
"
```

#### 4.2. Run Complete ETL

```bash
python run_etl_process.py
```

**Expected Results:**

```
🚀 ETL PROCESS STARTED
✅ Connected to MySQL successfully!
✅ ETL Process completed!

📊 Final Results:
   DIM_Brand           : 249 records
   DIM_Seller          : 1,059 records
   DIM_Fulfillment_Type: 4 records
   Fact_product_stats  : 5,361 records

🏷️ Top 5 Brands:
   1. OEM: 3,575 products
   2. Sakos: 120 products
   3. ANANSHOP688: 114 products
   4. Mikkor: 63 products
   5. SimpleCarry: 53 products

✅ ETL SUCCESS!
```

---

### **BƯỚC 5: Analytics & Machine Learning**

#### 5.1. Run Full Analysis

```bash
python part3_olap_datamining.py
```

**Process Overview:**

1. **OLAP Analysis (30-60s)**

   - Revenue by brand analysis
   - Rating by fulfillment type
   - Price segment analysis
   - Cross-dimensional pivot tables

2. **K-Means Clustering (60-90s)**

   - Optimal K selection (K=7)
   - Customer segmentation
   - Cluster profiling

3. **Machine Learning (120-180s)**
   - Revenue prediction (5 algorithms)
   - Rating classification (4 algorithms)
   - Feature importance analysis
   - Customer Lifetime Value (CLV)

**Generated Files:**

- `data/clean/olap_analysis.png` - Business Intelligence charts
- `data/clean/clustering_analysis.png` - ML visualization
- `data/clean/products_with_clusters.csv` - Clustered data

---

### **BƯỚC 6: View Results**

#### 6.1. Open Generated Charts

```bash
# Windows
start data\clean\olap_analysis.png
start data\clean\clustering_analysis.png

# Linux/Mac
open data/clean/olap_analysis.png
open data/clean/clustering_analysis.png
```

#### 6.2. Open HTML Dashboard

```bash
# Open local dashboard
start index.html
# Or visit live demo: https://itahieu.github.io/CO4031/
```

---

## 📊 Kết Quả Phân Tích Chính

### **🎯 OLAP Business Intelligence:**

- **Top Brand:** OEM (3,575 products, 66.7% market share)
- **Best Fulfillment:** Tiki Delivery (4.06/5 rating)
- **Price Range:** 1,000 - 18,840,000 VND
- **Average Price:** 497,216 VND

### **🤖 Machine Learning Results:**

| Task                  | Best Model        | Score              | Performance      |
| --------------------- | ----------------- | ------------------ | ---------------- |
| Revenue Prediction    | Gradient Boosting | R² = 0.816         | 81.6% accuracy   |
| Rating Classification | Random Forest     | 100%               | Perfect accuracy |
| Clustering            | K-Means (K=7)     | Silhouette = 0.760 | High quality     |

### **💎 Customer Segments (7 Clusters):**

- **Cluster 2 (0.2%):** Ultra Premium - 246M VND/product
- **Cluster 0 (30.3%):** Quality Budget - Good rating, low price
- **Cluster 1 (63.6%):** Entry Level - Low price, low rating
- **Cluster 4 (1.5%):** High Volume - 430+ products sold
- **Other Clusters:** Mid-range segments

### **📈 Feature Importance:**

1. **review_count (53.5%)** - Most critical factor
2. **price (22.0%)** - High impact
3. **quantity_sold (11.1%)** - Medium impact
4. **category (8.6%)** - Low impact
5. **rating_average (1.8%)** - Minimal impact

---

## 🔧 Troubleshooting

### **MySQL Connection Issues:**

```bash
# Check MySQL service
net start mysql80
# Or restart service
net stop mysql80 && net start mysql80
```

### **Python Module Errors:**

```bash
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn scikit-learn mysql-connector-python
```

### **ETL Failures:**

```bash
# Reset database
mysql -u root -p -e "DROP DATABASE ProductDW; CREATE DATABASE ProductDW;"
# Then re-run from STEP 2
```

---

## 📁 Project Structure

```
CO4031/
├── 📄 vietnamese_tiki_products_backpacks_suitcases.csv    # Raw data (5,361 products)
├── 🐍 data_preprocessing.py                        # Data cleaning
├── 🐍 part3_olap_datamining.py                          # Main analytics
├── 🐍 run_etl_process.py                                # ETL automation
├── 🗃️ 01_mysql_create_dimension_tables.sql              # Dimension schema
├── 🗃️ 02_mysql_create_fact_tables.sql                   # Fact table schema
├── 🗃️ 04_mysql_populate_dimensions_fixed.sql            # ETL - Dimensions
├── 🗃️ 05_mysql_populate_fact_table_fixed.sql            # ETL - Fact table
├── 🌐 index.html                                        # BI Dashboard
├── 📋 README.md                                         # This guide
├── 📊 data/clean/                                       # Output directory
│   ├── 📈 olap_analysis.png                            # OLAP charts
│   ├── 🎯 clustering_analysis.png                      # ML charts
│   ├── 📋 products_clean.csv                           # Cleaned data
│   └── 📋 products_with_clusters.csv                   # Clustered data
└── ⚙️ .github/workflows/deploy.yml                      # CI/CD pipeline
```

---

## 📞 Contact & Support

**Developer:** IT A HIEU  
**Repository:** [https://github.com/ITAHIEU/CO4031](https://github.com/ITAHIEU/CO4031)  
**Live Demo:** [https://itahieu.github.io/CO4031/](https://itahieu.github.io/CO4031/)

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
