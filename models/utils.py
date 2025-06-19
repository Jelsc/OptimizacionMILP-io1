import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "aulas.db"

def _connect():
    return sqlite3.connect(DB_PATH)

def get_aulas():
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, capacidad, piso FROM Aula")
        return [{"id": r[0], "nombre": r[1], "capacidad": r[2], "piso": r[3]} for r in cur.fetchall()]

def get_grupos():
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, estudiantes, materia FROM Grupo")
        return [{"id": r[0], "nombre": r[1], "estudiantes": r[2], "materia": r[3]} for r in cur.fetchall()]

def get_horarios():
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, bloque, hora FROM Horario")
        return [{"id": r[0], "bloque": r[1], "hora": r[2]} for r in cur.fetchall()]
