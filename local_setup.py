#!/usr/bin/env python3
"""
Complete Local Setup - One-click setup for local development
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run shell command with description"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_mysql_running():
    """Check if MySQL service is running"""
    try:
        # Try to connect to MySQL using .env credentials
        from dotenv import load_dotenv
        import mysql.connector
        load_dotenv()
        
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            port=int(os.getenv('MYSQL_PORT', 3306))
        )
        conn.close()
        return True
    except Exception as e:
        print(f"MySQL connection error: {e}")
        return False

def create_env_file():
    """Create .env file with default configuration"""
    env_content = """# MySQL Database Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=ProductDW
MYSQL_PORT=3306
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
    else:
        print("ℹ️  .env file already exists")

def main():
    print("🚀 Data Warehouse Local Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return
    
    # Create .env file
    create_env_file()
    
    # Install requirements
    if os.path.exists('requirements.txt'):
        if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
            print("💡 Try: pip install --user -r requirements.txt")
            return
    else:
        print("⚠️  requirements.txt not found")
    
    # Check MySQL
    if not check_mysql_running():
        print("❌ MySQL not running or not accessible")
        print("💡 Please start MySQL service and update .env file with correct credentials")
        return
    
    print("✅ MySQL is accessible")
    
    # Run ETL process
    print("\n📊 Running ETL Process...")
    if run_command("python local_etl_process.py", "ETL Process"):
        print("✅ Data warehouse setup completed")
    else:
        print("❌ ETL process failed")
        return
    
    # Run analysis
    print("\n🤖 Running Analysis...")
    if run_command("python local_analysis.py", "Data Analysis"):
        print("✅ Analysis completed")
    else:
        print("⚠️  Analysis failed, but ETL was successful")
    
    # Start web server
    print("\n🌐 Starting web server...")
    print("🎉 Setup completed successfully!")
    print("📊 View results at: http://localhost:8000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        os.system("python -m http.server 8000")
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()