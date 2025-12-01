#!/usr/bin/env python3
"""
Run ETL Process to Populate Dimension Tables
Chạy quá trình ETL để populate các dimension tables
"""

import mysql.connector
from mysql.connector import Error
import time
from datetime import datetime

def run_etl_process():
    """Chạy quá trình ETL để populate dimension tables"""
    print("🚀 BẮT ĐẦU QUÁ TRÌNH ETL")
    print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Kết nối MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='ProductDW',
            charset='utf8mb4'
        )
        
        if connection.is_connected():
            print("✅ Kết nối MySQL thành công!")
            
            cursor = connection.cursor(buffered=True)
            
            # Đọc và thực thi file ETL SQL
            print("📖 Đọc file corrected_etl_process.sql...")
            
            with open('corrected_etl_process.sql', 'r', encoding='utf-8') as file:
                sql_commands = file.read()
            
            # Tách các câu lệnh SQL
            commands = sql_commands.split(';')
            
            print("🔄 Thực thi các câu lệnh ETL...")
            print()
            
            for i, command in enumerate(commands):
                command = command.strip()
                if command and not command.startswith('--'):
                    try:
                        cursor.execute(command)
                        
                        # Lấy kết quả nếu có
                        if cursor.with_rows:
                            results = cursor.fetchall()
                            if results:
                                for row in results:
                                    if len(row) == 1:
                                        print(f"   {row[0]}")
                                    else:
                                        print(f"   {' | '.join(map(str, row))}")
                        
                        connection.commit()
                        
                    except Error as e:
                        if "doesn't exist" not in str(e) and "Duplicate entry" not in str(e):
                            print(f"⚠️  Lỗi câu lệnh {i+1}: {e}")
                        continue
            
            print("\n✅ ETL Process hoàn thành!")
            
            # Kiểm tra kết quả cuối cùng
            verify_etl_results(cursor)
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Lỗi ETL Process: {e}")

def verify_etl_results(cursor):
    """Kiểm tra kết quả ETL"""
    print("\n🔍 KIỂM TRA KẾT QUẢ ETL")
    print("=" * 40)
    
    try:
        # Đếm records trong các bảng
        tables = [
            'DIM_Brand', 'DIM_Seller', 'DIM_Category', 
            'DIM_Product', 'DIM_Fulfillment_Type', 'DIM_Time',
            'FACT_Product_Sales', 'STAGING_Products'
        ]
        
        results = {}
        
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                results[table] = count
                print(f"📊 {table:20}: {count:,} records")
            except Error as e:
                print(f"❌ Lỗi kiểm tra {table}: {e}")
        
        print()
        
        # Kiểm tra một số thống kê chi tiết
        print("📈 THỐNG KÊ CHI TIẾT:")
        print("-" * 30)
        
        # Top brands
        cursor.execute("""
            SELECT b.brand_name, COUNT(*) as count
            FROM DIM_Brand b
            INNER JOIN FACT_Product_Sales f ON b.brand_id = f.brand_id
            GROUP BY b.brand_id, b.brand_name
            ORDER BY count DESC
            LIMIT 5
        """)
        
        brands = cursor.fetchall()
        print("🏷️  Top 5 thương hiệu:")
        for i, (brand, count) in enumerate(brands, 1):
            print(f"   {i}. {brand}: {count:,} sản phẩm")
        
        print()
        
        # Top categories  
        cursor.execute("""
            SELECT c.category_name, COUNT(*) as count
            FROM DIM_Category c
            INNER JOIN FACT_Product_Sales f ON c.category_id = f.category_id
            GROUP BY c.category_id, c.category_name  
            ORDER BY count DESC
            LIMIT 5
        """)
        
        categories = cursor.fetchall()
        print("📂 Top 5 danh mục:")
        for i, (category, count) in enumerate(categories, 1):
            print(f"   {i}. {category}: {count:,} sản phẩm")
        
        print()
        
        # Price statistics
        cursor.execute("""
            SELECT 
                MIN(current_price) as min_price,
                MAX(current_price) as max_price,
                AVG(current_price) as avg_price,
                COUNT(*) as total_products
            FROM FACT_Product_Sales 
            WHERE current_price > 0
        """)
        
        price_stats = cursor.fetchone()
        if price_stats:
            print("💰 Thống kê giá:")
            print(f"   Giá thấp nhất: {price_stats[0]:,.0f} VND")
            print(f"   Giá cao nhất: {price_stats[1]:,.0f} VND") 
            print(f"   Giá trung bình: {price_stats[2]:,.0f} VND")
            print(f"   Tổng sản phẩm có giá: {price_stats[3]:,}")
        
        print()
        
        # Check data integrity
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM FACT_Product_Sales) as fact_records,
                (SELECT COUNT(*) FROM STAGING_Products) as staging_records
        """)
        
        integrity = cursor.fetchone()
        if integrity:
            fact_count = integrity[0]  
            staging_count = integrity[1]
            success_rate = (fact_count / staging_count * 100) if staging_count > 0 else 0
            
            print("🔗 Kiểm tra tính toàn vẹn dữ liệu:")
            print(f"   Staging records: {staging_count:,}")
            print(f"   Fact records: {fact_count:,}")  
            print(f"   Success rate: {success_rate:.1f}%")
            
            if success_rate > 90:
                print("   ✅ ETL thành công!")
            elif success_rate > 70:
                print("   ⚠️  ETL hoàn thành nhưng có một số dữ liệu bị mất")
            else:
                print("   ❌ ETL có vấn đề, cần kiểm tra lại")
        
    except Error as e:
        print(f"❌ Lỗi kiểm tra kết quả: {e}")

def create_sample_queries():
    """Tạo các query mẫu để test data warehouse"""
    print("\n📝 TẠO CÁC QUERY MẪU")
    print("=" * 35)
    
    queries = """-- ========================================

