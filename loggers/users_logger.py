import logging

users_logger = logging.getLogger(__name__)
users_logger.setLevel(logging.INFO)
users_formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
users_handler = logging.FileHandler(filename=f"loggers/{__name__}.log", mode="w", encoding='utf-8')

users_handler.setFormatter(users_formatter)
users_logger.addHandler(users_handler)
