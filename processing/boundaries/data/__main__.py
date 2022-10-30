from processing.boundaries.data import stats, merge
from processing.boundaries.data.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    stats.main()
    merge.main()
