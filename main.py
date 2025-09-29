import requests
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(override=True)

# Set up the page configuration for the Streamlit app
st.set_page_config(
    page_title="Previsão do Tempo",
    page_icon="☀️",
    layout="wide",
)

# --- API and Data Fetching Configuration ---
link_api = "http://api.weatherapi.com/v1/current.json"
api_key = os.getenv("chave")

# --- Streamlit Frontend ---
st.title("☀️ Previsão do Tempo em Minas Gerais")
st.subheader("Verifique as condições climáticas em tempo real para sua cidade.")

# Create a text input for the user to enter a city name
cidade = st.text_input(
    "Digite o nome da cidade para verificar o tempo:",
    "Belo Horizonte"
)

# Only proceed with the API request if a city is entered
if cidade:
    parametros = {
        "key": api_key,
        "q": cidade,
        "lang": "pt"
    }

    # Use a spinner to indicate that the app is loading data
    with st.spinner('Buscando dados do tempo...'):
        try:
            resposta = requests.get(link_api, params=parametros)
            resposta.raise_for_status()  # Raise an exception for bad status codes
            dados_requisição = resposta.json()

            # Extract the relevant weather data
            temperatura_celsius = dados_requisição["current"]["temp_c"]
            descricao = dados_requisição["current"]["condition"]["text"]
            icon_url = dados_requisição["current"]["condition"]["icon"]

            # Display the weather information
            st.success(f"Dados encontrados para **{cidade}**!")
            
            # Show the weather icon
            col_icon, col_temp, col_desc = st.columns([1, 2, 2])
            with col_icon:
                st.image(f"https:{icon_url}")
            
            with col_temp:
                st.metric(label="Temperatura Atual", value=f"{temperatura_celsius}°C")
            
            with col_desc:
                st.metric(label="Condição", value=descricao)

        except requests.exceptions.HTTPError as err:
            if resposta.status_code == 400:
                st.error(f"Não foi possível encontrar o tempo para **{cidade}**. Verifique o nome da cidade e tente novamente.")
            else:
                st.error(f"Ocorreu um erro na requisição: {err}")
        except requests.exceptions.RequestException as err:
            st.error(f"Ocorreu um erro na conexão. Por favor, tente novamente mais tarde. Erro: {err}")