from flask import Flask, render_template, jsonify
from db import obtener_conexion

app = Flask(__name__)

@app.route('/')
def index():
    conn = obtener_conexion()
    datos = {}
    if conn:
        cur = conn.cursor()
        tablas = ['productos', 'clientes', 'categorias', 'facturas', 'resenas', 'logs']
        for tabla in tablas:
            cur.execute(f"SELECT * FROM {tabla};")
            columnas = [desc[0] for desc in cur.description]
            filas = cur.fetchall()
            datos[tabla] = [dict(zip(columnas, fila)) for fila in filas]
        cur.close()
        conn.close()
    return render_template('index.html', datos=datos)

@app.route('/exportar/<tabla>')
def exportar(tabla):
    conn = obtener_conexion()
    if conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {tabla};")
        columnas = [desc[0] for desc in cur.description]
        filas = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify([dict(zip(columnas, fila)) for fila in filas])
    return jsonify({'error': 'No se pudo conectar a la base de datos'})

@app.route('/exportar_todo')
def exportar_todo():
    conn = obtener_conexion()
    datos = {}
    if conn:
        cur = conn.cursor()
        tablas = ['productos', 'clientes', 'categorias', 'facturas', 'resenas', 'logs']
        for tabla in tablas:
            cur.execute(f"SELECT * FROM {tabla};")
            columnas = [desc[0] for desc in cur.description]
            filas = cur.fetchall()
            datos[tabla] = [dict(zip(columnas, fila)) for fila in filas]
        cur.close()
        conn.close()
    return jsonify(datos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
