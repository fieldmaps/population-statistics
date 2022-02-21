import subprocess
from .utils import DATABASE, FILE_NAME, logging, cwd

logger = logging.getLogger(__name__)
inputs = cwd / f'../../../inputs/ciesin'


def main():
    subprocess.run(' '.join([
        'raster2pgsql',
        '-d', '-r', '-C', '-I', '-Y',
        '-t', '256x256',
        str((inputs / f'{FILE_NAME}_tiled.tif').resolve()),
        'ciesin_pop',
        '|',
        'psql',
        '--quiet',
        '-d', DATABASE,
    ]), shell=True)
    logger.info(f'finished')
