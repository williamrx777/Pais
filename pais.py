import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados do arquivo CSV
@st.cache
def load_data():
    df = pd.read_csv("paises.csv")
    return df

# Função para exibir as cidades de um país selecionado
def show_country_cities(df, selected_country):
    filtered_df = df[df['CountryCode'] == selected_country]
    st.write(f"Cidades de {selected_country}:")
    st.dataframe(filtered_df)
    return filtered_df

# Função para plotar um gráfico de barras com base na população das cidades do país selecionado
def plot_population_bar_chart(filtered_df, selected_country):
    fig = px.bar(filtered_df, x='Name', y='Population', labels={'Name': 'Cidade', 'Population': 'População'},
                 title=f'População das Cidades em {selected_country}')
    fig.update_xaxes(tickangle=45)
    fig.update_layout(height=600, width=1000)
    st.plotly_chart(fig, use_container_width=True)

# Carregar os dados do arquivo CSV
df = load_data()

# Selecionar um país específico
countries = df['CountryCode'].unique().tolist()
selected_country = st.sidebar.selectbox("Selecione um país:", countries)

# Exibir as cidades do país selecionado
filtered_df = show_country_cities(df, selected_country)

# Plotar um gráfico de barras com base na população das cidades do país selecionado
plot_population_bar_chart(filtered_df, selected_country)
