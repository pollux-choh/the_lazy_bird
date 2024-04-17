import os
import re
import base64
from pathlib import Path
from typing import Optional

class DocLoader:
    """
    DocLoader is a class for loading documents from a specified directory structure within the application.
    
    Attributes:
        base_dir (Path): The current working directory from where the script is executed.
        doc_root_dir (Path): The root directory where documents are stored.
        content_name (str): The name of the specific content directory under the document root.
        
    Author: choh@pollux.ai
    Git: https://github.com/pollux-choh
    Created: 2024-04-07
    """
    
    # NOTE - (2024.04.07,choh) 아래의 생성자는 python 3.9 이하의 호환을 위한 코드임
    #       향후 python 3.10 이상인 경우에는 주석 처리된 코드를 사용할 것
    #
    # Python 3.10 이상
    # def __init__(self, content_name: str, doc_dir: str | None = 'doc') -> None:
    #
    # Python 3.9 이하
    def __init__(self, content_name: str, doc_dir: Optional[str] = 'doc') -> None:
        """
        Initializes the DocLoader with a specific content name.
        
        Parameters:
            content_name (str): The name of the content directory to load documents from.
        """
        self.base_dir: Path = Path.cwd()  # Current working directory
        self.doc_root_dir: Path = self.base_dir / doc_dir  # Document root directory path
        self.content_name: str = content_name  # Name of the content directory
        self.content_dir:Path = self.doc_root_dir / content_name  # Full path to the content directory


    def __get_resource_path(self, content_name: str, file_name: str) -> Path:
        """
        Constructs the full path to a document based on its content name and file name.
        
        This is a private method intended for internal use to encapsulate the path construction logic.
        
        Parameters:
            content_name (str): The name of the content directory.
            file_name (str): The name of the file to be loaded.
            
        Returns:
            Path: The full path to the requested document.
        """
        return self.doc_root_dir / content_name / file_name


    def _get_images(self, markdown: str) -> list[tuple[str, str, str]]:
        """
        Extracts image information from markdown text.
        
        This method searches for markdown image syntax in the given markdown text and extracts the image titles and paths.
        
        Parameters:
            markdown (str): The markdown text to search for images.
        
        Returns:
            list of tuples: A list where each tuple contains image markdown, image title, and image path.
        """
        # example image markdown:
        # ![Test image](images/test.png "Alternate text")
        images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)

        return images


    def _convert_img_to_bytes(self, img_path: Path) -> str:
        """
        Converts an image file to its base64 encoded string.
        
        This method reads an image file from the given path, converts it into bytes, and then encodes it into a base64 string.
        
        Parameters:
            img_path (Path): The path to the image file.
        
        Returns:
            str: The base64 encoded string of the image.
        """
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        return encoded


    def _convert_img_to_html(self, img_path: Path, img_alt: str) -> str:
        """
        Generates an HTML <img> tag for the given image.
        
        This method takes the path and alternative text for an image, converts the image to a base64 encoded string, and then generates an HTML <img> tag with this image data.
        
        Parameters:
            img_path (Path): The path to the image file.
            img_alt (str): The alternative text for the image.
        
        Returns:
            str: An HTML <img> tag string containing the base64 encoded image.
        """
        img_format = img_path.suffix[1:]  # 파일 확장자 추출 ('.png' -> 'png')
        encoded_img = self._convert_img_to_bytes(img_path)  # 이미지를 바이트로 변환하고 base64로 인코딩
        #NOTE - (2024.04.10,choh) 이미지의 width를 임의로 100% 지정. 이후에 이를 인자로 받아들이도록 수정할 필요가 있음
        img_html = f'<img src="data:image/{img_format.lower()};base64,{encoded_img}" alt="{img_alt}" style="max-width: 100%;">' # 이미지 삽입 태그 생성
        
        return img_html


    def _convert_txt_to_markdown(self, markdown: str) -> str:
        """
        Converts markdown text containing image paths to markdown with embedded HTML <img> tags.
        
        This method processes a given markdown text, finds all image references, converts each image to an HTML <img> tag with a base64 encoded string, and replaces the original markdown image syntax with the HTML tag.
        
        Parameters:
            markdown (str): The original markdown text containing image paths.
        
        Returns:
            str: The modified markdown text with HTML <img> tags replacing markdown image syntax.
        """
        images = self._get_images(markdown)
        for image in images:
            image_markdown = image[0]
            image_alt = image[1]
            image_path = Path(self.content_dir / image[2])
            if image_path.exists():
                markdown = markdown.replace(image_markdown, self._convert_img_to_html(image_path, image_alt))
        
        return markdown


    def get_text(self, file_name: str) -> str:
        """
        Loads and returns the content of a specified document.
        
        This method tries to open and read the content of a file located under the
        specified content directory. If the file cannot be found or another error occurs,
        the method raises an appropriate exception.
        
        Parameters:
            file_name (str): The name of the file to be loaded.
            
        Returns:
            str: The text content of the file.
            
        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: If an error occurs while trying to read the file.
        """
        resource_path = self.__get_resource_path(self.content_name, file_name)
        try:
            return resource_path.read_text(encoding='UTF-8')  # Attempt to read the file content
        except FileNotFoundError as e:
            file_path = Path(self.doc_root_dir) / self.content_name
            raise FileNotFoundError(f"The file '{file_name}' does not exist in '{file_path})'.") from e
        except Exception as e:
            raise Exception(f"An error occurred while trying to read the file: {e}") from e


    def get_markdown(self, file_name: str) -> str:
        """
        Loads and returns the content of a specified document with images converted to HTML <img> tags.
        
        This method reads the content of a specified markdown file, converts any image links in the markdown 
        to HTML <img> tags using base64 encoding, and returns the modified markdown content.
        
        Parameters:
            file_name (str): The name of the markdown file to be loaded.
            
        Returns:
            str: The markdown content of the file with image paths replaced by HTML <img> tags.
            
        Raises:
            FileNotFoundError: If the specified file does not exist.
            Exception: If an error occurs while trying to read the file.
        """
        text = self.get_text(file_name)
        markdown = self._convert_txt_to_markdown(text)
        return markdown
