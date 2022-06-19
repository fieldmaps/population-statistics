import subprocess
from .utils import logging, cwd, run_process

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/meta_fb'


def build_vrt(name):
    subprocess.run([
        'gdalbuildvrt',
        '-q',
        data / f'hrsl_{name}/hrsl_{name}-latest.vrt',
        *sorted((data / f'hrsl_{name}').rglob('*.tif')),
    ])


def merge_data(name):
    (data / f'hrsl_{name}/v1').mkdir(parents=True, exist_ok=True)
    (data / f'hrsl_{name}/v1.5').mkdir(parents=True, exist_ok=True)
    for file in sorted((data / f'hrsl_{name}_original').rglob('*.tif*')):
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
            file,
            str(file).replace(f'/hrsl_{name}_original/', f'/hrsl_{name}/'),
        ])
        logger.info(file.name)
    build_vrt(name)
    logger.info(name)


def main():
    run_process(merge_data)
    logger.info('finished')
