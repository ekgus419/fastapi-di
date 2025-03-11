from src.core.transaction import Transactional

class BaseService:
    """
    모든 서비스가 상속받는 기본 서비스 클래스.
    트랜잭션 데코레이터를 활용할 수 있음.
    """

    @staticmethod
    @Transactional
    def execute_transaction(func, *args, **kwargs):
        """
        개별적인 트랜잭션 실행을 위해 서비스에서 호출할 수 있는 메서드.
        """
        return func(*args, **kwargs)
