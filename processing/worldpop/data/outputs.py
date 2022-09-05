import pandas as pd
from processing.worldpop.data.utils import DATABASE, logging, cwd, land_date

logger = logging.getLogger(__name__)
outputs = cwd / f'../../../data'
con = f'postgresql:///{DATABASE}'


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('worldpop_pop_out', con)
    df['wld_update'] = land_date
    df.to_excel(outputs / 'worldpop.xlsx', index=False)
    logger.info(f'finished')
