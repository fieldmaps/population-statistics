import subprocess
from multiprocessing import Pool

import httpx

from .utils import YEAR, adm0_list, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / "../../../inputs/worldpop"


def run_process():
    results = []
    pool = Pool()
    for row in adm0_list:
        args = [row["id"]]
        result = pool.apply_async(get_tif, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


def get_tif(id):
    url = f"https://data.worldpop.org/GIS/Population/Global_2000_{YEAR}/{YEAR}/{id.upper()}/{id}_ppp_{YEAR}.tif"
    file = f"unconstrained/{id}_ppp_{YEAR}.tif"
    with httpx.Client(http2=True) as client:
        with client.stream("GET", url) as r:
            with open(data / file, "wb") as f:
                for chunk in r.iter_raw():
                    f.write(chunk)
    logger.info(id)


def build_vrt():
    subprocess.run(
        [
            "gdalbuildvrt",
            "-q",
            data / "unconstrained.vrt",
            *sorted((data / "unconstrained").rglob("*.tif")),
        ]
    )


def main():
    if not (data / f"ppp_{YEAR}_unconstrained.tif").is_file():
        (data / "unconstrained").mkdir(parents=True, exist_ok=True)
        run_process()
        build_vrt()
    logger.info("finished")
