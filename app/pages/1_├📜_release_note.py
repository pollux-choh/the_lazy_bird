import streamlit as st
from utils.resource_loader import DocLoader

docs = DocLoader('release','doc')

st.title('Release Note')
st.write(docs.get_doc('release_note.md'))