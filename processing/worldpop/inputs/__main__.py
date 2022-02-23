from . import download, merge, inputs, stats, outputs
from .utils import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info('starting')
    download.main()
    merge.main()
    inputs.main()
    stats.main()
    outputs.main()
