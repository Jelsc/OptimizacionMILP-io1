import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import sys, pathlib

# Asegurarse de que pueda importar los módulos correctamente
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from models.solver import resolver_asignacion
from models.utils import (
    get_aulas, get_grupos, get_horarios,
    add_aula, add_grupo, add_horario,
    delete_aula, delete_grupo, delete_horario
)

# Configurar la página
st.set_page_config(page_title="MILP Asignación de Aulas", layout="centered")
st.title("Asignación óptima de aulas y horarios (MILP)")

# —————————————— Gestión de datos (siempre visible) ——————————————
with st.expander("Gestión de datos ✏️", expanded=False):
    tabs = st.tabs(["Aulas", "Materias", "Horarios"])

    # ─── Pestaña AULAS ───
    with tabs[0]:
        st.write("### Aulas actuales")
        df_aulas = pd.DataFrame(get_aulas())  # Cargar siempre datos frescos
        hdr = st.columns([1, 3, 2, 2, 1])
        hdr[0].markdown("**ID**"); hdr[1].markdown("**Nombre**")
        hdr[2].markdown("**Capacidad**"); hdr[3].markdown("**Piso**")
        hdr[4].markdown("**Acciones**")

        for _, r in df_aulas.iterrows():
            cols = st.columns([1, 3, 2, 2, 1])
            cols[0].write(r["id"]); cols[1].write(r["nombre"])
            cols[2].write(r["capacidad"]); cols[3].write(r["piso"])
            if cols[4].button("🗑️", key=f"del_aula_{r['id']}"):
                delete_aula(r["id"])
                st.success(f"Aula {r['nombre']} eliminada.")
            df_aulas = pd.DataFrame(get_aulas())

        st.markdown("---")
        st.write("### Agregar nueva Aula")
        with st.form("add_aula", clear_on_submit=True):
            na = st.text_input("Nombre aula")
            ca = st.number_input("Capacidad", min_value=1, value=30)
            pi = st.number_input("Piso", min_value=1, value=1)
            if st.form_submit_button("➕ Añadir Aula"):
                if na.strip():
                    add_aula(na.strip(), ca, pi)
                    st.success(f"Aula '{na}' agregada.")
                else:
                    st.error("El nombre no puede estar vacío.")

    # ─── Pestaña Materias ───
    with tabs[1]:
        st.write("### Materias actuales")
        df_grupos = pd.DataFrame(get_grupos())  # Carga fresca
        hdr = st.columns([1, 3, 3, 3, 1])
        hdr[0].markdown("**ID**"); hdr[1].markdown("**Nombre**")
        hdr[2].markdown("**Estudiantes**"); hdr[3].markdown("**Materia**")
        hdr[4].markdown("**Acciones**")

        for _, r in df_grupos.iterrows():
            cols = st.columns([1, 3, 3, 3, 1])
            cols[0].write(r["id"]); cols[1].write(r["nombre"])
            cols[2].write(r["estudiantes"]); cols[3].write(r["materia"])
            if cols[4].button("🗑️", key=f"del_grupo_{r['id']}"):
                delete_grupo(r["id"])
                st.success(f"Grupo {r['nombre']} eliminado.")

        st.markdown("---")
        st.write("### Agregar nueva Materia")
        with st.form("add_grupo", clear_on_submit=True):
            ng = st.text_input("Nombre grupo")
            es = st.number_input("Estudiantes", min_value=1, value=10)
            ma = st.text_input("Materia")
            if st.form_submit_button("➕ Añadir Grupo"):
                if ng.strip():
                    add_grupo(ng.strip(), es, ma)
                    st.success(f"Grupo '{ng}' agregado.")
                else:
                    st.error("El nombre no puede estar vacío.")

    # ─── Pestaña HORARIOS ───
    with tabs[2]:
        st.write("### Horarios actuales")
        df_horarios = pd.DataFrame(get_horarios())  # Carga fresca
        hdr = st.columns([1, 3, 3, 1])
        hdr[0].markdown("**ID**"); hdr[1].markdown("**Bloque**")
        hdr[2].markdown("**Hora**"); hdr[3].markdown("**Acciones**")

        for _, r in df_horarios.iterrows():
            cols = st.columns([1, 3, 3, 1])
            cols[0].write(r["id"]); cols[1].write(r["bloque"])
            cols[2].write(r["hora"])
            if cols[3].button("🗑️", key=f"del_horario_{r['id']}"):
                delete_horario(r["id"])
                st.success(f"Horario {r['bloque']} eliminado.")

        st.markdown("---")
        st.write("### Agregar nuevo Horario")
        with st.form("add_horario", clear_on_submit=True):
            bl = st.text_input("Bloque")
            hr = st.text_input("Rango hora")
            if st.form_submit_button("➕ Añadir Horario"):
                if bl.strip():
                    add_horario(bl.strip(), hr.strip())
                    st.success(f"Horario '{bl}' agregado.")
                else:
                    st.error("El bloque y la hora no pueden estar vacíos.")


