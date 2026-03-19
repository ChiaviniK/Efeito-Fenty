import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(
    page_title="Além do Tom | Data Hub",
    page_icon="💄",
    layout="wide"
)

# 2. Funções para carregar DADOS REAIS via URL (GitHub do The Pudding)
@st.cache_data
def carregar_dados_shades():
    """Carrega o dataset real de tons de base (Hex codes e Luminosidade)."""
    url_shades = "https://raw.githubusercontent.com/thepudding/data/master/foundation-names/allShades.csv"
    try:
        df = pd.read_csv(url_shades)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

@st.cache_data
def carregar_dados_numeros():
    """Carrega o dataset real que mapeia os números/nomes dos tons."""
    url_numbers = "https://raw.githubusercontent.com/thepudding/data/master/foundation-names/allNumbers.csv"
    try:
        df = pd.read_csv(url_numbers)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

# Carregando as variáveis com os dados reais
df_shades = carregar_dados_shades()
df_numeros = carregar_dados_numeros()

# 3. Construção da Interface
st.title("💄 Além do Tom: Hub de Datasets Reais")
st.markdown("""
Bem-vindo ao portal de dados do estudo de caso **"Além do Tom"**. 
Os dados disponibilizados aqui são provenientes do repositório público do projeto *The Naked Truth* (The Pudding), contendo informações reais de milhares de bases extraídas da Sephora e Ulta Beauty.
""")

st.divider()

# Layout em duas colunas
col1, col2 = st.columns(2)

with col1:
    st.header("📦 1. Espectro de Cores (Shades)")
    st.write("Dataset contendo a marca, produto, URL, código Hex e o valor de luminosidade (*lightness*) de cada tom. Essencial para análises de distribuição de cores.")
    
    if not df_shades.empty:
        # Exibe as primeiras linhas do dataset real
        st.dataframe(df_shades.head(10), use_container_width=True)
        
        # Botão de Download
        csv_shades = df_shades.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dataset de Cores (CSV)",
            data=csv_shades,
            file_name='thepudding_allShades.csv',
            mime='text/csv',
            type="primary"
        )

with col2:
    st.header("🏷️ 2. Nomenclatura e Numeração")
    st.write("Dataset que correlaciona os tons com os nomes e números dados pelas marcas. Útil para análises de NLP sobre como as marcas 'nomeiam' tons escuros vs. claros.")
    
    if not df_numeros.empty:
        # Exibe as primeiras linhas do dataset real
        st.dataframe(df_numeros.head(10), use_container_width=True)
        
        # Botão de Download
        csv_numeros = df_numeros.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Dataset de Nomes (CSV)",
            data=csv_numeros,
            file_name='thepudding_allNumbers.csv',
            mime='text/csv',
            type="primary"
        )

st.divider()

# Exemplo de visualização rápida com os dados reais
st.subheader("📊 Espiada nos Dados: Distribuição de Luminosidade")
st.write("Um histograma rápido mostrando a distribuição da luminosidade (do mais escuro ao mais claro) das bases listadas.")
if not df_shades.empty and 'lightness' in df_shades.columns:
    st.bar_chart(df_shades['lightness'].value_counts(bins=20).sort_index())
