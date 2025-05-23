import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = "postgresql://root:SVtoDZA0bt6Zuf3FF56Lfr6bFQsqdI74@dpg-d0obb9uuk2gs73ftusdg-a.oregon-postgres.render.com/ferreteria_mejorada"

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
