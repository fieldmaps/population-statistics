import xml.etree.ElementTree as ET
import subprocess
from pathlib import Path
from .utils import logging

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent
data = cwd / '../../../inputs/meta_fb'


def get_vrt(vrt):
    subprocess.run([
        'aws', 's3', 'cp',
        f's3://dataforgood-fb-data/hrsl-cogs/hrsl_general/hrsl_general-latest.vrt',
        vrt,
    ])
    with open(vrt, 'r') as f:
        text = f.read()
    text = text.replace('_general', '')
    with open(vrt, 'w') as f:
        f.write(text)


def get_files(vrt):
    result = []
    tree = ET.parse(vrt)
    files = [x.text for x in tree.iter('SourceFilename')]
    downloaded = ','.join([x.name for x in data.rglob('*.tif')])
    for file in files:
        if not file.split('/')[-1] in downloaded:
            result.append(file)
    for file in (data / 'hrsl').rglob('*.tif*'):
        if not file.name in ','.join(files):
            file.unlink()
    return result


def get_include(files):
    files = [x.replace('-v', f'_*-v') for x in files]
    include = [['--include', f'*{x}'] for x in files]
    include = [i for l in include for i in l]
    return include


def get_tif(include):
    subprocess.run([
        'aws', 's3', 'sync',
        '--exclude', '*',
        *include,
        f's3://dataforgood-fb-data/hrsl-cogs/',
        data,
    ])


def main():
    data.mkdir(parents=True, exist_ok=True)
    vrt = data / f'hrsl/hrsl-latest.vrt'
    get_vrt(vrt)
    files = get_files(vrt)
    include = get_include(files)
    get_tif(include)
    logger.info('finished')
