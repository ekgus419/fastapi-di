import logging
import logging.config
from src.core.settings import settings
from src.config.sql_pretty_formatter import SQLPrettyFormatter

def configure_logging():
    formatter_name = "sql_pretty" if settings.LOG_SQL_PRETTY else "default"
    logging_config = {
        'version': 1,
        'formatters': {
            'sql_pretty': {
                '()': SQLPrettyFormatter,
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            },
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': formatter_name,
                'level': 'INFO'
            },
        },
        'loggers': {
            'sqlalchemy.engine': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False
            }
        }
    }
    logging.config.dictConfig(logging_config)
