import logging

def setup_logging() -> None:
    handlers = [ logging.StreamHandler(), logging.FileHandler("logs/pipeline.log") ]
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s", handlers=handlers)