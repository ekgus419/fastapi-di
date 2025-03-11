from datetime import datetime, timezone, timedelta

class TimeProvider:
    """
    시간 관련 기능을 제공하는 유틸리티 클래스
    """

    @staticmethod
    def get_utc_now() -> datetime:
        """ 현재 UTC 시간을 반환 (timezone-aware datetime) """
        return datetime.now(timezone.utc)

    @staticmethod
    def get_kst_now() -> datetime:
        """ 현재 한국 시간 (KST, UTC+9)을 반환 """
        return datetime.now(timezone.utc) + timedelta(hours=9)

    @staticmethod
    def to_timestamp(dt: datetime) -> float:
        """ datetime 객체를 Unix Timestamp(초 단위)로 변환 """
        return dt.timestamp()
