from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la base de datos desde variable de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://root:SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74@dpg-d0obb9uuk2gs73ftusdg-a:5432/ferreteria_mejorada'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Producto  # Importar el modelo después de crear db

@app.route('/')
def index():
    productos = Producto.query.all()
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['POST'])
def add_producto():
    nombre = request.form.get('nombre')
    precio = request.form.get('precio')

    if nombre and precio:
        nuevo_producto = Producto(nombre=nombre, precio=float(precio))
        db.session.add(nuevo_producto)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_producto(id):
    producto = Producto.query.get(id)
    if producto:
        db.session.delete(producto)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
