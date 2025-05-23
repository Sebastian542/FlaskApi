import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, flash, Response
import json

app = Flask(__name__)
app.secret_key = "secretkey123"

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
        print("Error conexión DB:", e)
        return None

@app.route('/')
def index():
    return render_template('index.html')

# ---------------------- CRUD Categorías ----------------------
@app.route('/categorias')
def categorias():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM categorias ORDER BY id;")
    categorias = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/agregar', methods=['POST'])
def categoria_agregar():
    nombre = request.form.get('nombre_categoria')
    if not nombre:
        flash("El nombre es obligatorio.", "danger")
        return redirect(url_for('categorias'))
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s)", (nombre,))
        conn.commit()
        flash("Categoría agregada", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('categorias'))

@app.route('/categorias/editar/<int:id>', methods=['GET', 'POST'])
def categoria_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'GET':
        cur.execute("SELECT * FROM categorias WHERE id=%s", (id,))
        categoria = cur.fetchone()
        cur.close()
        conn.close()
        if not categoria:
            flash("Categoría no encontrada", "warning")
            return redirect(url_for('categorias'))
        return render_template('categoria_editar.html', categoria=categoria)
    else:
        nombre = request.form.get('nombre_categoria')
        if not nombre:
            flash("El nombre es obligatorio.", "danger")
            return redirect(url_for('categoria_editar', id=id))
        try:
            cur.execute("UPDATE categorias SET nombre_categoria=%s WHERE id=%s", (nombre, id))
            conn.commit()
            flash("Categoría actualizada", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('categorias'))

@app.route('/categorias/eliminar/<int:id>', methods=['POST'])
def categoria_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM categorias WHERE id=%s", (id,))
        conn.commit()
        flash("Categoría eliminada", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('categorias'))


# ---------------------- CRUD Productos ----------------------
@app.route('/productos')
def productos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM categorias ORDER BY id;")
    categorias = cur.fetchall()
    cur.execute("""SELECT p.*, c.nombre_categoria 
                   FROM productos p 
                   LEFT JOIN categorias c ON p.id_categoria = c.id 
                   ORDER BY p.id;""")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('productos.html', productos=productos, categorias=categorias)

