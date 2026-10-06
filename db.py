import mysql.connector
from datetime import datetime, timedelta

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Example@",
        database="threatdb"
    )

def create_tables_if_not_exist():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ips (
            id INT AUTO_INCREMENT PRIMARY KEY,
            ip VARCHAR(45),
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS domains (
            id INT AUTO_INCREMENT PRIMARY KEY,
            domain VARCHAR(255),
            timestamp DATETIME
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hashes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hash TEXT,
            timestamp DATETIME
        )
    """)
    
    conn.commit()
    conn.close()

def insert_ips(ip_list):
    create_tables_if_not_exist()
    conn = connect()
    cursor = conn.cursor()
    for ip in ip_list:
        cursor.execute("INSERT INTO ips (ip, timestamp) VALUES (%s, NOW())", (ip,))
    conn.commit()
    conn.close()

def insert_domains(domain_list):
    create_tables_if_not_exist()
    conn = connect()
    cursor = conn.cursor()
    for domain in domain_list:
        cursor.execute("INSERT INTO domains (domain, timestamp) VALUES (%s, NOW())", (domain,))
    conn.commit()
    conn.close()

def insert_hashes(hash_list):
    create_tables_if_not_exist()
    conn = connect()
    cursor = conn.cursor()
    for h in hash_list:
        cursor.execute("INSERT INTO hashes (hash, timestamp) VALUES (%s, NOW())", (h,))
    conn.commit()
    conn.close()

def get_old_records(table_name):
    create_tables_if_not_exist()
    conn = connect()
    cursor = conn.cursor()
    ninety_days_ago = datetime.now() - timedelta(days=90)
    cursor.execute(f"SELECT * FROM {table_name} WHERE timestamp < %s", (ninety_days_ago,))
    old_records = cursor.fetchall()
    conn.close()
    return old_records

def delete_old_records(table_name):
    create_tables_if_not_exist()
    conn = connect()
    cursor = conn.cursor()
    ninety_days_ago = datetime.now() - timedelta(days=90)
    cursor.execute(f"DELETE FROM {table_name} WHERE timestamp < %s", (ninety_days_ago,))
    conn.commit()
    conn.close()
