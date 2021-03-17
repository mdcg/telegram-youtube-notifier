import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        fmt="[server] %(asctime)s - %(levelname)s : %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
    )
)
logger.addHandler(handler)
