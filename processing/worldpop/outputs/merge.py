import pandas as pd
from .utils import logging, cwd

logger = logging.getLogger(__name__)
data = cwd / '../../data'
outputs = cwd / '../../outputs'


def main():
    worldpop = data / 'worldpop/worldpop.xlsx'
    un_wpp = data / 'un_wpp/un_wpp.xlsx'
    df = pd.read_excel(worldpop)
    df1 = pd.read_excel(un_wpp)
    df_adm0 = df.groupby('iso_3', dropna=False).sum(min_count=1).reset_index()
    df_adm0.to_excel(outputs / 'worldpop/worldpop.xlsx', index=False)
    logger.info('finished')
