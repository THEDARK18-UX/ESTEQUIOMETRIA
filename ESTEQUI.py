import streamlit as st
import random

st.set_page_config(page_title="QuimicAula - Estequiometría", layout="centered")

# Diccionario de reacciones químicas base
reacciones = [
    {
        "ecuacion": "2 H₂ + O₂ → 2 H₂O",
        "reactivo": "H₂",
        "producto": "H₂O",
        "relacion": (2, 2),
        "masa_molar_reactivo": 2.0,
        "masa_molar_producto": 18.0
    },
    {
        "ecuacion": "N₂ + 3 H₂ → 2 NH₃",
        "reactivo": "H₂",
        "producto": "NH₃",
        "relacion": (3, 2),
        "masa_molar_reactivo": 2.0,
        "masa_molar_producto": 17.0
    },
    {
        "ecuacion": "CH₄ + 2 O₂ → CO₂ + 2 H₂O",
        "reactivo": "CH₄",
        "producto": "CO₂",
        "relacion": (1, 1),
        "masa_molar_reactivo": 16.0,
        "masa_molar_producto": 44.0
    }
]

st.title("🧪 QuimicAula: Aprende Estequiometría Jugando")
st.write("Selecciona una función para comenzar:")

# Botones principales
col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 Generador de ejercicios aleatorios"):
        reaccion = random.choice(reacciones)
        masa_dada = random.randint(5, 50)

        moles_reactivo = masa_dada / reaccion["masa_molar_reactivo"]
        moles_producto = moles_reactivo * reaccion["relacion"][1] / reaccion["relacion"][0]
        masa_producto = moles_producto * reaccion["masa_molar_producto"]

        st.subheader("🔍 Ejercicio Aleatorio")
        st.markdown(f"""
        Dada la siguiente reacción balanceada:

        **{reaccion['ecuacion']}**

        Si se hacen reaccionar **{masa_dada} g** de **{reaccion['reactivo']}**,  
        ¿cuántos gramos de **{reaccion['producto']}** se obtendrán?
        """)

        st.info("Trata de resolverlo por tu cuenta antes de pedir la solución.")

        if st.button("Mostrar solución"):
            st.success(f"Respuesta: Se obtendrán aproximadamente **{masa_producto:.2f} g** de {reaccion['producto']}.")

with col2:
    st.subheader("📥 Resolver mi propio ejercicio")
    st.write("Completa los datos para que el sistema calcule la masa del producto.")

    ecuacion = st.selectbox("Selecciona una ecuación:", [r["ecuacion"] for r in reacciones])
    seleccionada = next(r for r in reacciones if r["ecuacion"] == ecuacion)

    masa_ingresada = st.number_input(f"Ingrese la masa en gramos de {seleccionada['reactivo']}:", min_value=0.0)

    if st.button("Calcular producto obtenido"):
        moles_reactivo = masa_ingresada / seleccionada["masa_molar_reactivo"]
        moles_producto = moles_reactivo * seleccionada["relacion"][1] / seleccionada["relacion"][0]
        masa_producto = moles_producto * seleccionada["masa_molar_producto"]

        st.success(f"Con {masa_ingresada} g de {seleccionada['reactivo']}, se obtendrán aproximadamente {masa_producto:.2f} g de {seleccionada['producto']}.")
