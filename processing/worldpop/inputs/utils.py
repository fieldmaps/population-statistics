import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'
cwd = Path(__file__).parent

data_types = ['unconstrained', 'constrained']


def apply_funcs(name, *args):
    for func in args:
        func(name)


def get_all_meta():
    df = pd.read_csv(cwd / '../../../inputs/meta.csv',
                     keep_default_na=False, na_values=['', '#N/A'])
    df['id'] = df['id'].str.lower()
    df['iso_3'] = df['id'].str.upper()
    df = df[['id', 'iso_3']]
    return df.to_dict('records')


def get_land_date():
    cwd = Path(__file__).parent
    with open(cwd / '../../../../adm0-generator/data/land/README.txt') as f:
        return f.readlines()[21][25:35]


land_date = get_land_date()
adm0_list = get_all_meta()
