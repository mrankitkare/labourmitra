import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'Ankit@@123'),
    'database': os.environ.get('DB_NAME', 'labourmitra'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'cursorclass': pymysql.cursors.DictCursor
}

try:
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()
    print('Connected to DB')
    
    # 1. Expand the ENUM temporarily to include both verified and approved to avoid data truncation errors
    cursor.execute("ALTER TABLE users MODIFY COLUMN verification_status ENUM('pending', 'verified', 'approved', 'rejected') DEFAULT 'pending'")
    print('Expanded ENUM temporarily')

    # 2. Update any existing 'verified' statuses to 'approved'
    cursor.execute("UPDATE users SET verification_status = 'approved' WHERE verification_status = 'verified'")
    print(f'Updated {cursor.rowcount} rows from verified to approved')

    # 3. Restrict the ENUM strictly to the industry standard
    cursor.execute("ALTER TABLE users MODIFY COLUMN verification_status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending'")
    print('Standardized ENUM to pending, approved, rejected')
    
    conn.commit()
    cursor.close()
    conn.close()
    print('Database status fixes applied successfully.')
except Exception as e:
    print('Error:', e)
