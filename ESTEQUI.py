import streamlit as st
from sympy import symbols, Eq, solve
import re

st.set_page_config(page_title="⚗️ QuimicAula PRO", layout="centered")
st.title("⚗️ QuimicAula PRO - Cálculo Estequiométrico")

# Tabla periódica (puedes ampliar según necesidad)
masas_molares = {
    "H": 1.008, "O": 16.00, "C": 12.01, "N": 14.01,
    "Cl": 35.45, "Na": 22.99, "K": 39.10, "Mg": 24.31,
    "Ca": 40.08, "S": 32.07, "Fe": 55.85, "Zn": 65.38
}

def parse_formula(formula):
    elementos = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    resultado = {}
    for elemento, cantidad in elementos:
        cantidad = int(cantidad) if cantidad else 1
        resultado[elemento] = resultado.get(elemento, 0) + cantidad
    return resultado

def balancear_ecuacion(reactivos, productos):
    todos = reactivos + productos
    elementos = sorted(set(e for f in todos for e in parse_formula(f)))
    n = len(todos)
    x = symbols(f'x1:{n+1}')
    ecuaciones = []

    for el in elementos:
        izq = sum(parse_formula(f).get(el, 0) * x[i] for i, f in enumerate(reactivos))
        der = sum(parse_formula(f).get(el, 0) * x[i+len(reactivos)] for i, f in enumerate(productos))
        ecuaciones.append(Eq(izq, der))

    ecuaciones.append(Eq(x[0], 1))  # Normalizar
    solucion = solve(ecuaciones, x, dict=True)[0]
    return [solucion.get(var, 1) for var in x]

def calcular_masa_molar(formula):
    elementos = parse_formula(formula)
    return sum(masas_molares.get(el, 0) * cant for el, cant in elementos.items())

# INTERFAZ STREAMLIT
st.markdown("### Paso 1: Ingrese Reactivos y Productos")

col1, col2 = st.columns(2)
with col1:
    reactivos = st.text_input("Reactivos (ej: H2, O2)", "H2, O2").replace(" ", "").split(",")
with col2:
    productos = st.text_input("Productos (ej: H2O)", "H2O").replace(" ", "").split(",")

if st.button("⚖️ Balancear ecuación"):
    try:
        coef = balancear_ecuacion(reactivos, productos)
        n_reac = len(reactivos)
        coef_reactivos = coef[:n_reac]
        coef_productos = coef[n_reac:]

        ecuacion = " + ".join(f"{int(c)} {r}" for c, r in zip(coef_reactivos, reactivos))
        ecuacion += " → "
        ecuacion += " + ".join(f"{int(c)} {p}" for c, p in zip(coef_productos, productos))

        st.success(f"✅ Ecuación balanceada:\n\n{ecuacion}")

        st.markdown("### Paso 2: Cálculo Estequiométrico")
        sustancias = reactivos + productos
        col3, col4 = st.columns(2)
        with col3:
            sust_dada = st.selectbox("Sustancia conocida (en gramos):", sustancias)
        with col4:
            gramos_dados = st.number_input("Cantidad (g):", min_value=0.0, format="%.2f")

        sust_obj = st.selectbox("Sustancia a calcular (en gramos):", [s for s in sustancias if s != sust_dada])

        if st.button("📈 Calcular Gramos"):
            idx_dada = sustancias.index(sust_dada)
            idx_obj = sustancias.index(sust_obj)
            masa_dada = calcular_masa_molar(sust_dada)
            masa_obj = calcular_masa_molar(sust_obj)
            moles_dada = gramos_dados / masa_dada
            proporcion = coef[idx_obj] / coef[idx_dada]
            moles_obj = moles_dada * proporcion
            gramos_obj = moles_obj * masa_obj

            st.markdown(f"""
            ### 📊 Resultado:
            - Moles de {sust_dada}: {moles_dada:.4f} mol  
            - Masa molar de {sust_obj}: {masa_obj:.2f} g/mol  
            - Gramos producidos de **{sust_obj}**: **{gramos_obj:.2f} g**
            """)
    except Exception as e:
        st.error(f"❌ Error al procesar: {e}")
