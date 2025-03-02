import logging
from typing import Callable

class BaseService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def run_in_transaction(self, func: Callable, *args, **kwargs):
        """
        트랜잭션 처리 로직을 시뮬레이션하는 메서드 (실제 DB 세션 관리 등).
        예: func 내부에서 예외 발생 시 롤백, 성공 시 커밋.
        """
        self.logger.info(f"[TX-START] {func.__name__}")
        try:
            result = func(*args, **kwargs)
            # 여기서 DB commit 로직 등
            self.logger.info(f"[TX-COMMIT] {func.__name__}")
            return result
        except Exception as e:
            self.logger.error(f"[TX-ROLLBACK] {func.__name__}, error={str(e)}")
            # 여기서 DB rollback 로직 등
            raise e

    def log_method_call(self, method_name: str, *args, **kwargs):
        """
        단순 로깅 예시 메서드. 호출되는 메서드명을 로깅할 수 있음.
        """
        self.logger.info(f"Method: {method_name}, args={args}, kwargs={kwargs}")