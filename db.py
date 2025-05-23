import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "dpg-d0obb9uuk2gs73ftusdg-a.db.render.com",
    "port": 5432,
    "dbname": "ferreteria_mejorada",
    "user": "root",
    "password": "SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74"
}

def get_connection():
    conn = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        cursor_factory=RealDictCursor
    )
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producto (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        stock INTEGER NOT NULL,
        precio NUMERIC(10, 2) NOT NULL,
        id_categoria INTEGER
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
