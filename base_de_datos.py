import sqlite3
import bcrypt

def inicializar_bd():
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fichajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tipo TEXT NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id)
        )
    """)
    conexion.commit()
    conexion.close()




def agregar_empleado(nombre, usuario, clave):
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()

    # Hash de la clave
    #clave_hash = bcrypt.hashpw(clave.encode('utf-8'), bcrypt.gensalt())

    cursor.execute("INSERT INTO empleados (nombre, usuario, clave) VALUES (?, ?, ?)", (nombre, usuario, clave))
    conexion.commit()
    conexion.close()

def autenticar_empleado(usuario, clave):
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT id, clave FROM empleados WHERE usuario = ?", (usuario,))
    empleado = cursor.fetchone()
    conexion.close()

    if empleado and  empleado[1]==clave:
        return empleado[0]  # Retorna el ID del empleado si es válido
    return None


def obtener_empleados():
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    conexion.close()
    return empleados

def obtener_fichajes():
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT f.id, e.nombre, f.fecha_hora, f.tipo
        FROM fichajes f
        JOIN empleados e ON f.id_empleado = e.id
    """)

def obtener_ultimo_fichaje(id_empleado):
        conexion = sqlite3.connect("empresa.db")
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT tipo 
            FROM fichajes 
            WHERE id_empleado = ? 
            ORDER BY fecha_hora DESC LIMIT 1
        """, (id_empleado,))
        ultimo_fichaje = cursor.fetchone()
        conexion.close()
        return ultimo_fichaje[0] if ultimo_fichaje else None

def actualizar_base_datos():
    conexion = sqlite3.connect("empresa.db")
    cursor = conexion.cursor()

    # Añadir columnas usuario y clave si no existen
    cursor.execute("ALTER TABLE empleados ADD COLUMN usuario TEXT")
    cursor.execute("ALTER TABLE empleados ADD COLUMN clave TEXT")

def registrar_fichaje(id_empleado, tipo):
        # Validar el tipo de fichaje
        ultimo_fichaje = obtener_ultimo_fichaje(id_empleado)
        if ultimo_fichaje == tipo:
            raise ValueError(f"No puedes registrar dos {tipo}s consecutivas.")

        # Registrar el fichaje si pasa la validación
        conexion = sqlite3.connect("empresa.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO fichajes (id_empleado, tipo) VALUES (?, ?)", (id_empleado, tipo))
        conexion.commit()
        conexion.close()


def obtener_fichajes_filtrados(empleado_id=None, mes=None):
        conexion = sqlite3.connect("empresa.db")
        cursor = conexion.cursor()
        query = """
            SELECT f.id, e.nombre, f.fecha_hora, f.tipo
            FROM fichajes f
            JOIN empleados e ON f.id_empleado = e.id
            WHERE 1=1
        """
        parametros = []
        if empleado_id:
            query += " AND f.id_empleado = ?"
            parametros.append(empleado_id)
        if mes:
            query += " AND strftime('%m', f.fecha_hora) = ?"
            parametros.append(mes.zfill(2))
        cursor.execute(query, parametros)
        fichajes = cursor.fetchall()
        conexion.close()
        return fichajes

