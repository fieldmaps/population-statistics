import pandas as pd
from .utils import DATABASE, logging, cwd, land_date

logger = logging.getLogger(__name__)
outputs = cwd / f'../../../outputs/ciesin'
con = f'postgresql:///{DATABASE}'


def main():
    outputs.mkdir(parents=True, exist_ok=True)
    df = pd.read_sql_table('ciesin_pop_out', con)
    df['wld_update'] = land_date
    with pd.ExcelWriter(outputs / 'population.xlsx') as w:
        for lvl in range(4, -1, -1):
            df = df.groupby([f'adm{l}_id' for l in range(lvl, -1, -1)] + ['iso_3', 'wld_update'],
                            dropna=False).sum(min_count=1).reset_index()
            df.to_excel(w, sheet_name=f'adm{lvl}', index=False)
        df = df.groupby(['iso_3', 'wld_update'],
                        dropna=False).sum(min_count=1).reset_index()
        df.to_excel(w, sheet_name=f'iso_3', index=False)
    logger.info(f'finished')
