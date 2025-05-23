# 🛠️ Ferretería - Sistema de Gestión

Este proyecto es una aplicación web desarrollada con **Flask** y **PostgreSQL** para gestionar de forma integral una ferretería. Permite el manejo completo de usuarios, productos, clientes, ventas y detalles de ventas (CRUD completo).

---

## ⚙️ ¿Qué se hizo a nivel técnico?

### 🔧 Backend (Flask + SQLAlchemy)

- Se creó una aplicación **Flask** modular con rutas centralizadas para cada entidad.
- Se definieron **5 modelos principales** usando SQLAlchemy:
  - `Usuario`: para gestionar accesos.
  - `Producto`: con stock y precio.
  - `Cliente`: con información de contacto.
  - `Venta`: ligada a clientes.
  - `DetalleVenta`: relación entre productos y ventas.
- Se implementaron todas las operaciones **CRUD** (crear, leer, actualizar, eliminar) para cada modelo, utilizando SQLAlchemy ORM.
- Se conectó la aplicación a una base de datos **PostgreSQL alojada en Render**, con autenticación mediante URI.
- Se implementó la relación **uno a muchos** entre `Cliente` y `Venta`, y entre `Venta` y `DetalleVenta`.

### 📐 Arquitectura

- Separación clara entre lógica de negocio (`app.py`), modelos (`models.py`) y plantillas (`templates/`).
- Configuración centralizada de la base de datos mediante `config.py`.

### 🎨 Frontend (HTML + Jinja2)

- Se utilizaron **plantillas Jinja2** para renderizar formularios y tablas dinámicamente desde Flask.
- Se diseñaron formularios de creación y edición con HTML5.
- Se usaron condicionales y bucles de Jinja2 para mostrar datos y manejar errores o vacíos.

---

## 🚀 Características

- Gestión de:
  - **Usuarios** (email, contraseña)
  - **Productos** (nombre, precio, stock)
  - **Clientes** (nombre, email, teléfono)
  - **Ventas** (cliente, fecha)
  - **Detalle de ventas** (producto, cantidad, precio unitario)
- CRUD completo
- Interfaz HTML simple y funcional
- Base de datos en la nube (Render)
- Código limpio y modular
