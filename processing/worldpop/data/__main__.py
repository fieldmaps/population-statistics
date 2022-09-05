from processing.worldpop.data import stats, outputs
from processing.worldpop.data.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    stats.main()
    outputs.main()
