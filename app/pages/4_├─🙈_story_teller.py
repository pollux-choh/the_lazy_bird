import streamlit as st
from langchain_openai import ChatOpenAI
from utils.app_config import AppConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

conf = AppConfig()

def _get_story_feel(_):
    return feeling

def _get_story_category(_):
    return category

st.set_page_config(
    page_title="The Lazy Bird > Story Teller",
    page_icon="🙈",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('✒️스토리 텔러')

with st.expander('스토리의 성격을 골라 주세요',expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        feeling = st.selectbox('느낌', ['활발한', '슬픈', '딱딱한', '희망찬', '무서운', '행복한'])
    with col2:
        category = st.selectbox('카테고리', ['소설', '시', '신문기사', '방송 스크립트'])
        
with st.expander('llm을 설정해 주세요',expanded=True):
    # col1, col2 = st.columns([1, 1])
    # with col1:
    llm = st.selectbox('LLM', ['활발한', '슬픈', '딱딱한', '희망찬', '무서운', '행복한'])
    # with col2:
    # category = st.selectbox('카테고리', ['소설', '시', '신문기사', '방송 스크립트'])

template = """너는 훌륭한 이야기 꾼이야. 주제와 관련된 이야기를 '{feel}' 느낌으로 만들어줘. '{category}'로 쓰기 적합하게 써줘.
    <주제>: {input}
    <스토리>:"""

def generate_response(user_input):

    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOpenAI(temperature=0.7, openai_api_key=conf.open_ai_key, model="gpt-3.5-turbo")

    chain = (
        RunnablePassthrough.assign(feel=_get_story_feel, category=_get_story_category)
        | prompt
        | llm
        | StrOutputParser()
    )
    
    result = chain.invoke({"input": f"{user_input}"})
    
    return result

with st.form('my_form'):
    user_input = st.text_area('Enter text:', '여행')
    submitted = st.form_submit_button('Submit')
    if submitted:
        result = generate_response(user_input)
        # print(result)
        st.markdown(f"{result}")
    