import subprocess
from .utils import logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/worldpop'


def main():
    if (data / 'unconstrained').is_dir():
        subprocess.run([
            'gdalwarp',
            '-q',
            '-multi',
            '-overwrite',
            '-co', 'BIGTIFF=YES'
            '-co', 'TILED=YES',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'ZLEVEL=9',
            '-co', 'NUM_THREADS=ALL_CPUS',
            '-wo', 'NUM_THREADS=ALL_CPUS',
            *sorted(list((data / 'unconstrained').resolve().rglob('*.tif'))),
            (data / 'unconstrained.tif').resolve(),
        ])
    logger.info('finished')
