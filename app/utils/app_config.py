import os
from dotenv import load_dotenv,dotenv_values
from typing import Dict
from utils.singleton_meta import SingletonMeta
from utils.env_manager import EnvManager
from pathlib import Path
from pydantic import BaseModel, ValidationError
import pandas as pd
import json

# 데이터 모델 정의
class LLMModel(BaseModel):
    brand: str
    llm_type: str
    llm_name: str
    description: str
    is_active: int
    is_alert: int
    
class AppConfig(metaclass=SingletonMeta):
    """
    AppConfig is a class for management api keys.
    
    Attributes:
        open_ai_key (str): 오픈 API 키
        doc_root_dir (Path): The root directory where documents are stored.
        content_name (str): The name of the specific content directory under the document root.
        
    Author: choh@pollux.ai
    Git: https://github.com/pollux-choh
    Created: 2024-04-08
    """
    _instance: str = None # singleton을 위한 변수

    def __init__(self) -> None:
        self.initialized = True
        
        # HACK - (2024.04.08, choh) 이부분이 pypi로 빌드했을때, 경로상에 문제가 생길 수 있음.
        #         OS 별로도 검증이 필요함
        # 기본 폴더
        self.base_dir:Path  = Path(__file__).resolve().parent.parent
        
        # .env 파일
        self.env_file:Path = self.base_dir / ".env"
        
        # credentials 파일들이 보관될 폴더
        self.secure_dir:Path  = self.base_dir / "secure"
        
        
        # secure directory가 없으면 생성
        self.__init_secure_dir(self.secure_dir)
        
        # 환경 변수를 load
        load_dotenv(self.env_file)
        
        # 환경변수중에 필요한 정보를 Appconfig 생성
        self.__set_env_values()
        
        # google crendential을 load
        self.__check_and_update_google_credentials()
        
        # llm 모델 정보들을 load
        self.llm_file:Path = self.base_dir / "doc" / "config" / "llm_model.json"
        self.llm_models = self._load_llm_models(self.llm_file)

        
    # secure directory가 없으면 생성
    def __init_secure_dir(self, path:Path) -> None:
        if not os.path.exists(path):
            os.makedirs(path)


    # 환경 변수를 설정
    def __set_env_values(self) -> None:
        # OpenAI API key
        self.open_ai_key = os.getenv("OPENAI_API_KEY")
        
        # Google Gemini API Key
        self.google_ai_key = os.getenv("GOOGLE_API_KEY")
        
        # google authentication 관련
        self.google_credentials:Path = self.secure_dir / "google_credentials.json"
        
    def is_credentials_exist(self,credential_path:Path) -> bool:
        return credential_path.exists()
    
    # credentials 파일이 존재하면, 환경 변수에 추가
    def __check_and_update_google_credentials(self) -> None:
        if self.is_credentials_exist(self.google_credentials):
            self.env_key_add("GOOGLE_APPLICATION_CREDENTIALS", self.google_credentials)
    
    # api key를 추가
    def env_key_add(self, param_name:str, value:str) -> None:
        EnvManager.add(self.env_file, param_name, value)
        load_dotenv(self.env_file, override=True)
        self.__set_env_values()

    # api key를 제거
    def env_key_remove(self, param_name:str) -> None:
        EnvManager.remove(self.env_file, param_name)
        load_dotenv(self.env_file, override=True)
        self.__set_env_values()

    # JSON 파일을 로드하고 데이터 검사
    def _load_llm_models(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        try:
            validated_data = [LLMModel(**item) for item in data]
        except ValidationError as e:
            print(f"Invalid data: {e}")
            return None
        
        # bool 형식의 열을 정수로 변환
        for item in validated_data:
            item.is_active = int(item.is_active)
            item.is_alert = int(item.is_alert)
        
        return pd.DataFrame([item.model_dump() for item in validated_data])

    def get_llm_models(self, **kwargs):
        """
        다양한 조건으로 LLM 모델을 필터링하여 반환합니다.
        가능한 필터링 조건: brand, llm_type, is_active 등
        :return: 필터링된 LLM 모델 DataFrame
        """
        query_conditions = ' and '.join([f"{k} == @{k}" for k in kwargs])
        if query_conditions:
            filtered_models = self.llm_models.query(query_conditions, local_dict=kwargs)
            return filtered_models
        else:
            return self.llm_models


if __name__ == "__main__":
    config = AppConfig()

    print("HELLOW")
    print(f"BASE_DIR = {config.base_dir}")