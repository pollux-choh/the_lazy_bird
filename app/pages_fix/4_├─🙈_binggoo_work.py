import os
import sys
from dotenv import load_dotenv

from pathlib import Path
import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from google.cloud import bigquery

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

import pandas as pd
import numpy as np


def init():
    # 환경변수 설정
    load_dotenv()

    global base_dir, assets_dir
    # 현재 스크립트 파일이 있는 디렉토리의 경로를 얻습니다.
    base_dir = Path(__file__).parent.parent
    # assets 디렉토리 경로를 구성합니다.
    assets_dir = base_dir / "assets" / "bingoo"

    # Streamlit Page 설정
    st.set_page_config(
        page_title="A.I Bingoo",
        page_icon=":smile_cat:",
        initial_sidebar_state="expanded"
    )

    # Initialization
    if 'openai_api_key' not in st.session_state:
        st.session_state['openai_api_key'] = ''

    if 'google_api_key' not in st.session_state:
        st.session_state['google_api_key'] = ''

    if 'gcp_key' not in st.session_state:
        st.session_state['bigquery_key_file'] = ''
        
    if 'llm_model' not in st.session_state:
        st.session_state['llm_model'] = 'Gemini'

    if os.getenv("OPENAI_API_KEY"):
        st.session_state['openai_api_key'] = os.getenv("OPENAI_API_KEY")
    else:
        # 에러 메시지를 출력하고 스트림릿 앱 실행을 중단
        st.error('OPENAI_API_KEY가 설정되지 않았습니다. Config에서 설정해 주세요.')
        sys.exit('OPENAI_API_KEY가 설정되지 않았습니다. Config에서 설정해 주세요.')

    if os.getenv("GOOGLE_API_KEY"):
        st.session_state['google_api_key'] = os.getenv("GOOGLE_API_KEY")
    else:
        # 에러 메시지를 출력하고 스트림릿 앱 실행을 중단
        st.error('GOOGLE_API_KEY 설정되지 않았습니다. Config에서 설정해 주세요.')
        sys.exit('GOOGLE_API_KEY 설정되지 않았습니다. Config에서 설정해 주세요.')
        
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        st.session_state['bigquery_key_file'] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    else:
        # 에러 메시지를 출력하고 스트림릿 앱 실행을 중단
        st.error('GOOGLE_APPLICATION_CREDENTIALS이 설정되지 않았습니다. Config에서 설정해 주세요.')
        sys.exit('GOOGLE_APPLICATION_CREDENTIALS이 설정되지 않았습니다. Config에서 설정해 주세요.')

    global gcp_project, gcp_dataset, gcp_table
    gcp_project = "operation-v"
    gcp_dataset = "prod_wm_work_history"
    gcp_table = "wm_work_history"

    global user_input, sql_command, bigquery_result, program_code, answer, response_schemas, output_parser
    # 단계별 필요한 변수들
    user_input = ""
    sql_command = ""
    bigquery_result = pd.DataFrame()
    program_code = ""
    answer = ""
    response_schemas = [
        ResponseSchema(name="answer", description="answer to the user's question"),
        ResponseSchema(
            name="source",
            description="source used to answer the user's question",
        ),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    
    if 'answer' not in st.session_state:
        st.session_state['answer'] = ''
        
    if 'app_progress' not in st.session_state:
        # USER_INPUT    - 1.유저의 질문을 받는 단계
        # SQL_GENERATED - 2.SQL문을 생성한 단계
        # QUERY_COMPLETE- 3.Bigquery 결과를 받은 단계
        # CODE_COMPLETE - 4.코드를 생성한 단계
        # ANSWER        - 5.답변을 생성한 단계
        st.session_state.app_progress = ""

def _get_table_name(_):
    return f"{gcp_project}.{gcp_dataset}.{gcp_table}"

def _get_schema(_):
    with open(str(assets_dir / 'schema_work.json'), "r", encoding='UTF8') as f:
        schema = f.read()
    return schema

def _get_dataframe(_):
    return bigquery_result

def _set_dataframe(df):
    bigquery_result = df

def _get_dataframe_str(_):
    # df_str = f"df.info = {bigquery_result.info()} , df.head = {bigquery_result.head()}, df shape = {bigquery_result.shape}, df = {bigquery_result}"
    # print(bigquery_result)
    # print(df_str)
    df_str = bigquery_result.to_string()
    return df_str 

def _get_sql_command(_):
    return sql_command

def _set_sql_command(sql:str):
    sql_command = sql

    
def _get_program_code(_):
    return program_code

def _set_program_code(code:str):
    program_code = code

    
def _get_answer(_):
    return answer

def _set_answer(answer:str):
    answer = answer


def _run_query(query_string:str) -> pd.DataFrame:
    try:
        client = bigquery.Client()
        df = client.query(query_string).to_dataframe()
        if not df.empty:
            df = df.replace({np.nan: None})
            return df
        
        return None
    except Exception as e:
        raise RuntimeError(f"Bigquery에서 데이터를 조회하는 중 오류가 발생했습니다. {e}")

def remove_triple_quotes(sql_command):
    if sql_command.startswith("```") and sql_command.endswith("```"):
        print(f"*************{sql_command}")
        # print(sql_command[6:-3])
        if sql_command.startswith("```bigquery "):
            if sql_command.startswith("```bigquery sql "):
                return sql_command.replace("```bigquery sql ", "").replace("```", "")
            return sql_command.replace("```bigquery ", "").replace("```", "")
        elif sql_command.startswith("```sql"):
            if sql_command.startswith("```sql bigquery"):
                return sql_command.replace("```sql bigquery", "").replace("```", "")
            return sql_command.replace("```sql", "").replace("```", "")


        
    else:
        return sql_command


def main():
    # 초기 변수를 선언
    init()
        
    # Stremlit UI 생성
    st.caption("EXIS software Engineering & Pollux.ai")
    col_title, col_llm_combo = st.columns([10,2])
    with col_title:
        st.title("작업 이력 담당자")
    with col_llm_combo:
        selectllm = st.selectbox("Language Model", ["Gemini", "GPT-3.5", "GPT-4"], index=0)
        if selectllm == "Gemini":
            st.session_state['llm_model'] = "Gemini"
            # st.write("Gemini")
        elif selectllm == "GPT-3.5":
            st.session_state['llm_model'] = "GPT-3.5"
            # st.write("GPT-3.5")
        elif selectllm == "GPT-4":
            st.session_state['llm_model'] = "GPT-4"
            # st.write("GPT-4")
            
    # 언어모델 불러오기
    if st.session_state['llm_model'] == "GPT-3.5":
        model = ChatOpenAI(api_key=st.session_state['openai_api_key'],temperature=0, model="gpt-3.5-turbo")
    elif st.session_state['llm_model'] == "GPT-4":
        model = ChatOpenAI(api_key=st.session_state['openai_api_key'],temperature=0, model="gpt-4")
    else:
        # model = ChatOpenAI(api_key=st.session_state['openai_api_key'],temperature=0, model="gpt-3.5-turbo")
        model = ChatGoogleGenerativeAI(temperature=0, model="gemini-pro", convert_system_message_to_human=True, verbose=True)
    
    # Chain 1 - SQL을 생성하기 위한 chain
    template_1 = """You are expert Biquery SQL. And bigquery table name is '{table_name}'.""" \
                """You refer to the schema:{schema} provided when creating bigquery SQL, 
                and the column name must refer only to the 'column_name' of the schema and no other column name can be used. 
                And if the column 'enum' type is determined, only the parameter name must be used in the bigquery SQL statement.
                , write a Bigquery SQL that would answer the user's question. 
                    <Question>: {input}
                    <SQL Query>:"""
                #    if worker name like this [system@exissw.com,service-account-operv-das-gateway,service-account-operv-wm], they are not real worker. so except them.
                # """When querying, values that are None should be excluded.""" \

    # prompt_1 = ChatPromptTemplate.from_template(template_1_1+template_1_2+template_1_3)
    prompt_1 = ChatPromptTemplate.from_template(template_1)
    chain_1 = (
        RunnablePassthrough.assign(table_name=_get_table_name)
        | RunnablePassthrough.assign(schema=_get_schema)
        | prompt_1
        | model.bind(stop=["\nSQLResult:"])
        | StrOutputParser()
    )

    # template_2_1 = """You've got this data:{dataframe}"""
    # template_2_2 = """You coding sql commnd({sql_command}) by referring to the schema({schema}) of table_name({table_name})."""
    # template_2_3 = """if worker name like this [system@exissw.com,service-account-operv-das-gateway,service-account-operv-wm], they are not real worker. so except them."""
    # template_2_4 = """Based on the pandas dataframe, you run python code and answer the question:
    #     <Question>: {input}
    #     <Python Code>:
    #     <Answer>:"""

    # prompt_2 = ChatPromptTemplate.from_template(template_2_1 + template_2_2 + template_2_3 + template_2_4)
    
    # # Chain 2 - 최종답변을 생성하기 위한 chain
    # chain_2 = (
    #     RunnablePassthrough.assign(dataframe=_get_dataframe_str,sql_command=_get_sql_command,schema=_get_schema,table_name=_get_table_name)
    #     | prompt_2
    #     | model.bind(stop=["\nAnswer:"])
    #     | StrOutputParser()
    # )
    
    template_2_1 = """You are warehouse manager. Please answer in the language asked. If answer in the english, you have to answer in the English. If answer in the Korean, you have to answer in the Korean.
    Here is the data:{df} to be analyzed and summarized.
    When answering, all numbers must decimal point is truncated and comma-separated notation. And if data name is 'None' replace to 'ETC' in korean '기타'.
    When showing data, refer to the schema:{schema} for the column header or enum type and express it in the form of a data name (data code). For example, PICKUP allows the viewer to refer to it.
    <Question>: {input}
    <Answer>:"""
        # And if there are big number. you can use comma to seperate number. And all number present int type. And if data name is 'None' replace to 'ETC' in korean '기타'.
        # if worker name like this [system@exissw.com,service-account-operv-das-gateway,service-account-operv-wm], they are not real worker. so except them."""
        # You coding sql commnd({sql_command}) by referring to the schema({schema}) of table_name({table_name}).
        # Based on the pandas dataframe, you run python code and answer the question:"""
        # <Question>: {input}"""
        # <Answer>:"""
    
    # format_instructions = output_parser.get_format_instructions()
    prompt_2 = ChatPromptTemplate.from_template(template_2_1)
    
    # Chain 2 - 최종답변을 생성하기 위한 chain
    chain_2 = (
        RunnablePassthrough.assign(df=_get_dataframe,sql_command=_get_sql_command,schema=_get_schema,table_name=_get_table_name)
        | prompt_2
        # | model.bind(stop=["\nAnswer:"])
        | model.bind(stop=["\Answer:"])
        | StrOutputParser()
        # | output_parser
    )
    
    template_3_1 = """You are data analysis. You should explain the results of your raw data({data}). you can reference schema({schema})"""
    template_3_2 = """if worker name like this [system@exissw.com,service-account-operv-das-gateway,service-account-operv-wm], they are not real worker. so except them."""
    template_3_3 = """if there are big number. you can use comma to seperate number. and all number present int type.
        <Question>: {input}"""


    prompt_3 = ChatPromptTemplate.from_template(template_3_1 + template_3_2 + template_3_3)
    
    # Chain 2 - 최종답변을 생성하기 위한 chain
    chain_3 = (
        RunnablePassthrough.assign(data=_get_dataframe_str,schema=_get_schema)
        | prompt_3
        | model.bind(stop=["\nAnswer:"])
        | StrOutputParser()
    )

    template_exception_1 = """너는 '{table_name}'의 {schema}를 참고해서 {sql_command}를 작성했다. 그러나 이 SQL은 Big Query에서 실행되지 않았다."""
    template_exception_2 = """너는 답변에 필요한 자료를 얻지 못했다. 그래서 공손하게 네가 답변을 얻기 위해 어떤 과정을 거쳤는지 설명해준다."""
    template_exception_3 = """그리고, 이에대한 답변을 네가 아는 지식안에서 찾아보고, 그에 대한 답변을 작성한다.
        <Question>: {input}
        <Answer>:"""

    prompt_exception = ChatPromptTemplate.from_template(template_exception_1 + template_exception_2 + template_exception_3)
    
    # Chain exception - 예외 상황에 답변하는 chain
    chain_exception = (
        RunnablePassthrough.assign(table_name=_get_table_name)
        | RunnablePassthrough.assign(schema=_get_schema)
        | RunnablePassthrough.assign(sql_command=_get_sql_command)
        | prompt_exception
        | model.bind(stop=["\nAnswer:"])
        | StrOutputParser()
    )

        
    interface_container = st.container(border=1)
    
    logo, interface = interface_container.columns([1, 8])

    # streamlit으로 제목과 input box 생성
    logo.image(str(assets_dir / 'assistant-profile-work.png'), width=60)

    # st.write(get_table_name())
    user_input = interface.text_input(
        "Fullfillment Center 운영에 관한 질문을 입력하세요.",
    )

    # 1.User가 질문을 입력하고 Enter를 치면 SQL 생성
    if user_input :
        st.session_state.app_progress = "USER_INPUT"
        with st.spinner("데이터 수집중!!...:runner:"):
            sql_command = chain_1.invoke({"input": f"{user_input}"})
            sql_command = remove_triple_quotes(sql_command)
            
            print(f"[SQL COMMAND]: {sql_command}")

            st.session_state.app_progress = "SQL_GENERATED"

    # 2.SQL이 반환되었다면 이를 보여주고, Biquery에 데이터 조회(이단계에서 코드 검증을 한번 해보면 좋음)
    if st.session_state.app_progress == "SQL_GENERATED" :
        with st.popover(":page_with_curl: 기초 자료 모음"):
            tab1, tab2, tab3 = st.tabs(["SQL", "Result", "Code"])
            with tab1:
                st.write(sql_command)
                st_copy_to_clipboard(sql_command)
                
                try:
                    global bigquery_result
                    bigquery_result = _run_query(sql_command)
                    print(f"[BIG QUERY RESULT]: {bigquery_result}")

                    _set_dataframe(bigquery_result)
                    if bigquery_result is not None:
                        st.session_state.app_progress = "QUERY_COMPLETE"
                        
                except (RuntimeError, UnboundLocalError) as e:
                    # 에러가 발생했을때 답변 처리
                    st.session_state['answer'] = chain_exception.invoke({"input": f"{user_input}"})
                    
    # 3.SQL이 반환되었다면 이를 보여주고, Biquery에 데이터 조회(이단계에서 코드 검증을 한번 해보면 좋음)
            with tab2:
                if st.session_state.app_progress == "QUERY_COMPLETE":
                    st.dataframe(bigquery_result)
                    global answer
                    answer = chain_2.invoke({"input": f"{user_input}"})
                    print(f"[ANSWER]: {answer}")
                    st.session_state['answer'] = answer
                    # print(f"[PROGRAM CODE]: {answer}")
                    
                    # st.session_state['program_code'] = program_code
                    st.session_state.app_progress = "ANSWER"
            
            # with tab3:
            #     if st.session_state.app_progress == "CODE_COMPLETE":
            #         st.write(program_code)
            #         answer = chain_3.invoke({"input": f"{user_input}", "dataframe": f"{bigquery_result}"})
            #         print(f"[ANSWER]: {answer}")
            #         st.session_state['answer'] = answer
            #         st.session_state.app_progress = "ANSWER"
                    
        st.markdown(st.session_state['answer'])
        
if __name__ == "__main__":
    main()