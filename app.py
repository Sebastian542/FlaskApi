# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
import mysql.connector
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# MySQL Connection
mysql_conn = mysql.connector.connect(
    host="dpg-d0obb9uuk2gs73ftusdg-a",
    port="5432",
    user="root",
    password="SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74",  # Cambia esto según tu configuración
    database="ferreteria_mejorada"
)
mysql_cursor = mysql_conn.cursor(dictionary=True)

# MongoDB Connection
mongo_client = MongoClient("mongodb+srv://Hoyos:Sha*1028480099@ferreterialogs.i9tps73.mongodb.net/?retryWrites=true&w=majority&appName=FerreteriaLogs")
mongo_db = mongo_client["ferreteria_logs"]
logs_collection = mongo_db["logs_eventos"]
resenas_collection = mongo_db["resenas"]

@app.route("/")
def index():
    mysql_cursor.execute("SELECT * FROM productos")
    productos = mysql_cursor.fetchall()

    mysql_cursor.execute("SELECT * FROM clientes")
    clientes = mysql_cursor.fetchall()

    mysql_cursor.execute("SELECT * FROM categorias")
    categorias = mysql_cursor.fetchall()

    mysql_cursor.execute("SELECT * FROM facturas")
    facturas = mysql_cursor.fetchall()

    logs = list(logs_collection.find())
    for log in logs:
        log["_id"] = str(log["_id"])

    resenas = list(resenas_collection.find())
    for resena in resenas:
        resena["_id"] = str(resena["_id"])

    return render_template("index.html", productos=productos, clientes=clientes, logs=logs, resenas=resenas, categorias=categorias, facturas=facturas)

@app.route("/agregar_producto", methods=["POST"])
def agregar_producto():
    datos = request.form
    mysql_cursor.execute("""
        INSERT INTO productos (nombre, descripcion, stock, precio, id_categoria)
        VALUES (%s, %s, %s, %s, %s)
    """, (datos["nombre"], datos["descripcion"], datos["stock"], datos["precio"], datos["id_categoria"]))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "crear_producto", "nombre": datos["nombre"]})
    return redirect(url_for("index"))

@app.route("/agregar_cliente", methods=["POST"])
def agregar_cliente():
    datos = request.form
    mysql_cursor.execute("""
        INSERT INTO clientes (nombre_completo, telefono, email, direccion, documento, tipo_cliente_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (datos["nombre_completo"], datos["telefono"], datos["email"], datos["direccion"], datos["documento"], datos["tipo_cliente_id"]))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "crear_cliente", "nombre": datos["nombre_completo"]})
    return redirect(url_for("index"))

@app.route("/agregar_resena", methods=["POST"])
def agregar_resena():
    datos = request.form
    resenas_collection.insert_one({
        "producto_id": datos["producto_id"],
        "cliente_id": datos["cliente_id"],
        "comentario": datos["comentario"],
        "puntuacion": int(datos["puntuacion"])
    })
    return redirect(url_for("index"))

@app.route("/agregar_categoria", methods=["POST"])
def agregar_categoria():
    nombre = request.form["nombre_categoria"]
    mysql_cursor.execute("INSERT INTO categorias (nombre_categoria) VALUES (%s)", (nombre,))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "crear_categoria", "nombre": nombre})
    return redirect(url_for("index"))

@app.route("/actualizar_categoria/<int:id>", methods=["POST"])
def actualizar_categoria(id):
    nombre = request.form["nombre_categoria"]
    mysql_cursor.execute("UPDATE categorias SET nombre_categoria = %s WHERE id_categoria = %s", (nombre, id))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "editar_categoria", "id": id, "nombre": nombre})
    return redirect(url_for("index"))

@app.route("/eliminar_categoria/<int:id>", methods=["POST"])
def eliminar_categoria(id):
    mysql_cursor.execute("DELETE FROM categorias WHERE id_categoria = %s", (id,))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "eliminar_categoria", "id": id})
    return redirect(url_for("index"))

@app.route("/crear_factura", methods=["POST"])
def crear_factura():
    datos = request.form
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mysql_cursor.execute("""
        INSERT INTO facturas (id_cliente, fecha_factura, metodo_pago, id_estado, total_facturas)
        VALUES (%s, %s, %s, %s, %s)
    """, (datos["id_cliente"], fecha, datos["metodo_pago"], datos["id_estado"], datos["total_facturas"]))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "crear_factura", "cliente_id": datos["id_cliente"], "total": datos["total_facturas"]})
    return redirect(url_for("index"))

@app.route("/actualizar_factura/<int:id>", methods=["POST"])
def actualizar_factura(id):
    datos = request.form
    mysql_cursor.execute("""
        UPDATE facturas SET metodo_pago = %s, id_estado = %s, total_facturas = %s WHERE id_factura = %s
    """, (datos["metodo_pago"], datos["id_estado"], datos["total_facturas"], id))
    mysql_conn.commit()
    logs_collection.insert_one({"accion": "editar_factura", "factura_id": id})
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
