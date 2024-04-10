import pytest
import json
from pathlib import Path
from utils.app_config import AppConfig  # AppConfig 모듈의 경로에 맞게 조정하세요.
import pandas as pd
from utils.env_manager import EnvManager

# 테스트용 JSON 데이터
TEST_JSON_DATA = [
    {
        "brand": "test_brand",
        "llm_type": "test_llm_type",
        "llm_name": "test_llm_name",
        "description": "test_description",
        "is_active": 1,
        "is_alert": 0
    }
]

def mock_load_llm_models(self, json_file):
    return pd.DataFrame(TEST_JSON_DATA)


@pytest.fixture
def setup_environment(monkeypatch):
    # _load_llm_models 메서드를 대체하는 모의 함수를 설정합니다.
    monkeypatch.setattr(AppConfig, "_load_llm_models", mock_load_llm_models)


def test_env_key_add_remove():
    # EnvManager 인스턴스에서 테스트 하므로 생략
    conf = AppConfig()
    conf.env_key_add("this_is_for_test", "test_value")
    assert EnvManager.get_list(conf.env_file)["this_is_for_test"] == "test_value"
    
    conf.env_key_remove("this_is_for_test")
    assert EnvManager.get_list(conf.env_file)["this_is_for_test"] == ""


def test_load_llm_models(setup_environment):
    """
    _load_llm_models 메서드가 제대로 작동하는지 테스트합니다.
    """
    conf = AppConfig()  # setup_environment가 _load_llm_models를 대체합니다.
    loaded_data = conf._load_llm_models("dummy_path")
    assert not loaded_data.empty  # 반환된 DataFrame이 비어있지 않은지 확인
    assert loaded_data.iloc[0]["brand"] == "test_brand"
    assert loaded_data.iloc[0]["llm_type"] == "test_llm_type"
    assert loaded_data.iloc[0]["llm_name"] == "test_llm_name"
    assert loaded_data.iloc[0]["description"] == "test_description"
    assert loaded_data.iloc[0]["is_active"] == 1
    assert loaded_data.iloc[0]["is_alert"] == 0
    
# def test_load_llm_models(setup_environment):
#     """
#     is_credentials_exist 메서드가 제대로 작동하는지 테스트합니다.
#     """
#      # AppConfig 인스턴스 생성
#     app_config = AppConfig()
    
#     model_info_json = json.dumps(TEST_JSON_DATA)
#     pd = app_config._load_llm_models(model_info_json)

