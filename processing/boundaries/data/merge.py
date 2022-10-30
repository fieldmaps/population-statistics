import pandas as pd
from processing.boundaries.data.utils import DATABASE, logging, cwd

logger = logging.getLogger(__name__)

data = cwd / '../../../data'
con = f'postgresql:///{DATABASE}'


def get_ids(l):
    return [f'adm{x}_id' for x in range(l, -1, -1)]


def export_attrs(df):
    df1 = df.groupby('adm0_id', dropna=False).sum(
        numeric_only=True, min_count=1).reset_index()
    df1 = df1.rename(columns={'area': 'area_0'})
    df1['area_0'] = df1['area_0'].astype(int)
    for l in range(1, 5):
        df2 = df[['adm0_id', f'adm{l}_id']]
        df2 = df2.drop_duplicates(subset=[f'adm{l}_id'])
        df2 = df2.groupby('adm0_id', dropna=False).count().reset_index()
        df1 = df1.merge(df2, on='adm0_id')
        df1[f'area_{l}'] = df1['area_0'] / df1[f'adm{l}_id']
        df1[f'area_{l}'] = df1[f'area_{l}'].astype(int)
        df1 = df1.drop(columns=[f'adm{l}_id'])
    df1.to_excel(data / f'area.xlsx', sheet_name='area', index=False)


def export_areas(df):
    for l in range(4, -1, -1):
        df1 = df.groupby(f'adm{l}_id', dropna=False).sum(
            numeric_only=True, min_count=1).reset_index()
        df1['area'] = df1['area'].astype(int)
        df1.to_parquet(data / f'area_{l}.parquet', index=False)
        df1.to_csv(data / f'area_{l}.csv.zip', index=False)


def main():
    data.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('adm4_polygons_area', con)
    export_attrs(df)
    export_areas(df)
    logger.info('finished')
