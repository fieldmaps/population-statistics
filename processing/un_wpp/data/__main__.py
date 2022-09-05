from processing.un_wpp.data import inputs
from processing.un_wpp.data.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    inputs.main()