st.markdown(
    """
    ## Parámetros de optimización

    **Umbral δ**  
    Representa el porcentaje de capacidad del aula que **puede quedar vacío** sin penalización.  
    - Un **δ bajo** (p. ej. 0 %) exige un ajuste muy preciso (pocas vacantes).  
    - Un **δ alto** (p. ej. 50 %) permite más espacio libre sin coste.

    **Penalización λ**  
    Es el **peso** que se resta de la función objetivo **por cada vacante** que supere el umbral δ.  
    - Un **λ bajo** (p. ej. 1) castiga suavemente el espacio desaprovechado.  
    - Un **λ alto** (p. ej. 50) fuerza al modelo a usar aulas lo más ajustadas posible.
    """
)


# --- Parámetros ---
col1, col2 = st.columns(2)
delta_pct   = col1.slider("Umbral δ de subutilización (%)", 0, 50, 20)
penalizacion = col2.number_input("Penalización λ (por vacante)", 0.0, 100.0, 10.0, 0.25,"%.2f")

delta = delta_pct / 100  # convertir a fracción

if st.button("Optimizar"):
    resultado = resolver_asignacion(delta, penalizacion)

    # Si no hay asignaciones válidas
    if not resultado:
        st.warning("No se obtuvo ninguna asignación válida con los parámetros dados.")
        st.stop()

    # Crear los diccionarios de grupos y horarios
    gr_d = {g["id"]: g["materia"] for g in get_grupos()}
    hr_d = {h["id"]: {"bloque": h["bloque"], "hora": h["hora"]} for h in get_horarios()}
    au_d = {a["id"]: {"nombre": a["nombre"], "piso": a["piso"]} for a in get_aulas()}

    # --- DataFrame final --- (con nombres de grupo y horario)
    asignaciones = []
    for res in resultado:
        aula_info = au_d[res["aula"]]
        asignaciones.append({
            "Materia": gr_d[res["grupo_id"]],   # Usamos el diccionario para acceder al nombre del grupo
            "Aula": aula_info["nombre"],  # Nombre del aula
            "Piso": aula_info["piso"],  # Piso del aula
            "Bloque": hr_d[res["horario_id"]]["bloque"],  # Usamos diccionario para el bloque
            "Horario": hr_d[res["horario_id"]]["hora"],  # Usamos diccionario para la hora
            "Vacantes": res["vacantes"]
        })

    df = pd.DataFrame(asignaciones)

    st.subheader("Asignaciones óptimas")
    st.dataframe(df, use_container_width=True)

    # --- Heatmap ---
    st.subheader("Mapa de ocupación (Materia vs Aula-Bloque)")

    df["Columna"] = df["Aula"].astype(str) + "-H" + df["Bloque"].astype(str)
    pivot = df.pivot(index="Materia", columns="Columna", values="Vacantes")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        pivot,
        annot=True,
        cmap="RdYlGn_r",  # verde -> lleno, rojo -> vacío
        ax=ax,
        cbar_kws={"label": "Vacantes"}
    )
    ax.set_xlabel("Aula-Horario")
    ax.set_ylabel("Materia")
    st.pyplot(fig)

    # --- Calcular porcentaje de utilización --- 
    total_capacidad = sum(df_aulas["capacidad"])
    total_vacantes = df["Vacantes"].sum()
    ocupacion = 100 * (total_capacidad - total_vacantes) / total_capacidad

    st.write(f"**Porcentaje de ocupación total:** {ocupacion:.2f}%")
    # Materia mejor y peor aprovechada
    mejor  = df.loc[df["Vacantes"].idxmin()]
    peor   = df.loc[df["Vacantes"].idxmax()]

    # Texto interpretativo
    interpretacion = (
        f"**Interpretación de resultados**\n\n"
        f"• El porcentaje de ocupación global fue de **{ocupacion:.2f}%**, "
        f"lo que indica un alto aprovechamiento del espacio.\n\n"
        f"• La materia **{mejor['Materia']}** se asignó sin vacantes ({mejor['Vacantes']} vacantes), "
        f"demostrando un ajuste perfecto.\n\n"
        f"• En contraste, la materia **{peor['Materia']}** quedó con **{peor['Vacantes']} vacantes**, "
        f"siendo el caso menos eficiente en esta corrida.\n\n"
    )

    st.markdown(interpretacion)

    # --- Guardar y ofrecer Excel ---
    excel_bytes = BytesIO()
    df.drop(columns="Columna").to_excel(excel_bytes, index=False)
    excel_bytes.seek(0)

    st.download_button(
        label="Descargar resultado en Excel",
        data=excel_bytes,
        file_name="resultado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
