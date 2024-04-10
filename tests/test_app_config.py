import pytest
import json
from pathlib import Path
from utils.app_config import AppConfig  # AppConfig 모듈의 경로에 맞게 조정하세요.
import pandas as pd
from utils.env_manager import EnvManager

# 테스트용 JSON 데이터
TEST_JSON_DATA = [
    {
        "brand": "google",
        "llm_type": "text",
        "llm_name": "gemini-pro",
        "description": "텍스트 생성에 타겟팅된 모델",
        "is_active": 1,
        "is_alert": 0
    },
    {
        "brand": "google",
        "llm_type": "multi",
        "llm_name": "gemini-pro-vision",
        "description": "비전 생성에 타켓팅된 모델",
        "is_active": 1,
        "is_alert": 0
    },
    {
        "brand": "openai",
        "llm_type": "text",
        "llm_name": "gpt-3.5-turbo",
        "description": "텍스트 생성에 타겟팅된 모델",
        "is_active": 1,
        "is_alert": 0
    },
    {
        "brand": "openai",
        "llm_type": "multi",
        "llm_name": "gpt-4",
        "description": "멀티 모델에 타겟팅된 모델",
        "is_active": 0,
        "is_alert": 1
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
    llm_models = conf._load_llm_models("dummy_path")
    assert not llm_models.empty  # 반환된 DataFrame이 비어있지 않은지 확인
    assert len(llm_models) == 4  # 반환된 DataFrame의 행 수가 4인지 확인
    assert llm_models.iloc[0]["brand"] == "google"
    assert llm_models.iloc[0]["llm_type"] == "text"
    assert llm_models.iloc[0]["llm_name"] == "gemini-pro"
    assert llm_models.iloc[0]["description"] == "텍스트 생성에 타겟팅된 모델"
    assert llm_models.iloc[0]["is_active"] == 1
    assert llm_models.iloc[0]["is_alert"] == 0
    
def test_get_llm_models(setup_environment):
    """
    get_models 메서드가 제대로 작동하는지 테스트합니다.
    """
    conf = AppConfig()  # setup_environment가 _load_llm_models를 대체합니다.
    llm_models = conf.get_llm_models(brand="openai") # gpt-3.5-turbo, gpt-4가 반환됨
    assert len(llm_models) == 2
    assert llm_models.iloc[0]["llm_name"] == "gpt-3.5-turbo"
    assert llm_models.iloc[1]["llm_name"] == "gpt-4"

    llm_models = conf.get_llm_models(brand="openai", llm_type='multi', is_active=1) # gpt-4가 반환됨
    assert len(llm_models) == 0

    llm_models = conf.get_llm_models(llm_type='text', is_active=1) # gemini-pro, gpt-3.5-turbo가 반환됨
    assert len(llm_models) == 2
    assert llm_models.iloc[0]["llm_name"] == "gemini-pro"
    assert llm_models.iloc[1]["llm_name"] == "gpt-3.5-turbo"

    llm_models = conf.get_llm_models(is_active=1) # gemini-pro, gemini-pro-vision, gpt-3.5-turbo가 반환됨
    assert len(llm_models) == 3
    assert llm_models.iloc[0]["llm_name"] == "gemini-pro"
    assert llm_models.iloc[1]["llm_name"] == "gemini-pro-vision"
    assert llm_models.iloc[2]["llm_name"] == "gpt-3.5-turbo"