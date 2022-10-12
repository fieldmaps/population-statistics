import logging
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_attrs(l):
    if l >= 1:
        return cwd / f'../../../../admin-boundaries/outputs/edge-matched/humanitarian/intl/adm{l}_polygons.xlsx'
    else:
        return cwd / '../../../../adm0-generator/outputs/osm/intl/adm0_polygons.xlsx'
