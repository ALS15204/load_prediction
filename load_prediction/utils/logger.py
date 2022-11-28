import logging
import os
from logging.config import dictConfig

ROTATING_FILE_HANDLER = "logging.handlers.RotatingFileHandler"
STREAM_HANDLER = "logging.StreamHandler"
DEFAULT_LEVEL = logging.INFO

FORMATTER_CONFIG = {
    "verbose": {
        "format": "[%(asctime)s] %(levelname)s %(processName)s %(name)s [%(filename)s:%(lineno)s] %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
}

HANDLER_CONFIG = {
    "file": {
        "class": ROTATING_FILE_HANDLER,
        "formatter": "verbose",
        "maxBytes": 10 * 1024 * 1024,  # 10 MB
        "backupCount": 3,
    },
    "console": {
        "class": STREAM_HANDLER,
        "formatter": "verbose",
        "stream": "ext://sys.stdout"
        , }
    , }


def setup_logger(logger_name: str, level=DEFAULT_LEVEL, log_file_dir: str = None, log_file_name: str = ""):
    console_handler = HANDLER_CONFIG["console"]
    console_handler["level"] = level

    handlers_cfg = {"console": {**HANDLER_CONFIG["console"], "level": level}}
    if log_file_dir is not None:
        prefix = log_file_name + "_" if log_file_name else ""
        handlers_cfg[f"file_{level}"] = {
            **HANDLER_CONFIG["file"],
            "level": level,
            "filename": os.path.join(log_file_dir, f"{prefix}{logging._levelToName[level]}.log")
        }

    cfg_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": FORMATTER_CONFIG,
        "handlers": handlers_cfg,
        "loggers": {logger_name: {"level": level, "handlers": handlers_cfg.keys()}},
    }
    dictConfig(cfg_dict)
    logger = logging.getLogger(logger_name)
    return logger
