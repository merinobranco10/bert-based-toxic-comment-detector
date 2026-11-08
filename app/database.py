import os
import sqlite3

from pathlib import Path


# ==========================================
# CONFIGURACION BASE DE DATOS
# ==========================================

DB_PATH = os.getenv(
    "DB_PATH",
    str(Path(__file__).resolve().parent.parent / "vigia.db")
)


def conectar():

    conexion = sqlite3.connect(DB_PATH)

    conexion.row_factory = sqlite3.Row

    return conexion


# ==========================================
# INICIALIZAR BASE DE DATOS
# ==========================================

def inicializar_db():

    with conectar() as conexion:

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL,
                infracciones INTEGER DEFAULT 0,
                estado TEXT DEFAULT 'Activo'
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                contenido TEXT NOT NULL,
                es_toxico INTEGER NOT NULL,
                probabilidad REAL NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS moderaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                clasificacion TEXT NOT NULL,
                probabilidad REAL NOT NULL,
                censurado INTEGER NOT NULL,
                infracciones INTEGER NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        usuarios = [
            ("usuario_01",),
            ("usuario_02",),
            ("usuario_03",)
        ]

        conexion.executemany("""
            INSERT OR IGNORE INTO usuarios (nombre)
            VALUES (?)
        """, usuarios)


# ==========================================
# CONSULTAR USUARIO
# ==========================================

def obtener_usuario(nombre):

    with conectar() as conexion:

        return conexion.execute("""
            SELECT *
            FROM usuarios
            WHERE nombre = ?
        """, (nombre,)).fetchone()


# ==========================================
# REGISTRAR MODERACION
# ==========================================

def registrar_moderacion(
    usuario,
    contenido,
    es_toxico,
    probabilidad
):

    with conectar() as conexion:

        if es_toxico:

            conexion.execute("""
                UPDATE usuarios
                SET infracciones = infracciones + 1
                WHERE nombre = ?
            """, (usuario,))

            contenido_guardado = "[COMENTARIO CENSURADO]"

        else:

            contenido_guardado = contenido

        datos_usuario = conexion.execute("""
            SELECT infracciones
            FROM usuarios
            WHERE nombre = ?
        """, (usuario,)).fetchone()

        if datos_usuario is None:
            raise ValueError("Usuario inexistente.")

        infracciones = datos_usuario["infracciones"]

        clasificacion = (
            "Tóxico" if es_toxico
            else "No tóxico"
        )

        conexion.execute("""
            INSERT INTO comentarios (
                usuario,
                contenido,
                es_toxico,
                probabilidad
            )
            VALUES (?, ?, ?, ?)
        """, (
            usuario,
            contenido_guardado,
            int(es_toxico),
            probabilidad
        ))

        conexion.execute("""
            INSERT INTO moderaciones (
                usuario,
                clasificacion,
                probabilidad,
                censurado,
                infracciones
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            usuario,
            clasificacion,
            probabilidad,
            int(es_toxico),
            infracciones
        ))

        return infracciones


# ==========================================
# OBTENER COMENTARIOS
# ==========================================

def obtener_comentarios():

    with conectar() as conexion:

        return conexion.execute("""
            SELECT *
            FROM comentarios
            ORDER BY id DESC
        """).fetchall()


# ==========================================
# OBTENER HISTORIAL
# ==========================================

def obtener_historial():

    with conectar() as conexion:

        return conexion.execute("""
            SELECT *
            FROM moderaciones
            ORDER BY id DESC
        """).fetchall()


# ==========================================
# OBTENER TODOS LOS USUARIOS
# ==========================================

def obtener_usuarios():

    with conectar() as conexion:

        return conexion.execute("""
            SELECT *
            FROM usuarios
            ORDER BY nombre
        """).fetchall()
