import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from processing.un_wpp.outputs.utils import logging, cwd

logger = logging.getLogger(__name__)
outputs = cwd / '../../../outputs/population/humanitarian/intl/un-wpp'


def zip_file(name):
    file = outputs / name
    file_zip = outputs / f'{name}.zip'
    file_zip.unlink(missing_ok=True)
    with ZipFile(file_zip, 'w', ZIP_DEFLATED) as z:
        z.write(file, file.name)
    file.unlink(missing_ok=True)


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
