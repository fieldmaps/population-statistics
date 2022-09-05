import logging
from pathlib import Path

cwd = Path(__file__).parent
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

cols_ids = ['adm4_id', 'adm3_id', 'adm2_id', 'adm1_id', 'adm0_id', 'iso_3']
# cols_meta = ['ps_lvl', 'ps_year', 'ps_census']
cols_meta = ['wld_update']
grps = ['t', 'f', 'm']
dests = ['00_04', '05_09', '10_14', '15_19', '20_24', '25_29', '30_34',
         '35_39', '40_44', '45_49', '50_54', '55_59', '60_plus']
special = ['t_15_24', 'f_15_49']


def get_ids(l=4):
    # return [f'adm{x}_id' for x in range(l, -1, -1)] + ['iso_3', 'ps_lvl', 'ps_year', 'ps_census']
    return [f'adm{x}_id' for x in range(l, -1, -1)] + ['iso_3', 'wld_update']


def get_cols():
    cols = grps
    for grp in grps:
        for dest in dests:
            cols.append(f'{grp}_{dest}')
    cols = cols + special
    return cols
