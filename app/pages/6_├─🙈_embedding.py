from openai import OpenAI
from utils.app_config import AppConfig

conf = AppConfig()

client = OpenAI(
    api_key=conf.open_ai_key
)

document = ['백터','데이터베이스는','말','그대로','백터를','저장하는','저장소입니다.']

response = client.embeddings.create(
    input = document,
    # open ai에서 제공하는 임베딩 모델
    model="text-embedding-ada-002"
)
response