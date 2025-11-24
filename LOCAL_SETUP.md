# Local Development Setup Guide

## Yêu cầu hệ thống
- Python 3.8+
- MySQL 8.0+
- Git

## Bước 1: Clone repository
```bash
git clone https://github.com/ITAHIEU/CO4031.git
cd CO4031
```

## Bước 2: Thiết lập Python environment
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Bước 3: Thiết lập MySQL Database
1. Khởi động MySQL server
2. Tạo user và database:
```sql
CREATE USER 'dwh_user'@'localhost' IDENTIFIED BY 'your_password';
CREATE DATABASE ProductDW;
GRANT ALL PRIVILEGES ON ProductDW.* TO 'dwh_user'@'localhost';
FLUSH PRIVILEGES;
```

## Bước 4: Cập nhật connection config
Tạo file `.env` với nội dung:
```
MYSQL_HOST=localhost
MYSQL_USER=dwh_user
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=ProductDW
MYSQL_PORT=3306
```

## Bước 5: Chạy dự án
```bash
# Chạy full setup
python local_setup.py

# Hoặc chạy từng bước:
python local_etl_process.py
python local_analysis.py
python -m http.server 8000
```

## Truy cập kết quả
- Web interface: http://localhost:8000
- Charts: data/clean/*.png
- Data files: data/clean/*.csv