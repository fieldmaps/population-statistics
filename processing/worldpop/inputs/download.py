import requests
from multiprocessing import Pool
from pathlib import Path
from .utils import logging, data_types, adm0_list

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / '../../../inputs/worldpop'


def run_process(funcs):
    results = []
    pool = Pool()
    for func in funcs:
        for row in adm0_list:
            args = [row['id'], row['iso_3']]
            result = pool.apply_async(func, args=args)
            results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


def get_tif(url, file, name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(data / file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info(name)


def get_tif_unconstrained(id, iso_3):
    url = f'https://data.worldpop.org/GIS/Population/Global_2000_2020/2020/{iso_3}/{id}_ppp_2020.tif'
    file = f'unconstrained/{id}_ppp_2020.tif'
    get_tif(url, file, f'unconstrained_{id}')


def get_tif_constrained(id, iso_3):
    url_1 = f'https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/BSGM/{iso_3}/{id}_ppp_2020_constrained.tif'
    url_2 = f'https://data.worldpop.org/GIS/Population/Global_2000_2020_Constrained/2020/maxar_v1/{iso_3}/{id}_ppp_2020_constrained.tif'
    file = f'constrained/{id}_ppp_2020_constrained.tif'
    for url in [url_1, url_2]:
        get_tif(url, file, f'constrained_{id}')


def main():
    for name in data_types:
        (data / name).mkdir(parents=True, exist_ok=True)
    funcs = [get_tif_unconstrained, get_tif_constrained]
    run_process(funcs)
    logger.info('finished')
