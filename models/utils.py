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

def add_aula(nombre: str, capacidad: int, piso: int):
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Aula (nombre, capacidad, piso) VALUES (?, ?, ?)",
            (nombre, capacidad, piso)
        )
        conn.commit()

def add_grupo(nombre: str, estudiantes: int, materia: str):
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Grupo (nombre, estudiantes, materia) VALUES (?, ?, ?)",
            (nombre, estudiantes, materia)
        )
        conn.commit()

def add_horario(bloque: str, hora: str):
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Horario (bloque, hora) VALUES (?, ?)",
            (bloque, hora)
        )
        conn.commit()

def delete_aula(aula_id: int):
    """Elimina el aula con el id dado."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Aula WHERE id = ?", (aula_id,))
        conn.commit()

def delete_grupo(grupo_id: int):
    """Elimina el grupo con el id dado."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Grupo WHERE id = ?", (grupo_id,))
        conn.commit()

def delete_horario(horario_id: int):
    """Elimina el horario con el id dado."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM Horario WHERE id = ?", (horario_id,))
        conn.commit()
