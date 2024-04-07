import os
import tempfile
import pytest
from app.utils.env_manager import EnvFileManager

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
    env = EnvFileManager(temp_env_file)
    env_list = env.get_list()
    assert len(env_list) == 2
    assert env_list['PARAM_1'] == 'Value1'
    assert env_list['PARAM_2'] == 'Value2'

def test_add(temp_env_file):
    """EnvFileManager 클래스의 add 메서드를 테스트합니다."""
    env = EnvFileManager(temp_env_file)
    env.add('PARAM_3', 'Value3')
    env_list = env.get_list()
    assert len(env_list) == 3
    assert env_list['PARAM_3'] == 'Value3'

def test_remove(temp_env_file):
    """EnvFileManager 클래스의 remove 메서드를 테스트합니다."""
    env = EnvFileManager(temp_env_file)
    env.remove('PARAM_1')
    env_list = env.get_list()
    assert len(env_list) == 2  # 환경 변수 'PARAM_1'이 아닌 'PARAM_2'만 남아있어야 합니다.
    assert env_list['PARAM_1'] == ''  # 'PARAM_1'의 값은 빈 문자열이어야 합니다.
    assert env_list['PARAM_2'] == 'Value2'  # 'PARAM_2'는 값이 변경되지 않았어야 합니다.

def test_purge(temp_env_file):
    """EnvFileManager 클래스의 purge 메서드를 테스트합니다."""
    env = EnvFileManager(temp_env_file)
    env.purge('PARAM_1')
    env_list = env.get_list()
    assert len(env_list) == 1
    assert 'PARAM_1' not in env_list

def test_purge_nonexistent_param(temp_env_file):
    """존재하지 않는 환경 변수를 purge하는 경우에 대한 테스트입니다."""
    env = EnvFileManager(temp_env_file)
    with pytest.raises(KeyError):
        env.purge('PARAM_NONEXISTENT')

def test_add_and_purge(temp_env_file):
    """새로운 환경 변수를 추가하고 purge하는 경우에 대한 테스트입니다."""
    env = EnvFileManager(temp_env_file)
    env.add('PARAM_3', 'Value3')
    env.purge('PARAM_3')
    env_list = env.get_list()
    assert len(env_list) == 2
    assert 'PARAM_3' not in env_list
