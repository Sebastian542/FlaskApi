from flask import Flask, request, jsonify
from db import get_connection, init_db

app = Flask(__name__)

# Crear tabla si no existe
init_db()

@app.route('/productos', methods=['GET'])
def listar_productos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto ORDER BY id;")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(productos), 200

@app.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = %s;", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conn.close()
    if producto:
        return jsonify(producto), 200
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion', '')
    stock = data.get('stock')
    precio = data.get('precio')
    id_categoria = data.get('id_categoria')

    if not nombre or stock is None or precio is None:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO producto (nombre, descripcion, stock, precio, id_categoria)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (nombre, descripcion, stock, precio, id_categoria))
    nuevo_producto = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(nuevo_producto), 201

@app.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    stock = data.get('stock')
    precio = data.get('precio')
    id_categoria = data.get('id_categoria')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = %s;", (id,))
    producto_existente = cursor.fetchone()
    if not producto_existente:
        cursor.close()
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    cursor.execute("""
        UPDATE producto
        SET nombre=%s, descripcion=%s, stock=%s, precio=%s, id_categoria=%s
        WHERE id=%s RETURNING *;
    """, (nombre, descripcion, stock, precio, id_categoria, id))
    producto_actualizado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(producto_actualizado), 200

@app.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = %s;", (id,))
    producto_existente = cursor.fetchone()
    if not producto_existente:
        cursor.close()
        conn.close()
        return jsonify({"error": "Producto no encontrado"}), 404

    cursor.execute("DELETE FROM producto WHERE id = %s;", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200


if __name__ == '__main__':
    app.run(debug=True)
