from processing.cod.outputs import merge
from processing.cod.outputs.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    merge.main()
