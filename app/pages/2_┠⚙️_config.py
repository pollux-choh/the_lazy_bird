import streamlit as st
import random
from dotenv import load_dotenv,dotenv_values
from utils.resource_loader import DocLoader
from utils.app_config import AppConfig

conf = AppConfig()
docs = DocLoader('config')

st.write(conf.open_ai_key)
st.write(conf.google_ai_key)
st.write(conf.google_credentials)

st.title('⚙️ Config')
st.write(docs.get_doc('description.md'))

# key 문자열을 보여주지 않도록 수정
def __mask_key_string(key:str) -> str:
    # key가 None이거나 빈 문자열인 경우를 처리
    if not key:
        return ''

    length = len(key)
    if length <= 6:
        return key[0] + '*' * (length - 2) + key[-1]
    else:
        mask_length = length - 6
        reduced_mask_length = max(mask_length - random.randint(3, 4), 1)  # Ensure at least 1 asterisk
        return key[:3] + '*' * reduced_mask_length + key[-3:]
    

# Application Info 패널
with st.expander("Application 정보 자세히 보기"):
    st.text_input('root directory',placeholder=conf.base_dir,disabled=True)
    st.text_input('".env" file path',placeholder=conf.env_file,disabled=True)


# OPEN AI 설정을 위한 컨테이너
st.subheader('Open AI')
open_ai = st.container(border=1)

# OPEN AI > Application Info 패널
with st.expander("Open AI API Key 발급에 관한 내용 보기"):
    st.write(docs.get_doc('openai.md'))

# OPEN AI > 설정 관련 패널
active_open_ai = open_ai.toggle('🔑 OpenAI ChatGPT API Key 활성화',value=conf.open_ai_key)
if active_open_ai:
    col1_1, col1_2 = open_ai.columns([7,1])
    
    with col1_1:
        open_ai_key = col1_1.text_input(
                            "OPENAI API Key를 입력하세요.", 
                            '',
                            label_visibility="collapsed",
                            placeholder=__mask_key_string(conf.open_ai_key))

    with col1_2:
        if conf.open_ai_key:
            if col1_2.button("삭제", key='btn_regist_openai',help="현재 등록된 API 키를 삭제합니다."):
                conf.env_remove('OPENAI_API_KEY')
                st.rerun()
                
        else:
            if col1_2.button("등록", key='btn_regist_openai', help="입력한 API 키를 등록합니다."):
                conf.env_add('OPENAI_API_KEY', open_ai_key)
                st.rerun()


# Google AI Platform 설정을 위한 컨테이너
st.subheader('Google AI Platform')

# Google AI Platform > Application Info 패널
with st.expander("Google AI platform 설정에 관한 내용 보기"):
    st.write(docs.get_doc('google_ai.md'))

# Google AI Platform > 설정 관련 패널
google_ai = st.container(border=1)

active_google_ai = google_ai.toggle('🔑 Gemini API Key 활성화')
if active_google_ai:
    google_ai.text_input('GEMINI API Key를 입력합니다. GCP credential에 포함되어 있으면 입력하지 않아도 됩니다.')


active_bigquery = google_ai.toggle('📧 GCP credential 활성화')
if active_bigquery:
    google_ai.file_uploader('GCP credentail(.json) 파일을 업로드 하세요.')
    google_ai.caption("👉 Authentication File 발급은 회사나 MSP의 GCP 관리자에게 문의하세요.")


