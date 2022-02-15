from time import time
import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
from .utils import logging, data_types

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / '../../../inputs/meta_fb'


def get_vrt(name, vrt):
    subprocess.run([
        'aws', 's3', 'cp',
        f's3://dataforgood-fb-data/hrsl-cogs/hrsl_{name}/hrsl_{name}-latest.vrt',
        vrt,
    ])


def get_tif(name, include):
    subprocess.run([
        'aws', 's3', 'sync',
        '--exclude', '*',
        *include,
        f's3://dataforgood-fb-data/hrsl-cogs/hrsl_{name}/',
        data / f'hrsl_{name}',
    ])


def main():
    start_time = time()
    data.mkdir(parents=True, exist_ok=True)
    for name in data_types:
        vrt = data / f'hrsl_{name}/hrsl_{name}-latest.vrt'
        get_vrt(name, vrt)
        tree = ET.parse(vrt)
        files = [x.text for x in tree.iter('SourceFilename')]
        include = [['--include', x] for x in files]
        include = [i for l in include for i in l]
        get_tif(name, include)
        for file in (data / f'hrsl_{name}').rglob('*.tif*'):
            if not file.name in ','.join(files):
                file.unlink()
    logger.info(time() - start_time)
