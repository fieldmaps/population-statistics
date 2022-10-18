import pandas as pd
from processing.worldpop.data.utils import DATABASE, logging, cwd

logger = logging.getLogger(__name__)
outputs = cwd / f'../../../data'
con = f'postgresql:///{DATABASE}'


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('worldpop_pop_out', con)
    df.to_parquet(outputs / 'worldpop.parquet', index=False)
    df.to_csv(outputs / 'worldpop.csv.zip', index=False, float_format='%.0f')
    logger.info(f'finished')
