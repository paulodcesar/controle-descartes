iimport streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import date

# Configuração inicial da página
st.set_page_config(
    page_title="Gestão de Descarte - PREMO",
    page_icon="🏗️",
    layout="centered"
)

# Nome do arquivo CSV onde os dados são salvos
NOME_ARQUIVO = "descartes.csv"

# Função para carregar os dados
def carregar_dados():
    if os.path.exists(NOME_ARQUIVO):
        return pd.read_csv(NOME_ARQUIVO)
    else:
        return pd.DataFrame(columns=["Data", "Produto", "Quantidade", "Motivo", "Observacoes"])

# Função para salvar novo registro
def salvar_registro(data, produto, quantidade, motivo, observacoes):
    df_existente = carregar_dados()
    novo_dado = pd.DataFrame([{
        "Data": data,
        "Produto": produto,
        "Quantidade": quantidade,
        "Motivo": motivo,
        "Observacoes": observacoes
    }])
    df_atualizado = pd.concat([df_existente, novo_dado], ignore_index=True)
    df_atualizado.to_csv(NOME_ARQUIVO, index=False)

# Exibição da Logo Oficial no Topo (Com largura fixa para não esticar)
if os.path.exists("logo.png"):
    st.image("logo.png", width=280)
else:
    st.title("🏗️ PREMO - Soluções Construtivas")

st.markdown("### **Sistema de Gestão de Descarte**")
st.caption("Controle Interno e Indicadores de Perdas")
st.divider()

# Menu lateral para navegação
opcao_menu = st.sidebar.radio(
    "Navegação",
    ["Registrar Descarte", "Visualizar Gráficos e Dados"]
)

if opcao_menu == "Registrar Descarte":
    st.subheader("📋 Novo Registro de Descarte")
    
    with st.form("form_descarte", clear_on_submit=True):
        data_ocorrido = st.date_input("Data do Ocorrido", value=date.today())
        
        produto = st.selectbox(
            "Produto Descartado",
            [
                "Bloco de Concreto",
                "Canaleta / Bloco J",
                "Piso Intertravado / Paver",
                "Tubo de Concreto",
                "Laje / Vigota",
                "Elemento Vazado / Cobogó",
                "Outro"
            ]
        )
        
        quantidade = st.number_input("Quantidade (unidades)", min_value=1, step=1, value=1)
        
        motivo = st.selectbox(
            "Motivo do Descarte",
            [
                "Trinca / Quebra no Manuseio",
                "Cura Inadequada / Falha de Resistência",
                "Defeito de Moldagem / Geometria",
                "Avariado no Transporte",
                "Outro"
            ]
        )
        
        observacoes = st.text_area("Observações Adicionais (ex: lote, máquina, etc.)")
        
        btn_salvar = st.form_submit_button("Salvar Registro")
        
        if btn_salvar:
            salvar_registro(data_ocorrido, produto, quantidade, motivo, observacoes)
            st.success("✅ Descarte registrado com sucesso!")

elif opcao_menu == "Visualizar Gráficos e Dados":
    st.subheader("📊 Indicadores e Perdas")
    
    df = carregar_dados()
    
    if df.empty:
        st.info("Nenhum registro encontrado até o momento.")
    else:
        # Métricas resumidas
        total_ocorrencias = len(df)
        total_pecas = df["Quantidade"].sum()
        
        col1, col2 = st.columns(2)
        col1.metric("Total de Ocorrências", total_ocorrencias)
        col2.metric("Total de Peças Descartadas", total_pecas)
        
        st.divider()
        
        # Gráfico 1: Peças descartadas por Produto
        df_produto = df.groupby("Produto")["Quantidade"].sum().reset_index()
        fig_produto = px.bar(
            df_produto,
            x="Produto",
            y="Quantidade",
            title="Total de Peças por Produto",
            color_discrete_sequence=["#F3B11A"],
            text_auto=True
        )
        fig_produto.update_layout(xaxis_title="Produto", yaxis_title="Quantidade")
        st.plotly_chart(fig_produto, use_container_width=True)
        
        # Gráfico 2: Distribuição por Motivo
        df_motivo = df.groupby("Motivo")["Quantidade"].sum().reset_index()
        fig_motivo = px.pie(
            df_motivo,
            names="Motivo",
            values="Quantidade",
            title="Distribuição por Motivo",
            hole=0.4
        )
        st.plotly_chart(fig_motivo, use_container_width=True)
        
        st.divider()
        
        # Tabela completa de registros
        st.subheader("📄 Histórico Completo")
        st.dataframe(df, use_container_width=True)
        
