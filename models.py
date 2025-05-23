import psycopg2

def crear_tabla_producto():
    try:
        conexion = psycopg2.connect(
            host="dpg-d0obb9uuk2gs73ftusdg-a",
            database="ferreteria_mejorada",
            user="root",
            password="SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74",
            port=5432
        )
        cursor = conexion.cursor()

        crear_tabla_sql = """
        CREATE TABLE IF NOT EXISTS producto (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            descripcion TEXT,
            stock INTEGER NOT NULL,
            precio NUMERIC(10, 2) NOT NULL,
            id_categoria INTEGER
        );
        """

        cursor.execute(crear_tabla_sql)
        conexion.commit()
        print("Tabla 'producto' creada correctamente (o ya existía).")

    except psycopg2.Error as e:
        print("Error creando la tabla:", e)

    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

if __name__ == "__main__":
    crear_tabla_producto()
