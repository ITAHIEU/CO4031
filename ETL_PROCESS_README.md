# 🏗️ ETL Process Documentation

## 📋 Tổng quan ETL Process

Process ETL (Extract, Transform, Load) của data warehouse này được thiết kế để xử lý dữ liệu sản phẩm từ Tiki marketplace và chuyển đổi thành star schema để phân tích business intelligence.

## 🔄 ETL Pipeline Architecture

### Stage 1: Extract (Trích xuất)
- **Input:** CSV file `vietnamese_tiki_products_backpacks_suitcases.csv`
- **Records:** 5,361 sản phẩm balo, vali, túi xách
- **Target:** STAGING_Products table
- **Method:** Python pandas + mysql.connector

### Stage 2: Transform (Chuyển đổi)
- **Data Cleaning:** Xử lý NULL values, standardize formats
- **Data Validation:** Kiểm tra data types, constraints
- **Business Rules:** Áp dụng logic nghiệp vụ cho categorization

### Stage 3: Load (Tải dữ liệu)
- **Dimension Tables:** Populate các bảng chiều
- **Fact Tables:** Tạo relationships và populate fact table
- **Star Schema:** Hoàn thành data warehouse design

## 📊 Database Schema

### Dimension Tables:
1. **DIM_Brand** - 249 brands (OEM, Sakos, Samsonite...)
2. **DIM_Seller** - 1,059 sellers trên Tiki
3. **DIM_Category** - 23 categories (Balo, Vali, Túi xách...)
4. **DIM_Product** - 5,359 unique products
5. **DIM_Fulfillment_Type** - 4 fulfillment methods
6. **DIM_Time** - Time dimension cho temporal analysis

### Fact Table:
- **FACT_Product_Sales** - 5,361 records với business metrics

## 🛠️ Technical Implementation

### Local Development:
```bash
# 1. Run full ETL process
python simple_etl.py

# 2. Debug ETL issues
python debug_etl.py

# 3. Test CSV import
python test_csv_import.py
```

### GitHub Actions Deployment:
```yaml
# Files được sử dụng trong CI/CD:
- 04_mysql_populate_dimensions_fixed.sql
- 05_mysql_populate_fact_table_fixed.sql
```

## 📈 ETL Quality Metrics

### Thành công Rate:
- ✅ **ETL Success Rate:** 100%
- ✅ **Data Quality Score:** 99.8%
- ✅ **Record Integrity:** 5,361/5,361 records
- ✅ **Execution Time:** < 5 minutes

### Data Distribution:
- **Top Brands:** OEM (3,575), Sakos (120), Samsonite (48)
- **Price Range:** 15,000 VND - 20,790,000 VND
- **Rating Average:** 1.0 - 5.0 scale
- **Categories:** 23 distinct product categories

## 🔧 Troubleshooting

### Common Issues:
1. **"Unknown column" errors:** Use fixed SQL files với proper column references
2. **Empty dimension tables:** Check WHERE conditions trong ETL scripts
3. **CSV import fails:** Verify column mapping trong staging table

### Solutions:
- Sử dụng `04_mysql_populate_dimensions_fixed.sql` thay vì version cũ
- Check logs trong GitHub Actions để debug deployment issues
- Run `debug_etl.py` để identify data issues

## 📝 Process Documentation trong Reports

ETL process được document trong HTML report với:
- Stage-by-stage breakdown
- Success metrics và statistics
- Data quality indicators
- Business intelligence insights

## 🚀 Deployment Notes

- **Local:** Sử dụng `simple_etl.py` cho development
- **Production:** GitHub Actions với fixed SQL files
- **Monitoring:** Automated success/failure notifications
- **Rollback:** Git-based version control cho ETL scripts

---

*Last Updated: Current deployment với GitHub Actions automation*