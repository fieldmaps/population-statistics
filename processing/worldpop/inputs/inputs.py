import subprocess
from pathlib import Path
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / f'../../../inputs/worldpop'


def main(name):
    subprocess.run(' '.join([
        'raster2pgsql',
        '-d', '-C', '-I', '-Y',
        '-t', '256x256',
        str((data / f'{name}.tif').resolve()),
        f'worldpop_pop_{name}',
        '|',
        'psql',
        '--quiet',
        '-d', DATABASE,
    ]), shell=True)
    logger.info(name)
