import pandas as pd
from .utils import DATABASE, logging, cwd, land_date

logger = logging.getLogger(__name__)
outputs = cwd / f'../../../data/ciesin'
con = f'postgresql:///{DATABASE}'


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('ciesin_pop_out', con)
    df['wld_update'] = land_date
    df.to_excel(outputs / 'ciesin.xlsx', index=False)
    logger.info(f'finished')
