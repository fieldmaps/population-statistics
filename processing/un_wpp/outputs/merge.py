import pandas as pd
from .utils import logging, cwd

logger = logging.getLogger(__name__)
config = cwd / '../../../config'
outputs = cwd / '../../../outputs'

fields = ['t', 'f', 'm', 't_00_04', 't_15_24', 't_60_plus', 'f_15_49']


def get_ids(l):
    return [f'adm{x}_id' for x in range(l, -1, -1)] + ['iso_3', 'wld_update']


def main():
    df = pd.read_excel(outputs / 'worldpop.xlsx', sheet_name='adm4_id')
    df2 = pd.read_excel(outputs / 'meta_fb.xlsx', sheet_name='adm4_id')
    df = df.merge(df2, on=get_ids(4), how='outer')
    df['t_x'] = df['t_y'].combine_first(df['t_x'])
    df = df.rename(columns={'t_x': 't'})
    df = df.drop('t_y', axis=1)
    with pd.ExcelWriter(outputs / 'un_wpp.xlsx') as writer:
        for l in range(4, -2, -1):
            df = df.groupby(get_ids(l), dropna=False).sum(
                min_count=1).reset_index()
            sheet_name = f'adm{l}_id' if l >= 0 else 'iso_3'
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    logger.info('finished')
