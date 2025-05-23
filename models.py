from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    stock = db.Column(db.Integer)
    precio = db.Column(db.Float)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    documento = db.Column(db.String(20))
    tipo_cliente_id = db.Column(db.Integer)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100))

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    metodo_pago = db.Column(db.String(50))
    id_estado = db.Column(db.Integer)
    total_facturas = db.Column(db.Float)

class Resena(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    comentario = db.Column(db.String(300))
    puntuacion = db.Column(db.Integer)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
