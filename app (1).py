import streamlit as st

st.set_page_config(page_title="Simulador DIFAL - Comparativo Detalhado", layout="centered")
st.title("🧮 Simulador de ICMS DIFAL - Comparativo Detalhado")
st.markdown("Informe o valor do produto em cada linha abaixo para simular o DIFAL, conforme a alíquota interestadual. A alíquota interna do MT é considerada fixa em **17%**.")

# Alíquota interna de MT
aliquota_interna = 17.0

# Entrada dos valores dos produtos
valor_4 = st.number_input("🔹 Linha 1 - Valor do Produto (ICMS Interestadual 4%)", min_value=0.0, format="%.2f", key="valor_4")
valor_7 = st.number_input("🔹 Linha 2 - Valor do Produto (ICMS Interestadual 7%)", min_value=0.0, format="%.2f", key="valor_7")
valor_12 = st.number_input("🔹 Linha 3 - Valor do Produto (ICMS Interestadual 12%)", min_value=0.0, format="%.2f", key="valor_12")

def calcular_difal(valor, aliq_inter):
    if valor <= 0:
        return 0.0, 0.0, 0.0, 0.0
    base_calculo = valor / (1 - (aliquota_interna / 100))  # por dentro
    icms_mt = base_calculo * (aliquota_interna / 100)
    icms_origem = valor * (aliq_inter / 100)  # por fora
    difal = icms_mt - icms_origem
    efetiva = (difal / valor) * 100
    return base_calculo, icms_origem, difal, efetiva

def format_brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_pct(v):
    return f"{v:.2f}%"

if st.button("🧾 Calcular DIFAL"):
    for valor, aliq_inter, label in [
        (valor_4, 4.0, "Linha 1 - ICMS 4%"),
        (valor_7, 7.0, "Linha 2 - ICMS 7%"),
        (valor_12, 12.0, "Linha 3 - ICMS 12%"),
    ]:
        base, icms_origem, difal, efetiva = calcular_difal(valor, aliq_inter)

        st.markdown(f"### 🔍 {label}")
        if valor <= 0:
            st.warning("Nenhum valor informado para esta linha.")
        else:
            st.write(f"**▶ Valor do Produto:** {format_brl(valor)}")
            st.write(f"**▶ Base de Cálculo por Dentro (ICMS 17%):** {format_brl(base)}")
            st.write(f"**▶ ICMS de Origem ({aliq_inter}%):** {format_brl(icms_origem)}")
            st.write(f"**▶ DIFAL a Recolher para o MT:** {format_brl(difal)}")
            st.write(f"**▶ Alíquota Efetiva do DIFAL:** {format_pct(efetiva)}")
            st.markdown("---")
