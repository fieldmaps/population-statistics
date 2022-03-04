import subprocess
from multiprocessing import Pool
from .utils import logging, cwd, data_types

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/meta_fb'


def run_process(files):
    results = []
    pool = Pool()
    for file in files:
        args = [file]
        result = pool.apply_async(merge_tif, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


def merge_tif(file):
    files = [str(file).replace('_general', f'_{dt}') for dt in data_types]
    vrt = data / file.name.replace('.tif', '.vrt')
    output = str(file).replace('_general', '')
    subprocess.run([
        'gdalbuildvrt',
        '-q',
        '-separate',
        vrt,
        *files,
    ])
    subprocess.run([
        'gdal_translate',
        '-q',
        '--config', 'GDAL_NUM_THREADS', 'ALL_CPUS',
        '-co', 'TILED=YES',
        '-co', 'BLOCKXSIZE=512',
        '-co', 'BLOCKYSIZE=512',
        '-co', 'COMPRESS=DEFLATE',
        '-co', 'ZLEVEL=9',
        '-ot', 'Float32',
        vrt,
        output,
    ])
    vrt.unlink(missing_ok=True)
    logger.info(file.name)


def build_vrt():
    subprocess.run([
        'gdalbuildvrt',
        '-q',
        data / 'hrsl/hrsl-latest.vrt',
        *sorted((data / 'hrsl').rglob('*.tif')),
    ])


def main():
    (data / 'hrsl/v1').mkdir(parents=True, exist_ok=True)
    (data / 'hrsl/v1.5').mkdir(parents=True, exist_ok=True)
    files = sorted((data / 'hrsl_general').resolve().rglob('*.tif'))
    for file in files:
        merge_tif(file)
    # run_process(files)
    build_vrt()
    logger.info('finished')
