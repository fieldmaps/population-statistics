from processing.un_wpp.inputs import download
from processing.un_wpp.inputs.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    download.main()
