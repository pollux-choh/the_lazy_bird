import streamlit as st
from utils.resource_loader import DocLoader
from utils.app_config import AppConfig

doc = DocLoader('streamlit')
conf = AppConfig()

st.title('📱 Streamlit 공부 하기')
st.write(doc.get_text('site_list.md'))