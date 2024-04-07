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
    
    def get_doc(self, file_name: str) -> str:
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
        except FileNotFoundError:
            raise FileNotFoundError(f"The file '{file_name}' does not exist in '{self.doc_root_dir}\{self.content_name}'.")
        except Exception as e:
            raise Exception(f"An error occurred while trying to read the file: {e}")
