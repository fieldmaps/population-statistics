import subprocess
import pandas as pd
from pathlib import Path
from .utils import DATABASE, logging

logger = logging.getLogger(__name__)
cwd = Path(__file__).parent


def main():
    file = cwd / f'../../../../admin-boundaries/data/edge-matched/humanitarian/intl/adm4_polygons.gpkg'
    file_attr = cwd / f'../../../outputs/cod/population.xlsx'
    con = f'postgresql:///{DATABASE}'
    # for lvl in [0, 4]:
    #     df = pd.read_excel(file_attr, sheet_name=f'adm{lvl}')
    #     df.to_sql(f'adm{lvl}_population', con,
    #               if_exists='replace', index=False, method='multi')
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
