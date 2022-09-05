import subprocess
from processing.worldpop.inputs.utils import DATABASE, YEAR, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / f'../../../inputs/worldpop'


def main():
    query = (data / 'query.sql').resolve()
    query.unlink(missing_ok=True)
    with open(query, 'w') as f:
        subprocess.run([
            'raster2pgsql',
            '-d', '-C', '-I', '-R', '-Y',
            '-t', 'auto',
            (data / f'ppp_{YEAR}_unconstrained.tif').resolve(),
            'worldpop_pop',
        ], stdout=f, stderr=subprocess.DEVNULL)
    subprocess.run([
        'psql',
        '--quiet',
        '-d', DATABASE,
        '-f', query,
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    query.unlink(missing_ok=True)
    logger.info(f'finished')
