from multiprocessing import Pool
from . import download, merge, inputs, stats, outputs
from .utils import logging, data_types

logger = logging.getLogger(__name__)


def run_process(func):
    results = []
    pool = Pool()
    for name in data_types:
        args = [name]
        result = pool.apply_async(func, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


if __name__ == '__main__':
    logger.info('starting')
    # download.main()
    # merge.main()
    # run_process(inputs.main)
    # run_process(stats.main)
    outputs.main()
