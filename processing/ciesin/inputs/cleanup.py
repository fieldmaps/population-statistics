from .utils import FILE_NAME, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/ciesin'


def main():
    (data / f'{FILE_NAME}.tif').unlink(missing_ok=True)
    logger.info('finished')
