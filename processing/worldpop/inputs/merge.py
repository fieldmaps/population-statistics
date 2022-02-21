import subprocess
from multiprocessing import Pool
from .utils import logging, cwd, data_types

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/worldpop'


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


def merge_tif(name):
    if (data / name).is_dir():
        options = [
            'gdalwarp',
            # '-q',
            '-multi',
            '-overwrite',
            '-co', 'TILED=YES',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'ZLEVEL=9',
            '-co', 'NUM_THREADS=ALL_CPUS',
            '-wo', 'NUM_THREADS=ALL_CPUS',
            *sorted(list((data / f'{name}').resolve().rglob('*.tif'))),
            (data / f'{name}.tif').resolve(),
        ]
        if name == data_types[0]:
            options.extend(['-co', 'BIGTIFF=YES'])
        subprocess.run(options)
        logger.info(name)


def main():
    run_process(merge_tif)
