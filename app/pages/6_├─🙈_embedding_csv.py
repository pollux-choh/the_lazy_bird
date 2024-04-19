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
from langchain_community.document_loaders.csv_loader import CSVLoader
from collections import defaultdict
from langchain_openai import OpenAIEmbeddings

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
collection_name = "logi_news"


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
file_path = r"D:\ws-pollux\the_lazy_bird\app\secure\article_small.csv"
with st.expander("original text"):
    st.markdown(file_path)
    
loader = CSVLoader(
    file_path=file_path,
    source_column = "article",
    metadata_columns = ["url", "heading", "journalist", "report_date", "sub_heading"],
    encoding='UTF-8',
    csv_args={
        "delimiter": "|",
        "quotechar": '"',
    },
)
documents = loader.load()

with st.expander(f"{len(documents)} article loaded"):
    st.markdown(documents)

# st.write(documents)
# text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=10)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
)


chunks = text_splitter.split_documents(documents)
with st.expander(f"{len(chunks)} doc splited"):
    st.markdown(chunks)

credentials = service_account.Credentials.from_service_account_file(conf.google_credentials)

gemini_embeddings = GoogleGenerativeAIEmbeddings(
    credentials=credentials,
    model="models/text-embedding-004",
    task_type="retrieval_document",
    )

openai_embeddings = OpenAIEmbeddings(
    api_key=conf.open_ai_key,
    model="text-embedding-ada-002"
    )

# qdrant = Qdrant.from_documents(
#     docs,
#     openai_embeddings,
#     location=":memory:",  # Local mode with in-memory storage only
#     collection_name="logi_news",
# )


# url = "http://localhost:6333"
# client = QdrantClient(url, port=6333, grpc_port=6333)

# qdrant = Qdrant(
#     embeddings=doc_embeddings,
#     client=client,
#     # prefer_grpc=True,
#     collection_name="my_documents",
# )
# url = "http://localhost"
# qdrant = Qdrant.from_documents(
#     docs, 
#     embeddings,
#     url=url,
#     prefer_grpc=True,
#     collection_name="my_documents",
#     # force_recreate=True,
# )
# documents=docs,

# query = st.text_input(label="Query")
# st.title("[QUERY]")
# st.write(query)

# if st.button("Query"):
#     found_docs = qdrant.similarity_search_with_score(query)

#     st.title("[ANSWER]")
#     document, score = found_docs[0]
#     st.write(document.page_content)
#     st.write(f"\nScore: {score}")
#     # st.write(found_docs[0].page_content)
#     # st.write(found_docs[0].metadata)

# if st.button("Query"):
#     found_docs = qdrant.similarity_search_with_score(query)

#     # URL을 기준으로 문서 그룹화
#     grouped_documents = defaultdict(list)
#     for doc, score in found_docs:
#         grouped_documents[doc.metadata['url']].append((doc, score))

#     # 결과 출력
#     for url, docs in grouped_documents.items():
#         st.title(f"Documents for {url}")
#         for doc, score in docs:
#             st.write(doc.page_content)
#             st.write(f"Score: {score}")
#             st.write("---")  # 문서 간 구분선

# https://medium.com/@adrirajchaudhuri/understanding-vector-search-using-qdrant-77a06c180e02
# Create Qdrant Client
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(
    url='http://localhost:6333', 
)

# client.create_collection(
client.recreate_collection(
    collection_name="my-collection",
    vectors_config=models.VectorParams(
      size=1536,
      distance=models.Distance.COSINE
    )
)

# Converting chunks into points which are central entity of Qdrant
# and putting them up on vector store

import uuid
from qdrant_client.http.models import PointStruct

# 기사 임베딩 하기
points = []
for idx,chunk in enumerate(chunks):
    embeddings = openai_embeddings.embed_query(chunk.page_content)
    # embeddings = response['data'][0]['embedding']
    point_id = str(uuid.uuid4())  # Generate a unique ID for the point

    print(f"POINT_ID = {point_id}")
    print(f"PAYLOAD = {chunk.page_content}")
    print(f"vetor length = {len(embeddings)}")
    points.append(PointStruct(id=point_id,payload={"text": chunk.page_content},vector=embeddings))

# 기사 백터에 넣기
client.upsert(
    collection_name="my-collection",
    wait=True,
    points=points
)

# 쿼리하기
query = "현대글로비스 물류 드림 캠프에 대해서 설명 해줘."
embeddings = openai_embeddings.embed_query(query)
# response = openai.Embedding.create(
#     input=query,
#     model="text-embedding-ada-002"
# )
# embeddings = response['data'][0]['embedding']
search_result = client.search(
    collection_name="my-collection",
    query_vector=embeddings,
    limit=3
)
prompt=""
for result in search_result:
    prompt += result.payload['text']
concatenated_string = " ".join([prompt,query])
# completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": concatenated_string}
#     ]
# )
# completion.choices[0].message.content

from langchain_openai import ChatOpenAI
from utils.app_config import AppConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatOpenAI(
    openai_api_key=conf.open_ai_key,
    model="gpt-4-turbo",
    temperature=0)

# prompt = ChatPromptTemplate.from_template(concatenated_string)

# chain = (
#     prompt
#     | llm
#     | StrOutputParser()
# )

# result = chain.invoke()

result = llm.invoke(concatenated_string)
print(f"\n\n\n질문 = {query}")
print(f"\n답변 = {result}")
st.write(f"\n\n\n질문 = {query}")
st.write(f"\n답변 = {result}")