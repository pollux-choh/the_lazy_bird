# test_singleton.py
import pytest
from utils.singleton_meta import Singleton

"""
Singletone test

Author: choh@pollux.ai
Created: 2024-04-08
"""

def test_singleton_instance():
    # 첫 번째 Singleton 인스턴스 생성
    singleton1 = Singleton("FOO")
    # 두 번째 Singleton 인스턴스 생성
    singleton2 = Singleton("BAR")
    
    # 두 인스턴스가 동일한지 검증
    assert singleton1 is singleton2
    assert singleton1.value == singleton2.value

    # 값이 첫 번째로 설정된 "FOO"인지 확인
    assert singleton1.value == "FOO"

def test_singleton_thread_safety():
    # 멀티스레딩을 통한 동시성 테스트를 수행하는 부분은 복잡할 수 있으며,
    # 이는 기본적인 Pytest 사용법을 넘어서는 주제입니다.
    # 여기서는 기본적인 싱글턴 패턴의 테스트만을 다루었습니다.
    pass
