import os
from pathlib import Path
import streamlit as st
import pandas as pd

data_df = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization Data Visualization Data Visualization Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)

# Using "with" notation
with st.sidebar:
    # add_content = st.data_editor(
    #     data_df,
    #     column_config={
    #         "category": st.column_config.SelectboxColumn(
    #             "Documents",
    #             help="The category of the documents",
    #             width="medium",
    #             options=[
    #                 "📊 Data Exploration",
    #                 "📈 Data Visualization",
    #                 "🤖 LLM",
    #             ],
    #             required=True,
    #         )
    #     },
    #     hide_index=True,
    # )
    
    # add_content2 = st.column_config.SelectboxColumn(
    #     "Documents",
    #     help="The category of the documents",
    #     width="medium",
    #     options=[
    #         "📊 Data Exploration",
    #         "📈 Data Visualization",
    #         "🤖 LLM",
    #     ],
    #     required=True,
    # )
    data_df
    
st.title('Release Note')
st.markdown('''
            ### 2024-03-21 Release Note ###
            
            0.1a 버전 작업이력 담당자, 미출 처리 담당자를 따로 구성하였습니다.
            
            __주요패치__
            > * 새로운 미출 처리 담당자가 입사하였습니다.
            ---
            
            ### 2024-03-14 Release Note ###
            
            0.1a 버전 Gemini 추가, Environment Manager, 예외상황 처리를 추가 하였습니다.
            
            __주요패치__
            > * 설정하기 화면에 LLM을 선택할 수 있도록 추가하였습니다.
            > * Gemini를 추가하였으나, 아직 실험적 입니다.
            > * Google BigQuery 인증키를 안정적으로 갱신 할 수 있습니다.
            > * Environment Manager를 추가하여, 환경변수를 관리할 수 있습니다.
            > * 예외상황 처리를 추가하여, Error 발생시 더욱 친절한 답변을 보여줍니다.
            ---
            
            ### 2024-03-13 Release Note ###
            
            0.1a 버전의 버그를 수정 하여, 안정화 하였습니다.
            
            __주요패치__
            > * 설정하기에서 화면이 갱신되지 않는 문제를 해결 하였습니다.
            > * assets 접근 방식을 Pathlib으로 변경하여 절대 경로로 접근하게 변경하였습니다.
            ---
            
            ### 2024-03-12 Release Note ###
            
            0.1a 버전을 출시 하였습니다. 
            
            __주요기능__
            > * 설정하기 - OpenAI API키와 GCP 서비스 키를 설정할 수 있습니다.
            > * 데이터 탐색 - BigQuery에서 데이터를 탐색할 수 있습니다.
            ''')