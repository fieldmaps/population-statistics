from . import download, merge, inputs
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    # download.main()
    # merge.main()
    inputs.main()
