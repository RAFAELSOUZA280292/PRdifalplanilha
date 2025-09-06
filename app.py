import streamlit as st

st.set_page_config(page_title="Simulador DIFAL - Uso e Consumo (Paraná)", layout="centered")
st.title("🧮 Simulador de ICMS DIFAL - Uso e Consumo (Paraná)")
st.markdown(
    "Informe o valor do produto em cada linha abaixo para simular o DIFAL de **Uso e Consumo / Ativo Imobilizado** no Paraná, "
    "conforme a alíquota interestadual. A alíquota interna do PR pode ser ajustada na lateral."
)
st.markdown("> **Atenção**: Este cálculo utiliza a metodologia da 'Base de Cálculo Única', conforme EC 87/2015, comum para operações a consumidor final não contribuinte ou uso/consumo/ativo imobilizado para contribuintes.")

# ==========================
# Configurações na barra lateral
# ==========================
st.sidebar.header("⚙️ Configurações – PR (Destino)")
preset = st.sidebar.selectbox(
    "Alíquota interna do PR (%)",
    options=["19,5 (padrão)", "19,0", "18,0", "Outro valor..."],
    index=0,
    help="Selecione um preset ou informe um valor personalizado."
)

if preset == "Outro valor...":
    aliquota_interna_pr = st.sidebar.number_input(
        "Informe a alíquota interna do PR (%)",
        min_value=0.0, max_value=35.0, value=19.5, step=0.1, format="%.2f",
        help="Percentual da alíquota interna aplicável no PR."
    )
else:
    # Converte string com vírgula para float
    aliquota_interna_pr = float(preset.replace("(padrão)", "").strip().replace(",", ".").replace("%", ""))

st.sidebar.caption(f"Alíquota interna atual usada no cálculo: **{aliquota_interna_pr:.2f}%**")

# ==========================
# Entradas dos valores dos produtos
# ==========================
valor_4 = st.number_input(
    "🔹 Linha 1 - Valor do Produto (ICMS Interestadual 4%)",
    min_value=0.0, format="%.2f", key="valor_4_pr_uc", step=0.01
)
valor_7 = st.number_input(
    "🔹 Linha 2 - Valor do Produto (ICMS Interestadual 7%)",
    min_value=0.0, format="%.2f", key="valor_7_pr_uc", step=0.01
)
valor_12 = st.number_input(
    "🔹 Linha 3 - Valor do Produto (ICMS Interestadual 12%)",
    min_value=0.0, format="%.2f", key="valor_12_pr_uc", step=0.01
)

def calcular_difal_uso_consumo(valor_produto, aliq_inter, aliq_interna_destino):
    """
    Calcula o DIFAL a recolher para o estado do Paraná para Uso e Consumo/Ativo Imobilizado
    utilizando a metodologia da 'Base de Cálculo Única'.

    Args:
        valor_produto (float): O valor do produto (Base de Cálculo única).
        aliq_inter (float): A alíquota interestadual (%).
        aliq_interna_destino (float): A alíquota interna do estado de destino (PR) (%).

    Returns:
        tuple: (base_calculo_unica, icms_origem, difal, aliquota_efetiva_difal)
    """
    if valor_produto <= 0:
        return 0.0, 0.0, 0.0, 0.0

    base_calculo_unica = valor_produto
    icms_origem = base_calculo_unica * (aliq_inter / 100.0)
    icms_destino_calculado = base_calculo_unica * (aliq_interna_destino / 100.0)
    difal = max(icms_destino_calculado - icms_origem, 0.0)  # evita negativo em casos atípicos
    efetiva = (difal / valor_produto) * 100.0 if valor_produto else 0.0

    return base_calculo_unica, icms_origem, difal, efetiva

def format_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_pct(v: float) -> str:
    return f"{v:.2f}%"

if st.button("🧾 Calcular DIFAL para PR (Uso e Consumo)"):
    total_difal_recolher = 0.0

    simulacoes = [
        (valor_4, 4.0, "Linha 1 - ICMS Interestadual 4%"),
        (valor_7, 7.0, "Linha 2 - ICMS Interestadual 7%"),
        (valor_12, 12.0, "Linha 3 - ICMS Interestadual 12%"),
    ]

    for valor_input, aliq_inter_cenario, label_cenario in simulacoes:
        base, icms_origem, difal, efetiva = calcular_difal_uso_consumo(
            valor_input, aliq_inter_cenario, aliquota_interna_pr
        )

        st.markdown(f"### 🔍 {label_cenario}")
        if valor_input <= 0:
            st.warning("Nenhum valor informado para esta linha.")
        else:
            st.write(f"**▶ Valor do Produto (Base Única):** {format_brl(base)}")
            st.write(f"**▶ ICMS de Origem ({aliq_inter_cenario}%):** {format_brl(icms_origem)}")
            st.write(f"**▶ ICMS Interno PR ({aliquota_interna_pr:.2f}%):** {format_brl(base * (aliquota_interna_pr / 100.0))}")
            st.write(f"**▶ DIFAL a Recolher para o PR:** {format_brl(difal)}")
            st.write(f"**▶ Alíquota Efetiva do DIFAL:** {format_pct(efetiva)}")
            st.markdown("---")
            total_difal_recolher += difal

    if total_difal_recolher > 0:
        st.markdown("---")
        st.subheader("📊 Resumo Total")
        st.metric(
            label="Valor Total do DIFAL a Recolher para o PR",
            value=format_brl(total_difal_recolher)
        )
    else:
        st.info("Nenhum valor de produto foi inserido para calcular o DIFAL total.")