@app.route('/productos/agregar', methods=['POST'])
def producto_agregar():
    nombre = request.form.get('nombre_producto')
    descripcion = request.form.get('descripcion')
    stock = request.form.get('stock')
    precio = request.form.get('precio')
    id_categoria = request.form.get('id_categoria')
    if not nombre or not stock or not precio or not id_categoria:
        flash("Complete todos los campos obligatorios.", "danger")
        return redirect(url_for('productos'))
    try:
        stock = int(stock)
        precio = float(precio)
        id_categoria = int(id_categoria)
    except ValueError:
        flash("Valores numéricos incorrectos.", "danger")
        return redirect(url_for('productos'))
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO productos 
                       (nombre_producto, descripcion, stock, precio, id_categoria)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (nombre, descripcion, stock, precio, id_categoria))
        conn.commit()
        flash("Producto agregado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('productos'))

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def producto_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'GET':
        cur.execute("SELECT * FROM productos WHERE id=%s", (id,))
        producto = cur.fetchone()
        cur.execute("SELECT * FROM categorias ORDER BY id")
        categorias = cur.fetchall()
        cur.close()
        conn.close()
        if not producto:
            flash("Producto no encontrado", "warning")
            return redirect(url_for('productos'))
        return render_template('producto_editar.html', producto=producto, categorias=categorias)
    else:
        nombre = request.form.get('nombre_producto')
        descripcion = request.form.get('descripcion')
        stock = request.form.get('stock')
        precio = request.form.get('precio')
        id_categoria = request.form.get('id_categoria')
        if not nombre or not stock or not precio or not id_categoria:
            flash("Complete todos los campos obligatorios.", "danger")
            return redirect(url_for('producto_editar', id=id))
        try:
            stock = int(stock)
            precio = float(precio)
            id_categoria = int(id_categoria)
        except ValueError:
            flash("Valores numéricos incorrectos.", "danger")
            return redirect(url_for('producto_editar', id=id))
        try:
            cur.execute("""UPDATE productos SET nombre_producto=%s, descripcion=%s, stock=%s, precio=%s, id_categoria=%s WHERE id=%s""",
                        (nombre, descripcion, stock, precio, id_categoria, id))
            conn.commit()
            flash("Producto actualizado", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('productos'))

@app.route('/productos/eliminar/<int:id>', methods=['POST'])
def producto_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM productos WHERE id=%s", (id,))
        conn.commit()
        flash("Producto eliminado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('productos'))


# ---------------------- CRUD Clientes ----------------------
@app.route('/clientes')
def clientes():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM clientes ORDER BY id;")
    clientes = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/clientes/agregar', methods=['POST'])
def cliente_agregar():
    nombre = request.form.get('nombre')
    telefono = request.form.get('telefono')
    email = request.form.get('email')
    direccion = request.form.get('direccion')
    documento = request.form.get('documento')
    if not nombre or not documento:
        flash("Nombre y documento son obligatorios.", "danger")
        return redirect(url_for('clientes'))
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO clientes (nombre, telefono, email, direccion, documento) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (nombre, telefono, email, direccion, documento))
        conn.commit()
        flash("Cliente agregado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('clientes'))

@app.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'GET':
        cur.execute("SELECT * FROM clientes WHERE id=%s", (id,))
        cliente = cur.fetchone()
        cur.close()
        conn.close()
        if not cliente:
            flash("Cliente no encontrado", "warning")
            return redirect(url_for('clientes'))
        return render_template('cliente_editar.html', cliente=cliente)
    else:
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        direccion = request.form.get('direccion')
        documento = request.form.get('documento')
        if not nombre or not documento:
            flash("Nombre y documento son obligatorios.", "danger")
            return redirect(url_for('cliente_editar', id=id))
        try:
            cur.execute("""UPDATE clientes SET nombre=%s, telefono=%s, email=%s, direccion=%s, documento=%s WHERE id=%s""",
                        (nombre, telefono, email, direccion, documento, id))
            conn.commit()
            flash("Cliente actualizado", "success")
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('clientes'))

@app.route('/clientes/eliminar/<int:id>', methods=['POST'])
def cliente_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM clientes WHERE id=%s", (id,))
        conn.commit()
        flash("Cliente eliminado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('clientes'))


# ---------------------- CRUD Ventas ----------------------
@app.route('/ventas')
def ventas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT v.*, c.nombre AS nombre_cliente
                   FROM ventas v
                   LEFT JOIN clientes c ON v.id_cliente = c.id
                   ORDER BY v.id;""")
    ventas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('ventas.html', ventas=ventas)

@app.route('/ventas/agregar', methods=['GET', 'POST'])
def venta_agregar():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    if request.method == 'GET':
        cur.execute("SELECT * FROM clientes ORDER BY id;")
        clientes = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('venta_agregar.html', clientes=clientes)
    else:
        id_cliente = request.form.get('id_cliente')
        fecha_venta = request.form.get('fecha_venta')
        if not id_cliente or not fecha_venta:
            flash("Cliente y fecha son obligatorios", "danger")
            return redirect(url_for('venta_agregar'))
        try:
            id_cliente = int(id_cliente)
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO ventas (id_cliente, fecha_venta) VALUES (%s, %s) RETURNING id", (id_cliente, fecha_venta))
            id_venta = cur.fetchone()[0]
            conn.commit()
            flash("Venta agregada, ahora agregue detalles.", "success")
            return redirect(url_for('detalle_agregar', id_venta=id_venta))
        except Exception as e:
            conn.rollback()
            flash(f"Error: {e}", "danger")
            return redirect(url_for('ventas'))
        finally:
            cur.close()
            conn.close()

@app.route('/ventas/eliminar/<int:id>', methods=['POST'])
def venta_eliminar(id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Primero eliminar detalles de venta para mantener integridad
        cur.execute("DELETE FROM detalle_venta WHERE id_venta=%s", (id,))
        cur.execute("DELETE FROM ventas WHERE id=%s", (id,))
        conn.commit()
        flash("Venta eliminada junto con sus detalles", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('ventas'))

# ---------------------- CRUD Detalle de Venta ----------------------
@app.route('/detalle_venta/<int:id_venta>')
def detalle_venta(id_venta):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""SELECT dv.*, p.nombre_producto 
                   FROM detalle_venta dv
                   LEFT JOIN productos p ON dv.id_producto = p.id
                   WHERE dv.id_venta = %s
                   ORDER BY dv.id;""", (id_venta,))
    detalles = cur.fetchall()
    cur.execute("SELECT * FROM productos ORDER BY id")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('detalle_venta.html', detalles=detalles, productos=productos, id_venta=id_venta)

@app.route('/detalle_venta/<int:id_venta>/agregar', methods=['POST'])
def detalle_agregar(id_venta):
    id_producto = request.form.get('id_producto')
    cantidad = request.form.get('cantidad')
    precio_venta = request.form.get('precio_venta')
    if not id_producto or not cantidad or not precio_venta:
        flash("Complete todos los campos.", "danger")
        return redirect(url_for('detalle_venta', id_venta=id_venta))
    try:
        id_producto = int(id_producto)
        cantidad = int(cantidad)
        precio_venta = float(precio_venta)
    except ValueError:
        flash("Valores numéricos incorrectos.", "danger")
        return redirect(url_for('detalle_venta', id_venta=id_venta))
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_venta)
                       VALUES (%s, %s, %s, %s)""",
                    (id_venta, id_producto, cantidad, precio_venta))
        conn.commit()
        flash("Detalle agregado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('detalle_venta', id_venta=id_venta))

@app.route('/detalle_venta/<int:id_venta>/eliminar/<int:id_detalle>', methods=['POST'])
def detalle_eliminar(id_venta, id_detalle):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM detalle_venta WHERE id=%s", (id_detalle,))
        conn.commit()
        flash("Detalle eliminado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('detalle_venta', id_venta=id_venta))


# --- API REST simple para obtener productos en JSON ---
@app.route('/api/productos')
def api_productos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM productos ORDER BY id;")
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return Response(json.dumps(productos), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
