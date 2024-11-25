import sqlite3
def actualizar_base_datos():
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()

    # Añadir columnas usuario y clave si no existen
    cursor.execute("ALTER TABLE empleados ADD COLUMN usuario TEXT")
    cursor.execute("ALTER TABLE empleados ADD COLUMN clave TEXT")
