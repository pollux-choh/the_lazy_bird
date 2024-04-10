import streamlit as st
import pandas as pd
from utils.resource_loader import DocLoader
from utils.app_config import AppConfig

conf = AppConfig()
docs = DocLoader('main')
st.set_page_config(
    page_title="The Lazy Bird",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.container(border=1):
    tab1, tab2 = st.tabs(["공지사항", "프로젝트 소개"])

    with tab1:
        st.write(docs.get_text('notice.md'))

    with tab2:
        st.write(docs.get_text('project_info.md'))

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