import streamlit as st
from utils.resource_loader import DocLoader

docs = DocLoader('config')

st.title('⚙️ Config')
st.write(docs.get_doc('description.md'))

# OPEN AI 설정을 위한 컨테이너
st.subheader('Open AI')
open_ai = st.container(border=1)

active_open_ai = open_ai.toggle('OpenAI ChatGPT')
if active_open_ai:
    open_ai.text_input('🔑OPENAI API Key')
    open_ai.link_button("API Key 발급 링크", "https://platform.openai.com/api-keys")
    if open_ai.text_input:

# Google AI Platform 설정을 위한 컨테이너
st.subheader('Google AI Platform')
google_ai = st.container(border=1)

active_google_ai = google_ai.toggle('Google Gemini')
if active_google_ai:
    tab1, tab2 = google_ai.tabs(["🔑API Key 방식", "📧Authentication File 방식"])
    
    with tab1:
        tab1.text_input('GEMINI API Key')
        tab1.link_button("API Key 발급 링크", "https://aistudio.google.com/app/apikey")
    with tab2:
        tab2.file_uploader('GEMINI Authentication File')
        tab2.caption("👉 Authentication File 발급은 회사나 MSP의 GCP 관리자에게 문의하세요.")

active_bigquery = google_ai.toggle('Google BigQuery')
if active_bigquery:
    google_ai.file_uploader('Google BigQuery Authentication File')
    google_ai.caption("👉 Authentication File 발급은 회사나 MSP의 GCP 관리자에게 문의하세요.")