import sqlite3
from datetime import datetime
import pandas as pd

def init_database():
    """Khởi tạo database SQLite"""
    conn = sqlite3.connect('sentiments.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_sentiment(text, sentiment, confidence):
    """Lưu kết quả phân loại vào database"""
    conn = sqlite3.connect('sentiments.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute(
        'INSERT INTO sentiments (text, sentiment, confidence, timestamp) VALUES (?, ?, ?, ?)',
        (text, sentiment, confidence, timestamp)
    )
    conn.commit()
    conn.close()

def get_all_sentiments():
    """Lấy tất cả lịch sử phân loại"""
    conn = sqlite3.connect('sentiments.db')
    df = pd.read_sql_query('SELECT * FROM sentiments ORDER BY timestamp DESC LIMIT 50', conn)
    conn.close()
    return df

def get_statistics():
    """Lấy thống kê"""
    conn = sqlite3.connect('sentiments.db')
    c = conn.cursor()
    c.execute('SELECT sentiment, COUNT(*) as count FROM sentiments GROUP BY sentiment')
    stats = dict(c.fetchall())
    conn.close()
    return stats

def clear_database():
    """Xóa toàn bộ dữ liệu"""
    conn = sqlite3.connect('sentiments.db')
    c = conn.cursor()
    c.execute('DELETE FROM sentiments')
    conn.commit()
    conn.close()
