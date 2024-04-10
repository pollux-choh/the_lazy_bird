import pytest
from unittest.mock import MagicMock
from pathlib import Path
from utils.resource_loader import DocLoader  # doc_loader.py 파일에서 DocLoader 클래스를 임포트
import base64

"""
DocLoader test

Author: choh@pollux.ai
Git: https://github.com/pollux-choh
Created: 2024-04-07
"""

base64_img:str = 'iVBORw0KGgoAAAANSUhEUgAAAAMAAAADCAIAAADZSiLoAAAAF0lEQVR4nGP8//8/AwMDAwMDEwMMIFgAVCQDAyJaISoAAAAASUVORK5CYII='

# 이미지 파일 읽기를 시뮬레이션하는 함수
def mock_read_bytes(self):
    if self.name == 'test.png':
        # Assuming the file is an image, return the base64 encoded bytes
        return base64.b64decode(base64_img)
    else:
        raise FileNotFoundError(f"No such file: '{self}'")

def mock_read_text(self, encoding=None):
    if self.name == "PYTEST.md":
        return '![Test Image](images/test.png "Alternate text")'
    if self.name == "PYTEST_NONE_EXPLAN_OPTIONS.md":
        return '![Test Image](images/test.png)'
    raise FileNotFoundError

@pytest.fixture
def doc_loader():
    # DocLoader 인스턴스를 'main' 콘텐츠 이름으로 초기화
    loader = DocLoader("main")
    return loader

def test_doc_loader_initialization(doc_loader):
    # 초기화 검사
    assert doc_loader.content_name == "main"
    assert doc_loader.doc_root_dir == Path.cwd() / 'doc'

def test_get_resource_path(doc_loader):
    # 문서 경로 생성 검사
    expected_path = Path.cwd() / 'doc' / 'main' / 'PYTEST.md'
    assert doc_loader._DocLoader__get_resource_path('main', 'PYTEST.md') == expected_path

def test_get_text_exist(monkeypatch, doc_loader):
    # Path.read_text 메소드를 mock_read_text로 목킹
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    # 실제 문서 내용이 예상과 일치하는지 검사
    content = doc_loader.get_text("PYTEST.md")
    assert content == '![Test Image](images/test.png "Alternate text")'
    
def test_get_txt_not_exist(monkeypatch, doc_loader):
    # Path.read_text 메소드를 mock_read_text로 목킹
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    # 존재하지 않는 파일 접근 시 예외 발생 검사
    with pytest.raises(FileNotFoundError):
        _ = doc_loader.get_text("nonexistent_file.md")

def test_get_txt(monkeypatch, doc_loader):
    # Mock the Path.read_text and Path.read_bytes methods
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    
    # 이후의 테스트를 작성해 줄것
    text = doc_loader.get_text("PYTEST.md")
    assert text == '![Test Image](images/test.png "Alternate text")'
    
def test_get_images(doc_loader):
    content = mock_read_text(Path("PYTEST.md"))
    imgs = doc_loader._get_images(content)
    
    # 이미지에 설명이 있는 경우
    assert imgs == [('![Test Image](images/test.png "Alternate text")', 'Test Image', 'images/test.png', '"Alternate text"')]

    # 이미지의 설명을 생략한 경우
    content_2 = mock_read_text(Path("PYTEST_NONE_EXPLAN_OPTIONS.md"))
    imgs_2 = doc_loader._get_images(content_2)
    assert imgs_2 == [('![Test Image](images/test.png)', 'Test Image', 'images/test.png', "")]
    
def test_convert_img_to_html(monkeypatch, doc_loader):
    monkeypatch.setattr(Path, "read_bytes", mock_read_bytes)
    html = doc_loader._convert_img_to_html(Path("images/test.png"), "Test Image")
    assert html == f'<img src="data:image/png;base64,{base64_img}" alt="Test Image" style="max-width: 100%;">'
    
def test_get_markdown(monkeypatch, doc_loader):
    # Mock the Path.read_text and Path.read_bytes methods
    monkeypatch.setattr(Path, "read_text", mock_read_text)
    monkeypatch.setattr(Path, "read_bytes", mock_read_bytes)

    # 항상 True를 반환하도록 Path.exists 메소드를 목킹합니다.
    monkeypatch.setattr(Path, "exists", lambda x: True)
    
    markdown = doc_loader.get_markdown("PYTEST.md")
    assert markdown == f'<img src="data:image/png;base64,{base64_img}" alt="Test Image" style="max-width: 100%;">'