from dotenv import load_dotenv,dotenv_values
from typing import Dict
from utils.singleton_meta import SingletonMeta
from utils.env_manager import EnvFileManager
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

    def __init__(self, 
                 open_ai_key: str = None,
                 gemini_key:str = None) -> None:
        
        # HACK - (2024.04.08, choh) 이부분이 pypi로 빌드했을때, 경로상에 문제가 생길 수 있음.
        #         OS 별로도 검증이 필요함
        self.base_dir = Path(__file__).resolve().parent.parent
        self.env_file = f"{self.base_dir}/.env"
        # self.env_manager = EnvFileManager(str(self.base_dir))
        # .env 파일을 읽고 dict로 저장  
        self.env_dict: Dict[str, str] = dotenv_values(self.env_file)
        
        self.open_ai_key = open_ai_key
    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """
        
        
        
if __name__ == "__main__":
    config = AppConfig()
    
    print("HELLOW")
    print(f"BASE_DIR = {config.base_dir}")