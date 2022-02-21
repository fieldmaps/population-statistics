import subprocess
import xml.etree.ElementTree as ET
from multiprocessing import Pool
from .utils import logging, cwd, data_types

logger = logging.getLogger(__name__)
data = cwd / '../../../inputs/meta_fb'


def run_process(func, files):
    results = []
    pool = Pool()
    for name in files:
        args = [name]
        result = pool.apply_async(func, args=args)
        results.append(result)
    pool.close()
    pool.join()
    for result in results:
        result.get()


def merge_tif(name):
    files = [data / f"hrsl_{dt}/{name.replace('general', dt)}"
             for dt in data_types]
    vrt = data / \
        f"hrsl/hrsl-{name.replace('v1/', '').replace('v1.5/', '').replace('_general', '').replace('.tif', '.vrt')}"
    output = data / f"hrsl/{name.replace('_general', '')}"
    subprocess.run([
        'gdalbuildvrt',
        '-q',
        '-separate',
        vrt,
        *files,
    ])
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
        vrt,
        output,
    ])
    vrt.unlink(missing_ok=True)
    logger.info(name)


def build_vrt():
    subprocess.run([
        'gdalbuildvrt',
        '-q',
        data / 'hrsl/hrsl-latest.vrt',
        *(data / 'hrsl').rglob('*.tif'),
    ])


def main():
    (data / 'hrsl/v1').mkdir(parents=True, exist_ok=True)
    (data / 'hrsl/v1.5').mkdir(parents=True, exist_ok=True)
    vrt = data / f'hrsl_general/hrsl_general-latest.vrt'
    tree = ET.parse(vrt)
    files = [x.text for x in tree.iter('SourceFilename')]
    run_process(merge_tif, files)
    build_vrt()
