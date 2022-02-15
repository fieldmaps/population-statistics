import subprocess
from pathlib import Path
from .utils import DATABASE, logging, data_types

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / f'../../../inputs/meta_fb'


def main(name):
    subprocess.run(' '.join([
        'raster2pgsql',
        '-d', '-C', '-I', '-Y',
        '-t', '256x256',
        str((data / f'hrsl_{name}/hrsl_{name}-latest.vrt').resolve()),
        f'meta_fb_pop_{data_types[name]}',
        '|',
        'psql',
        '--quiet',
        '-d', DATABASE,
    ]), shell=True)
    logger.info('finished')
