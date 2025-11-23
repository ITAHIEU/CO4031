-- ========================================
-- ENABLE_LOCAL_INFILE.sql
-- ========================================
-- Bật local_infile để import CSV

-- Kiểm tra cấu hình hiện tại
SHOW VARIABLES LIKE 'local_infile';
SHOW VARIABLES LIKE 'secure_file_priv';

-- Bật local_infile
SET GLOBAL local_infile = 1;

-- Kiểm tra lại
SHOW VARIABLES LIKE 'local_infile';

SELECT 'local_infile enabled! Now you can import CSV files.' as Status;