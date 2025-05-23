from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.signals import before_first_request

app = Flask(__name__)

# Configuración conexión a PostgreSQL en Render
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql://root:SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74@"
    "dpg-d0obb9uuk2gs73ftusdg-a.db.render.com:5432/ferreteria_mejorada"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo ejemplo de Producto
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

# Función para crear tablas al arrancar el servidor (si no existen)
def crear_tablas():
    with app.app_context():
        db.create_all()
        print("Tablas creadas o ya existentes")

# Conectar la señal para correr antes de la primera petición
before_first_request.connect(crear_tablas, app)

@app.route('/')
def index():
    return "API de la ferretería funcionando!"

@app.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    resultado = []
    for p in productos:
        resultado.append({
            'id': p.id,
            'nombre': p.nombre,
            'precio': p.precio,
            'cantidad': p.cantidad
        })
    return jsonify(resultado)

@app.route('/productos', methods=['POST'])
def crear_producto():
    data = request.json
    nuevo_producto = Producto(
        nombre=data['nombre'],
        precio=data['precio'],
        cantidad=data['cantidad']
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify({'mensaje': 'Producto creado', 'id': nuevo_producto.id}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
