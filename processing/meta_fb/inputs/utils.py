import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'
cwd = Path(__file__).parent

data_types = {
    'general': 't',
    'women': 'f',
    'men': 'm',
    'children_under_five': 't_00_04',
    'youth_15_24': 't_15_24',
    'elderly_60_plus': 't_60_plus',
    'women_of_reproductive_age_15_49': 'f_15_49',
}


def apply_funcs(name, *args):
    for func in args:
        func(name)


def get_all_meta():
    dtypes = {'meta_fb': 'Int8'}
    df = pd.read_csv(cwd / '../../../inputs/meta.csv', dtype=dtypes,
                     keep_default_na=False, na_values=['', '#N/A'])
    df = df.rename(columns={'meta_fb': 'exists'})
    df['id'] = df['id'].str.lower()
    df['iso_3'] = df['id'].str.upper()
    df = df[['id', 'iso_3', 'exists']]
    df = df[df['exists'] > 0]
    return df.to_dict('records')


def get_land_date():
    cwd = Path(__file__).parent
    with open(cwd / '../../../../adm0-generator/data/land/README.txt') as f:
        return f.readlines()[21][25:35]


land_date = get_land_date()
adm0_list = get_all_meta()
