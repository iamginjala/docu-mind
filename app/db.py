import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("db_name")
DB_HOST = os.getenv("db_host")
DB_PORT = os.getenv("db_port")
DB_USERNAME = os.getenv("db_username")
DB_PASSWORD = os.getenv("db_password")

conn = psycopg2.connect(f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

cur = conn.cursor()
cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
rows = cur.fetchall()
for table in rows:
    print(table)
conn.close()