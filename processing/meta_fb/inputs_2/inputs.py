import subprocess
from .utils import DATABASE, cwd, logging

logger = logging.getLogger(__name__)
data = cwd / f'../../../inputs/meta_fb'


def main():
    query = (data / 'hrsl.sql').resolve()
    query.unlink(missing_ok=True)
    with open(query, 'w') as f:
        subprocess.run([
            'raster2pgsql',
            '-d', '-C', '-I', '-R', '-Y',
            # '-b', '1',
            '-t', '512x512',
            (data / f'hrsl/hrsl-latest.vrt').resolve(),
            'meta_fb_pop',
        ], stdout=f)
    subprocess.run([
        'psql',
        '--quiet',
        '-d', DATABASE,
        '-f', query,
    ])
    # query.unlink(missing_ok=True)
    logger.info('finished')
