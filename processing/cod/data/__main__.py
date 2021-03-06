from multiprocessing import Pool
from . import attributes, concat
from .utils import logging, adm0_list

logger = logging.getLogger(__name__)


def read_csv():
    results = []
    pool = Pool()
    for row in adm0_list:
        args = [row['id'], row['ps_lvl'], row]
        result = pool.apply_async(attributes.main, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


if __name__ == '__main__':
    logger.info('starting')
    read_csv()
    concat.main()
