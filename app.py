import streamlit as st

st.set_page_config(page_title="Simulador DIFAL - Comparativo Detalhado (PR)", layout="centered")
st.title("🧮 Simulador de ICMS DIFAL - Comparativo Detalhado (Paraná)")
st.markdown("Informe o valor do produto em cada linha abaixo para simular o DIFAL, conforme a alíquota interestadual. A alíquota interna do PR é considerada fixa em **19,5%**.")

# Alíquota interna do PR
aliquota_interna_pr = 19.5

# Entrada dos valores dos produtos
# As chaves 'valor_4_pr', 'valor_7_pr', 'valor_12_pr' garantem que os campos são únicos se você tiver outros simuladores
valor_4 = st.number_input("🔹 Linha 1 - Valor do Produto (ICMS Interestadual 4%)", min_value=0.0, format="%.2f", key="valor_4_pr")
valor_7 = st.number_input("🔹 Linha 2 - Valor do Produto (ICMS Interestadual 7%)", min_value=0.0, format="%.2f", key="valor_7_pr")
valor_12 = st.number_input("🔹 Linha 3 - Valor do Produto (ICMS Interestadual 12%)", min_value=0.0, format="%.2f", key="valor_12_pr")

def calcular_difal(valor, aliq_inter):
    """
    Calcula o DIFAL a recolher para o estado do Paraná.

    Args:
        valor (float): O valor do produto.
        aliq_inter (float): A alíquota interestadual.

    Returns:
        tuple: (base_calculo, icms_origem, difal, efetiva)
    """
    if valor <= 0:
        return 0.0, 0.0, 0.0, 0.0
    
    # Cálculo da Base de Cálculo por Dentro (considerando a alíquota interna do PR)
    # Valor da operação / (1 - (alíquota interna / 100))
    base_calculo = valor / (1 - (aliquota_interna_pr / 100))
    
    # ICMS devido ao estado de destino (PR)
    icms_destino_pr = base_calculo * (aliquota_interna_pr / 100)
    
    # ICMS já pago no estado de origem (calculado "por fora" do valor do produto)
    icms_origem = valor * (aliq_inter / 100)
    
    # Diferencial de Alíquotas (DIFAL)
    difal = icms_destino_pr - icms_origem
    
    # Alíquota Efetiva do DIFAL sobre o valor do produto
    efetiva = (difal / valor) * 100
    
    return base_calculo, icms_origem, difal, efetiva

def format_brl(v):
    """Formata um valor numérico como moeda brasileira."""
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_pct(v):
    """Formata um valor numérico como porcentagem."""
    return f"{v:.2f}%"

if st.button("🧾 Calcular DIFAL para PR"):
    # Lista de cenários a serem simulados (valor do produto, alíquota interestadual, rótulo)
    simulacoes = [
        (valor_4, 4.0, "Linha 1 - ICMS Interestadual 4%"),
        (valor_7, 7.0, "Linha 2 - ICMS Interestadual 7%"),
        (valor_12, 12.0, "Linha 3 - ICMS Interestadual 12%"),
    ]

    for valor_input, aliq_inter_cenario, label_cenario in simulacoes:
        base, icms_origem, difal, efetiva = calcular_difal(valor_input, aliq_inter_cenario)

        st.markdown(f"### 🔍 {label_cenario}")
        if valor_input <= 0:
            st.warning("Nenhum valor informado para esta linha.")
        else:
            st.write(f"**▶ Valor do Produto:** {format_brl(valor_input)}")
            st.write(f"**▶ Base de Cálculo por Dentro (ICMS Interno PR {aliquota_interna_pr}%):** {format_brl(base)}")
            st.write(f"**▶ ICMS de Origem ({aliq_inter_cenario}%):** {format_brl(icms_origem)}")
            st.write(f"**▶ DIFAL a Recolher para o PR:** {format_brl(difal)}")
            st.write(f"**▶ Alíquota Efetiva do DIFAL:** {format_pct(efetiva)}")
            st.markdown("---")
