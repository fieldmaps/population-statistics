from processing.meta import pop
from processing.meta.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    pop.main('population')
    logger.info('finished')
