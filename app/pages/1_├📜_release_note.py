import streamlit as st
from utils.pollux_util import DocLoader

docs = DocLoader('release')

st.title('Release Note')
st.write(docs.get_doc('release_note.md'))