import pandas as pd
from processing.un_wpp.data.utils import DATA_NAME, YEAR, cwd, logging

logger = logging.getLogger(__name__)
inputs = cwd / '../../../inputs/un_wpp'
data = cwd / '../../../data'


def main():
    data.mkdir(exist_ok=True, parents=True)
    file = inputs / DATA_NAME
    df = pd.read_csv(file, low_memory=False)
    df = df[df['VarID'] == 2]
    df = df[df['Time'] == YEAR]
    df = df[df['LocID'] < 900]
    df = df[['iso_3', 'PopTotal']]
    df = df.rename(columns={'PopTotal': 't'})
    df['t'] = df['t'].apply(lambda x: x * 1000)
    df = df.sort_values('iso_3')
    df.to_excel(data / 'un_wpp.xlsx', index=False)
    logger.info('finished')
