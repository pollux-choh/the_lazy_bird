import os
from dotenv import load_dotenv,dotenv_values
from typing import Dict
from utils.singleton_meta import SingletonMeta
from utils.env_manager import EnvManager
from pathlib import Path

class AppConfig(metaclass=SingletonMeta):
    """
    AppConfig is a class for management api keys.
    
    Attributes:
        open_ai_key (str): 오픈 API 키
        doc_root_dir (Path): The root directory where documents are stored.
        content_name (str): The name of the specific content directory under the document root.
        
    Author: choh@pollux.ai
    Created: 2024-04-08
    """
    value: str = None # singleton을 위한 변수

    def __init__(self) -> None:
        # HACK - (2024.04.08, choh) 이부분이 pypi로 빌드했을때, 경로상에 문제가 생길 수 있음.
        #         OS 별로도 검증이 필요함
        self.base_dir = Path(__file__).resolve().parent.parent
        self.env_file = f"{self.base_dir}/.env"
        
        # 환경 변수를 load
        load_dotenv(self.env_file)
        # print(self.env_file)
        self.__set_env_values()

    # 환경 변수를 설정
    def __set_env_values(self):
        self.open_ai_key = os.getenv("OPENAI_API_KEY")
        self.google_ai_key = os.getenv("GOOGLE_API_KEY")
        self.google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
    def env_add(self, param_name:str, value:str):
        EnvManager.add(self.env_file, param_name, value)
        load_dotenv(self.env_file, override=True)
        self.__set_env_values()

    def env_remove(self, param_name:str):
        EnvManager.remove(self.env_file, param_name)
        load_dotenv(self.env_file, override=True)
        self.__set_env_values()
        
        
if __name__ == "__main__":
    config = AppConfig()
    
    print("HELLOW")
    print(f"BASE_DIR = {config.base_dir}")