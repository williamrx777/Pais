import streamlit as st
import pandas as pd
import plotly.express as px

# Setting page configuration
st.set_page_config(
    page_title="Países",
    page_icon="🗺️"
)


# Carregar o arquivo CSV
@st.cache
def load_data():
    df = pd.read_csv("paises.csv")  # Substitua "nome_do_arquivo.csv" pelo caminho do seu arquivo CSV
    return df

# Carregar os dados
df = load_data()

# Exibir widgets para seleção de país e critérios de pesquisa
st.sidebar.title("Filtros de Pesquisa")
countries = st.sidebar.multiselect("Selecione país(es):", df['CountryCode'].unique().tolist())
name_query = st.sidebar.text_input("Digite o nome da cidade:")
district_query = st.sidebar.text_input("Digite o nome do distrito:")
population_query = st.sidebar.number_input("Digite a população mínima:", value=0)

# Aplicar filtros aos dados
filtered_df = df.copy()
if countries:
    filtered_df = filtered_df[filtered_df['CountryCode'].isin(countries)]
if name_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(name_query, case=False)]
if district_query:
    filtered_df = filtered_df[filtered_df['District'].str.contains(district_query, case=False)]
if population_query:
    filtered_df = filtered_df[filtered_df['Population'] >= population_query]

# Exibir as cidades filtradas
# st.write("Cidades Filtradas:")
# st.dataframe(filtered_df)

# Plotar um gráfico de barras com base na população das cidades filtradas
fig = px.bar(filtered_df, x='Name', y='Population', labels={'Name': 'Cidade', 'Population': 'População'},
             title='População das Cidades')
fig.update_xaxes(tickangle=45)
fig.update_layout(height=600, width=1000)
st.plotly_chart(fig, use_container_width=True)
