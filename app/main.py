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

st.title("The Lazy Bird")

with st.container(border=1):
    tab1, tab2 = st.tabs(["공지사항", "프로젝트 소개"])

    with tab1:
        st.write(docs.get_doc('notice.md'))

    with tab2:
        st.write(docs.get_doc('project_info.md'))

st.subheader("👏👏빌드 축하 공연🎉🎉")
with st.container(border=1):
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.text("(여자)아이들((G)I-DLE) - '나는 아픈 건 딱 질색이니까")
        st.video('https://www.youtube.com/watch?v=ATK7gAaZTOM')
        # st.divider()
        st.caption("https://www.youtube.com/watch?v=ATK7gAaZTOM")

    with col2:
        st.text("ILLIT(아일릿) - Magnetic")
        # st.divider()
        st.video('https://www.youtube.com/watch?v=TEKyEQL-S8o&list=RDTEKyEQL-S8o&start_radio=1')
        st.caption("https://www.youtube.com/watch?v=TEKyEQL-S8o")

    with col3:
        st.text("비비 (BIBI) - 밤양갱(Bam Yang Gang)")
        st.video('https://www.youtube.com/watch?v=smdmEhkIRVc')
        # st.divider()
        st.caption("https://www.youtube.com/watch?v=smdmEhkIRVc")