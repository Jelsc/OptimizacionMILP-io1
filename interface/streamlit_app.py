import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import sys, pathlib

# Asegurarse de que pueda importar los módulos correctamente
sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent))

from models.solver import resolver_asignacion
from models.utils import get_grupos, get_horarios

# Configurar la página
st.set_page_config(page_title="MILP Asignación de Aulas", layout="centered")
st.title("Asignación óptima de aulas y horarios (MILP)")

# --- Parámetros ---
col1, col2 = st.columns(2)
delta_pct   = col1.slider("Umbral δ de subutilización (%)", 0, 50, 20)
penalizacion = col2.number_input("Penalización λ (por vacante)", 1, 100, 10)

delta = delta_pct / 100  # convertir a fracción

if st.button("Optimizar"):
    resultado = resolver_asignacion(delta, penalizacion)

    # Si no hay asignaciones válidas
    if not resultado:
        st.warning("No se obtuvo ninguna asignación válida con los parámetros dados.")
        st.stop()

    # Crear los diccionarios de grupos y horarios
    gr_d = {g["id"]: g["nombre"] for g in get_grupos()}
    hr_d = {h["id"]: {"bloque": h["bloque"], "hora": h["hora"]} for h in get_horarios()}

    # --- Leyendas de Grupos y Bloques ---
    with st.expander("Leyenda de Grupos"):
        grupos_info = [{"ID": g["id"], "Nombre": g["nombre"], "Materia": g["materia"]} for g in get_grupos()]
        st.table(pd.DataFrame(grupos_info).set_index("ID"))

    # --- DataFrame final --- (con nombres de grupo y horario)
    asignaciones = []
    for res in resultado:
        asignaciones.append({
            "Grupo": gr_d[res["grupo_id"]],   # Usamos el diccionario para acceder al nombre del grupo
            "Aula": res["aula"],
            "Bloque": hr_d[res["horario_id"]]["bloque"],  # Usamos diccionario para el bloque
            "Horario": hr_d[res["horario_id"]]["hora"],  # Usamos diccionario para la hora
            "Vacantes": res["vacantes"]
        })

    df = pd.DataFrame(asignaciones)

    st.subheader("Asignaciones óptimas")
    st.dataframe(df, use_container_width=True)

    # --- Heatmap ---
    st.subheader("Mapa de ocupación (Grupo vs Aula-Bloque)")

    df["Columna"] = df["Aula"].astype(str) + "-H" + df["Bloque"].astype(str)
    pivot = df.pivot(index="Grupo", columns="Columna", values="Vacantes")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(
        pivot,
        annot=True,
        cmap="RdYlGn_r",  # verde -> lleno, rojo -> vacío
        ax=ax,
        cbar_kws={"label": "Vacantes"}
    )
    ax.set_xlabel("Aula-Horario")
    ax.set_ylabel("Grupo")
    st.pyplot(fig)

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
