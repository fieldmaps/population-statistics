from . import merge
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("starting")
    merge.main()
