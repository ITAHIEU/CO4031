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
    """Chạy quá trình ETL hoàn chỉnh từ CSV đến Data Warehouse"""
    print("🚀 BẮT ĐẦU QUÁ TRÌNH ETL HOÀN CHỈNH")
    print(f"⏰ Thời gian bắt đầu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Import pandas để đọc CSV
        import pandas as pd
        
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
            
            # Disable foreign key checks
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0')
            
            # Step 1: Import CSV data
            print("📂 Bước 1: Import CSV data...")
            try:
                df = pd.read_csv('vietnamese_tiki_products_backpacks_suitcases.csv')
                print(f"✅ Đọc được {len(df)} records từ CSV")
                
                # Clear staging table
                cursor.execute('TRUNCATE TABLE STAGING_Products')
                
                # Insert data
                insert_query = '''
                INSERT INTO STAGING_Products 
                (row_index, id, name, description, original_price, price, fulfillment_type, 
                 brand, review_count, rating_average, favourite_count, pay_later, 
                 current_seller, date_created, number_of_images, vnd_cashback, has_video, 
                 category, quantity_sold)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                
                data_to_insert = []
                for index, row in df.iterrows():
                    data_to_insert.append(tuple(row))
                    if len(data_to_insert) >= 500:
                        cursor.executemany(insert_query, data_to_insert)
                        data_to_insert = []
                
                if data_to_insert:
                    cursor.executemany(insert_query, data_to_insert)
                
                connection.commit()
                
                cursor.execute('SELECT COUNT(*) FROM STAGING_Products')
                count = cursor.fetchone()[0]
                print(f"✅ Import thành công: {count} records vào STAGING_Products")
                
            except FileNotFoundError:
                print("❌ Không tìm thấy file CSV, bỏ qua bước import")
            except Exception as e:
                print(f"⚠️  Lỗi import CSV: {e}")
            
            # Step 2: Clear existing data
            print("\n🗑️ Bước 2: Xóa dữ liệu cũ...")
            cursor.execute('TRUNCATE TABLE Fact_product_stats')
            cursor.execute('TRUNCATE TABLE DIM_Brand')
            cursor.execute('TRUNCATE TABLE DIM_Seller')
            cursor.execute('TRUNCATE TABLE DIM_Fulfillment_Type')
            print("✅ Đã xóa dữ liệu cũ")
            
            # Step 3: Populate dimensions
            print("\n🏗️ Bước 3: Populate dimension tables...")
            
            # DIM_Brand
            cursor.execute('''
            INSERT IGNORE INTO DIM_Brand (brand_name)
            SELECT DISTINCT 
                CASE 
                    WHEN brand IS NULL OR TRIM(brand) = '' THEN 'Unknown'
                    ELSE TRIM(brand)
                END as brand_name
            FROM STAGING_Products
            ''')
            cursor.execute('SELECT COUNT(*) FROM DIM_Brand')
            brand_count = cursor.fetchone()[0]
            print(f"   DIM_Brand populated: {brand_count} records")
            
            # DIM_Seller
            cursor.execute('''
            INSERT IGNORE INTO DIM_Seller (seller_name)
            SELECT DISTINCT
                CASE 
                    WHEN current_seller IS NULL OR TRIM(current_seller) = '' THEN 'Unknown Seller'
                    ELSE TRIM(current_seller)
                END as seller_name
            FROM STAGING_Products
            ''')
            cursor.execute('SELECT COUNT(*) FROM DIM_Seller')
            seller_count = cursor.fetchone()[0]
            print(f"   DIM_Seller populated: {seller_count} records")
            
            # DIM_Fulfillment_Type
            cursor.execute('''
            INSERT INTO DIM_Fulfillment_Type (fulfillment_type, description)
            VALUES 
                ('dropship', 'Dropshipping fulfillment'),
                ('tiki_delivery', 'Tiki delivery'),
                ('seller_delivery', 'Seller delivery'),
                ('unknown', 'Unknown fulfillment')
            ''')
            cursor.execute('SELECT COUNT(*) FROM DIM_Fulfillment_Type')
            fulfillment_count = cursor.fetchone()[0]
            print(f"   DIM_Fulfillment_Type populated: {fulfillment_count} records")
            
            # Step 4: Populate fact table
            print("\n📊 Bước 4: Populate fact table...")
            cursor.execute('''
            INSERT INTO Fact_product_stats (
                product_id, brand_id, seller_id, fulfillment_id,
                price, quantity_sold, rating_average, review_count
            )
            SELECT 
                sp.id as product_id,
                db.brand_id,
                ds.seller_id,
                df.fulfillment_id,
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
            WHERE sp.id IS NOT NULL
            ''')
            
            cursor.execute('SELECT COUNT(*) FROM Fact_product_stats')
            fact_count = cursor.fetchone()[0]
            print(f"   Fact_product_stats populated: {fact_count} records")
            
            # Re-enable foreign key checks
            cursor.execute('SET FOREIGN_KEY_CHECKS = 1')
            connection.commit()
            
            print("\n✅ ETL Process hoàn thành!")
            
            # Kiểm tra kết quả cuối cùng
            verify_etl_results(cursor)
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Lỗi ETL Process: {e}")
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")

def verify_etl_results(cursor):
    """Kiểm tra kết quả ETL"""
    print("\n🔍 KIỂM TRA KẾT QUẢ ETL")
    print("=" * 40)
    
    try:
        # Đếm records trong các bảng - theo schema mới
        tables = [
            'DIM_Brand', 'DIM_Seller', 'DIM_Fulfillment_Type',
            'Fact_product_stats', 'STAGING_Products'
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
        

        cursor.execute("""
            SELECT b.brand_name, COUNT(*) as count
            FROM DIM_Brand b
            INNER JOIN Fact_product_stats f ON b.brand_id = f.brand_id
            GROUP BY b.brand_id, b.brand_name
            ORDER BY count DESC
            LIMIT 5
        """)
        
        brands = cursor.fetchall()
        print("🏷️  Top 5 thương hiệu:")
        for i, (brand, count) in enumerate(brands, 1):
            print(f"   {i}. {brand}: {count:,} sản phẩm")
        
        print()
        
        # Top sellers  
        cursor.execute("""
            SELECT s.seller_name, COUNT(*) as count
            FROM DIM_Seller s
            INNER JOIN Fact_product_stats f ON s.seller_id = f.seller_id
            GROUP BY s.seller_id, s.seller_name  
            ORDER BY count DESC
            LIMIT 5
        """)
        
        sellers = cursor.fetchall()
        print("🏪 Top 5 sellers:")
        for i, (seller, count) in enumerate(sellers, 1):
            print(f"   {i}. {seller}: {count:,} sản phẩm")
        
        print()
        
        # Price statistics - theo schema mới
        cursor.execute("""
            SELECT 
                MIN(price) as min_price,
                MAX(price) as max_price,
                AVG(price) as avg_price,
                COUNT(*) as total_products
            FROM Fact_product_stats 
            WHERE price > 0
        """)
        
        price_stats = cursor.fetchone()
        if price_stats and price_stats[0] is not None:
            print("💰 Thống kê giá:")
            print(f"   Giá thấp nhất: {price_stats[0]:,.0f} VND")
            print(f"   Giá cao nhất: {price_stats[1]:,.0f} VND") 
            print(f"   Giá trung bình: {price_stats[2]:,.0f} VND")
            print(f"   Tổng sản phẩm có giá: {price_stats[3]:,}")
        else:
            print("💰 Thống kê giá: Không có dữ liệu")
        
        print()
        
        # Check data integrity
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM Fact_product_stats) as fact_records,
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

def main():
    """Hàm chính"""
    print("🏗️  ETL PROCESS - POPULATE DIMENSION TABLES")
    print("=" * 60)
    
    start_time = time.time()
    
    # Chạy ETL
    run_etl_process()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Thời gian thực hiện: {duration:.2f} giây")
    print("🎉 HOÀN THÀNH ETL PROCESS!")
    print()

if __name__ == "__main__":
    main()