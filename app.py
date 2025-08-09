import streamlit as st

st.set_page_config(page_title="Simulador DIFAL - Uso e Consumo (Paraná)", layout="centered")
st.title("🧮 Simulador de ICMS DIFAL - Uso e Consumo (Paraná)")
st.markdown("Informe o valor do produto em cada linha abaixo para simular o DIFAL de **Uso e Consumo / Ativo Imobilizado** no Paraná, conforme a alíquota interestadual. A alíquota interna do PR é considerada fixa em **19,5%**.")
st.markdown("> **Atenção**: Este cálculo utiliza a metodologia da 'Base de Cálculo Única', conforme EC 87/2015, comum para operações a consumidor final não contribuinte ou uso/consumo/ativo imobilizado para contribuintes.")

# Alíquota interna do PR
aliquota_interna_pr = 19.5

# Entrada dos valores dos produtos
valor_4 = st.number_input("🔹 Linha 1 - Valor do Produto (ICMS Interestadual 4%)", min_value=0.0, format="%.2f", key="valor_4_pr_uc")
valor_7 = st.number_input("�� Linha 2 - Valor do Produto (ICMS Interestadual 7%)", min_value=0.0, format="%.2f", key="valor_7_pr_uc")
valor_12 = st.number_input("🔹 Linha 3 - Valor do Produto (ICMS Interestadual 12%)", min_value=0.0, format="%.2f", key="valor_12_pr_uc")

def calcular_difal_uso_consumo(valor_produto, aliq_inter, aliq_interna_destino):
    """
    Calcula o DIFAL a recolher para o estado do Paraná para Uso e Consumo/Ativo Imobilizado
    utilizando a metodologia da "Base de Cálculo Única".

    Args:
        valor_produto (float): O valor do produto (Base de Cálculo única).
        aliq_inter (float): A alíquota interestadual.
        aliq_interna_destino (float): A alíquota interna do estado de destino (PR).

    Returns:
        tuple: (base_calculo_unica, icms_origem, difal, aliquota_efetiva_difal)
    """
    if valor_produto <= 0:
        return 0.0, 0.0, 0.0, 0.0
    
    # Base de cálculo única é o próprio valor do produto
    base_calculo_unica = valor_produto
    
    # ICMS já pago no estado de origem (calculado sobre a base única)
    icms_origem = base_calculo_unica * (aliq_inter / 100)
    
    # ICMS que seria devido internamente no destino (PR), calculado sobre a base única
    icms_destino_calculado = base_calculo_unica * (aliq_interna_destino / 100)
    
    # Diferencial de Alíquotas (DIFAL)
    difal = icms_destino_calculado - icms_origem
    
    # Alíquota Efetiva do DIFAL sobre o valor do produto
    # É importante notar que a "alíquota efetiva" aqui é apenas o DIFAL em % sobre o valor do produto.
    efetiva = (difal / valor_produto) * 100
    
    return base_calculo_unica, icms_origem, difal, efetiva

def format_brl(v):
    """Formata um valor numérico como moeda brasileira."""
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_pct(v):
    """Formata um valor numérico como porcentagem."""
    return f"{v:.2f}%"

if st.button("🧾 Calcular DIFAL para PR (Uso e Consumo)"):
    # Lista de cenários a serem simulados (valor do produto, alíquota interestadual, rótulo)
    simulacoes = [
        (valor_4, 4.0, "Linha 1 - ICMS Interestadual 4%"),
        (valor_7, 7.0, "Linha 2 - ICMS Interestadual 7%"),
        (valor_12, 12.0, "Linha 3 - ICMS Interestadual 12%"),
    ]

    for valor_input, aliq_inter_cenario, label_cenario in simulacoes:
        base, icms_origem, difal, efetiva = calcular_difal_uso_consumo(valor_input, aliq_inter_cenario, aliquota_interna_pr)

        st.markdown(f"### 🔍 {label_cenario}")
        if valor_input <= 0:
            st.warning("Nenhum valor informado para esta linha.")
        else:
            st.write(f"**▶ Valor do Produto (Base Única):** {format_brl(base)}")
            st.write(f"**▶ ICMS de Origem ({aliq_inter_cenario}%):** {format_brl(icms_origem)}")
            st.write(f"**▶ ICMS Interno PR ({aliquota_interna_pr}%):** {format_brl(base * (aliquota_interna_pr / 100))}") # Explicitar o ICMS interno PR
            st.write(f"**▶ DIFAL a Recolher para o PR:** {format_brl(difal)}")
            st.write(f"**▶ Alíquota Efetiva do DIFAL:** {format_pct(efetiva)}")
            st.markdown("---")
