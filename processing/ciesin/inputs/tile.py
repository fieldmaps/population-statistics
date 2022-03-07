import subprocess
from .utils import FILE_NAME, logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/ciesin'


def main():
    input = (data / f'{FILE_NAME}.tif').resolve()
    output = (data / f'{FILE_NAME}_tiled.tif').resolve()
    if input.is_file():
        subprocess.run([
            'gdal_translate',
            '--config', 'GDAL_NUM_THREADS', 'ALL_CPUS',
            '-co', 'TILED=YES',
            '-co', 'BLOCKXSIZE=128',
            '-co', 'BLOCKYSIZE=128',
            '-co', 'COMPRESS=DEFLATE',
            '-co', 'ZLEVEL=9',
            input,
            output,
        ])
    logger.info('finished')
