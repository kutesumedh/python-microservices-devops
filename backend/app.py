from flask import Flask, jsonify
import psycopg2
import os
import logging

app = Flask(__name__)

# PostgreSQL config
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "mydb")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_PORT = os.environ.get("DB_PORT", 5432)

# Logging setup
LOG_FILE = "/logs/app.log"
os.makedirs("/logs", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')

# DB connection
def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

# Initialize table
conn = get_db_connection()
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(50)
    );
""")
conn.commit()
cur.close()
conn.close()
logging.info("Database initialized.")

# API endpoint
@app.route("/api/data")
def get_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    logging.info("/api/data called")
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)