import requests
import streamlit as st
import os
import pprint
from dotenv import load_dotenv

load_dotenv(override=True)

st.set_page_config(
    page_title="Previsão do Tempo",
    page_icon="☀️",
    layout="wide",
)

link_api = "http://api.weatherapi.com/v1/current.json"
api_key = st.secrets["API_KEY_TEMP"]


parametros = {
    "key": api_key,
    "q": "Minas Gerais",
    "lang": "pt"
}
resposta = requests.get(link_api, params=parametros)

print(resposta.status_code)
print(resposta.content)

if resposta.status_code == 200:
    dados_requisição = resposta.json()
    pprint.pprint(dados_requisição)
temperatura_celsius = dados_requisição["current"]["temp_c"]
descricao = dados_requisição["current"]["condition"]["text"]
print(f"A temperatura atual em Minas Gerais é de {temperatura_celsius}°C com {descricao}.") 



st.title("☀️ Previsão do Tempo")
st.subheader("Verifique as condições climáticas em tempo real para sua cidade.")

cidade = st.text_input(
    "Digite o nome da cidade para verificar o tempo:",
    "Belo Horizonte"
)

if cidade:
    parametros = {
        "key": api_key,
        "q": cidade,
        "lang": "pt"
    }





    with st.spinner('Buscando dados do tempo...'):
        try:
            resposta = requests.get(link_api, params=parametros)
            resposta.raise_for_status()  
            dados_requisição = resposta.json()

        
            temperatura_celsius = dados_requisição["current"]["temp_c"]
            descricao = dados_requisição["current"]["condition"]["text"]
            humidade = dados_requisição["current"]["humidity"]
            vel_vento = dados_requisição["current"]["wind_kph"]
            icon_url = dados_requisição["current"]["condition"]["icon"]

       
            st.success(f"Dados encontrados para **{cidade}**!")
            
      
            col_icon, col_temp, col_desc, col_humi, col_vento = st.columns([1, 2, 2, 4, 4])
            with col_icon:
                st.image(f"https:{icon_url}")
            
            with col_temp:
                st.metric(label="Temperatura Atual", value=f"{temperatura_celsius}°C")
            
            with col_desc:
                st.metric(label="Condição", value=descricao)

            with col_humi:
                st.metric(label="Humidade", value=f"{humidade}°%")
            with col_vento:
                st.metric(label="Velocidade do vento", value=f"{vel_vento}°KM/h")

        except requests.exceptions.HTTPError as err:
            if resposta.status_code == 400:  
                st.error(f"Não foi possível encontrar o tempo para **{cidade}**. Verifique o nome da cidade e tente novamente.")
            else:
                st.error(f"Ocorreu um erro na requisição: {err}")
        except requests.exceptions.RequestException as err:
            st.error(f"Ocorreu um erro na conexão. Por favor, tente novamente mais tarde. Erro: {err}")