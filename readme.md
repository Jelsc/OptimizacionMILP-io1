# Optimización de Asignación de Aulas y Horarios (MILP)

Este proyecto utiliza **Programación Lineal Entera Mixta (MILP)** para asignar grupos de estudiantes a aulas y horarios en una universidad, maximizando el aprovechamiento del espacio y penalizando la subutilización significativa.

## Requisitos
- Python 3.10+
- Librerías: ver `requirements.txt`

## Estructura
- base/: contiene la base SQLite
- modelo/: lógica de optimización
- interfaz/: app web opcional con Streamlit


## Pasos para ejecutar el proyecto

## 1. Clonar el proyecto de github
git clone (link)

## 2. da permisos para usar el entorno virtual (opcional)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

## 3. Crear un entorno virtual (opcional)
python -m venv venv

## 4. Activar el entorno virtual (opcional)
venv\Scripts\activate

## 5. Instalar dependencias
pip install -r requirements.txt

## 6. Crear la base de datos
python crear_base.py

## 7. Ejecuta la aplicacion (te pedira un correo, coloca cualquiera)
streamlit run interface/streamlit_app.py


## Cómo ejecutar
1. Activá el entorno virtual
2. Ejecutá `main.py` o `streamlit run interfaz/streamlit_app.py`


