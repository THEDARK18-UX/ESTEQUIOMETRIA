# app.py
import streamlit as st
from sympy import symbols, Eq, solve
import re

st.set_page_config(page_title="⚗️ QuimicAula PRO", layout="centered")
st.title("⚗️ QuimicAula PRO - Resolución Estequiométrica Total")

# Tabla periódica simple (puedes expandirla)
masas_molares = {
    "H": 1.008, "O": 16.00, "C": 12.01, "N": 14.01,
    "Cl": 35.45, "Na": 22.99, "K": 39.10, "Mg": 24.31,
    "Ca": 40.08, "S": 32.07, "Fe": 55.85, "Zn": 65.38
}

def parse_formula(formula):
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    parsed = {}
    for (element, count) in elements:
        count = int(count) if count else 1
        parsed[element] = parsed.get(element, 0) + count
    return parsed

def balancear_ecuacion(reactivos, productos):
    elementos = sorted(set(e for f in reactivos + productos for e in parse_formula(f)))
    n = len(reactivos) + len(productos)
    variables = symbols(f'x1:{n+1}')
    ecuaciones = []
    for el in elementos:
        lhs = sum(parse_formula(f).get(el, 0) * variables[i] for i, f in enumerate(reactivos))
        rhs = sum(parse_formula(f).get(el, 0) * variables[i+len(reactivos)] for i, f in enumerate(productos))
        ecuaciones.append(Eq(lhs, rhs))
    ecuaciones.append(Eq(variables[0], 1))
    solucion = solve(ecuaciones, variables, dict=True)[0]
    return [solucion.get(v, 1) for v in variables]

def calcular_masa_molar(formula):
    parsed = parse_formula(formula)
    return sum(masas_molares[el] * cant for el, cant in parsed.items())

# --- Interfaz ---
st.markdown("### Paso 1: Ingrese Reactivos y Productos")

col1, col2 = st.columns(2)
with col1:
    reactivos = st.text_input("Reactivos (separados por comas)", "H2, O2").replace(" ", "").split(",")
with col2:
    productos = st.text_input("Productos (separados por comas)", "H2O").replace(" ", "").split(",")

if st.button("🔬 Balancear ecuación"):
    try:
        coef = balancear_ecuacion(reactivos, productos)
        n_reac = len(reactivos)
        coefs_reac = coef[:n_reac]
        coefs_prod = coef[n_reac:]

        ecuacion = " + ".join(f"{int(c)} {r}" for c, r in zip(coefs_reac, reactivos))
        ecuacion += " → "
        ecuacion += " + ".join(f"{int(c)} {p}" for c, p in zip(coefs_prod, productos))

        st.success(f"✅ Ecuación balanceada:\n\n{ecuacion}")

        st.markdown("### Paso 2: Cálculo Estequiométrico")

        sustancias = reactivos + productos
        col3, col4 = st.columns(2)
        with col3:
            sustancia_dada = st.selectbox("Sustancia conocida (tienes en gramos):", sustancias)
        with col4:
            gramos_dados = st.number_input("Cantidad disponible (en gramos):", min_value=0.0, format="%.2f")

        sustancia_objetivo = st.selectbox("Sustancia a calcular (en gramos):", [s for s in sustancias if s != sustancia_dada])

        if st.button("📈 Calcular"):
            idx_dada = sustancias.index(sustancia_dada)
            idx_objetivo = sustancias.index(sustancia_objetivo)

            masa_dada = calcular_masa_molar(sustancia_dada)
            masa_obj = calcular_masa_molar(sustancia_objetivo)

            moles_dada = gramos_
