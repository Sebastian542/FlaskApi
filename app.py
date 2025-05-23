import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_PARAMS = {
    'host': "dpg-d0obb9uuk2gs73ftusdg-a.oregon-postgres.render.com",
    'port': 5432,
    'database': "ferreteria_mejorada",
    'user': "root",
    'password': "SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74"
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

# ---- RUTAS USUARIOS ----
@app.route('/usuarios')
def usuarios():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM usuarios ORDER BY id")
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/agregar', methods=['POST'])
def usuarios_agregar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, password))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def usuarios_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        cur.execute("UPDATE usuarios SET nombre=%s, email=%s, password=%s WHERE id=%s",
                    (nombre, email, password, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('usuarios'))
    else:
        cur.execute("SELECT * FROM usuarios WHERE id=%s", (id,))
        usuario = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('usuario_editar.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def usuarios_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('usuarios'))

# ---- RUTAS PRODUCTOS ----
@app.route('/productos')
def productos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM productos ORDER BY id")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/productos/agregar', methods=['POST'])
def productos_agregar():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    precio = request.form.get('precio')
    stock = request.form.get('stock')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s)",
        (nombre, descripcion, precio, stock)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def productos_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        cur.execute("UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s WHERE id=%s",
                    (nombre, descripcion, precio, stock, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('productos'))
    else:
        cur.execute("SELECT * FROM productos WHERE id=%s", (id,))
        producto = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('producto_editar.html', producto=producto)

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def productos_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('productos'))

# ---- RUTAS CLIENTES ----
@app.route('/clientes')
def clientes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM clientes ORDER BY id")
    clientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/agregar', methods=['POST'])
def clientes_agregar():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    telefono = request.form.get('telefono')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)",
                (nombre, email, telefono))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('clientes'))

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def clientes_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        cur.execute("UPDATE clientes SET nombre=%s, email=%s, telefono=%s WHERE id=%s",
                    (nombre, email, telefono, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('clientes'))
    else:
        cur.execute("SELECT * FROM clientes WHERE id=%s", (id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('cliente_editar.html', cliente=cliente)

@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
def clientes_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM clientes WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('clientes'))

# ---- RUTAS VENTAS ----
@app.route('/ventas')
def ventas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM ventas ORDER BY id")
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('ventas.html', ventas=ventas)

@app.route('/ventas/agregar', methods=['POST'])
def ventas_agregar():
    id_cliente = request.form.get('id_cliente')
    fecha = request.form.get('fecha')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO ventas (id_cliente, fecha) VALUES (%s, %s)",
                (id_cliente, fecha))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('ventas'))

@app.route('/ventas/editar/<int:id>', methods=['GET', 'POST'])
def ventas_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente')
        fecha = request.form.get('fecha')
        cur.execute("UPDATE ventas SET id_cliente=%s, fecha=%s WHERE id=%s",
                    (id_cliente, fecha, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ventas'))
    else:
        cur.execute("SELECT * FROM ventas WHERE id=%s", (id,))
        venta = cur.fetchone()

        cur.execute("SELECT id, nombre FROM clientes ORDER BY nombre")
        clientes = cur.fetchall()

        cur.close()
        conn.close()
        return render_template('venta_editar.html', venta=venta, clientes=clientes)

@app.route('/ventas/eliminar/<int:id>', methods=['POST'])
def ventas_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ventas WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('ventas'))

# ---- RUTAS DETALLE VENTA ----
@app.route('/detalle_venta/<int:id_venta>')
def detalle_venta(id_venta):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        SELECT dv.id, p.nombre AS producto, dv.cantidad, dv.precio_venta
        FROM detalle_venta dv
        JOIN productos p ON dv.id_producto = p.id
        WHERE dv.id_venta = %s
    """, (id_venta,))
    detalles = cur.fetchall()

    cur.execute("SELECT id, nombre FROM productos ORDER BY nombre")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('detalle_venta.html', id_venta=id_venta, detalles=detalles, productos=productos)

@app.route('/detalle_venta/<int:id_venta>/agregar', methods=['POST'])
def detalle_agregar(id_venta):
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad')
    precio_venta = request.form.get('precio_venta')

    if not id_producto or not cantidad or not precio_venta:
        return redirect(url_for('detalle_venta', id_venta=id_venta))

    try:
        id_producto = int(id_producto)
        cantidad = int(cantidad)
        precio_venta = float(precio_venta)
    except ValueError:
        return redirect(url_for('detalle_venta', id_venta=id_venta))

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT stock FROM productos WHERE id=%s", (id_producto,))
    producto = cur.fetchone()
    if producto is None:
        cur.close()
        conn.close()
        return redirect(url_for('detalle_venta', id_venta=id_venta))

    stock_actual = producto[0]
    if cantidad > stock_actual:
        cur.close()
        conn.close()
        return redirect(url_for('detalle_venta', id_venta=id_venta))

    cur.execute("""
        INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_venta)
        VALUES (%s, %s, %s, %s)
    """, (id_venta, id_producto, cantidad, precio_venta))

    nuevo_stock = stock_actual - cantidad
    cur.execute("UPDATE productos SET stock=%s WHERE id=%s", (nuevo_stock, id_producto))

    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalle_venta', id_venta=id_venta))

@app.route('/detalle_venta/<int:id_venta>/eliminar/<int:id_detalle>', methods=['POST'])
def detalle_eliminar(id_venta, id_detalle):
    conn = get_connection()
    cur = conn.cursor()
    # Primero obtener cantidad para reponer stock
    cur.execute("SELECT id_producto, cantidad FROM detalle_venta WHERE id=%s", (id_detalle,))
    detalle = cur.fetchone()
    if detalle:
        id_producto, cantidad = detalle
        # Eliminar detalle
        cur.execute("DELETE FROM detalle_venta WHERE id=%s", (id_detalle,))
        # Actualizar stock
        cur.execute("UPDATE productos SET stock = stock + %s WHERE id = %s", (cantidad, id_producto))
        conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('detalle_venta', id_venta=id_venta))


if __name__ == '__main__':
    app.run(debug=True)
