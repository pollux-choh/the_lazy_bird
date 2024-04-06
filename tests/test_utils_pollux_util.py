import pytest
from unittest.mock import MagicMock
from pathlib import Path
from utils.pollux_util import DocLoader  # doc_loader.py 파일에서 DocLoader 클래스를 임포트

# 목(mock) 함수를 정의하여 실제 파일 시스템 읽기를 시뮬레이션
def mock_read_text(self, encoding=None):
    if self.name == "main_notice.md":
        return "Test document content."
    raise FileNotFoundError

@pytest.fixture
def doc_loader():
    # DocLoader 인스턴스를 'main' 콘텐츠 이름으로 초기화
    loader = DocLoader("main")
    return loader

def test_doc_loader_initialization(doc_loader):
    # 초기화 검사
    assert doc_loader.content_name == "main"
    assert doc_loader.doc_root_dir == Path.cwd() / 'app' / 'doc'

def test_get_resource_path(doc_loader):
    # 문서 경로 생성 검사
    expected_path = Path.cwd() / 'app' / 'doc' / 'main' / 'main_notice.md'
    assert doc_loader._DocLoader__get_resource_path('main', 'main_notice.md') == expected_path

def test_get_doc_exist(monkeypatch, doc_loader):
    # Path.read_text 메소드를 mock_read_text로 목킹
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    
    # 실제 문서 내용이 예상과 일치하는지 검사
    content = doc_loader.get_doc("main_notice.md")
    assert content == "Test document content."

def test_get_doc_not_exist(monkeypatch, doc_loader):
    # Path.read_text 메소드를 mock_read_text로 목킹
    monkeypatch.setattr(Path, "read_text", mock_read_text)

    # 존재하지 않는 파일 접근 시 예외 발생 검사
    with pytest.raises(FileNotFoundError):
        _ = doc_loader.get_doc("nonexistent_file.md")
