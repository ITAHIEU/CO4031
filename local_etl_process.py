#!/usr/bin/env python3
"""
Local ETL Process - Setup and run data warehouse locally
"""

import mysql.connector
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_connection():
    """Create database connection using environment variables"""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', '123456'),
        database=os.getenv('MYSQL_DATABASE', 'ProductDW'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        allow_local_infile=True
    )

def run_sql_file(connection, sql_file):
    """Execute SQL file"""
    print(f"[INFO] Running {sql_file}...")
    
    with open(sql_file, 'r', encoding='utf-8') as file:
        sql_content = file.read()
    
    # Split by semicolon and execute each statement
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    cursor = connection.cursor()
    for statement in statements:
        if statement:
            try:
                cursor.execute(statement)
                # Consume any remaining results
                try:
                    cursor.fetchall()
                except:
                    pass
                connection.commit()
            except Exception as e:
                print(f"[WARNING] {e}")
    cursor.close()
    print(f"[SUCCESS] Completed {sql_file}")

def main():
    print("[INFO] Starting Local ETL Process...")
    
    try:
        # Connect to MySQL
        conn = get_db_connection()
        print("[SUCCESS] Connected to MySQL")
        
        # Run SQL files in order
        sql_files = [
            '00_mysql_create_database.sql',
            '01_mysql_create_dimension_tables.sql',
            '02_mysql_create_fact_tables.sql',
            '03_mysql_import_csv_data.sql',
            '04_mysql_populate_dimensions.sql',
            '05_mysql_populate_fact_table.sql'
        ]
        
        for sql_file in sql_files:
            if os.path.exists(sql_file):
                run_sql_file(conn, sql_file)
            else:
                print(f"⚠️  File not found: {sql_file}")
        
        conn.close()
        print("[SUCCESS] ETL Process completed successfully!")
        
        # Run data preprocessing
        print("\n[INFO] Running data preprocessing...")
        os.system("python data_preprocessing.py")
        
        # Run OLAP and Data Mining
        print("\n[INFO] Running OLAP and Data Mining analysis...")
        os.system("python part3_olap_datamining.py")
        
        print("\n[SUCCESS] All processes completed!")
        print("[INFO] Check data/clean/ folder for results")
        print("[INFO] Run 'python -m http.server 8000' to view web interface")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        print("[INFO] Make sure MySQL is running and credentials are correct in .env file")

if __name__ == "__main__":
    main()