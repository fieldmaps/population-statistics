import shutil
from .utils import cwd, logging, data_types

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/meta_fb'


def main():
    for name in data_types:
        shutil.rmtree(data / f'hrsl_{name}_original', ignore_errors=True)
    logger.info('finished')
