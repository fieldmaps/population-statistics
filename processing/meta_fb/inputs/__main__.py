from . import download, inputs, merge, cleanup
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    download.main()
    merge.main()
    cleanup.main()
    inputs.main()
