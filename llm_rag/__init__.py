import os
import logging

LOGGING_FORMAT = str('%(levelname)s | %(message)s') # %(asctime)s

logger = logging.getLogger(__name__)
# Set the overall minimum logging level
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGGING_FORMAT)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

from llm_rag.rag import Rag

rag = Rag()