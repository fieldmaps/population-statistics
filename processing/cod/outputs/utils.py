import logging
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

cols_ids = ['adm4_id', 'adm3_id', 'adm2_id', 'adm1_id', 'adm0_id']
cols_meta = ['pop_src', 'pop_src1', 'pop_lvl', 'pop_year']
grps = ['t', 'f', 'm']
dests = ['00_04', '05_09', '10_14', '15_19', '20_24', '25_29', '30_34',
         '35_39', '40_44', '45_49', '50_54', '55_59', '60_plus']
special = ['t_15_24', 'f_15_49']


def get_pop_cols():
    cols = ['t', 'f', 'm']
    for grp in grps:
        for dest in dests:
            cols.append(f'{grp}_{dest}')
    cols = cols + special
    return cols


def get_all_cols():
    return cols_ids + cols_meta + get_pop_cols()


def get_attrs(l):
    if l >= 1:
        return cwd / f'../../../../admin-boundaries/outputs/edge-matched/humanitarian/intl/adm{l}_polygons.xlsx'
    else:
        return cwd / '../../../../adm0-generator/outputs/osm/intl/adm0_polygons.xlsx'
