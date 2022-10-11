import pandas as pd
from processing.worldpop.data.utils import DATABASE, logging, cwd

logger = logging.getLogger(__name__)
outputs = cwd / f'../../../data'
con = f'postgresql:///{DATABASE}'


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('worldpop_pop_out', con)
    df.to_excel(outputs / 'worldpop.xlsx', index=False)
    logger.info(f'finished')
