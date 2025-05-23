import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Datos de conexión (se mantienen en variables globales para reusar)
DB_PARAMS = {
    'host': "dpg-d0obb9uuk2gs73ftusdg-a.oregon-postgres.render.com",
    'port': 5432,
    'database': "ferreteria_mejorada",
    'user': "root",
    'password': "SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74"
}

def get_connection():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print("❌ Error al conectar con psycopg2:", e)
        return None

@app.route('/')
def index():
    conn = get_connection()
    if not conn:
        return "Error de conexión a la base de datos.", 500

    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Obtener datos
    cur.execute("SELECT * FROM categorias;")
    categorias = cur.fetchall()

    cur.execute("SELECT p.*, c.nombre_categoria FROM productos p LEFT JOIN categorias c ON p.id_categoria = c.id;")
    productos = cur.fetchall()

    cur.execute("SELECT * FROM clientes;")
    clientes = cur.fetchall()

    # Puedes agregar otras consultas similares para facturas y reseñas

    cur.close()
    conn.close()

    return render_template('index.html',
                           categorias=categorias,
                           productos=productos,
                           clientes=clientes)

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    nombre = request.form['nombre_categoria']
    conn = get_connection()
    if not conn:
        return "Error de conexión a la base de datos.", 500

    cur = conn.cursor()
    cur.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s);", (nombre,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion', '')
    stock = int(request.form['stock'])
    precio = float(request.form['precio'])
    id_categoria = int(request.form['id_categoria'])
    conn = get_connection()
    if not conn:
        return "Error de conexión a la base de datos.", 500
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO productos (nombre, descripcion, stock, precio, id_categoria)
        VALUES (%s, %s, %s, %s, %s);
    """, (nombre, descripcion, stock, precio, id_categoria))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre_completo = request.form['nombre_completo']
    telefono = request.form.get('telefono', '')
    email = request.form.get('email', '')
    direccion = request.form.get('direccion', '')
    documento = request.form.get('documento', '')
    tipo_cliente_id = request.form.get('tipo_cliente_id')
    tipo_cliente_id = int(tipo_cliente_id) if tipo_cliente_id else None

    conn = get_connection()
    if not conn:
        return "Error de conexión a la base de datos.", 500
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clientes (nombre_completo, telefono, email, direccion, documento, tipo_cliente_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (nombre_completo, telefono, email, direccion, documento, tipo_cliente_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    # Solo imprime la versión para confirmar conexión al iniciar
    try:
        conn_test = get_connection()
        if conn_test:
            cur_test = conn_test.cursor()
            cur_test.execute("SELECT version();")
            version = cur_test.fetchone()
            print("✅ Conectado correctamente a PostgreSQL:", version)
            cur_test.close()
            conn_test.close()
    except Exception as e:
        print("❌ Error al conectar con psycopg2 al iniciar:", e)

    app.run(host='0.0.0.0', debug=True)
