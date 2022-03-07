from . import tile, cleanup, inputs
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    tile.main()
    cleanup.main()
    inputs.main()
