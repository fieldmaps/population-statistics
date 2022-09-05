import shutil
import pandas as pd
from processing.cod.data.utils import cwd, logging, grps, cols, col_map, get_ids, get_srcs, cols_meta

logger = logging.getLogger(__name__)
data = cwd / '../../../data/cod'


def clean_attrs(df, name, lvl, row):
    l_max = row['ps_lvl_max']
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('_tl', '')
    df.columns = df.columns.str.replace('plus', '_plus')
    df.columns = df.columns.str.replace('__plus', '_plus')
    if df[f'adm{l_max}_pcode'].duplicated().any():
        logger.info(f'DUPLICATE adm{l_max}_pcode: {name}')
        raise RuntimeError(f'DUPLICATE adm{l_max}_pcode: {name}')
    for l in range(0, lvl+1):
        df = df.rename(columns={f'adm{l}_pcode': f'adm{l}_src'})
    df = df.groupby(get_srcs(lvl), dropna=False).sum(min_count=1).reset_index()
    return df


def add_meta(df, row):
    for col in cols_meta:
        df[col] = row[col]
    return df


def agg_attrs_sum(df, col, grp, start):
    col_name = col_map[start]
    if not df[col].isna().all():
        df[f'{grp}_{col_name}'] = df[[f'{grp}_{col_name}', col]].agg(
            'sum', axis='columns')
    return df


def agg_attrs(df, lvl):
    for col in cols:
        if col not in df.columns:
            df[col] = None
    for col in df.columns:
        if col not in [*get_srcs(lvl), *grps]:
            col_split = col.split('_')
            grp = col_split[0]
            start = int(col_split[1])
            try:
                end = col_split[2]
                if end == 'plus':
                    end = start + 4
                if int(end) - start < 5:
                    df = agg_attrs_sum(df, col, grp, start)
            except IndexError:
                df = agg_attrs_sum(df, col, grp, start)
    df = df[get_srcs(lvl) + cols]
    return df


def add_special(df):
    df['t_15_24'] = df['t_15_19'] + df['t_20_24']
    df['f_15_49'] = df['f_15_19'] + df['f_20_24'] + df['f_25_29'] + \
        df['f_30_34'] + df['f_35_39'] + df['f_40_44'] + df['t_45_49']
    return df


def add_ids(df, lvl, df1):
    if lvl > 0:
        df1 = df1[get_ids(lvl)].drop_duplicates()
        df1 = df1.drop(columns=get_srcs(lvl-1))
        df = df.merge(df1, on=f'adm{lvl}_src')
    else:
        df1 = df1[[*get_ids(0), 'iso_2']].drop_duplicates()
        df = df.rename(columns={f'adm{lvl}_src': 'iso_2'})
        df = df.merge(df1, on='iso_2')
    return df


def main(name, lvl, row, df1):
    data.mkdir(parents=True, exist_ok=True)
    file = cwd / f'../../../inputs/cod/{name}.csv'
    output = data / f'{name}.xlsx'
    output.unlink(missing_ok=True)
    df = pd.read_csv(file, keep_default_na=False, na_values=['', '#N/A'])
    df = clean_attrs(df, name, lvl, row)
    df = agg_attrs(df, lvl)
    df = add_special(df)
    df = add_meta(df, row)
    df = add_ids(df, lvl, df1)
    df.to_excel(output, index=False)


def cleanup():
    shutil.rmtree(data, ignore_errors=True)
