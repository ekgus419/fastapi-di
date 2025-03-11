from functools import wraps
from sqlalchemy.orm import Session


def Transactional(func):
    """
    Spring의 @Transactional과 유사한 동작을 수행하는 데코레이터.
    - 새로운 세션을 생성하고, 예외 발생 시 rollback 처리
    - 정상적으로 실행되면 commit 후 세션 종료
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        from src.core.container import container  # 🔥 여기서 import하여 순환 참조 방지

        session: Session = container.db_session()  # 새로운 DB 세션 생성
        try:
            kwargs["db"] = session  # 세션을 인자로 전달
            result = func(*args, **kwargs)  # 서비스 메서드 실행
            session.commit()  # 정상 실행되면 commit
            return result
        except Exception as e:
            session.rollback()  # 예외 발생 시 rollback
            raise e
        finally:
            session.close()  # 세션 종료

    return wrapper
