import requests
from multiprocessing import Pool
from pathlib import Path
from .utils import logging, adm0_list

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / '../../../inputs/worldpop'


def run_process():
    results = []
    pool = Pool()
    for row in adm0_list:
        args = [row['id'], row['iso_3']]
        result = pool.apply_async(get_tif, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


def get_tif(id, iso_3):
    url = f'https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/{iso_3}/{id}_ppp_2020.tif'
    file = f'unconstrained/{id}_ppp_2020.tif'
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(data / file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info(id)


def main():
    if not (data / 'unconstrained.tif').is_file():
        (data / 'unconstrained').mkdir(parents=True, exist_ok=True)
        run_process()
    logger.info('finished')
