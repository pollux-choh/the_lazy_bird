import streamlit as st
from google.oauth2 import service_account
from openai import OpenAI
from utils.app_config import AppConfig
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as gemini_client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_text_splitters import CharacterTextSplitter,RecursiveCharacterTextSplitter
from langchain_community.document_loaders.text import TextLoader
from utils.resource_loader import DocLoader
conf = AppConfig()
doc = DocLoader(content_name='embedding')


# client = OpenAI(
#     api_key=conf.open_ai_key
# )

# document = ['백터','데이터베이스는','말','그대로','백터를','저장하는','저장소입니다.']

# response = client.embeddings.create(
#     input = document,
#     # open ai에서 제공하는 임베딩 모델
#     model="text-embedding-ada-002"
# )
# response

st.write('sudo docker run -p 6333:6333 qdrant/qdrant')
st.link_button("Go to Qdrant DB Web UI", "http://localhost:6333/dashboard")
collection_name = "example_collection"

# client = QdrantClient(url="http://localhost:6333")
# gemini_client.configure(credentials=conf.google_credentials)
# gemini_client.configure(api_key=conf.google_ai_key)


# results = [
#     gemini_client.embed_content(
#         model="models/embedding-001",
#         content=sentence,
#         task_type="retrieval_document",
#         title="Qdrant x Gemini",
#     )
#     for sentence in texts
# ]
# st.write(conf.google_credentials)
credentials = service_account.Credentials.from_service_account_file(conf.google_credentials)

embeddings = GoogleGenerativeAIEmbeddings(
    credentials=credentials,
    model="models/text-embedding-004",
    task_type="retrieval_document",
    )

# vectors = doc_embeddings.embed_documents(texts)

# len(vectors), len(vectors[0])

# texts = [
#     "Qdrant is a vector database that is compatible with Gemini.",
#     "Gemini is a new family of Google PaLM models, released in December 2023.",
# ]

# text_path = r"D:\ws-pollux\the_lazy_bird\app\doc\embedding\state_of_the_union.txt"
# doc.get_text('nuti_tree.txt')
# text_path = r"D:\ws-pollux\the_lazy_bird\app\doc\embedding\nuti_tree.txt"
# text_path = doc.get_text('nuti_tree.txt')
text_path = doc.content_dir / 'nuti_tree.txt'
with st.expander("original text"):
    st.markdown(doc.get_text('nuti_tree.txt'))
    
loader = TextLoader(text_path,encoding='UTF-8')
documents = loader.load()

# text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap  = 50,
    length_function = len,
)
docs = text_splitter.split_documents(documents)

with st.expander("document"):
    st.write(docs)

qdrant = Qdrant.from_documents(
    docs,
    embeddings,
    location=":memory:",  # Local mode with in-memory storage only
    collection_name="my_documents",
)

# url = "http://localhost:6333"
# client = QdrantClient(url, port=6333, grpc_port=6333)

# qdrant = Qdrant(
#     embeddings=doc_embeddings,
#     client=client,
#     # prefer_grpc=True,
#     collection_name="my_documents",
# )
'''
url = "http://localhost"
qdrant = Qdrant.from_documents(
    docs, 
    embeddings,
    url=url,
    prefer_grpc=True,
    collection_name="my_documents",
    # force_recreate=True,
)
'''
# documents=docs,

text_input_placeholder = "그도 단번에 기운을 회복하며 대답하였다."
query = st.text_input(label="Query",placeholder=text_input_placeholder)
# st.title("[QUERY]")
# st.write(query)
if st.button("Query"):
    found_docs = qdrant.similarity_search_with_score(query)

    st.title("[ANSWER]")
    document, score = found_docs[0]
    st.write(document.page_content)
    st.write(f"\nScore: {score}")
    # st.write(found_docs[0].page_content)
    # st.write(found_docs[0].metadata)