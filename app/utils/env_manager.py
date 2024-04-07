import os
from typing import Dict
from dotenv import dotenv_values
from pathlib import Path

class EnvFileManager:
    def __init__(self, env_file_path: str):
        self.env_file_path: str = env_file_path
        # .env 파일을 읽고 dict로 저장
        self.env_dict: Dict[str, str] = dotenv_values(env_file_path)

    def get_list(self) -> Dict[str, str]:
        """env 파일에 있는 dict를 반환합니다."""
        return self.env_dict

    def add(self, param_name: str, value: str) -> None:
        """만약 중복된 값이 있다면 업데이트, 중복이 없다면 추가.
        변경 사항을 .env 파일에 저장합니다."""
        self.env_dict[param_name] = value
        self._save()

    def remove(self, param_name: str) -> None:
        """해당하는 env 값만을 제거 (값을 빈 문자열로 설정).
        변경 사항을 .env 파일에 저장합니다."""
        if param_name in self.env_dict:
            self.env_dict[param_name] = ""
            self._save()
        else:
            raise KeyError(f"{param_name} not found in the .env file")

    def purge(self, param_name: str) -> None:
        """해당하는 env 변수를 완전히 삭제.
        변경 사항을 .env 파일에 저장합니다."""
        if param_name in self.env_dict:
            del self.env_dict[param_name]
            self._save()
        else:
            raise KeyError(f"{param_name} not found in the .env file")

    def _save(self) -> None:
        """내부적으로 사용되는 함수로, 현재 환경 변수의 dict를 .env 파일에 저장합니다."""
        with open(self.env_file_path, 'w') as env_file:
            for key, value in self.env_dict.items():
                env_file.write(f"{key}={value}\n")

if __name__ == "__main__":
    base_dir = Path(__file__).parent
    env_file_name = '.env'
    # os.path.join을 사용하여 파일 경로 조합
    env_full_path = os.path.join(str(base_dir), env_file_name)
    env = EnvFileManager(env_full_path)

    # ENV list 확인
    print(f"ENV LIST = {env.get_list()}")
    
    # 파라미터 추가
    env.add('PARAM_4', 'ThisIsForthParam')
    print(f"ENV LIST = {env.get_list()}")

    # 파라미터 값만 제거
    env.remove('PARAM_4')
    print(f"After remove PARAM_4 = {env.get_list()}")

    # 파라미터 완전히 삭제
    try:
        env.purge('PARAM_5')  # 'PARAM_5'가 없으므로 예외가 발생합니다.
        print(f"ENV LIST = {env.get_list()}")
    except KeyError as e:
        print(e)
        
    # 다시 'PARAM_4'를 추가 후 완전 삭제를 시도해 보기
    env.add('PARAM_4', 'ThisIsForthParam')
    env.purge('PARAM_4')  # 'PARAM_4'를 완전히 삭제합니다.
    print(f"After purge PARAM_4 = {env.get_list()}")
    env.add('A', 'ThisIsForthParamAAAAA')
    env.add('B', 'ThisIsForthParamBBBBB')
    env.add('C', 'ThisIsForthParamCCCCC')
    # env.purge('A')  # 'A'를 완전히 삭제합니다.
    # env.purge('B')
    # env.purge('C')
