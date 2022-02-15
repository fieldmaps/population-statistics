import subprocess
from .utils import DATABASE, logging, cwd

logger = logging.getLogger(__name__)
inputs = cwd / f'../../../inputs/ciesin'


def main():
    subprocess.run(' '.join([
        'raster2pgsql',
        '-d', '-r', '-C', '-I', '-Y',
        '-t', '256x256',
        str((inputs / 'gpw_v4_population_count_rev11_2020_30_sec.tif').resolve()),
        'ciesin_pop',
        '|',
        'psql',
        '--quiet',
        '-d', DATABASE,
    ]), shell=True)
    logger.info(f'finished')
