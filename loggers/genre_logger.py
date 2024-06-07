import logging

genre_logger = logging.getLogger(__name__)
genre_logger.setLevel(logging.INFO)
genre_formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
genre_handler = logging.FileHandler(filename=f"loggers/{__name__}.log", mode="w", encoding='utf-8')

genre_handler.setFormatter(genre_formatter)
genre_logger.addHandler(genre_handler)