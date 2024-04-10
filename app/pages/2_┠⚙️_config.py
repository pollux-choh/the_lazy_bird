import os
import streamlit as st
import random
from dotenv import load_dotenv,dotenv_values
from utils.resource_loader import DocLoader
from utils.app_config import AppConfig

conf = AppConfig()
docs = DocLoader('config')
st.set_page_config(
    page_title="The Lazy Bird > Config",
    page_icon="⚙️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('⚙️ Config')
st.write(docs.get_text('description.md'))


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

# LLM Info 패널
with st.expander("LLM 정보 자세히 보기"):
    st.write("사용할 수 있는 LLM 모델 정보를 확인할 수 있습니다.")
    conf.llm_models
    
# OPEN AI 설정을 위한 컨테이너
st.subheader('Open AI')

# OPEN AI > Application Info 패널
with st.expander("Open AI API Key 설정하는 방법 보기"):
    st.write(docs.get_text('openai.md'))

# OPEN AI > 설정 관련 패널
open_ai = st.container(border=1)
active_open_ai = open_ai.toggle('🔑 OpenAI ChatGPT API Key', value=conf.open_ai_key)
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
            if col1_2.button("삭제", key='btn_delete_open_ai_key',help="현재 등록된 API 키를 삭제합니다."):
                conf.env_key_remove('OPENAI_API_KEY')
                st.rerun()

        else:
            if col1_2.button("등록", key='btn_regist_open_ai_key', help="입력한 API 키를 등록합니다."):
                conf.env_key_add('OPENAI_API_KEY', open_ai_key)
                st.rerun()


# Google AI Platform 설정을 위한 컨테이너
st.subheader('Google AI Platform')

# Google AI Platform > Application Info 패널
with st.expander("Google AI platform 설정하는 방법 보기"):
    st.write(docs.get_text('google_ai.md'))

# Google AI Platform > 설정 관련 패널
google_ai = st.container(border=1)

active_google_ai = google_ai.toggle('🔑 Gemini API Key', value=conf.google_ai_key)
if active_google_ai:
    col2_1, col2_2 = google_ai.columns([7,1])

    with col2_1:
        google_ai_key = col2_1.text_input(
                            "'GEMINI API Key를 입력합니다. GCP credential에 포함되어 있으면 입력하지 않아도 됩니다.'", 
                            '',
                            label_visibility="collapsed",
                            placeholder=__mask_key_string(conf.google_ai_key))

    with col2_2:
        if conf.google_ai_key:
            if col2_2.button("삭제", key='btn_delete_google_api_key',help="현재 등록된 API 키를 삭제합니다."):
                conf.env_key_remove('GOOGLE_API_KEY')
                st.rerun()
        
        else:
            if col2_2.button("등록", key='btn_regist_google_api_key', help="입력한 API 키를 등록합니다."):
                conf.env_key_add('GOOGLE_API_KEY', google_ai_key)
                st.rerun()


active_google_credential = google_ai.toggle('📧 GCP credential', value=conf.is_credentials_exist(conf.google_credentials))
if active_google_credential:
    if conf.is_credentials_exist(conf.google_credentials):
        if google_ai.button("Google credential file 삭제하기", key='btn_delete_google_credential',help="현재 등록된 GCP credential을 삭제합니다."):
            # conf.env_key_remove('GOOGLE_APPLICATION_CREDENTIALS')
            os.remove(conf.google_credentials)
            st.success('기존 인증 파일이 삭제되었습니다.')
            st.rerun()
    else:
        uploaded_file = google_ai.file_uploader('GCP credentail(.json) 파일을 업로드 하세요.', label_visibility="collapsed", type=['json'])
        if uploaded_file is not None:
            # 파일 쓰기
            with open(conf.google_credentials, 'wb') as f:
                f.write(uploaded_file.read())
            st.success('파일 업로드 완료')
            st.rerun()


