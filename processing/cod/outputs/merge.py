import pandas as pd
from processing.cod.outputs.utils import (
    logging, cwd, get_pop_cols, get_all_cols, cols_meta, get_attrs)

logger = logging.getLogger(__name__)
data = cwd / '../../../data'
outputs = cwd / '../../../outputs/population/humanitarian/intl/cod'

fields = ['t', 'f', 'm', 't_00_04', 't_15_24', 't_60_plus', 'f_15_49']


def get_ids(l):
    return [f'adm{x}_id' for x in range(l, -1, -1)]


def get_full_ids(l):
    return get_ids(l) + ['pop_src'] + fields


def apply_factor(df):
    df1 = pd.read_parquet(data / 'un_wpp.parquet')
    dfx = df.groupby(['iso_3'], dropna=False).sum(
        numeric_only=True, min_count=1).reset_index()
    dfx = dfx.merge(df1, on='iso_3', how='left')
    dfx['factor'] = dfx['t_y'] / dfx['t_x']
    dfx['factor'] = dfx['factor'].fillna(1)
    dfx = dfx[['iso_3', 'factor']]
    df = df.merge(dfx, on='iso_3')
    for field in get_pop_cols():
        df[field] = df[field] * df['factor']
    df = df.drop(columns=['factor'])
    return df


def get_df():
    df1 = pd.read_parquet(outputs / f'../meta-fb/adm4_population.parquet')
    df1 = df1[get_full_ids(4)]
    df1['join'] = df1['adm4_id']
    df1['fraction'] = 1
    df2 = pd.read_parquet(data / 'cod.parquet')
    df2 = df2[['adm0_id', 'pop_lvl']].drop_duplicates()
    df1 = df1.merge(df2, on='adm0_id', how='outer')
    return df1


def add_fraction(df):
    frames = [df[df['pop_lvl'].isna()]]
    for l in range(4, -1, -1):
        df1 = df[df['pop_lvl'] == l].copy()
        df1['join'] = df1[f'adm{l}_id']
        df1['pop_src1'] = df1['pop_src']
        df1['pop_src'] = 'cod'
        df2 = pd.read_parquet(
            outputs / f'../meta-fb/adm{l}_population.parquet')
        df2 = df2[get_ids(l) + ['t']]
        df1 = df1.merge(df2, on=get_ids(l))
        df1['fraction'] = df1['t_x'] / df1['t_y']
        df1 = df1.rename(columns={'t_x': 't'})
        df1 = df1.drop(columns=fields + ['t_y'])
        frames.append(df1)
    return pd.concat(frames).sort_values(by='adm4_id').drop(columns=['pop_lvl']).drop_duplicates()


def add_sadd(df):
    df1 = pd.read_parquet(data / 'cod.parquet')
    df1 = apply_factor(df1)
    df1 = df1.drop(columns=get_ids(4))
    df = df.merge(df1, on='join', how='outer')
    df = df.drop(columns=['join'])
    for field in fields:
        df[field] = df[f'{field}_x'].combine_first(df[f'{field}_y'])
        df = df.drop(columns=[f'{field}_x', f'{field}_y'])
    return df


def apply_fraction(df):
    for col in get_pop_cols():
        df[col] = df[col] * df['fraction']
        df[col] = df[col].round(0)
    df = df.drop(columns=['fraction'])
    df = df[get_all_cols()]
    return df


def export_df(df):
    for l in range(4, -1, -1):
        df1 = df.groupby(get_ids(l) + cols_meta, dropna=False).sum(
            numeric_only=True, min_count=1).reset_index()
        df2 = pd.read_excel(get_attrs(l))
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
    df1 = get_df()
    df2 = add_fraction(df1)
    df3 = add_sadd(df2)
    df4 = apply_fraction(df3)
    export_df(df4)
