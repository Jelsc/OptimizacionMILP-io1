import sqlite3
import os

# Asegurarse que la carpeta 'database/' existe
os.makedirs("database", exist_ok=True)

# Crear y conectar a la base de datos
conn = sqlite3.connect("database/aulas.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Aula")
cursor.execute("DROP TABLE IF EXISTS Grupo")
cursor.execute("DROP TABLE IF EXISTS Horario")

# Crear tabla Aula
cursor.execute("""
CREATE TABLE IF NOT EXISTS Aula (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    capacidad INTEGER NOT NULL,
    piso INTEGER NOT NULL
)
""")

# Insertar Aulas
aulas = [
    ('Aula 101', 45, 1), ('Aula 102', 45, 1), ('Aula 103', 60, 1), ('Aula 104', 30, 1),
    ('Aula 201', 45, 2), ('Aula 202', 45, 2), ('Aula 203', 60, 2), ('Aula 204', 30, 2),
    ('Aula 301', 60, 3), ('Aula 302', 60, 3), ('Aula 303', 40, 3),
    ('Aula 401', 60, 4), ('Aula 402', 60, 4), ('Aula 403', 40, 4),
    ('Aula 501', 120, 5), ('Aula 502', 120, 5)
]

cursor.executemany("INSERT INTO Aula (nombre, capacidad, piso) VALUES (?, ?, ?)", aulas)

# Crear tabla Grupo
cursor.execute("""
CREATE TABLE IF NOT EXISTS Grupo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    estudiantes INTEGER NOT NULL,
    materia TEXT NOT NULL
)
""")

# Insertar Grupos
grupos = [
    ('Grupo 1', 35, 'Cálculo I'),
    ('Grupo 2', 50, 'Física I'),
    ('Grupo 3', 120, 'Introducción a la Ingeniería'),
    ('Grupo 4', 40, 'Redes I'),
    ('Grupo 5', 60, 'Álgebra Lineal')
]

cursor.executemany("INSERT INTO Grupo (nombre, estudiantes, materia) VALUES (?, ?, ?)", grupos)

# Crear tabla Horario
cursor.execute("""
CREATE TABLE IF NOT EXISTS Horario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bloque TEXT NOT NULL,
    hora TEXT NOT NULL
)
""")

# Insertar Horarios
horarios = [
    ('B1', '07:00–09:15'),
    ('B2', '09:15–11:30'),
    ('B3', '11:30–13:45'),
    ('B4', '14:00–16:15'),
    ('B5', '16:15–18:30'),
    ('B6', '18:30–20:45')
]

cursor.executemany("INSERT INTO Horario (bloque, hora) VALUES (?, ?)", horarios)

# Guardar y cerrar
conn.commit()
conn.close()

print("Base de datos creada con éxito")