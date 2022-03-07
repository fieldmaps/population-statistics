import subprocess
from .utils import DATABASE, FILE_NAME, logging, cwd

logger = logging.getLogger(__name__)
data = cwd / f'../../../inputs/ciesin'


def main():
    query = (data / 'query.sql').resolve()
    query.unlink(missing_ok=True)
    with open(query, 'w') as f:
        subprocess.run([
            'raster2pgsql',
            '-d', '-r', '-C', '-I', '-R', '-Y',
            '-t', 'auto',
            (data / f'{FILE_NAME}_tiled.tif').resolve(),
            'ciesin_pop',
        ], stdout=f)
    subprocess.run([
        'psql',
        '--quiet',
        '-d', DATABASE,
        '-f', query,
    ])
    query.unlink(missing_ok=True)
    logger.info(f'finished')
