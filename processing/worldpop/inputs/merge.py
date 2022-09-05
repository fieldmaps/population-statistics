import subprocess
from processing.worldpop.inputs.utils import YEAR, logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/worldpop'


def main():
    if (data / 'unconstrained.vrt').is_file():
        subprocess.run([
            'gdal_translate',
            '--config', 'GDAL_NUM_THREADS', 'ALL_CPUS',
            '-co', 'BIGTIFF=YES',
            '-co', 'TILED=YES',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'ZLEVEL=9',
            (data / 'unconstrained.vrt').resolve(),
            (data / f'ppp_{YEAR}_unconstrained.tif').resolve(),
        ])
    logger.info('finished')
