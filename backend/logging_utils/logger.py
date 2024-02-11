import logging
from logging.handlers import SysLogHandler
from logging_utils.database_handler import DatabaseLogHandler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import os

import datetime

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(
            f"Request: {request.method} {request.url} | Headers: {request.headers}")
        response = await call_next(request)
        logger.info(
            f"Response: {response.status_code} | Headers: {response.headers}")
        return response


def log_processed_data(file_name, option, result):
    logger = setup_logger(file_name)
    logger.info(f"Processed file: {file_name} using option: {option}")
    logger.info(f"Processed data result: {result}")


def setup_logger(file_name):
    # Ensure the logs directory exists
    # LOGS_DIR = "logs"
    # os.makedirs(LOGS_DIR, exist_ok=True)

    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H_%M_%S')

    data_logger = logging.getLogger(f"data_logger_{file_name}")
    data_logger.setLevel(logging.INFO)

    # File handler to write logs to the logs directory
    base_file_path = os.path.join(
        LOGS_DIR, f"{file_name}_{formatted_datetime}.log")

    # Check if the file already exists and append an incrementing number if it does
    counter = 1
    while os.path.exists(base_file_path):
        base_file_path = os.path.join(
            LOGS_DIR, f"{file_name}_{formatted_datetime}_{counter}.log")
        counter += 1

    file_handler = logging.FileHandler(base_file_path)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not data_logger.handlers:
        data_logger.addHandler(file_handler)

    # data_logger.addHandler(file_handler)

    # TODO: come back to this

    # SysLogHandler for persistent storage
    # SYSLOG_HOST = 'your_syslog_host_here'
    # SYSLOG_PORT = 'your_syslog_port_here'
    # syslog = SysLogHandler(address=(SYSLOG_HOST, SYSLOG_PORT))
    # syslog_formatter = logging.Formatter(f'{file_name}: %(levelname)s %(message)s')
    # syslog.setFormatter(syslog_formatter)
    # data_logger.addHandler(syslog)

    database_handler = DatabaseLogHandler()
    data_logger.addHandler(database_handler)

    return data_logger


class LogCollector:
    def __init__(self):
        self.messages = []

    def info(self, message):
        # You could add more information here, like timestamp, log level, etc.
        self.messages.append({'level': 'INFO', 'message': message})

    def warning(self, message):
        self.messages.append({'level': 'WARNING', 'message': message})

    def error(self, message):
        self.messages.append({'level': 'ERROR', 'message': message})

    # Add more methods if needed, e.g., debug, critical, etc.
