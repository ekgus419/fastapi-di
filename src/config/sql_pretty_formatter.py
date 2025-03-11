import logging
import sqlparse

class SQLPrettyFormatter(logging.Formatter):
    def format(self, record):
        message = record.getMessage().strip()
        # 쿼리문으로 보이는 경우 (SELECT, INSERT, UPDATE, DELETE 등)
        if message.upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
            try:
                message = sqlparse.format(message, reindent=True, keyword_case='upper')
            except Exception:
                pass
            record.msg = message
        return super().format(record)
