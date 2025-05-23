import psycopg2

def obtener_conexion():
    try:
        conn = psycopg2.connect(
            host="dpg-d0obb9uuk2gs73ftusdg-a.oregon-postgres.render.com",
            port=5432,
            database="ferreteria_mejorada",
            user="root",
            password="SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74"
        )
        return conn
    except Exception as e:
        print("❌ Error al conectar con psycopg2:", e)
        return None
