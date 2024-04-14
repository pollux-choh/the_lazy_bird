import streamlit as st
from langchain_openai import ChatOpenAI
from utils.app_config import AppConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

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

with st.expander('llm에 대한 설정을 해 주세요.',expanded=True):
    # active가 되어있는 llm 모델들을 가져옴
    llm_models = conf.get_llm_models(is_active=1)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_llm_name = st.selectbox('LLM', llm_models["llm_name"].tolist())
    with col2:
        llm_temerpature = st.slider('Temperature(허언증 정도, 1이면 허언증 최고)', 0.0, 1.0, 0.0, step=0.1)

with st.expander('스토리의 성격을 골라 주세요',expanded=True):
    col1, col2 = st.columns([1, 1])
    with col1:
        feeling = st.selectbox('느낌', ['활발한', '슬픈', '딱딱한', '희망찬', '무서운', '행복한'])
    with col2:
        category = st.selectbox('카테고리', ['소설', '시', '신문기사', '방송 스크립트'])

template = """너는 훌륭한 이야기 꾼이야. 주제와 관련된 이야기를 '{feel}' 느낌으로 만들어줘. '{category}'로 쓰기 적합하게 써줘.
    <주제>: {input}
    <스토리>:"""

def generate_response(user_input):
    # 사용자가 선택한 LLM 모델 이름을 기반으로 해당 모델 정보를 DataFrame에서 찾음
    selected_model_info = conf.llm_models[conf.llm_models['llm_name'] == selected_llm_name].iloc[0]
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm_brand = selected_model_info["brand"]
    llm_model_name = selected_model_info["llm_name"]
    
    if llm_brand == "google":
        llm = ChatGoogleGenerativeAI(
            google_api_key=conf.google_ai_key,
            model=llm_model_name,
            temperature=llm_temerpature,
            convert_system_message_to_human=True)
        
    elif llm_brand == "openai":
        llm = ChatOpenAI(
            openai_api_key=conf.open_ai_key,
            model=llm_model_name,
            temperature=llm_temerpature)
    else:
        raise ValueError("지원하지 않는 LLM 모델입니다.")
    
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
    