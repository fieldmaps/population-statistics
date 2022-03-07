import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'

grps = ['t', 'f', 'm']
dests = ['00_04', '05_09', '10_14', '15_19', '20_24', '25_29', '30_34',
         '35_39', '40_44', '45_49', '50_54', '55_59', '60_64', '65_plus']
cols_meta = ['ps_lvl', 'ps_year', 'ps_census']


def get_ps_ids():
    cols = cols_meta + grps
    for grp in grps:
        for dest in dests:
            cols.append(f'{grp}_{dest}')
    return cols


def get_ids(level, end=0, attrs=True):
    ids = []
    for l in range(level, end-1, -1):
        ids.extend([
            f'adm{l}_id',
            f'adm{l}_src',
            f'adm{l}_name',
            f'adm{l}_name1',
            f'adm{l}_name2',
        ])
    if attrs:
        ids.extend([
            'src_lvl', 'src_lang', 'src_lang1', 'src_lang2',
            'src_date', 'src_update',
            'src_name', 'src_name1',
            'src_lic', 'src_url', 'src_grp',
        ])
        ids.extend([
            'iso_cd', 'iso_2', 'iso_3', 'iso_3_grp',
            'region3_cd', 'region3_nm',
            'region2_cd', 'region2_nm',
            'region1_cd', 'region1_nm',
            'status_cd', 'status_nm',
            'wld_date', 'wld_update',
            'wld_view', 'wld_notes',
        ])
    return ids
