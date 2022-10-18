import pandas as pd
from processing.cod.data.utils import cwd, logging, adm0_list, get_ids, get_cols, cols_meta

logger = logging.getLogger(__name__)
data = cwd / '../../../data/cod'
outputs = cwd / '../../../data'


def main():
    frames = []
    outputs.mkdir(parents=True, exist_ok=True)
    for row in adm0_list:
        name = row['id']
        file = (data / f'{name}.parquet')
        df = pd.read_parquet(file)
        frames.append(df)
    df = pd.concat(frames)
    df = df[get_ids(4, True) + ['iso_3'] + cols_meta[1:] + get_cols()]
    df['join'] = df['adm4_id'].combine_first(df['adm3_id']).combine_first(
        df['adm2_id']).combine_first(df['adm1_id']).combine_first(df['adm0_id'])
    df = df.sort_values(by=get_ids(4, reverse=True))
    df.to_parquet(outputs / 'cod.parquet', index=False)
    df.to_csv(outputs / 'cod.csv.zip', index=False, float_format='%.0f')
    logger.info('finished')
