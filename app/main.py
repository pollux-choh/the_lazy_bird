import streamlit as st
import pandas as pd
from utils.pollux_util import DocLoader

docs = DocLoader('main')

# 데이터를 로드합니다.
data_df = pd.DataFrame(
    {
        "category": [
            "📊 Data Exploration",
            "📈 Data Visualization",
            "🤖 LLM",
            "📊 Data Exploration",
        ],
    }
)

st.write(docs.get_doc('main_notice.md'))

st.video('https://www.youtube.com/watch?v=TEKyEQL-S8o&list=RDTEKyEQL-S8o&start_radio=1')