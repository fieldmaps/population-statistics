import pandas as pd
from processing.meta_fb.data.utils import DATABASE, logging, cwd

logger = logging.getLogger(__name__)
outputs = cwd / f'../../../data'
con = f'postgresql:///{DATABASE}'


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('meta_fb_pop_out', con)
    df.to_parquet(outputs / 'meta_fb.parquet', index=False)
    df.to_csv(outputs / 'meta_fb.csv.zip', index=False, float_format='%.0f')
    logger.info(f'finished')
