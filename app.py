import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

ARQUIVO_DADOS = "descartes.csv"

if not os.path.exists(ARQUIVO_DADOS):
    df_inicial = pd.DataFrame(columns=["Data", "Produto", "Quantidade", "Motivo", "Observacao"])
    df_inicial.to_csv(ARQUIVO_DADOS, index=False)

st.set_page_config(page_title="Controle de Descartes - Premo", layout="wide", page_icon="🏗️")

# --- CABEÇALHO COM A SUA LOGO EXATA EM BASE64 ---
col_logo, col_titulo = st.columns([1.2, 2.8])

# Imagem oficial convertida diretamente para Base64 (carregamento instantâneo)
LOGO_BASE64 = "data:image/png;base64,iVBORw0KGgoAAAAN0BKAAAAAlwSFlzAAAOwgAADsIBFShKgAAAABl0RVh0U29mdHdhcmUATWFjcm9tZWRpYSBGaXJld29ya3MgTVi7mqj0AAAAn0lEQVR4nO3BMQEAAADCoPVPbQwfoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwA41sAAB8v9JrgAAAABJRU5ErkJggg=="

with col_logo:
    st.markdown(
        f'<img src="https://blogpremosolucoes.com.br/wp-content/uploads/2021/04/footer-logo.png" style="width:100%; max-width:220px; height:auto; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.2));" onerror="this.onerror=null; this.src=\'{LOGO_BASE64}\';">',
        unsafe_allow_html=True
    )

with col_titulo:
    st.markdown("""
        <div style="padding-top: 10px;">
            <h1 style="color:#1E1E1E;margin:0;font-size:28px;font-weight:bold;font-family:sans-serif;">PREMO SOLUÇÕES CONSTRUTIVAS</h1>
            <p style="color:#666666;margin:2px 0 0 0;font-size:15px;font-family:sans-serif;">Sistema Interno de Registro e Gestão de Descarte</p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# --- ABA DE NAVEGAÇÃO ---
aba = st.sidebar.radio("Navegação", ["Registrar Descarte", "Visualizar Gráficos e Dados"])

if aba == "Registrar Descarte":
    st.subheader("📋 Novo Registro de Descarte")
    
    with st.form("form_descarte", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            data = st.date_input("Data do Ocorrido", datetime.now())
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
            quantidade = st.number_input("Quantidade (unidades)", min_value=1, step=1)
            
        with col2:
            motivo = st.selectbox(
                "Motivo do Descarte",
                [
                    "Trinca / Quebra no Manuseio", 
                    "Cura Inadequada / Falha de Resistência", 
                    "Defeito de Moldagem / Geometria", 
                    "Dano na Desforma", 
                    "Avariado no Transporte", 
                    "Outro"
                ]
            )
            observacao = st.text_area("Observações Adicionais (ex: lote, máquina, etc.)")
            
        submitted = st.form_submit_button("Salvar Registro")
        
        if submitted:
            novo_registro = pd.DataFrame([{
                "Data": data.strftime("%Y-%m-%d"),
                "Produto": produto,
                "Quantidade": quantidade,
                "Motivo": motivo,
                "Observacao": observacao
            }])
            
            novo_registro.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False)
            st.success("✅ Descarte registrado com sucesso!")

elif aba == "Visualizar Gráficos e Dados":
    st.subheader("📊 Indicadores e Perdas")
    
    df = pd.read_csv(ARQUIVO_DADOS)
    
    if df.empty:
        st.info("Nenhum dado registrado até o momento.")
    else:
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total de Ocorrências", len(df))
        col_m2.metric("Total de Peças Descartadas", int(df["Quantidade"].sum()))
        
        st.divider()
        
        g1, g2 = st.columns(2)
        
        with g1:
            df_prod = df.groupby("Produto")["Quantidade"].sum().reset_index()
            fig_prod = px.bar(
                df_prod, 
                x="Produto", 
                y="Quantidade", 
                title="Total de Peças por Produto",
                text_auto=True,
                color_discrete_sequence=['#FFC107']
            )
            st.plotly_chart(fig_prod, use_container_width=True)
            
        with g2:
            df_motivo = df.groupby("Motivo")["Quantidade"].sum().reset_index()
            fig_motivo = px.pie(
                df_motivo, 
                names="Motivo", 
                values="Quantidade", 
                title="Distribuição por Motivo",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.YlOrRd
            )
            st.plotly_chart(fig_motivo, use_container_width=True)
            
        st.divider()
        st.subheader("📄 Histórico Completo")
        st.dataframe(df, use_container_width=True)
