import os
from typing import Dict
from dotenv import dotenv_values
from pathlib import Path

class EnvFileManager():
    """
    AppConfig is a class for management api keys.
    
    Attributes:
        env_file_path (str): envfile의 경로
        
    Author: choh@pollux.ai
    Created: 2024-04-08
    """
    
    # def __init__() -> None:

    @classmethod
    def get_list(cls, env_file_path: str) -> Dict[str, str]:
        """env 파일에 있는 dict를 반환합니다."""
        env_dict: Dict[str, str] = dotenv_values(env_file_path)
        return env_dict

    @classmethod
    def add(cls, env_file_path: str, param_name: str, value: str) -> None:
        """만약 중복된 값이 있다면 업데이트, 중복이 없다면 추가.
        변경 사항을 .env 파일에 저장합니다."""
        env_dict = cls.get_list(env_file_path)
        env_dict[param_name] = value
        cls.__save(cls, env_file_path, env_dict)

    @classmethod
    def remove(cls, env_file_path: str, param_name: str) -> None:
        """해당하는 env 값만을 제거 (값을 빈 문자열로 설정).
        변경 사항을 .env 파일에 저장합니다."""
        env_dict = cls.get_list(env_file_path)
        if param_name in env_dict.items():
            env_dict[param_name] = ""
            cls.__save(cls,env_file_path,env_dict)
        else:
            raise KeyError(f"{param_name} not found in the .env file")
        
    @classmethod
    def purge(cls, env_file_path: str, param_name: str) -> None:
        """해당하는 env 변수를 완전히 삭제.
        변경 사항을 .env 파일에 저장합니다."""
        env_dict = cls.get_list(env_file_path)
        if param_name in env_dict.items():
            del env_dict[param_name]
            cls.__save(cls, env_file_path, env_dict)
        else:
            raise KeyError(f"{param_name} not found in the .env file")
        
    def __save(self, env_file_path: str,  env_dict: Dict[str, str]) -> None:
        """내부적으로 사용되는 함수로, 현재 환경 변수의 dict를 .env 파일에 저장합니다."""
        with open(env_file_path, 'w') as env_file:
            for key, value in env_dict.items():
                env_file.write(f"{key}={value}\n")

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    env_file_name = '.env'
    # os.path.join을 사용하여 파일 경로 조합
    env_full_path = os.path.join(str(base_dir), env_file_name)

    # ENV list 확인
    print(f"ENV LIST = {EnvFileManager.get_list(env_full_path)}")
    
    # 파라미터 추가
    EnvFileManager.add(env_full_path,'PARAM_4', 'ThisIsForthParam')
    print(f"ENV LIST = {EnvFileManager.get_list(env_full_path)}")

    # 파라미터 값만 제거
    EnvFileManager.remove(env_full_path,'PARAM_4')
    print(f"After remove PARAM_4 = {EnvFileManager.get_list(env_full_path)}")

    # 파라미터 완전히 삭제
    try:
        EnvFileManager.purge(env_full_path,'PARAM_5')  # 'PARAM_5'가 없으므로 예외가 발생합니다.
        print(f"ENV LIST = {EnvFileManager.get_list(env_full_path)}")
    except KeyError as e:
        print(e)
        
    # 다시 'PARAM_4'를 추가 후 완전 삭제를 시도해 보기
    EnvFileManager.add(env_full_path,'PARAM_4', 'ThisIsForthParam')
    EnvFileManager.purge(env_full_path,'PARAM_4')  # 'PARAM_4'를 완전히 삭제합니다.
    print(f"After purge PARAM_4 = {EnvFileManager.get_list(env_full_path)}")
    EnvFileManager.add(env_full_path,'A', 'ThisIsForthParamAAAAA')
    EnvFileManager.add(env_full_path,'B', 'ThisIsForthParamBBBBB')
    EnvFileManager.add(env_full_path,'C', 'ThisIsForthParamCCCCC')
    # env.purge('A')  # 'A'를 완전히 삭제합니다.
    # env.purge('B')
    # env.purge('C')
