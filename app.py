from flask import Flask, request, redirect, url_for, flash, render_template
import psycopg2

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambia esto por una clave segura

def get_connection():
    return psycopg2.connect(
        host="dpg-d0obb9uuk2gs73ftusdg-a.oregon-postgres.render.com",
        port=5432,
        database="ferreteria_mejorada",
        user="root",
        password="SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74"
    )

@app.route('/detalle_venta/<int:id_venta>')
def detalle_venta(id_venta):
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Obtener detalles de la venta
        cur.execute("""
            SELECT dv.id, p.nombre, dv.cantidad, dv.precio_venta
            FROM detalle_venta dv
            JOIN productos p ON dv.id_producto = p.id
            WHERE dv.id_venta = %s
        """, (id_venta,))
        detalles = cur.fetchall()
        
        # Obtener lista de productos para el formulario
        cur.execute("SELECT id, nombre FROM productos")
        productos = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    
    return render_template('detalle_venta.html', id_venta=id_venta, detalles=detalles, productos=productos)

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
        cur.execute("SELECT stock FROM productos WHERE id=%s", (id_producto,))
        producto = cur.fetchone()
        if producto is None:
            flash("Producto no encontrado.", "danger")
            return redirect(url_for('detalle_venta', id_venta=id_venta))
        
        stock_actual = producto[0]
        if cantidad > stock_actual:
            flash(f"No hay suficiente stock. Disponible: {stock_actual}", "danger")
            return redirect(url_for('detalle_venta', id_venta=id_venta))
        
        # Insertar detalle de venta
        cur.execute("""
            INSERT INTO detalle_venta (id_venta, id_producto, cantidad, precio_venta)
            VALUES (%s, %s, %s, %s)
        """, (id_venta, id_producto, cantidad, precio_venta))
        
        # Actualizar stock
        nuevo_stock = stock_actual - cantidad
        cur.execute("UPDATE productos SET stock=%s WHERE id=%s", (nuevo_stock, id_producto))
        
        conn.commit()
        flash("Detalle de venta agregado y stock actualizado", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Error: {e}", "danger")
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('detalle_venta', id_venta=id_venta))

if __name__ == '__main__':
    app.run(debug=True)
