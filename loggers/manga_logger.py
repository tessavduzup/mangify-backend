import logging

manga_logger = logging.getLogger(__name__)
manga_logger.setLevel(logging.INFO)
manga_formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
manga_handler = logging.FileHandler(filename=f"loggers/{__name__}.log", mode="w", encoding='utf-8')

manga_handler.setFormatter(manga_formatter)
manga_logger.addHandler(manga_handler)