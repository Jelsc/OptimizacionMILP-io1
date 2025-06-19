from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpBinary, LpContinuous
from .utils import get_aulas, get_grupos, get_horarios

def resolver_asignacion(delta: float = 0.2, penalizacion: float = 10):
    # Obtener los datos usando las funciones que ya tienes
    aulas     = get_aulas()     # Lista de diccionarios
    grupos    = get_grupos()    # Lista de diccionarios
    horarios  = get_horarios()  # Lista de diccionarios

    # 2. Crear diccionarios rápidos de acceso para grupos y aulas
    gr_d = {g["id"]: g["nombre"] for g in grupos}   # Diccionario: id → nombre del grupo
    hr_d = {h["id"]: {"bloque": h["bloque"], "hora": h["hora"]} for h in horarios}  # id → bloque + hora
    C = {a["id"]: a["capacidad"] for a in aulas}  # Diccionario: id → capacidad del aula

    # Índices
    I = [g["id"] for g in grupos]  # Listado de IDs de grupos
    J = [a["id"] for a in aulas]   # Listado de IDs de aulas
    T = [h["id"] for h in horarios]  # Listado de IDs de horarios

    # Datos rápidos para lookup
    S = {g["id"]: g["estudiantes"] for g in grupos}  # Diccionario: id → cantidad de estudiantes por grupo

    # ---------- Modelo ----------
    m = LpProblem("Asignacion_Aulas", LpMaximize)

    # Variables
    x = LpVariable.dicts("x", [(i, j, t) for i in I for j in J for t in T], 0, 1, LpBinary)
    u = LpVariable.dicts("U", [(i, j, t) for i in I for j in J for t in T], 0, None, LpContinuous)

    # Función objetivo
    m += lpSum(S[i] * x[(i, j, t)] for i in I for j in J for t in T) \
         - penalizacion * lpSum(u[(i, j, t)] for i in I for j in J for t in T)

    # --- Restricciones ---

    # 1. Cada grupo debe ser asignado exactamente una vez
    for i in I:
        m += lpSum(x[(i, j, t)] for j in J for t in T) == 1

    # 2. Un aula-horario puede recibir como máximo un grupo
    for j in J:
        for t in T:
            m += lpSum(x[(i, j, t)] for i in I) <= 1

    # 3. La capacidad del aula debe ser suficiente
    for i in I:
        for j in J:
            for t in T:
                m += S[i] * x[(i, j, t)] <= C[j]

    # 4. Penalización cuando el espacio libre excede δ * Cj
    for i in I:
        for j in J:
            for t in T:
                m += u[(i, j, t)] >= (C[j] - S[i] - delta * C[j]) * x[(i, j, t)]

    # ---------- Resolver ----------
    m.solve()  # Usa CBC por defecto

    # ---------- Resultados ----------
    asignaciones = []
    for i in I:
        for j in J:
            for t in T:
                if x[(i, j, t)].value() == 1:
                    asignaciones.append({
                        "grupo_id": i,
                        "grupo_nombre": gr_d[i],  # Acceso directo con diccionario
                        "aula": j,
                        "horario_id": t,
                        "bloque": hr_d[t]["bloque"],  # Acceso rápido con diccionario
                        "rango": hr_d[t]["hora"],  # Acceso rápido con diccionario
                        "vacantes": C[j] - S[i]
                    })

    # Imprimir las asignaciones óptimas
    print("Asignaciones óptimas:")
    for a in asignaciones:
        print(a)

    print(f"\nValor función objetivo: {m.objective.value():.0f}")
    return asignaciones
