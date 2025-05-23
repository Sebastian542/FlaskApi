from app import db


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    stock = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))
    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    documento = db.Column(db.String(20))
    tipo_cliente_id = db.Column(db.Integer)

class Categoria(db.Model):
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Factura(db.Model):
    id_factura = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    metodo_pago = db.Column(db.String(50))
    id_estado = db.Column(db.Integer)
    total_facturas = db.Column(db.Float)

class Resena(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    comentario = db.Column(db.String(255))
    puntuacion = db.Column(db.Integer)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accion = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
