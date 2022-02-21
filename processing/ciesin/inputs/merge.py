import subprocess
from .utils import FILE_NAME, logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/ciesin'


def merge_tif():
    input = data / f'{FILE_NAME}.tif'
    output = data / f'{FILE_NAME}_tiled.tif'
    if input.is_file():
        subprocess.run([
            'gdalwarp',
            '-q',
            '-multi',
            '-overwrite',
            '-co', 'TILED=YES',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'ZLEVEL=9',
            '-co', 'NUM_THREADS=ALL_CPUS',
            '-wo', 'NUM_THREADS=ALL_CPUS',
            input,
            output,
        ])


def main():
    merge_tif()
    logger.info('finished')
