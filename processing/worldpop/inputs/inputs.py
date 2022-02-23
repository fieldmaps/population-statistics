import subprocess
from pathlib import Path
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / f'../../../inputs/worldpop'


def main():
    subprocess.run(' '.join([
        'raster2pgsql',
        '-d', '-C', '-I', '-Y',
        '-t', '256x256',
        str((data / f'unconstrained.tif').resolve()),
        f'worldpop_pop',
        '|',
        'psql',
        '--quiet',
        '-d', DATABASE,
    ]), shell=True)
    logger.info('finished')
