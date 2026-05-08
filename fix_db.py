import pymysql
from werkzeug.security import generate_password_hash
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
    
    # 1. Check if email column exists
    cursor.execute("SHOW COLUMNS FROM users LIKE 'email'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE users ADD COLUMN email VARCHAR(255) DEFAULT NULL")
        print('Added email column')

    # 2. Modify role ENUM to include admin
    cursor.execute("ALTER TABLE users MODIFY COLUMN role ENUM('labour', 'customer', 'admin') NOT NULL")
    print('Modified role ENUM to include admin')
    
    # 3. Insert or Update admin user
    hashed_pw = generate_password_hash('Ankit@123')
    cursor.execute("SELECT * FROM users WHERE email='ankitkare21@gmail.com'")
    admin = cursor.fetchone()
    
    if admin:
        cursor.execute("UPDATE users SET password=%s, role='admin' WHERE email='ankitkare21@gmail.com'", (hashed_pw,))
        print('Updated existing admin password to hash and set role to admin')
    else:
        cursor.execute("INSERT INTO users (name, mobile, email, password, role, verification_status) VALUES ('Admin', '0000000000', 'ankitkare21@gmail.com', %s, 'admin', 'verified')", (hashed_pw,))
        print('Inserted new admin user')
        
    conn.commit()
    cursor.close()
    conn.close()
    print('Database fixes applied successfully.')
except Exception as e:
    print('Error:', e)