USE ProductDW;

-- 1. Phân tích theo thương hiệu
SELECT 'BRAND ANALYSIS' as Analysis_Type;
SELECT 
    b.brand_name,
    COUNT(f.product_id) as total_products,
    SUM(f.quantity_sold) as total_quantity_sold,
    AVG(f.current_price) as avg_price,
    SUM(f.current_price * f.quantity_sold) as total_revenue
FROM DIM_Brand b
INNER JOIN FACT_Product_Sales f ON b.brand_id = f.brand_id
GROUP BY b.brand_id, b.brand_name
ORDER BY total_revenue DESC
LIMIT 10;

-- 2. Phân tích theo danh mục
SELECT 'CATEGORY ANALYSIS' as Analysis_Type;
SELECT 
    c.category_name,
    COUNT(f.product_id) as total_products,
    AVG(f.current_price) as avg_price,
    AVG(f.rating_average) as avg_rating,
    SUM(f.quantity_sold) as total_sold
FROM DIM_Category c  
INNER JOIN FACT_Product_Sales f ON c.category_id = f.category_id
GROUP BY c.category_id, c.category_name
ORDER BY total_products DESC;

-- 3. Top sản phẩm bán chạy
SELECT 'TOP SELLING PRODUCTS' as Analysis_Type;
SELECT 
    p.product_name,
    b.brand_name,
    c.category_name,
    f.current_price,
    f.quantity_sold,
    f.rating_average,
    (f.current_price * f.quantity_sold) as revenue
FROM FACT_Product_Sales f
INNER JOIN DIM_Product p ON f.product_id = p.product_id
INNER JOIN DIM_Brand b ON f.brand_id = b.brand_id  
INNER JOIN DIM_Category c ON f.category_id = c.category_id
ORDER BY f.quantity_sold DESC, revenue DESC
LIMIT 10;

-- 4. Phân tích giá theo khoảng
SELECT 'PRICE RANGE ANALYSIS' as Analysis_Type;
SELECT 
    CASE 
        WHEN current_price < 100000 THEN 'Under 100K'
        WHEN current_price < 500000 THEN '100K-500K'
        WHEN current_price < 1000000 THEN '500K-1M'  
        WHEN current_price < 5000000 THEN '1M-5M'
        ELSE 'Above 5M'
    END as price_range,
    COUNT(*) as product_count,
    AVG(rating_average) as avg_rating,
    SUM(quantity_sold) as total_sold
FROM FACT_Product_Sales
WHERE current_price > 0
GROUP BY 
    CASE 
        WHEN current_price < 100000 THEN 'Under 100K'
        WHEN current_price < 500000 THEN '100K-500K'
        WHEN current_price < 1000000 THEN '500K-1M'
        WHEN current_price < 5000000 THEN '1M-5M'  
        ELSE 'Above 5M'
    END
ORDER BY MIN(current_price);

-- 5. Phân tích seller performance  
SELECT 'SELLER PERFORMANCE' as Analysis_Type;
SELECT 
    s.seller_name,
    COUNT(f.product_id) as total_products,
    AVG(f.current_price) as avg_product_price,
    AVG(f.rating_average) as avg_rating,
    SUM(f.quantity_sold) as total_quantity_sold
FROM DIM_Seller s
INNER JOIN FACT_Product_Sales f ON s.seller_id = f.seller_id  
GROUP BY s.seller_id, s.seller_name
HAVING total_products >= 5
ORDER BY total_quantity_sold DESC
LIMIT 15;
"""
    
    with open('sample_olap_queries.sql', 'w', encoding='utf-8') as f:
        f.write(queries)
    
    print("✅ Đã tạo file: sample_olap_queries.sql")
    print("💡 Bạn có thể chạy file này để test Data Warehouse")

def main():
    """Hàm chính"""
    print("🏗️  ETL PROCESS - POPULATE DIMENSION TABLES")
    print("=" * 60)
    
    start_time = time.time()
    
    # Chạy ETL
    run_etl_process()
    
    # Tạo sample queries
    create_sample_queries()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Thời gian thực hiện: {duration:.2f} giây")
    print("🎉 HOÀN THÀNH ETL PROCESS!")
    print()

if __name__ == "__main__":
    main()