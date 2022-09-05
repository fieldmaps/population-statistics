from processing.meta_fb.outputs import merge
from processing.meta_fb.outputs.utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    merge.main()
