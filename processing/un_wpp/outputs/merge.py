import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from processing.un_wpp.outputs.utils import logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../../data'
outputs = cwd / '../../../outputs/population/humanitarian/intl/un-wpp'

fields = ['t', 'f', 'm', 't_00_04', 't_15_24', 't_60_plus', 'f_15_49']


def zip_file(name):
    file = outputs / name
    file_zip = outputs / f'{name}.zip'
    file_zip.unlink(missing_ok=True)
    with ZipFile(file_zip, 'w', ZIP_DEFLATED) as z:
        z.write(file, file.name)
    file.unlink(missing_ok=True)


def export_factor(df):
    df1 = pd.read_excel(data / 'un_wpp.xlsx')
    dfx = df.groupby(['iso_3'], dropna=False).sum(
        numeric_only=True, min_count=1).reset_index()
    dfx = dfx.merge(df1, on='iso_3', how='left')
    dfx['factor'] = dfx['t_y'] / dfx['t_x']
    dfx['factor'] = dfx['factor'].fillna(1)
    dfx = dfx[['iso_3', 'factor']]
    return dfx


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    for l in range(4, -1, -1):
        df = pd.read_excel(outputs / f'../worldpop/adm{l}_population.xlsx')
        df1 = pd.read_excel(outputs / f'../meta-fb/adm{l}_population.xlsx')
        df = df.merge(df1, on=df.columns.tolist()[:-2], how='outer')
        df['t_x'] = df['t_y'].combine_first(df['t_x'])
        df['pop_src_x'] = df['pop_src_y'].combine_first(df['pop_src_x'])
        df = df.rename(columns={'t_x': 't', 'pop_src_x': 'pop_src'})
        df = df.drop(columns=['t_y', 'pop_src_y'])

        dfx = export_factor(df)
        df = df.merge(dfx, on='iso_3')
        for field in fields:
            df[field] = df[field] * df['factor']
            df[field] = df[field].round(0).fillna(0).astype(int)
        df = df.drop(columns=['factor'])

        if l > 0:
            df['src_date'] = df['src_date'].dt.date
            df['src_update'] = df['src_update'].dt.date
        df['wld_date'] = df['wld_date'].dt.date
        df['wld_update'] = df['wld_update'].dt.date
        df.to_excel(outputs / f'adm{l}_population.xlsx', index=False)
        df.to_csv(outputs / f'adm{l}_population.csv', index=False)
        zip_file(f'adm{l}_population.csv')
        if l > 0:
            df['src_date'] = pd.to_datetime(df['src_date'])
            df['src_date'] = df['src_date'].dt.strftime('%Y-%m-%d')
            df['src_update'] = pd.to_datetime(df['src_update'])
            df['src_update'] = df['src_update'].dt.strftime(
                '%Y-%m-%d')
        df['wld_date'] = pd.to_datetime(df['wld_date'])
        df['wld_date'] = df['wld_date'].dt.strftime('%Y-%m-%d')
        df['wld_update'] = pd.to_datetime(df['wld_update'])
        df['wld_update'] = df['wld_update'].dt.strftime('%Y-%m-%d')
        df.to_json(outputs / f'adm{l}_population.json', orient='records')
        zip_file(f'adm{l}_population.json')
    logger.info('finished')
