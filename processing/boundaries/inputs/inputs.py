import subprocess
from processing.boundaries.inputs.utils import DATABASE, cwd, logging

logger = logging.getLogger(__name__)


def main():
    file = cwd / f'../../../../admin-boundaries/data/edge-matched/humanitarian/intl/adm4_polygons.gpkg'
    subprocess.run([
        'ogr2ogr',
        '-overwrite',
        '-makevalid',
        '-dim', 'XY',
        '-t_srs', 'EPSG:4326',
        '-lco', 'FID=fid',
        '-lco', 'GEOMETRY_NAME=geom',
        '-nln', f'adm4_polygons',
        '-f', 'PostgreSQL', f'PG:dbname={DATABASE}',
        file,
    ])
    logger.info(f'finished')
