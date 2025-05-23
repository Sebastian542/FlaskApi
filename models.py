from db import get_connection

def crear_tabla_productos():
    query = """
    CREATE TABLE IF NOT EXISTS productos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        descripcion TEXT,
        precio NUMERIC(10, 2) NOT NULL,
        stock INTEGER NOT NULL
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()

def insertar_producto(nombre, descripcion, precio, stock):
    query = """
    INSERT INTO productos (nombre, descripcion, precio, stock)
    VALUES (%s, %s, %s, %s);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (nombre, descripcion, precio, stock))
        conn.commit()

def listar_productos():
    query = "SELECT * FROM productos;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
