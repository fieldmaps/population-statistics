from processing.meta_fb.inputs import download, inputs
from processing.meta_fb.inputs.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    download.main()
    inputs.main()
