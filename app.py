from flask import Flask, render_template, request, redirect
from models import db, Producto, Cliente, Categoria, Factura, Resena, Log
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html",
                           productos=Producto.query.all(),
                           clientes=Cliente.query.all(),
                           categorias=Categoria.query.all(),
                           facturas=Factura.query.all(),
                           resenas=Resena.query.all(),
                           logs=Log.query.all())

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    p = Producto(
        nombre=request.form['nombre'],
        descripcion=request.form['descripcion'],
        stock=request.form['stock'],
        precio=request.form['precio'],
        id_categoria=request.form['id_categoria']
    )
    db.session.add(p)
    db.session.add(Log(accion='Nuevo producto', nombre=p.nombre))
    db.session.commit()
    return redirect('/')

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    c = Cliente(
        nombre_completo=request.form['nombre_completo'],
        telefono=request.form['telefono'],
        email=request.form['email'],
        direccion=request.form['direccion'],
        documento=request.form['documento'],
        tipo_cliente_id=request.form['tipo_cliente_id']
    )
    db.session.add(c)
    db.session.add(Log(accion='Nuevo cliente', nombre=c.nombre_completo))
    db.session.commit()
    return redirect('/')

@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
    cat = Categoria(nombre_categoria=request.form['nombre_categoria'])
    db.session.add(cat)
    db.session.add(Log(accion='Nueva categoría', nombre=cat.nombre_categoria))
    db.session.commit()
    return redirect('/')

@app.route('/actualizar_categoria/<int:id_categoria>', methods=['POST'])
def actualizar_categoria(id_categoria):
    cat = Categoria.query.get_or_404(id_categoria)
    cat.nombre_categoria = request.form['nombre_categoria']
    db.session.commit()
    return redirect('/')

@app.route('/eliminar_categoria/<int:id_categoria>', methods=['POST'])
def eliminar_categoria(id_categoria):
    cat = Categoria.query.get_or_404(id_categoria)
    db.session.delete(cat)
    db.session.commit()
    return redirect('/')

@app.route('/crear_factura', methods=['POST'])
def crear_factura():
    f = Factura(
        id_cliente=request.form['id_cliente'],
        metodo_pago=request.form['metodo_pago'],
        id_estado=request.form['id_estado'],
        total_facturas=request.form['total_facturas']
    )
    db.session.add(f)
    db.session.add(Log(accion='Nueva factura', nombre=f"id_cliente: {f.id_cliente}"))
    db.session.commit()
    return redirect('/')

@app.route('/agregar_resena', methods=['POST'])
def agregar_resena():
    r = Resena(
        producto_id=request.form['producto_id'],
        cliente_id=request.form['cliente_id'],
        comentario=request.form['comentario'],
        puntuacion=request.form['puntuacion']
    )
    db.session.add(r)
    db.session.add(Log(accion='Nueva reseña', nombre=r.comentario))
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
