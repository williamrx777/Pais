import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# Função para se conectar ao banco de dados MySQL
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="gmr123.",
            database="world"
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            st.write(f"Conectado ao MySQL Server versão {db_info}")
            return connection
    except mysql.connector.Error as e:
        st.error(f"Erro ao conectar ao MySQL Server: {e}")
        return None

# Função para executar consultas SQL
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor
    except mysql.connector.Error as e:
        st.error(f"Erro ao executar a consulta: {e}")
        return None

# Conectar ao banco de dados
connection = connect_to_mysql()

# Verificar se a conexão foi bem sucedida antes de prosseguir
if connection:
    # Exemplo de consulta SQL
    query = """SELECT * FROM city;"""
    cursor = execute_query(connection, query)
    
    # Exibir os resultados da consulta
    if cursor:
        result = cursor.fetchall()
        if result:
            # Criar um DataFrame pandas a partir dos resultados da consulta
            df = pd.DataFrame(result, columns=['ID', 'Name', 'CountryCode', 'District', 'Population'])
            
            # Selecionar um país específico
            countries = df['CountryCode'].unique().tolist()
            selected_country = st.sidebar.selectbox("Selecione um país:", countries)
            
            # Filtrar as cidades pelo país selecionado
            filtered_df = df[df['CountryCode'] == selected_country]
            
            # Exibir as cidades do país selecionado
            st.write(f"Cidades de {selected_country}:")
            st.dataframe(filtered_df)
            
            # Plotar um gráfico de barras com base na população das cidades do país selecionado
            fig = px.bar(filtered_df, x='Name', y='Population', labels={'Name': 'Cidade', 'Population': 'População'},
                         title=f'População das Cidades em {selected_country}')
            fig.update_xaxes(tickangle=45)
            fig.update_layout(height=600, width=1000)
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.write("Nenhum resultado encontrado.")
        
        # Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        connection.close()
