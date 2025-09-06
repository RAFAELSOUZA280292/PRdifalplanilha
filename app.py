import streamlit as st

st.set_page_config(page_title="Simulador DIFAL - Uso e Consumo (Paraná)", layout="centered")
st.title("🧮 Simulador de ICMS DIFAL - Uso e Consumo (Paraná)")
st.markdown(
    "Informe o valor do produto em cada linha abaixo para simular o DIFAL de **Uso e Consumo / Ativo Imobilizado** no Paraná. "
    "Defina a **alíquota interna do PR** na lateral (presets de 7%, 12%, 19,5% ou opção para informar)."
)
st.markdown("> **Atenção**: Este cálculo usa a metodologia da 'Base de Cálculo Única' (EC 87/2015).")

# ==========================
# Barra lateral – Alíquota interna PR
# ==========================
st.sidebar.header("⚙️ Alíquota Interna – PR (Destino)")

preset = st.sidebar.selectbox(
    "Escolha a alíquota interna do PR",
    options=["7%", "12%", "19,5%", "Informar..."],
    index=2,  # 19,5% como padrão
    help="Selecione um dos presets ou informe um valor manualmente."
)

def parse_pct_string(s: str):
    """Converte string percentual com vírgula ou ponto em float; retorna None se inválido."""
    try:
        return float(s.strip().replace("%", "").replace(",", "."))
    except Exception:
        return None

if preset == "Informar...":
    # Campo texto (sem botões de incremento) para digitação livre
    pct_str = st.sidebar.text_input(
        "Digite a alíquota interna do PR (%)",
        placeholder="ex.: 19,5",
        help="Use vírgula ou ponto. Ex.: 19,5"
    )
    aliquota_interna_pr = parse_pct_string(pct_str) if pct_str else None

    if aliquota_interna_pr is None:
        st.sidebar.warning("Informe um percentual válido (ex.: 19,5).")
else:
    aliquota_interna_pr = parse_pct_string(preset)

if aliquota_interna_pr is not None:
    st.sidebar.caption(f"Alíquota interna atual: **{aliquota_interna_pr:.2f}%**")

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
    Calcula o DIFAL a recolher para PR (Uso e Consumo/Ativo Imobilizado) usando 'Base de Cálculo Única'.
    Retorna: base, icms_origem, difal, aliquota_efetiva_difal
    """
    if valor_produto <= 0:
        return 0.0, 0.0, 0.0, 0.0

    base = valor_produto
    icms_origem = base * (aliq_inter / 100.0)
    icms_destino = base * (aliq_interna_destino / 100.0)
    difal = max(icms_destino - icms_origem, 0.0)  # evita negativo em casos atípicos
    efetiva = (difal / base) * 100.0 if base else 0.0
    return base, icms_origem, difal, efetiva

def format_brl(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_pct(v: float) -> str:
    return f"{v:.2f}%"

btn = st.button("🧾 Calcular DIFAL para PR (Uso e Consumo)")

if btn:
    if aliquota_interna_pr is None:
        st.error("Defina uma **alíquota interna do PR** válida antes de calcular.")
    else:
        total_difal = 0.0
        simulacoes = [
            (valor_4, 4.0, "Linha 1 - ICMS Interestadual 4%"),
            (valor_7, 7.0, "Linha 2 - ICMS Interestadual 7%"),
            (valor_12, 12.0, "Linha 3 - ICMS Interestadual 12%"),
        ]

        for valor_input, aliq_inter, label in simulacoes:
            base, icms_origem, difal, efetiva = calcular_difal_uso_consumo(
                valor_input, aliq_inter, aliquota_interna_pr
            )

            st.markdown(f"### 🔍 {label}")
            if valor_input <= 0:
                st.warning("Nenhum valor informado para esta linha.")
            else:
                st.write(f"**▶ Valor do Produto (Base Única):** {format_brl(base)}")
                st.write(f"**▶ ICMS de Origem ({aliq_inter}%):** {format_brl(icms_origem)}")
                st.write(f"**▶ ICMS Interno PR ({aliquota_interna_pr:.2f}%):** {format_brl(base * (aliquota_interna_pr / 100.0))}")
                st.write(f"**▶ DIFAL a Recolher para o PR:** {format_brl(difal)}")
                st.write(f"**▶ Alíquota Efetiva do DIFAL:** {format_pct(efetiva)}")
                st.markdown("---")
                total_difal += difal

        if total_difal > 0:
            st.markdown("---")
            st.subheader("📊 Resumo Total")
            st.metric("Valor Total do DIFAL a Recolher para o PR", format_brl(total_difal))
        else:
            st.info("Nenhum valor de produto foi inserido para calcular o DIFAL total.")
