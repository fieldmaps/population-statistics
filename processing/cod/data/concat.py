import pandas as pd
from processing.cod.data.utils import cwd, logging, adm0_list, get_ids, get_cols, cols_meta

logger = logging.getLogger(__name__)
data = cwd / '../../../data/cod'
outputs = cwd / '../../../data'


def main():
    frames = []
    outputs.mkdir(parents=True, exist_ok=True)
    output = (outputs / 'cod.xlsx')
    output.unlink(missing_ok=True)
    for row in adm0_list:
        name = row['id']
        file = (data / f'{name}.xlsx')
        df = pd.read_excel(file, keep_default_na=False, na_values=['', '#N/A'])
        frames.append(df)
    df = pd.concat(frames)
    df = df[cols_meta[:1] + get_ids(4) + cols_meta[1:] + get_cols()]
    df = df.sort_values(by=cols_meta[:1] + get_ids(4))
    df.to_excel(output, index=False)
    logger.info('finished')
