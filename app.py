from models import crear_tabla_productos, insertar_producto, listar_productos

# Crear la tabla
crear_tabla_productos()

# Insertar producto de ejemplo
insertar_producto("Martillo", "Martillo de acero con mango de goma", 25.99, 15)

# Listar productos
productos = listar_productos()
for p in productos:
    print(f"{p['id']}: {p['nombre']} - {p['descripcion']} (${p['precio']}) Stock: {p['stock']}")
