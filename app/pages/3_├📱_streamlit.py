import os
from pathlib import Path
import streamlit as st
import pandas as pd

data_df = pd.DataFrame(
    {
        "category": [
            "📊 stremlit 시작하기",
            "📈 streamlit 60일",
            "🤖 추천 사이트",
            "📊 커뮤니티",
        ],
    }
)

# Using "with" notation
with st.sidebar:
    data_df
    
st.title('Streamlit')
st.write(data_df.select_dtypes('category'))