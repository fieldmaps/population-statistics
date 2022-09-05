from processing.worldpop.outputs import merge
from processing.worldpop.outputs.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    merge.main()
