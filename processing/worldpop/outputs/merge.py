import pandas as pd
from processing.worldpop.outputs.utils import logging, cwd, get_attrs

logger = logging.getLogger(__name__)

data = cwd / '../../../data'
outputs = cwd / '../../../outputs/population/humanitarian/intl/worldpop'

fields = ['t']


def get_ids(l):
    return [f'adm{x}_id' for x in range(l, -1, -1)] + ['iso_3']


def apply_factor(df):
    df1 = pd.read_parquet(data / 'un_wpp.parquet')
    dfx = df.groupby(['iso_3'], dropna=False).sum(
        numeric_only=True, min_count=1).reset_index()
    dfx = dfx.merge(df1, on='iso_3', how='left')
    dfx['factor'] = dfx['t_y'] / dfx['t_x']
    dfx['factor'] = dfx['factor'].fillna(1)
    dfx = dfx[['iso_3', 'factor']]
    df = df.merge(dfx, on='iso_3')
    for field in fields:
        df[field] = df[field] * df['factor']
        df[field] = df[field].round(0)
    df = df.drop(columns=['factor'])
    return df


def export_attrs(df):
    for l in range(4, -1, -1):
        df1 = df.groupby(get_ids(l), dropna=False).sum(
            numeric_only=True, min_count=1).reset_index()
        df2 = pd.read_excel(get_attrs(l))
        df2['pop_src'] = 'worldpop'
        df2 = df2.merge(df1, on=get_ids(l))
        if l > 0:
            df2['src_date'] = df2['src_date'].dt.date
            df2['src_update'] = df2['src_update'].dt.date
        df2['wld_date'] = df2['wld_date'].dt.date
        df2['wld_update'] = df2['wld_update'].dt.date
        df2.to_parquet(outputs / f'adm{l}_population.parquet', index=False)
        df2.to_excel(outputs / f'adm{l}_population.xlsx', index=False)
        df2.to_csv(outputs / f'adm{l}_population.csv.zip',
                   index=False, float_format='%.0f')
        if l > 0:
            df2['src_date'] = pd.to_datetime(df2['src_date'])
            df2['src_date'] = df2['src_date'].dt.strftime('%Y-%m-%d')
            df2['src_update'] = pd.to_datetime(df2['src_update'])
            df2['src_update'] = df2['src_update'].dt.strftime('%Y-%m-%d')
        df2['wld_date'] = pd.to_datetime(df2['wld_date'])
        df2['wld_date'] = df2['wld_date'].dt.strftime('%Y-%m-%d')
        df2['wld_update'] = pd.to_datetime(df2['wld_update'])
        df2['wld_update'] = df2['wld_update'].dt.strftime('%Y-%m-%d')
        df2.to_json(outputs / f'adm{l}_population.json.zip', orient='records')


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(data / 'worldpop.parquet')
    df = df.drop(columns=['count'])
    df = apply_factor(df)
    export_attrs(df)
    logger.info('finished')
