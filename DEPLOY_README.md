# Data Warehouse Project - CO4031

## 🚀 GitHub Actions Auto Deploy

Dự án được tự động deploy qua GitHub Actions mỗi khi push code lên `main` branch.

### 📋 Deploy Pipeline:

1. **Setup Environment**
   - Ubuntu latest
   - MySQL 8.0 service
   - Python 3.9 + dependencies

2. **Database Deployment**
   - Tạo database ProductDW
   - Tạo dimension & fact tables
   - Import CSV data (5,361 records)
   - Populate dimensions & fact tables

3. **Data Analysis**
   - Chạy data preprocessing
   - Thực hiện OLAP analysis
   - Tạo clustering với Machine Learning

4. **Artifacts**
   - Upload charts & analysis results
   - Export cleaned data

### 🔧 Cách sử dụng:

1. **Auto Deploy:** Mỗi lần push code sẽ tự động trigger deploy
2. **Manual Deploy:** Vào Actions tab → Chọn workflow → Run workflow
3. **Monitor:** Xem logs trong Actions tab

### 📊 Kết quả Deploy:

- ✅ Database với 6 dimension tables
- ✅ 1 fact table với 5,361 records  
- ✅ OLAP analysis charts
- ✅ Machine Learning clustering
- ✅ Cleaned datasets

### 🌐 GitHub Actions Status:

[![Deploy Data Warehouse](https://github.com/ITAHIEU/CO4031/actions/workflows/deploy.yml/badge.svg)](https://github.com/ITAHIEU/CO4031/actions/workflows/deploy.yml)

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── deploy.yml              # GitHub Actions workflow
├── data/clean/                 # Cleaned data & analysis results
├── 00-05_mysql_*.sql          # Database pipeline
├── *.py                       # Python analysis scripts
└── *.csv                      # Source data
```