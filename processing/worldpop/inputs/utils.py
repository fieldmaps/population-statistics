import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

DATABASE = 'population_statistics'
YEAR = 2020
cwd = Path(__file__).parent


def get_all_meta():
    df = pd.read_csv(cwd / '../../../inputs/meta.csv',
                     keep_default_na=False, na_values=['', '#N/A'])
    df['id'] = df['iso_wp'].combine_first(df['iso_3'])
    df['id'] = df['id'].str.lower()
    df = df[['id']]
    return df.to_dict('records')


adm0_list = get_all_meta()
