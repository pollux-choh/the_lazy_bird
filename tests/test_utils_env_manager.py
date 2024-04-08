import os
import tempfile
import pytest
from utils.env_manager import EnvManager  # 경로가 변경되었을 수 있으니 확인이 필요

"""
EnvFileManager test

Author: choh@pollux.ai
Created: 2024-04-07
"""

@pytest.fixture
def temp_env_file():
    """임시 .env 파일을 생성하고 파일 경로를 반환합니다."""
    content = "PARAM_1=Value1\nPARAM_2=Value2\n"
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(content)
        temp_file.flush()
        yield temp_file.name
    os.unlink(temp_file.name)

def test_get_list(temp_env_file):
    """EnvFileManager 클래스의 get_list 메서드를 테스트합니다."""
    env_list = EnvManager.get_list(temp_env_file)
    assert len(env_list) == 2
    assert env_list['PARAM_1'] == 'Value1'
    assert env_list['PARAM_2'] == 'Value2'

def test_add(temp_env_file):
    """EnvFileManager 클래스의 add 메서드를 테스트합니다."""
    EnvManager.add(temp_env_file, 'PARAM_3', 'Value3')
    env_list = EnvManager.get_list(temp_env_file)
    assert len(env_list) == 3
    assert env_list['PARAM_3'] == 'Value3'

def test_remove(temp_env_file):
    """EnvFileManager 클래스의 remove 메서드를 테스트합니다."""
    EnvManager.remove(temp_env_file, 'PARAM_1')
    env_list = EnvManager.get_list(temp_env_file)
    assert len(env_list) == 2  # 'PARAM_1' 값을 빈 문자열로 설정 후에도 여전히 2개의 키가 남아 있어야 합니다.
    assert env_list['PARAM_1'] == ''  # 'PARAM_1'의 값이 빈 문자열인지 확인합니다.

def test_purge(temp_env_file):
    """EnvFileManager 클래스의 purge 메서드를 테스트합니다."""
    EnvManager.purge(temp_env_file, 'PARAM_1')
    env_list = EnvManager.get_list(temp_env_file)
    assert len(env_list) == 1
    assert 'PARAM_1' not in env_list

def test_purge_nonexistent_param(temp_env_file):
    """존재하지 않는 환경 변수를 purge하는 경우에 대한 테스트입니다."""
    with pytest.raises(KeyError):
        EnvManager.purge(temp_env_file, 'PARAM_NONEXISTENT')

def test_add_and_purge(temp_env_file):
    """새로운 환경 변수를 추가하고 purge하는 경우에 대한 테스트입니다."""
    EnvManager.add(temp_env_file, 'PARAM_3', 'Value3')
    EnvManager.purge(temp_env_file, 'PARAM_3')
    env_list = EnvManager.get_list(temp_env_file)
    assert len(env_list) == 2
    assert 'PARAM_3' not in env_list
