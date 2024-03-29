from multiprocessing import Pool

import pandas as pd

from . import attributes, concat
from .utils import adm0_list, cwd, logging

logger = logging.getLogger(__name__)
boundaries = (
    cwd
    / "../../../../admin-boundaries/outputs/edge-matched/humanitarian/intl/adm4_polygons.xlsx"
)


def run_process(func, df1):
    results = []
    pool = Pool()
    for row in adm0_list:
        args = [row["id"], row["pop_lvl"], row, df1]
        result = pool.apply_async(func, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


if __name__ == "__main__":
    logger.info("starting")
    df1 = pd.read_excel(boundaries)
    run_process(attributes.main, df1)
    concat.main()
    attributes.cleanup()
